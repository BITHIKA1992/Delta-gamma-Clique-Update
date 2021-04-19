# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:27:18 2020

@author: Bithika
"""
from CliqueMaster_2 import CliqueMaster
from Clique_2 import Clique
import sys
import time as TM
from collections import deque, defaultdict
import psutil
import os
import gc


class edge_on_clique:
    def __init__(self,links_prev_delta, new_links_file, C_T1, C_T1_ex, delta, gamma, T1, T2):
        ## inputs
        self.links_prev_delta = links_prev_delta
        self.new_links_file = new_links_file
        self.C_T1_ex = C_T1_ex
        self.C_T1 = C_T1
        self.delta = delta
        self.gamma = gamma
        self.T1 = T1
        self.T2 = T2
        
        #outputs, and processing
        self.Cm_2 = CliqueMaster()
        ### keep the links of last delta duration to process in next update cycle
        self.links_post_delta = [] 
        self.new_f = set()
        self.new_f_maxsize = 0
        self.new_f_maxdur = 0
        
        ### Some Statistics Data:
        self._node_count = 0  # -- done
        self._static_edge_count = 0  # -- done
        self._temporal_link_count = 0  # -- done
        
        self._subclique_check_count = 0
        self._subclique_check_size = 0
        self._extended_clique_count = 0
        self._extended_clique_size = 0
        self._intermediate_clique_count = 0
        self._intermediate_clique_size = 0
        self._maximal_clique_count = 0
        self._maximal_clique_size = 0
        self._removed_clique_count = 0
        
        self._extra_space_subclique_check = 0 # -- done
        self._extra_space_link_store = 0  # -- done
        
        self._prepare_data_time = 0  # -- done
        self._rightts_expand_time = 0  # -- done
        self._enumerate_time = 0  # --done
        self._removal_time = 0  # -- done
        self._total_time = 0  # -- done
        self._total_space = 0 # -- done
        
        self._stat = dict()
        
    def read_links_for_current_update(self):
        current_links = []
        file_ = open('./Datasets/' + self.new_links_file, 'r')
        for line in file_:
            contents = line.split(" ")
            t = int(contents[0])
            u = str(contents[1].strip())
            v = str(contents[2].strip())
            
            if t > self.T1 and t <= self.T2:
                current_links.append([t, u, v])
                self._temporal_link_count +=1
        file_.close()
        return current_links
        
    def prepare_data(self):
        #### Prepare the data for processing
        start_time = TM.time()
        times_2 = defaultdict(list)
        nodes_2 = defaultdict(set)
        nb_lines = 0
        
        ### Add the links from previous delta duration
        for item in self.links_prev_delta:
            t = int(item[0])
            u = str(item[1])
            v = str(item[2])
            link = frozenset([u, v])
            
            times_2[link].append(t)
            nodes_2[u].add(v)
            nodes_2[v].add(u)
            nb_lines += 1
            
        end_time = TM.time()
        self._prepare_data_time += float("{:.3f}".format(end_time - start_time))
        
        current_links = self.read_links_for_current_update()
        
        start_time = TM.time()
        for item in current_links:
            t = int(item[0])
            u = str(item[1])
            v = str(item[2])
            link = frozenset([u, v])
            
            times_2[link].append(t)
            nodes_2[u].add(v)
            nodes_2[v].add(u)
            nb_lines += 1
                
            if t >= self.T2 - self.delta:
                self.links_post_delta.append([t, u, v])
                
        self.Cm_2._times = times_2
        self.Cm_2._nodes = nodes_2
        
        
        ### stat
        self._node_count += len(nodes_2.keys())
        self._static_edge_count += len(times_2.keys())
        end_time = TM.time()
        self._prepare_data_time += float("{:.3f}".format(end_time - start_time))
        self._extra_space_link_store += ((  sys.getsizeof(times_2) \
                                          + sys.getsizeof(current_links) \
                                          + sys.getsizeof(nodes_2))/1024.0 )
        del current_links
        
        print("****** Prepare Data Statistics **********")
        print("Delta, Gamma: ", self.delta, self.gamma )
        print("[T1, T2] : ", self.T1, self.T2)
        print("Number of Nodes: ", self._node_count)
        print("Number of static edges: ", self._static_edge_count)
        print("Number of New links in the current update: ", self._temporal_link_count)
        print("Total links to be processed including previous delta: ", nb_lines)
        print("Number of links for last delta: ", len(self.links_post_delta))
        print("Time to Pre-Process data: ", self._prepare_data_time)
        
        return 
    
    def initialize_delta_gamma_clique(self, delta, gamma):
        print("****** Initialization **********")
        start_time = TM.time()
        for e in self.Cm_2._times.keys():
            link = e
            temp_ts = self.Cm_2._times[link]
            temp_ts.sort()
            if len(temp_ts) >= gamma:
                for i in range(len(temp_ts) - gamma +1):
                    if (temp_ts[i + gamma-1] - temp_ts[i]) == delta:
                        tb = temp_ts[i]
                        te = temp_ts[i + gamma-1]
                        time0 = (tb, te)
                        c = Clique((link, time0), set([]))
                        c.getAdjacentNodes_2(self.Cm_2._times, self.Cm_2._nodes, delta, gamma)
                        self.Cm_2.addClique(c)
                    elif (temp_ts[i + gamma-1] - temp_ts[i]) < delta:
                        tb = temp_ts[i]
                        te = temp_ts[i + gamma-1]
                        time1 = (te-delta, te)
                        time2 = (tb, tb + delta)
                        c1 = Clique((link, time1), set([]))
                        c1.getAdjacentNodes_2(self.Cm_2._times, self.Cm_2._nodes, delta, gamma)
                        self.Cm_2.addClique(c1)   
                        c2 = Clique((link, time2), set([]))
                        c2.getAdjacentNodes_2(self.Cm_2._times, self.Cm_2._nodes, delta, gamma)
                        self.Cm_2.addClique(c2) 
        end_time = TM.time()
        print("Initialized Clique Count in Current update cycle:", len(self.Cm_2._S_set))
        print("Initialization Time: ", float("{:.3f}".format(end_time - start_time)))
        return 

    def final_clique_set_build(self):
        if self.T1 == -1:
            start_time = TM.time()
            self.new_f = self.Cm_2._R
            end_time = TM.time()
            self.new_f_maxsize += self.Cm_2._maxsize
            self.new_f_maxdur += self.Cm_2._maxdur
            self._total_time += float("{:.3f}".format(end_time - start_time))
            #self._total_space += (len(self.new_f)/1024/1024)
            self._total_space += (sys.getsizeof(self.new_f)/1024.0)
            return
        else:
            start_time = TM.time()
            self.new_f = self.Cm_2._R.union(self.C_T1 - self.C_T1_ex)
            end_time = TM.time()
            _maxsize = []
            _maxdur = []
            for c in self.new_f:
                _maxsize.append(len(c._X))
                _maxdur.append(c._te - c._tb)
            self.new_f_maxsize += max(_maxsize)
            self.new_f_maxdur += max(_maxdur)            
            self._total_time += float("{:.3f}".format(end_time - start_time))
            #self._total_space += (len(self.new_f)/1024)
            self._total_space += (sys.getsizeof(self.new_f)/1024.0)
            return
                

    def enumerate_edge_on_clique(self):
        ### prepare data for processing
        self.prepare_data()
        
        ### extend the right time stamp of the cliques in C_T1_ex
        if self.T1 != -1:
            start_time = TM.time()
            for c in self.C_T1_ex:
                self.Cm_2.addClique(c)
            self.Cm_2.getDeltaGammaCliques_RightTS(self.delta, self.gamma, dt=1,\
                                                   Tb= self.T1, Te= self.T2)
            end_time = TM.time()
            
            ### stat:
            self._intermediate_clique_count += len(self.Cm_2._S_set)
            self._intermediate_clique_size += (sys.getsizeof(self.Cm_2._S_set)/1024.0)
            self._rightts_expand_time = float("{:.3f}".format(end_time - start_time))
            print("****** Right TS expansion -- from previous update **********")
            print("Intermediate clique count (for right ts only):", self._intermediate_clique_count)
            print("Intermediate clique size(KB) (for right ts only):", self._intermediate_clique_size)
            print("Right TS expansion time:", self._rightts_expand_time)
            
            #### free up memory space
            self.Cm_2._S = deque()
            self.Cm_2._S_set = set()
            
        ### Initialize the cliques
        start_time = TM.time()
        self.initialize_delta_gamma_clique(self.delta, self.gamma)
        ### Enumerate with the expansion in three ways
        self.Cm_2.getDeltaGammaCliques(self.delta, self.gamma, dt=1, Tb= self.T1, Te=self.T2)
        end_time = TM.time()
        
        ### stat:  ################
        print("****** Enumeration **********")
        self._enumerate_time = float("{:.3f}".format(end_time - start_time))        
        self._subclique_check_count += len(self.Cm_2._Rext1)
        self._subclique_check_size += (sys.getsizeof(self.Cm_2._Rext1)/1024.0)
        self._extended_clique_count += len(self.Cm_2._Rext)
        self._extended_clique_size += (sys.getsizeof(self.Cm_2._Rext)/1024.0)
        self._intermediate_clique_count += len(self.Cm_2._S_set)
        self._intermediate_clique_size += (sys.getsizeof(self.Cm_2._S_set)/1024.0)
        print("Clique Count for extension: ", self._extended_clique_count)
        print("Clique Size for extension (KB): ", self._extended_clique_size)
        print("Intermediate Clique Count for extension: ", self._intermediate_clique_count)
        print("Intermediate clique size for extension (KB): ", self._intermediate_clique_size)
        print("Maximal clique count before removal of subcliques: ", len(self.Cm_2._R))
        print("Enumeration time: ", self._enumerate_time)
        #### free up memory space
        self.Cm_2._S = deque()
        self.Cm_2._S_set = set()
        self._extra_space_subclique_check += (sys.getsizeof(self.Cm_2._R_dic)/1024.0)  ### as twice counted
        ###########################
        
        ### Removal of sub-cliques
        if self.T1 != -1: 
            start_time = TM.time()
            self.Cm_2.remove_sub_cliques()
            end_time = TM.time()
        
            ### Stat:  #######
            print("****** Removal of subcliques **********")
            self._removal_time += float("{:.3f}".format(end_time - start_time)) 
            self._removed_clique_count += len(self.Cm_2._Rext1 - (self.Cm_2._R.intersection(self.Cm_2._Rext1)))
            self._extra_space_subclique_check += (sys.getsizeof(self.Cm_2._R_dic)/1024.0)
            print("Subclique_Check_Count: ", self._subclique_check_count)
            print("Subclique_Check_Size(KB): ", self._subclique_check_size)
            print("removed_clique_count: ", self._removed_clique_count)
            print("Extra space for removal(KB):", self._extra_space_subclique_check)
            print("Removal Time:", self._removal_time)
            #### free up memory space
            self.Cm_2._R_dic = defaultdict(list)
            self.Cm_2._Rext1 = set()
        

        ### stat: for total computation
        self._maximal_clique_count += len(self.Cm_2._R)
        self._maximal_clique_size += (sys.getsizeof(self.Cm_2._R)/1024.0)
        self._total_time += (self._prepare_data_time \
                             + self._rightts_expand_time \
                             + self._enumerate_time \
                             + self._removal_time )
        self._total_space += ((self._subclique_check_size + self._extended_clique_size \
                          + 2 * self._intermediate_clique_size + self._maximal_clique_size \
                          + self._extra_space_subclique_check + self._extra_space_link_store))
        
        ###  Total maximal clique set till T2
        self.final_clique_set_build()
        self.get_statistics()
        
        return self.new_f, self.Cm_2._Rext, self.links_post_delta, self._stat
        
        
    def get_statistics(self):
        self._stat['_node_count'] = self._node_count 
        self._stat['_static_edge_count'] = self._static_edge_count
        self._stat['_temporal_link_count'] = self._temporal_link_count 

        self._stat['_intermediate_clique_count'] = self._intermediate_clique_count 
        self._stat['_intermediate_clique_size'] = self._intermediate_clique_size 
        self._stat['_subclique_check_count'] = self._subclique_check_count 
        self._stat['_subclique_check_size'] = self._subclique_check_size 
        self._stat['_removed_clique_count'] = self._removed_clique_count 
        
        self._stat['_maximal_clique_count'] = self._maximal_clique_count
        self._stat['_maximal_clique_size'] = self._maximal_clique_size
        self._stat['_extended_clique_count'] = self._extended_clique_count 
        self._stat['_extended_clique_size'] = self._extended_clique_size 

    
        self._stat['_prepare_data_time'] = self._prepare_data_time 
        self._stat['_rightts_expand_time'] = self._rightts_expand_time 
        self._stat['_enumerate_time'] = self._enumerate_time
        self._stat['_removal_time'] = self._removal_time
        
        self._stat['_total_time'] = self._total_time
        self._stat['_total_space'] = self._total_space
        self._stat['_new_max_clique_count'] = str(len(self.new_f))
        self._stat['_max_cardinality'] = str(self.new_f_maxsize)
        self._stat['_max_duration'] = str(self.new_f_maxdur)
        
        print("****** Total Statistics **********")
        print("Number of Intermediate Cliques: ", self._intermediate_clique_count )
        print("Number of Cliques to be extended: ", self._extended_clique_count )
        print("Number of Cliques to be removed: ", self._removed_clique_count )
        print("Number of Maximal cliques: ", str(len(self.new_f)), "till timestamp-", self.T2  )
        print("Max cardinality: ", str(self.new_f_maxsize) )
        print("Max duration: ", str(self.new_f_maxdur) )
        print("Total Time for current update: ", self._total_time )
        print("Total Space(KB) for current update: ", self._total_space )
        print("***********************************")
        
        #process = psutil.Process(os.getpid())
        #self._total_memory = process.memory_info().rss/1024/1024
        #print("Used Memory:", self._total_memory , "MB")
        

if __name__ == "__main__": 
    correctness_check = True
    Partion_Times = [-1, 1247664519, 1247680559]
    delta = 420
    gamma = 4
    data_file = "infectious_dataset"
    total_cycle_stat = defaultdict(list)
    
    for i in range(len(Partion_Times) -1):
        T1 = Partion_Times[i]
        T2 = Partion_Times[i+1]
        print("#####################", T1, T2, "#################")
        new_links_file = data_file + "_" + str(T2)+".txt"
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
    print("########  Correctness check ##########")
    if correctness_check:
        ec = edge_on_clique([], data_file+".txt" , set(), set() ,\
                                     delta, gamma, Partion_Times[0], Partion_Times[-1])
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
            
    #result = { **total_cycle_stat, **full_run_stat }
    