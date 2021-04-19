# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:32:00 2020

@author: Bithika
"""

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
    
####  Take the result of independent run  
    
Number_of_partition = 2
partition_type = 'm'   
meta_file = "infectious_meta_new.txt"
final_result_file = "./Results/"+"Results_"+meta_file.split("_")[0]+'_meta_new_time_space.csv'
final_result = []

file_ = open('./Datasets/' + meta_file, 'r')
for line in file_:
    contents = line.split(",")
    delta = int(contents[0])
    gamma = int(contents[1])
    
    if Number_of_partition < 3:       
        result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' + str(partition_type)+'_wp.pkl'
    else:
         result_file = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                        + meta_file.split("_")[0] + '_' \
               + str(delta) + '_' + str(gamma) + '_' \
               + str(Number_of_partition) + str(partition_type)+'_wp.pkl'  
               
    print(result_file)
    pfile=open(result_file,  'rb')
    total_cycle_stat = pickle.load(pfile)
    pfile.close()
    
    result_file_1 = result_file.split("_wp.pkl")[0] +'_wop.pkl' 
    pfile1=open(result_file_1,  'rb')
    full_run_stat = pickle.load(pfile1)
    pfile1.close()
    print(result_file_1)
    
    if meta_file.split("_")[0] != 'as180':
        if Number_of_partition < 3:                          
            result_file_e = "./Results/"+meta_file.split("_")[0]+"/Results_" \
                            + meta_file.split("_")[0] + '_' \
                   + str(delta) + '_' + str(gamma) + '_' + str('e')+'_wp.pkl'
        else:
            result_file_e =  "./Results/"+meta_file.split("_")[0]+"/Results_" \
                            + meta_file.split("_")[0] + '_' \
                   + str(delta) + '_' + str(gamma) + '_' \
                   + str(Number_of_partition) + str('e')+'_wp.pkl' 
        print(result_file_e)
        pfile=open(result_file_e,  'rb')
        total_cycle_stat_e = pickle.load(pfile)
        pfile.close()


    
    
    ### Size(Count) of C_I_T1, C_T1, C_T1_ex, C_I_T2_T1, C_T2_check, C_T2_removed, C_T2_T1, C_T2
    ### Computational Time, Space
    
    ### Correctness check computational time and space

    new_f_m_time = sum(total_cycle_stat['_total_time'])
    new_f_space_m_KB = max(total_cycle_stat['_total_space'])
    new_f_pspace_m_MB = total_cycle_stat['_total_process_memory_MB'][0]
    
    new_f_e_time = sum(total_cycle_stat_e['_total_time'])
    new_f_space_e_KB = max(total_cycle_stat_e['_total_space'])
    new_f_pspace_e_MB = total_cycle_stat_e['_total_process_memory_MB'][0]
    
    C_time = full_run_stat['_total_time']
    C_space_KB = full_run_stat['_total_space']
    C_pspace_MB = full_run_stat['_total_process_memory_MB']
    
    final_result.append([delta, gamma, new_f_e_time, new_f_m_time, C_time, \
                         new_f_space_e_KB, new_f_space_m_KB, C_space_KB, \
                         new_f_pspace_e_MB, new_f_pspace_m_MB, C_pspace_MB])
    
column_names = ['delta', 'gamma',\
                'new_f_e_time', 'new_f_m_time', 'C_time', \
                'new_f_space_e_KB', 'new_f_space_m_KB', 'C_space_KB', \
                'new_f_pspace_e_MB', 'new_f_pspace_m_MB', 'C_pspace_MB']
df = pd.DataFrame(final_result, columns = column_names )
df.to_csv(final_result_file, index=False)
     
    
