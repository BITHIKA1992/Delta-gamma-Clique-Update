import sys
import pandas as pd
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt

Number_of_partions = 3
partition_type = 'm' ## or 'e' or 'm', 
Partion_Times = []

if len(sys.argv) == 2:
    filename = str(sys.argv[1])
else:
    #filename = './Datasets/infectious_69full.txt'
    #filename = './Datasets/infectious_dataset.txt'
    #filename = './Datasets/ht09_contact_list.txt'
    #filename = './Datasets/bitcoin.txt' # -- not used
    filename = './Datasets/college_msg.txt'
    #filename = './Datasets/haggle_contact.txt'
    #filename = './Datasets/as733full_new.txt'
    #filename = './Datasets/as180.txt'
    #filename = './Datasets/Powerlaw_5K.txt'
    print("Give the file name to read the link stream")

#filename='infectious_dataset.txt'
# Read stream  ### Add in life_cycle  Get the T1

life_cycle = dict()
file_ = open(filename, 'r')
times = dict()
nodes = set()

for line in file_:   
    contents = line.split(" ")
    t = int(contents[0])
    u = contents[1].strip()
    v = contents[2].strip()
    link = frozenset([u, v])
    if t not in life_cycle.keys():
        life_cycle[t] = []
    life_cycle[t].append(link)
    if link not in times.keys():
        times[link] = []
    times[link].append(t)
    nodes.add(u)
    nodes.add(v)
    

temp = [[i, len(life_cycle[i])] for i in life_cycle.keys()]
temp_df = pd.DataFrame(temp, columns=['ts', 'edgecount'])

#plt.rcParams['axes.labelsize'] = 20
#plt.rcParams['axes.labelweight'] = 'bold'
#plt.rcParams['axes.titlesize'] = 20
#plt.rcParams['axes.titleweight'] = 'bold'
#plt.rcParams['xtick.labelsize'] = 16
#plt.rcParams['ytick.labelsize'] = 16

plt.plot(temp_df[:]['ts'], temp_df[:]['edgecount'], 'o')
plt.ylabel("Number of links")
plt.xlabel("Time stamps")
plt.title("Link Count at Each Time stamp")
#plt.show()
plt.savefig("collegemsg_linkvsTS.jpg")

#### If T1 == (T2- T0)/2  ###  --- Slicing the lifecycle equally in two halves.
T1_equal =  int( min(temp_df[:]['ts']) + (max(temp_df[:]['ts']) - min(temp_df[:]['ts']))/2 )


####  Median... ---- Divide the edgecount equally
timestamps = []
for i in life_cycle.keys():
    for j in life_cycle[i]:
        timestamps.append(i)
T1_median = int(np.median(timestamps))

###################################################################################
print("Life cycle of the link stream***********")
print("Start Time:", min(timestamps ))
print("End Time:", max(timestamps ))
print("T1_equal:", T1_equal)
print("T1_median:", T1_median)

###################################################################################

plot_y = [len(times[i]) for i in times.keys()] 
plt.hist(plot_y)
plt.xlabel("Number of occurences")
plt.ylabel("Edge-Count")
plt.title("Histogram on static edge-count") #for Number of occurences of static edges")
plt.show()
#plt.savefig("powerlaw5K_hist.jpg")

print(Counter(plot_y))


if partition_type == 'e':
    for i in np.linspace(min(timestamps)-1, max(timestamps), Number_of_partions + 1):
        Partion_Times.append(int(np.ceil(i)))
    Partion_Times[0] = -1
    
if partition_type == 'm':
    for i in range(0,len(timestamps), round(len(timestamps)/Number_of_partions)):
        Partion_Times.append(int(timestamps[i]))
    Partion_Times[0] = -1
    if len(Partion_Times) < Number_of_partions + 1:
        Partion_Times.append(timestamps[-1])
        
print(Partion_Times)
        
        