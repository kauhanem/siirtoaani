import numpy as np
from scipy import stats
import csv

def finngen(names,name=None):
    name_paths = [
        "etunimet.csv",
        "sukunimet.csv"
        ]

    namebase = {}

    for path in name_paths:
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
        namebase[path] = [f_names,f_probs,xk]
    
    nms = namebase["etunimet.csv"][0]
    sur = namebase["sukunimet.csv"][0]
    pk_n = namebase["etunimet.csv"][1]
    pk_s = namebase["sukunimet.csv"][1]
    xk_n = namebase["etunimet.csv"][2]
    xk_s = namebase["sukunimet.csv"][2]

    first = stats.rv_discrete(values=(xk_n,pk_n))
    last = stats.rv_discrete(values=(xk_s,pk_s))

    i_n = first.rvs(size=names)
    i_s = last.rvs(size=names)

    full_names = []

    for i in range(len(i_n)):
        etu = nms[i_n[i]]
        suku = sur[i_s[i]]
        full_names.append(f"{etu} {suku}")

    if name:
        with open(f"{name}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f,delimiter=',')
            for line in full_names:
                w.writerow(line)

    return full_names