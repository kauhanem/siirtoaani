import csv

import numpy as numpy
from scipy import stats

def finngen(names,format="first sur",file=None):
    # lataa csv:t
    paths = [
        "miehet.csv",
        "naiset.csv",
        "kunnat.csv",
        "iät.csv"
    ]

    firsts = []
    others = []
    surs = []
    cities = []

    # määrittele funktiot
    def sex():
        s = sexes[s_d.rvs(size=1)]
        return s
    def name(s):
        n = firsts[n_d.rvs(size=1)]
        return n
    def surname():
        sn = surs[sr_d.rvs(size=1)]
        return sn
    def birthday(s):
        return b
    def idn(s,b):
        return id
    def city():
        c = cities[c_d.rvs(size=1)]
        return c
    
    # splittaa format-string
    p = []
    d = []

    # luo n nimeä loopissa
    full_names = []
    for i in range(names):
        s = sex()
        b = birthday(s)

        for j in range(len(p)):
            string = ""
            piece = p[j]
            delim = d[j]

            if piece == "name":
                P = name(s)
            elif piece == "surname":
                P = surname()
            elif piece == "birthday":
                P = b
            elif piece == "id":
                P = idn(s,b)
            elif piece == "city":
                P = city()
            
            string = P + delim
            full_names.append(string)
    
    # luo csv nimistä
    if file:
        with open(f"{file}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f,delimiter=',')
            [w.writerow(row.split(", ")) for row in full_names]

    # palauta nimet
    return full_names