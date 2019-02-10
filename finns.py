import csv

import numpy as np
from scipy import stats


def finngen(names,file=None,ages=False,cities=False):
    name_paths = [
        "etunimet.csv",
        "sukunimet.csv"
        ]

    if ages:
        name_paths.append("iät.csv")

    if cities:
        name_paths.append("kunnat.csv")

    b = []

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

        dist = stats.rv_discrete(values=(xk,f_probs))
        i_f = dist.rvs(size=names)

        strings = [f_names[n] for n in i_f]

        b.append(strings)
    
    full_names = []
    l = len(b)
    
    for i in range(names):
        name = ""
        for j in range(l):
            substring = b[j][i]
            if j == 0:
                delimiter = ", "
            elif j < l-1:
                delimiter = ", "
            else:
                delimiter = ""
            name += substring + delimiter
        full_names.append(name)

    if file:
        with open(f"{file}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f,delimiter=',')
            [w.writerow(row.split(", ")) for row in full_names]

    return full_names
