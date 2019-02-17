import csv

import numpy as np
from scipy import stats

class nameGen:
    def __init__(self,paths):
        self.distributions = {
            "sex" : self.createSexDist(paths["sex"]),
            "first" : self.createFirstDist(paths["first"]),
            "other" : self.createOtherDist(paths["other"]),
            "sur" : self.createSurDist(paths["sur"]),
            "bday" : self.createBDayDist(paths["bday"]),
            "city" : self.createCityDist(paths["city"])
        }

    def generatePiece(self,piece,names):
        return self.distributions[piece].rvs(size=names)
    
    
    def createSexDist(self,path):
        fl = []
        f_names = []
        f_probs = []
        
        total = 0
        with open(path,'r',encoding='utf-8') as f:
            for line in f:
                values = line.split(',')
                values[1] = int(values[1])
                total += values[1]
                fl.append(values)

        for k in fl:
            f_names.append(k[0])
            k[1] = float(k[1]/total)
            f_probs.append(k[1])
        
        xk = np.arange(len(f_names))

        f.close()

        return stats.rv_discrete(values=(xk,f_probs))

    def createFirstDist(self):
        

def finngen(names,name_format="first sur",file=None):
    # lataa csv:t
    paths = {
        "miehet.csv",
        "naiset.csv",
        "kunnat.csv",
        "iät.csv"
    }

    firsts = []
    others = []
    surs = []
    cities = []
    sexes = []
    
    # splittaa format-string
    f_s = ""
    d_s = ""
    f_l = []
    
    for i in name_format:
        if i.isalpha():
            if d_s:
                f_l.append(d_s)
                d_s = ""
            f_s += i
        else:
            if f_s:
                f_l.append(f_s)
                f_s = ""
            d_s += i
    if f_s:
        f_l.append(f_s)
    else:
        f_l.append(d_s)

    # luo n nimeä loopissa
    full_names = []
    string = ""
    full_names.append(string)
    
    # luo csv nimistä
    if file:
        with open(f"{file}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f,delimiter=',')
            [w.writerow(row.split(", ")) for row in full_names]

    # palauta nimet
    return full_names