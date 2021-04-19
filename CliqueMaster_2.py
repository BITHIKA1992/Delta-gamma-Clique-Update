# -*-coding:utf8*-
import sys
from collections import deque
from Clique_2 import Clique
import pandas as pd
from matplotlib import pyplot as plt
from collections import defaultdict
global dt
dt = 1
class CliqueMaster:

    def __init__(self):
        self._S = deque()
        self._S_set = set()
        self._R = set()
        self._Rext = set()   ######  Bithika : 01-04-2020 store the cliques that can be extended
        self._Rext1 = set() #### Bithika: for polishing
        self._times = dict()
        self._nodes = dict()
        #self._graph = nx.Graph()
        #self._result_list = []
        self._R_dic = defaultdict(list)
        self._iternum = 0
        self._maxsize = 0
        self._maxdur = 0


    def addClique(self, c):
        """ Adds a clique to S,
        checking beforehand that this clique is not already present in S. """
        if c not in self._S_set:
            self._S.appendleft(c)
            #self._S.append(c)
            self._S_set.add(c)

    def getClique(self):
        c = self._S.pop()
        #sys.stderr.write("\nGetting clique " + str(c) + "\n")
        return c

    def getDeltaCliques(self, delta):
        """ Returns a set of maximal cliques. """
        iternum = 0
        maxsize = 0
        maxdur = 0

        while len(self._S) != 0:
            iternum += 1
            sys.stderr.write("S:" + str(len(self._S)) + "\n")
            sys.stderr.write("T " + str(iternum) + " " + str(len(self._R)) + "\n")
            c = self.getClique()
            is_max = True

            # Grow time on the right side
            td = c.getTd(self._times, delta)
            if c._te != td + delta:
                c_add = Clique((c._X, (c._tb, td + delta)), c._candidates)
                self.addClique(c_add)
                sys.stderr.write(
                    "Adding " +
                    str(c_add) +
                    " (time delta extension)\n")
                is_max = False
            else:
                sys.stderr.write(str(c) + " cannot grow on the right side\n")

            # Grow time on the left side
            tp = c.getTp(self._times, delta)
            if c._tb != tp - delta:
                c_add = Clique((c._X, (tp - delta, c._te)), c._candidates)
                self.addClique(c_add)
                sys.stderr.write(
                    "Adding " +
                    str(c_add) +
                    " (left time delta extension)\n")
                is_max = False
            else:
                sys.stderr.write(str(c) + " cannot grow on the left side\n")

            # Grow node set
            candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
            sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

            for node in candidates:
                if c.isClique(self._times, node, delta):
                    Xnew = set(c._X).union([node])
                    sys.stderr.write(str(candidates) +
                                     " VS " +
                                     str(c._candidates) +
                                     "\n")
                    c_add = Clique(
                        (frozenset(Xnew), (c._tb, c._te)), c._candidates)
                    self.addClique(c_add)
                    sys.stderr.write(
                        "Adding " +
                        str(c_add) +
                        " (node extension)\n")
                    is_max = False

            if is_max:
                sys.stderr.write(str(c) + " is maximal\n")
                maxsize = max(maxsize, len(c._X))
                maxdur = max(maxdur, c._te - c._tb)
                sys.stderr.write("M " + str(iternum) + " " + str(maxsize) + " " + str(maxdur) + "\n")
                
                self._R.add(c)
                  
        return self._R

        
 

##### Bithika:
    def printCliques(self):
        sys.stdout.write('Number of Maximal Cliques: '+str(len(self._R)) + "\n")
        #print(self._result_list)
        #Maximal_Clique_df = pd.DataFrame(self._result_list, columns=['node_set', 'cardinality', 'tb', 'te', 'duration'])
        #Maximal_Clique_df.to_csv('result_clique.txt', index=False)
        for c in self._R:
            sys.stdout.write(str(c) + "\n")
            
#### Bithika:
    def printCliquesDistribution(self, delta):
        _result_list = []
        for c in self._R:
            _result_list.append([list(c._X), len(c._X), c._tb, c._te, c._te - c._tb])
        Maximal_Clique_df = pd.DataFrame(_result_list, columns=['node_set', 'cardinality', 'tb', 'te', 'duration'])
        Maximal_Clique_df = Maximal_Clique_df[['cardinality','duration']]
        Maximal_Clique_df = Maximal_Clique_df.astype(int) 
        Maximal_Clique_df = Maximal_Clique_df[ ~((Maximal_Clique_df['duration'] == 2*delta) & (Maximal_Clique_df['cardinality'] == 2))]       
        Maximal_Cardinality_df = Maximal_Clique_df.groupby(['cardinality'], sort=True).size().reset_index(name='counts')
        Maximal_Duration_df = Maximal_Clique_df.groupby(['duration'], sort=True).size().reset_index(name='counts')
        Maximal_df = Maximal_Clique_df.groupby(['cardinality','duration'], sort=True).size().reset_index(name='counts')
        print("Maximal cardinality DF:")
        print(Maximal_Cardinality_df)
        print("Maximal duration DF:")
        print(Maximal_Duration_df)
        print("Maximal DF:")
        print(Maximal_df)
        plt.bar(Maximal_Cardinality_df['cardinality'], Maximal_Cardinality_df['counts'])
        #plt.ylim(0,700)
        plt.xlabel('Cardinality')
        plt.ylabel('Count')
        plt.title('Frequency Distribution of Maximal Cardinality')
        plt.show()
        plt.plot(Maximal_Duration_df['duration'], Maximal_Duration_df['counts'])
        #plt.ylim(0,20)
        plt.xlabel('Duration')
        plt.ylabel('Count')
        plt.title('Frequency Distribution of Maximal Duration')
        plt.show()
        #Maximal_df = Maximal_df[1:]
        #Maximal_df[['cardinality','counts']].boxplot(by='cardinality')
        #plt.show()
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter( Maximal_df['cardinality'], Maximal_df['duration'], Maximal_df['counts'], c=Maximal_df['counts'])
        ax.set_title('Detailed View on #Maximal Cliques')
        ax.set_xlabel('Cardinality')
        ax.set_ylabel('Duration')
        ax.set_zlabel('Count')
        plt.show()

#### Bithika:           
    def printInitialCliques(self):
        for c in self._S:
            #sys.stdout.write(str(c) + ' neighbor candidates:' + str(c._candidates) + "\n")
            sys.stdout.write(str(c) + "\n")

#### Bithika:

    def getDeltaGammaCliques(self, delta, gamma, dt, Tb=None, Te= None):
        """ Returns a set of maximal cliques. """
        iternum = 0
        maxsize = 0
        maxdur = 0
        extended_clique_count = 0
        polished_clique_count = 0

        while len(self._S) != 0:
            iternum += 1
            #sys.stderr.write("S:" + str(len(self._S)) + "\n")
            #sys.stderr.write("T " + str(iternum) + " " + str(len(self._R)) + "\n")
            self._iternum = iternum
            c = self.getClique()
            is_max = True
            
            # Grow time on the right side
            td = c.getTd_2(self._times, delta, gamma)
            if c._te < td + delta:   #if c._te != td + delta:
                c_add = Clique((c._X, (c._tb, td + delta)), c._candidates)
                self.addClique(c_add)
                #sys.stderr.write( "Adding " + str(c_add) + " (time delta extension)\n")
                is_max = False
            else:
                pass
                #sys.stderr.write(str(c) + " cannot grow on the right side\n")
                
            # Grow time on the left side
            tp = c.getTp_2(self._times, delta, gamma)
            if c._tb > tp - delta:     #if c._tb != tp - delta:
                c_add = Clique((c._X, (tp - delta, c._te)), c._candidates)
                self.addClique(c_add)
                #sys.stderr.write("Adding " +str(c_add) + " (left time delta extension)\n")
                is_max = False
            else:
                pass
                #sys.stderr.write(str(c) + " cannot grow on the left side\n")


            # Grow node set
            candidates1 = c.getAdjacentNodes_2(self._times, self._nodes, delta, gamma)
            candidates = candidates1.intersection(c._candidates)
            c._candidates = candidates
            #sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

            for node in candidates:
                #print("Check:::", c.isClique_2(self._times, node, delta, gamma))
                if c.isClique_2(self._times, node, delta, gamma):
                    Xnew = set(c._X).union([node])
                    #sys.stderr.write(str(candidates1) + " VS " + str(c._candidates) + "\n")
                    #try:  ####  Bithika:  01-04-2020
                    #    neigh_set_temp = self._graph.neighbors(node)
                    #except:
                    #    neigh_set_temp = c._candidates                    
                    c_add = Clique(
                        (frozenset(Xnew), (c._tb, c._te)), c._candidates) #.intersection(set(list( self._graph.neighbors(node) ))))   ### static graph neighbors added in candidates
                    self.addClique(c_add)
                    #sys.stderr.write("Adding " + str(c_add) + " (node extension)\n")
                    is_max = False



            if is_max:
                #sys.stderr.write(str(c) + " is maximal\n")
                maxsize = max(maxsize, len(c._X))
                maxdur = max(maxdur, c._te - c._tb)
                #sys.stderr.write("M " + str(iternum) + " " + str(maxsize) + " " + str(maxdur) + "\n")
                self._iternum = iternum
                self._maxsize = maxsize
                self._maxdur = maxdur
                #self._result_list.append([list(c._X), len(c._X), c._tb, c._te, c._te - c._tb])  
                self._R.add(c)
                self._R_dic[c._X].append((c._tb, c._te))
                if c._tb <= Tb:
                    polished_clique_count += 1
                    self._Rext1.add(c)  
                    polished_clique_count += 1
                
            if c._te >= Te:
                extended_clique_count += 1
                self._Rext.add(c)

        return self._R
    
    def remove_sub_cliques(self):   
        temp = self._R_dic.copy()
        for c in self._Rext1:
            removed_first = 0
            if c._X in temp.keys():
                for item in temp[c._X]:
                    if (c._tb > item[0] and c._te <=item[1]) or (c._tb >= item[0] and c._te < item[1]):
                        if c in self._R:
                            self._R.remove(c)
                            self._R_dic[c._X].remove((c._tb, c._te))
                            removed_first += 1
                            #print(c, item)
            #print(removed_first)
            if removed_first == 0:
                flag = 0
                temp_list = [sub_X for sub_X in temp.keys() if len(c._X.difference(sub_X)) == 0]
                    #print(c, temp_list)
                for sub_X in temp_list:
                    if sub_X == c._X:
                        continue
                    for j in temp[sub_X]:
                        if c._tb >= j[0] and c._te <= j[1]:
                            if c in self._R:
                                flag += 1
                if flag > 0:
                    self._R.remove(c)
                    self._R_dic[c._X].remove((c._tb, c._te))
        del temp
        return
                    
    def getDeltaGammaCliques_RightTS(self, delta, gamma, dt, Tb=None, Te= None):
        """ Returns a set of maximal cliques. """
        iternum = 0
        maxsize = 0
        maxdur = 0
        extended_clique_count = 0
        polished_clique_count = 0

        while len(self._S) != 0:
            iternum += 1
            #sys.stderr.write("S:" + str(len(self._S)) + "\n")
            #sys.stderr.write("T " + str(iternum) + " " + str(len(self._R)) + "\n")
            self._iternum = iternum
            c = self.getClique()
            is_max = True
            
            # Grow time on the right side
            td = c.getTd_2(self._times, delta, gamma)
            if c._te < td + delta:   #if c._te != td + delta:
                c_add = Clique((c._X, (c._tb, td + delta)), c._candidates)
                self.addClique(c_add)
                #sys.stderr.write( "Adding " + str(c_add) + " (time delta extension)\n")
                is_max = False
            else:
                pass
                #sys.stderr.write(str(c) + " cannot grow on the right side\n")


            if is_max:
                #sys.stderr.write(str(c) + " is maximal\n")
                maxsize = max(maxsize, len(c._X))
                maxdur = max(maxdur, c._te - c._tb)
                #sys.stderr.write("M " + str(iternum) + " " + str(maxsize) + " " + str(maxdur) + "\n")
                self._iternum = iternum
                self._maxsize = maxsize
                self._maxdur = maxdur
                #self._result_list.append([list(c._X), len(c._X), c._tb, c._te, c._te - c._tb])  
                self._R.add(c)
                self._R_dic[c._X].append((c._tb, c._te))
                if c._tb <= Tb:
                    polished_clique_count += 1
                    self._Rext1.add(c)  
                    polished_clique_count += 1
                
            if c._te >= Te:
                extended_clique_count += 1
                self._Rext.add(c)
                

        return self._R
    

                        
    def __str__(self):
        msg = ""
        for c in self._R:
            msg += str(c) + "\n"
        return msg
