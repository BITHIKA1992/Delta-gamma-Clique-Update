# -*- coding: utf-8 -*-
"""
Created on Sun May 10 13:04:12 2020

@author: Bithika
"""
import pickle
import pandas as pd
#pfile=open('D:/Work-Research/Work with Suman/Delta-Gamma-Update/Code/new_code_v3/Results/infectious/Results_infectious_180_4_m.pkl','rb')
#total_cycle_stat = pickle.load(pfile)
#full_run_stat = pickle.load(pfile)
#pfile.close()


#for i in full_run_stat.keys():
#    print(type(full_run_stat[i]))
#    
#for i in total_cycle_stat.keys():
#    print(type(total_cycle_stat[i]))
    
    
    
Number_of_partition = 2 
partition_type = 'e'   
meta_file = "infectious_meta.txt"
final_result_file = "./Results/"+"Results_"+meta_file.split("_")[0]+'_'+str(partition_type)+'.csv'
final_result = []

file_ = open('./Datasets/' + meta_file, 'r')
for line in file_:
    contents = line.split(",")
    delta = int(contents[0])
    gamma = int(contents[1])
    
    if Number_of_partition <= 3:       
        result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' + str(partition_type)+'.pkl'
    else:
         result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' \
               + str(Number_of_partition) + str(partition_type)+'.pkl'  
    print(result_file)
    pfile=open(result_file,  'rb')
    total_cycle_stat = pickle.load(pfile)
    full_run_stat = pickle.load(pfile)
    pfile.close()
    
    
    ### Size(Count) of C_I_T1, C_T1, C_T1_ex, C_I_T2_T1, C_T2_check, C_T2_removed, C_T2_T1, C_T2
    ### Computational Time, Space
    
    ### Correctness check computational time and space
    C_I_T1 = total_cycle_stat['_intermediate_clique_count'][0]
    C_T1 = total_cycle_stat['_maximal_clique_count'][0]
    C_T1_ex = total_cycle_stat['_extended_clique_count'][0]
    
    C_I_T2_T1 = total_cycle_stat['_intermediate_clique_count'][1]
    C_T2_check = total_cycle_stat['_subclique_check_count'][1]
    C_T2_removed = total_cycle_stat['_removed_clique_count'][1]
    C_T2_T1 = total_cycle_stat['_maximal_clique_count'][1]
    
    C_T2 = total_cycle_stat['_new_max_clique_count'][1]
    new_f_time = sum(total_cycle_stat['_total_time'])
    new_f_space = max(total_cycle_stat['_total_space'])
    
    C_time = full_run_stat['_total_time']
    C_space = full_run_stat['_total_space']
    
    final_result.append([delta, gamma, C_I_T1, C_T1, C_T1_ex, C_I_T2_T1, C_T2_check,\
                         C_T2_removed, C_T2_T1, C_T2, new_f_time, new_f_space, C_time, C_space ])
    
column_names = [ 'delta', 'gamma',\
                'C_I_T1', 'C_T1', 'C_T1_ex', 'C_I_T2_T1', 'C_T2_check', 'C_T2_removed', 'C_T2_T1',\
                'C_T2', 'new_f_time', 'new_f_space', 'C_time', 'C_space']
df = pd.DataFrame(final_result, columns = column_names )
df.to_csv(final_result_file, index=False)
     
    
    