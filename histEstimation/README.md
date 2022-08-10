# How to collect histogram estimates for different bucket sizes

Step 1 - 
Setting up all the input files. Two input files are located in ```input_file/``` 

• qry_templates.csv - This file has all benchmark queries in the below format
```
   vetex | condition | vertex cardinality 
   Person|start.id <= 37383395354120|10295 
   Person|start.id >= 14|10295 
   Person|start.id <= 10604|10295 
```
To add a new query, add it to the end of the file following the above format.

• histInput.csv - This file has vertex and attributes names to create histograms. The number of buckets will be asked during script running. The file format is below -
```
   vetex | attribute
   Post|id
   Post|imageFile
   Post|locationIP 
```
To add a new entry, just add it to the end of the file following the above format.

Step 2 - 
Updating histEstimation folder permission for ```tigergraph``` user.
```
sudo chown -R tigergraph histEstimation
```

Step 3 - 
Updating edge information. To get histogram estimates, we need at least one hop query. This script supports edges only for Person, Post, Comment, and Forum vertex.
```
    if vertex in ["Person", "Post", "Comment"]:
        edge = "-(IS_LOCATED_IN>)-  :tgt"
    else:
        edge = "-(HAS_MEMBER>)-  :tgt"
```
To add a new vertex, update the ```edge``` variable accordingly. line 41 - 44 in ```hist_estimates.py ``` file.

Step 4 -
Increasing query timeout period as some histogram creation queries might take more than the default timeout period (16 Seconds). For LDBC SNB scale factor 1, 300 seconds timeout worked.
```
gadmin config entry RESTPP.Factory.DefaultQueryTimeoutSec
gadmin config apply
gadmin restart
```


Step 5 -
Run script ```python3 hist_estimates.py```. Input ```00``` to exit from the script.

The final result will be in ```hist_result.csv```. Result format will be like below example -
```
query_no | Vertex | where | True Cardinality | True Selectivity | estimate-10 | estimate-40 | 
1 | Person | start.id == 19791209304198 | 1 | 9.713453132588635e-05 | 9.713453132588635E-5 | 9.713453132588635E-5 | 
2 | Person | start.id == 32985348835009 | 1 | 9.713453132588635e-05 | 9.713453132588635E-5 | 9.713453132588635E-5 | 
```
