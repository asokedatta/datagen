import os
import subprocess
import json

final_result = {}
#### True Cardinality and selectivity collection
PATH = "input_files/qry_templates.csv"

def collect_true_card(_query): # This function will return true cardinality of a query
    cmd = "gsql -g ldbc_snb temp.gsql"
    result = subprocess.getoutput("gsql -g ldbc_snb temp.gsql")
    
    result = result.split(',')[-1].split(':')[-1].replace('}]','').replace('}','').strip()
    return result


query_header = "use graph ldbc_snb \n\
set cost_opt = true \n\
set single_gpr = true \n"

query_no = 1
# wf1 = open("TrueCardinality.csv",'w')
print("\n\n$$$ Collecting True Cardinality and Selectivity ..\n")
header = "query_no | Vertex | where | True Cardinality | True Selectivity | "
final_result["header"] = header
print(header)
for line in open(PATH, 'r').readlines():
    line = line.strip()
    if not line:
        continue
    data = line.split('|')
    vertex = data[0]
    cond = data[1]
    size = int(data[2])

    # Query creation
    create_stmt = "CREATE OR REPLACE QUERY h_"
    create_stmt += str(query_no) + "()" + \
    "FOR GRAPH ldbc_snb SYNTAX _v2 {\n\n\n"
    edge = None
    if vertex in ["Person", "Post", "Comment"]:
        edge = "-(IS_LOCATED_IN>)-  :tgt"
    else:
        edge = "-(HAS_MEMBER>)-  :tgt"

    query = query_header + create_stmt + \
    "vs = \n \
     SELECT start \n \
     FROM " + vertex + " :start\n" + \
     "\t"+edge + "\n "\
     "\tWHERE " + cond + "\n ; \n" + \
     "result = \n \
     SELECT start \n \
     FROM " + vertex + " :start\n" + \
     "\tWHERE " + cond + "\n ; \n" + \
     "PRINT result.size(); \n}"
    
    # Modify query for collecting true cardinalitys
    query_true_card = query.replace('set cost_opt = true \nset single_gpr = true','') \
                    + "\ninterpret query h_" + str(query_no) + "()"
    wf = open("temp.gsql",'w')
    wf.writelines(query_true_card)
    wf.close()
    true_card = collect_true_card("[h_" + str(query_no) +'].')
    # print(true_card)
    out_line = str(query_no) + ' | ' + vertex + ' | ' + cond + ' | ' + true_card + ' | ' + str(int(true_card)/size)
    print(out_line)
    whr = vertex +": " +cond.split('.',1)[1]
    final_result[whr.strip()] = out_line + ' | '
    # wf1.writelines(out_line + '\n')

    # writing query for histogram estimation
    output_path = "queries/h_" + str(query_no) + ".gsql"
    wf = open(output_path, 'w')
    wf.write(query)
    wf.close()

    # Reset buffers
    query = "" 
    query_no += 1
    # if query_no == 3: break
# wf1.close()

############################################################################################################################
##### Building histogram and adding histogram queries
input_file = "input_files/histInput.csv"

while 1:
    no_of_buckets = input("\nNumber of buckets ( Enter 00 to exit) # ")
    if no_of_buckets.strip() == "00": break
    final_result["header"] += ("estimate-" + no_of_buckets + ' | ')
     
    print("\n$$$ Deleting existing and Creating new histograms ... \n")
    # Delete existing histograms
    cmd = "curl -s --user tigergraph:tigergraph -X DELETE \"localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb\""
    p2 = subprocess.run(cmd, shell=True)

    i = 0
    
    # Create new histogram for inputs
    for line in open(input_file, 'r').readlines():
        data = line.strip().split('|')
        vertex = data[0]
        attr = data[1]
        
        print("Creating histogram for # ",vertex, "(vertex) # ",attr, "(attribute) # ", no_of_buckets+"(number of buckets)")
        cmd1 = f"curl -s --user tigergraph:tigergraph -X POST \"http://localhost:14240/gsqlserver/gsql/stats/histogram?graph=ldbc_snb&vertex={vertex}&attribute={attr}&buckets={no_of_buckets}&compute=true\" | jq ."
        p1 = subprocess.Popen(cmd1, shell=True)
        p1.wait()
    
    
    print("\n$$$ Cleaning log.DEBUG and adding new histograms queries ... \n")
    ### Adding histogram queries
    PATH = "queries/"
    queries = os.listdir(PATH)

    # Clear debug log
    cmd1 = " > /home/tigergraph/tigergraph/log/gsql/log.DEBUG"
    subprocess.run(cmd1, shell = True)

    debug_file = "/home/tigergraph/tigergraph/log/gsql/log.DEBUG"
    content = open(debug_file).read()
    print("Chekcing Debug file content # \n",content)

    # Delete all existing query
    cmd2 = "gsql -g ldbc_snb DROP QUERY ALL"
    subprocess.run(cmd2, shell = True)

    # Creating new queries
    for file in queries:
        query = PATH + file
        cmd = f"gsql -g ldbc_snb {query}"
        print(" Adding query $ ",file)
        subprocess.run(cmd, shell = True)
    
    ### Parsing estimated selectivity
    debug_file = "/home/tigergraph/tigergraph/log/gsql/log.DEBUG"

    selectivity = dict()

   
    i = 1
    visited = []
    for line in open(debug_file, 'r').readlines():
        if "selectivity" in line:
            data = line.split("selectivity")[1]
            vertex_cond = data.split(" = ")[0].strip()
            sel = data.split(" = ")[1].strip()
            vertex = vertex_cond.split(": ")[0][1:]
            cond = vertex_cond.split(": ")[1][:-1]
            vertex_cond = vertex_cond.replace('(','').replace(')','').strip() 
            if vertex_cond in final_result and vertex_cond not in visited and sel != "missing":
                # print(vertex_cond,sel)
                final_result[vertex_cond] += sel + ' | '
                visited.append(vertex_cond)
            '''
            if vertex_cond not in selectivity and :
                selectivity[vertex_cond] = sel
                output_line = str(i) + '|' + vertex + '|' + cond + '|' + sel + '\n'
                print(output_line)
                w_f.write(output_line)
                i += 1
            '''
w_f = open("hist_result.csv", 'w')    
for key,val in final_result.items():
    print(key, val)
    w_f.write(val+'\n')
w_f.close()
print("Final result path hist_result.csv")