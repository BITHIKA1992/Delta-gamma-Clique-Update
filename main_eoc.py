# -*- coding: utf-8 -*-
"""
Created on Sun May 10 10:06:12 2020

@author: Bithika
"""

from recursive_edge_on_clique import edge_on_clique
from collections import defaultdict
import gc
import os
import psutil
import pickle


correctness_check = True
partition_type = 'm' #'e' or 'm' , set manully
#partition_type = 'e'

## execute get_T1.py.... to get Partion_Times
if partition_type == 'm':
    #Partition_Times = [-1, 1247663519, 1247680559]  ## infectious_dataset
    Partition_Times = [-1, 107180, 212360]  ## ht09_contact_list
else: ## 'e'
    #Partition_Times = [-1, 1247666349, 1247680559]  ## infectious_dataset
    Partition_Times = [-1, 106190, 212360]   ## ht09_contact_list
    
### special case: (uncomment when required)
#Partition_Times = [-1, 70800, 160000, 212360]  ## ht09_contact_list
#partition_type = 's'    ## ht09_contact_list

    
#delta = 420
#gamma = 4
#data_file = "infectious_dataset.txt"
#meta_file = "infectious_meta.txt"

data_file =  "ht09_contact_list.txt"
meta_file = "ht09contact_meta.txt"

#log_file = "./logs/log_" + meta_file.split("_")[0]  + '_' \
#           + str(delta) + '_' + str(gamma) + '_' + str(partition_type)+'.txt'

file_ = open('./Datasets/' + meta_file, 'r')
for line in file_:
    contents = line.split(",")
    delta = int(contents[0])
    gamma = int(contents[1])
    
    
    print("\n")
    print("\n")   
    print("\n")  
    if len(Partition_Times) <= 3:       
        result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' + str(partition_type)+'.pkl'
    else:
         result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' \
               + str(len(Partition_Times) -1) + str(partition_type)+'.pkl'     
    
    total_cycle_stat = defaultdict(list)
    
    for i in range(len(Partition_Times) -1):
        T1 = Partition_Times[i]
        T2 = Partition_Times[i+1]
        print("#####################   Update Cycle: ", (i+1) ,"      #################")
        #new_links_file = data_file + "_" + str(T2)+".txt"
        new_links_file = data_file
        if T1 == -1:
            links_prev_delta = []
            C_T1 = set()
            C_T1_ex = set()
    
        ec = edge_on_clique(links_prev_delta, new_links_file , C_T1, C_T1_ex ,\
                                 delta, gamma, T1, T2)
        C_T2, C_T2_ex, links_post_delta, _stat = ec.enumerate_edge_on_clique()
        
        ### copy 
        del C_T1, C_T1_ex, links_prev_delta
        C_T1 = C_T2.copy()
        C_T1_ex = C_T2_ex.copy()
        links_prev_delta = links_post_delta.copy()
        for k in _stat.keys():
            total_cycle_stat[k].append(_stat[k])
        ## Free memory space    
        del ec, _stat, C_T2, C_T2_ex, links_post_delta,
        gc.collect()
        
    new_f = C_T1
    process = psutil.Process(os.getpid())
    _total_memory = process.memory_info().rss/1024/1024
    print("Used Memory:", _total_memory , "MB")
    print("######## Statitics With EOC method  ########")
    print("Number of Maximal cliques:"  , len(new_f))
    print("Max cardinality:", total_cycle_stat['_max_cardinality'][-1] )
    print("Max duration:",  total_cycle_stat['_max_duration'][-1] )
    print("Total Time by partition scheme:", sum(total_cycle_stat['_total_time']))  
    print("Max Space(KB) by partition scheme: ", max(total_cycle_stat['_total_space']) )
    
    
    
    #### Correctness Check
    print("\n ########  Correctness check ##########")
    if correctness_check:
        ec = edge_on_clique([], data_file , set(), set() ,\
                                     delta, gamma, Partition_Times[0], Partition_Times[-1])
        C_full, _, _ , full_run_stat = ec.enumerate_edge_on_clique()
        del ec
        gc.collect()
        process = psutil.Process(os.getpid())
        _total_memory = process.memory_info().rss/1024/1024
        print("Used Memory:", _total_memory , "MB")
        
        if len(new_f - C_full) == 0:
            print("No non-maximal cliques present")
        if len(C_full - new_f) == 0:
            print("No maximal cliques missed")

    ### copy the result into pickle
    pfile=open(result_file,'wb')
    pickle.dump(total_cycle_stat, pfile)
    pickle.dump(full_run_stat, pfile)
    pfile.close()
    
file_.close()