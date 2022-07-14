# Data Gen

Step 1 :  Use ```find . -name gsql_data_generator``` in the TigerGraph installed package to find where this binary is.

Step 2 :  To change number of vertexes and edges modify parameters in ```ldbc_snb_old.json``` file.

Step 3 :  Run gsql_data_generator. 
```gsql_data_generator config.yaml input.json offset(default=0)```

Replace config.yaml and input.json from files provided in this repo.

Please find more details in below link.
1) https://graphsql.atlassian.net/wiki/spaces/QA/pages/908034073/Usage+of+New+data+generator
2) https://graphsql.atlassian.net/wiki/spaces/~628b9e669c617b006a6ca980/pages/2788786760/GSQL+data+generator+Controlling+the+distribution+of+data

 
