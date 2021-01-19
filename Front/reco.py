import warnings
import numpy as np
import os, sys, getopt, glob
import scipy.sparse.csgraph
import pprint
import json
import datetime

dma = datetime.date.today()
dmin = datetime.date(2014, 1, 1)
dmax_integers = dma-dmin
dmax = dmax_integers.days


def as_ChronicleNegfromVisu(o):
    c = ChronicleReco()
    o_new = {"items":{}, "info":{}, "tconst":{}}
    for item_index, data in enumerate(o) :
        o_new["items"][item_index] = (data["labels"][0],0)
        o_new["info"][item_index] = ("DrugDelivery", "drugDelivered", "atc")
        for const in data["successors"] :
            tupleof_items = (item_index,int(const["_dest"]))
            o_new["tconst"][tupleof_items] = {0 : (int(const["_u"]), int(const["_l"]))}
    o_new["subclass"] = []
    o_new["pid"] = 0
    #c.__dict__ = o
    c.add_chronicle(o_new)
    return c

class ChronicleReco:
    """Class for a chronicle pattern modelingo
    """
    
    npat = 0
    def __init__(self):
        
        self.tconst = {}  #temporal constraints,
                        # keys: couple (ei,ej) where ei is a index in the item ei vers ej
                        #   in the multiset
                        # values; couple (lb,ub)
        self.inconsistent = False
        self.items = {}      # description of the pattern events, id du dernier item doit être egal à la taille de la sequence
        self.info = {}        # define type for each item
        self.subclass = []
        self.pid = ChronicleReco.npat   # pattern id
        self.__size = 0
        self.tidl_pos = []
        ChronicleReco.npat += 1

    def __len__(self):
        return self.__size

    def __iter__(self):
        for const, v in self.tconst.items():
            yield (const, v), self.items[const[0]], self.items[const[1]]

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def add_chronicle(self, chro):
        self.add_items(chro['items'])
        self.add_subclass(chro['subclass'])
        self.add_info(chro['info'])
        self.add_constraints(chro['tconst'])
        self.pid = chro["pid"]
        #self.tidl_pos = chro["tidl_pos"]
        #self.verif_neg()
        self.__size = len(self.items) 
        if self.inconsistent :
            raise NameError('Inconsistent Chronicle')

    def add_items(self, items):
        """Add an item to the chronicle
        The function creates all infinite constraints, without variability
        - the id of the event correspond to the order of added items
        """
        for ide, name in items.items(): 
            #ide : numeric id of the item
            #name : tuple (name, type) type is 0(classic) or 1(negation)
            self.items[ide] = name
            self.__size += 1
            for i in range(ide+1, self.__size):
                try:
                    if (self.items[i] == name) and (name[1] == 0): #avoid to find same event if two same items in chronicle
                        self.tconst[(i,ide)] = {0:(1,float("inf")) } 
                except:
                    pass
                    

    def add_info(self, info):
        """Add complementary infos of a state in the chronicle
        -pos correspond to the order of added items
        -infos is a n-tuple containing info of the item 
        """
        citems = set(self.items.keys())
        infitems = set(info.keys())
        infprob = citems - infitems #as much info as items
        itemprob = infitems - citems #as much info as items

        if infprob or itemprob :
            if infprob:
                print("error: Following item info missing, ", infprob)
            else :
                print("error: Items info ",itemprob," is not a chronicle item, ")
            self.inconsistent = True
            return
        else:
            self.info = info
        
    def add_subclass(self, subclass):
        newsub = [] #to make couple of subclasses (simply verif)
        for sb in subclass:
            if not type(sb) is tuple:
                self.inconsistent = True
                print ("error: subclass must be a tuple ")
                return
            sbsorted = sorted(set(sb)) 
            if sbsorted[0] not in self.items:
                    self.inconsistent = True
                    print ("error in subclass add : ", sbsorted[0] ," is not a chronicle item")
                    return
            for i in range(1,len(sbsorted)) :  
                if sbsorted[i] not in self.items:
                    self.inconsistent = True
                    print ("error in subclass add : ", sbsorted[i] ," is not a chronicle item ")
                    return
                elif self.items[sbsorted[i]][1] == 1:
                    self.inconsistent = True
                    print ("error in subclass add : ", sbsorted[i] ," is a negative item")
                    return
                else : #add constraint for same class of item
                    self.tconst[(sbsorted[i-1],sbsorted[i])] = {0:(1,float("inf")) }
                    newsub.append((sbsorted[i-1],sbsorted[i]))

        self.subclass = newsub


    def add_constraints(self, tconst):
        """Add a constraint-template to the chronicle pattern
        - ei, ej: index of the events in the multiset
        - constr: a 2-tuple (min,max) 
        """
        #Dans args on a e'' eventuellement
        self.tconst.update(tconst)
        
        for eiej, edge in tconst.items(): #link bewteen ei and ej

            for typetr, constr in edge.items():

                if not type(eiej) is tuple:
                    del self.tconst[eiej]
                    print ("error: constraint ", eiej, " must be a tuple => ignored")
                    break;
                    
                if len(eiej) != 2:
                    del self.tconst[eiej]
                    print ("error: constraint ", eiej ," must have 2 values => ignored ")
                    break;

    def convert_dates_to_integers(self,sequence):
        new_seq = {}
        id_to_date = {}
        for event, list_dates in sequence.items():
            new_seq[event] = []
            for date in list_dates :
                delta = date-dmin
                new_seq[event].append (delta.days)
                id_to_date[delta.days] = date

        return new_seq, id_to_date


    def recognize(self,sequence_with_dates):
        #sequence and dates are sorted
        """
        Method that checks whether the chronicle occurs in the sequence 
        sequence: list of events
        Return a list of occurrences
        """
        sequence, id_to_date = self.convert_dates_to_integers(sequence_with_dates)
        occurrences = [] #list of occurrences 
        item = self.items[0][0] 
        first_tconst = [k for k in self.tconst if k[0]==0] #take every constraints from item 0
        if self.items[0][1] == 1:
            print("First chronicle item must be positive")
            return
            
        if not sequence  :
            print("no events found in the sequence\n")
            return occurrences
        #print("SEQUENCE: ", sequence)
        if item in sequence: #try item exists in seq
            all_occs = []
            # print("item: ",item)
            for date in sequence[item]: #all occurrences dates
                #init occs
                occs = [{0:(-float("inf"),float("inf"))}]*self.__size
                for k,(_,neg) in self.items.items() :
                    if neg == 1:
                        occs[k] = {1:(-float("inf"),float("inf"))} 
                occs[0] = {0:(date,date)} 
                #propagate constraints from the first item
                all_occs.append(occs)
            all_occs = self.propagate(first_tconst, 0, sequence, all_occs)
            all_occs = self.__recrecognize__(all_occs, 1, sequence)
            if all_occs:
                occurrences.extend( all_occs ) #cause occs is a lsit of lists
            #add occurrence to list of occurences
        # print("\n FINAL \n occurrences : \n",occurrences)

        # Easy format for the visu : list of occurrences[{"A001":date},{item_name:date}]
        new_occs = [list(map(lambda x : id_to_date[x[0][0]], e)) for e in all_occs[0]]
        new_occs_with_itemsname = [[(self.items[item_num][0], date) for item_num, date in enumerate(new_occ)] for new_occ in new_occs]
        return new_occs_with_itemsname

    def propagate(self, futur_tconst, item_index, sequence, occs):

        global dmax
        new_occs = []

        for occ in occs:
            cpt = 0
            for eiej in futur_tconst: #remind ei is item_index
                # print("futur_tconst eiej :", eiej)
                ej = eiej[1]
                ei = eiej[0]

                if 0 in self.tconst[eiej] : #check if positive edge
                    try :
                        date = occ[ei][0][1]
                    except :
                        date = occ[ei][1][1]
                    titj = self.tconst[eiej][0]
                    ejless = max(0,date+titj[0],occ[ej][0][0]) #lower bound where ej must occur
                    ejup = min(date+titj[1],dmax,occ[ej][0][1]) #upper bound where ej must occur
                    if ejless <= ejup:
                        occ[ej] = {0:(ejless,ejup)}
                    else :
                        break;

                elif 1 in self.tconst[eiej] : #check if negative edge
                    titj = self.tconst[eiej][1]
                    nj = self.items[ej][0]
                    try :
                        date = occ[ei][0][1]
                    except :
                        date = occ[ei][1][1]
                    if occ[ej][1][1] != float("inf"):
                        #Conjunction of neg
                        #Has to occur during the observable period ()
                        tmin = max(0, min(date+titj[0],occ[ej][1][0])) #take min lower bound
                        tmax = min(dmax, max(date+titj[1],occ[ej][1][1])) #take max upper bound
                    else :
                        tmin = date+titj[0]
                        tmax = date+titj[1]
                    if (tmin > tmax) or (tmax > dmax) or (tmin < 0): #check if interval is valid
                        break;
                    else :
                        interval1 = set(range(tmin,tmax+1))
                        try :
                            dates_ck = set(sequence[nj]) & interval1 #inter btw item occurrence date and given interval
                        except :
                            dates_ck = set()
                        if not dates_ck :
                            occ[ej] = {1:(tmin,tmax)}
                        else :
                            break;
                cpt += 1
            if cpt == len(futur_tconst) : # all the const have been verified
                new_occs.append(occ)
                # print(" all the const have been verified :", occ)
        return new_occs

    def __recrecognize__(self, occs, item_index, sequence):
        """
        recursive call for occurrence recognition
        return a list of occurrences recognized from the last_item_index of the chronicle until its last item
        """
        global dmax
        satisfaible = False

        if item_index == self.__size:
            return [occs]
        else:
            futur_tconst = [(ei,ej) for ei,ej in self.tconst if ei == item_index ]
        
        occurrences = []
        ck = self.items[item_index][0]
        for occ in occs :
            # print("NEW OCC in item", item_index)
            new_new_occ = []
            new_occs = []
            if 0 in occ[item_index] :
                max_occ = max(occ[item_index][0][0],0)
                min_occ = min(occ[item_index][0][1]+1,dmax)
                interval0 = set(range(int(max_occ),int(min_occ)+1))
                try :
                    dates_ck = set(sequence[ck]) & interval0 # All dates from occurence date of ck in the given interval0
                    satisfaible = True
                except :
                    dates_ck = set()
                    satisfaible = False
                for d in dates_ck: #become dates
                    if satisfaible == True :
                        new_occ = occ[:]
                        new_occ[item_index] = {0:(d , d)}
                        new_occs.append(new_occ)
                        # print("occurrence candidate", new_occ, "is satisfaible")

                if satisfaible == True and new_occs :
                    if futur_tconst :
                        new_occs = self.propagate(futur_tconst, item_index, sequence, new_occs)
                        new_new_occ.extend(new_occs)
                    else :
                        new_new_occ.extend(new_occs)

            elif 1 in occ[item_index] :
                # print("occurrence candidate", occ, "is satisfaible (neg item)")
                new_occs.append(occ)
                if futur_tconst :
                    new_occs = self.propagate(futur_tconst, item_index, sequence, new_occs) 
                    #Propagation based on end of interval
                    new_new_occ.extend(new_occs)
                    
                else :
                    new_new_occ.extend(new_occs)  
            
            if new_new_occ:
                new_new_occ = self.__recrecognize__(new_new_occ, item_index+1, sequence)
                occurrences.extend(new_new_occ)

        return occurrences