# -*- coding: utf-8 -*-
"""
Assignment 3
"""

import math

from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # m:
    # the number of recommedations to return
    # defaults to 10
    #
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        lst = []
        lst4 = []
        flst = []
        finalR = {}
        sumPofX = 0
        lstY = []
        
        for userY, userYRatings in self.usersItemRatings.items():
            if userX != userY:
                PearXY = self.pearsonFn(self.usersItemRatings[userX],self.usersItemRatings[userY])
                normPearXY = (PearXY+1)/2
                tup = (userY,normPearXY)
                lst.append(tup)
                
        sortedlst = sorted(lst, key=itemgetter(1), reverse = True)
        # print(sortedlst)
        # print()

        for j in range(self.k):
            lst4.append(sortedlst[j])
            sumPofX = sumPofX + sortedlst[j][1]
        
        if (len(lst4) == 1):
            nameOfNei = lst4[0][0]
            userXItemRatings = self.usersItemRatings[userX]
            userYItemRatings = self.usersItemRatings[nameOfNei]
            for item in userYItemRatings.keys():
                if (item not in userXItemRatings.keys()):
                    key = item
                    val = self.usersItemRatings[nameOfNei][key]

                    tup = (key, val)
                    flst.append(tup)
                finalR[userX] = flst 

            return finalR[userX]
                
            
        elif (len(lst4) >1):
            userYItemRatings = self.usersItemRatings[userY]
            userXItemRatings = self.usersItemRatings[userX]
            
            itemlst = []
            for i in range(self.k):
                for item in self.usersItemRatings[sortedlst[i][0]].keys():    
                    if item not in self.usersItemRatings[userX].keys():
                        itemlst.append(item)
            itemlst = set(itemlst)
            # print(itemlst)
            
            
            for i in lst4:
                name = i[0]
                w = i[1]/sumPofX
                tup = (name, w)
                lstY.append(tup)
            # print(lstY)
            
            
            Rec = {}
            for item in itemlst:
                Rec[item] = 0
                for i in range(self.k):
                    if item in self.usersItemRatings[sortedlst[i][0]].keys():
                        Rec[item] = Rec[item] + lstY[i][1]*self.usersItemRatings[sortedlst[i][0]][item]
                Rec[item] = round(Rec[item],2)
            # print (Rec)
            # print(type(Rec))
            
            fRecs = sorted(Rec.items(), key=itemgetter(1), reverse=True)
            return(fRecs)
            




        
