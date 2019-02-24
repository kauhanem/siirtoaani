import csv

import numpy as np
from scipy import stats


class Dist:
    def __init__(self, path):
        self.f_names = []
        f_probs = []

        total = 0
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                values = line.split(',')

                if len(values) == 2:
                    name = values[0]
                    value = values[1]

                    self.f_names.append(name)

                    value = int(value)
                    total += value

                    f_probs.append(value)

                elif len(values) > 2:
                    year = values[0]
                    months = values[1:]

                    for m in range(len(months)):
                        name = [str(m+1),year]

                        self.f_names.append(name)
                        
                        value = int(months[m])
                        total += value

                        f_probs.append(value)
        f.close()

        f_probs = np.asarray(f_probs,dtype='float')

        f_probs /= total
        
        xk = np.arange(len(self.f_names))

        self.dist = stats.rv_discrete(values=(xk, f_probs))

    def generate(self, names=1):
        i = self.dist.rvs(size=names)

        if names == 1:
            return_value = self.f_names[i[0]]

        else:
            return_value = [self.f_names[j] for j in i]

        return return_value


def generate_names(names, name_format, dists):
    full_names = []

    for i in range(names):
        name = []
        sex = dists["sex"].generate()

        for piece in name_format:
            if piece == "first":
                if sex == "f":
                    key = "first_f"
                else:
                    key = "first_m"
            
            elif piece == "other":
                if sex == "f":
                    key = "other_f"
                else:
                    key = "other_m"
            
            else:
                key = piece

            p = dists[key].generate()

            if piece == "bday":
                month = int(p[0])
                year = int(p[1])

                if month == "2":
                    if year % 4 == 0 and (not year % 100 == 0 or year % 400 == 0):
                        days = 29
                    else:
                        days = 28
                elif month in ["1","3","5","7","8","10","12"]:
                    days = 31
                else:
                    days = 30
                
                day = np.random.random_integers(1,days+1)

                p = str(day) + "." + str(month) + "." + str(year)

            name.append(p)
        
        full_names.append(name)

    return full_names

def namegen(names,name_format="first sur",file=None):  
    paths = {
        "sex": "distributions/sex.csv",
        "first_m": "distributions/first_m.csv",
        "other_m": "distributions/other_m.csv",
        "first_f": "distributions/first_f.csv",
        "other_f": "distributions/other_f.csv",
        "sur": "distributions/sur.csv",
        "bday": "distributions/bday.csv",
        "city": "distributions/city.csv"
    }

    dists = {
        "sex": Dist(paths["sex"]),
        "first_m": Dist(paths["first_m"]),
        "other_m": Dist(paths["other_m"]),
        "first_f": Dist(paths["first_f"]),
        "other_f": Dist(paths["other_f"]),
        "sur": Dist(paths["sur"]),
        "bday": Dist(paths["bday"]),
        "city": Dist(paths["city"])
    }
    
    # splittaa format-string
    f_s = ""
    d_s = ""
    pieces = []
    delims = []

    for i in name_format:
        if i.isalpha():
            if d_s:
                delims.append(d_s)
                d_s = ""
            f_s += i
        else:
            if f_s:
                pieces.append(f_s)
                f_s = ""
            d_s += i
    if f_s:
        pieces.append(f_s)
    else:
        delims.append(d_s)

    # luo n nimeä loopissa
    full_names = generate_names(names,pieces,dists)
    
    # luo csv nimistä
    if file:
        with open(f"{file}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f,delimiter=',')
            [w.writerow(row.split(", ")) for row in full_names]

    length = len(pieces) + len(delims)

    for i in range(len(full_names)):
        name = full_names[i]
        
        string = ""
        
        n = 0
        d = 0

        for j in range(length):
            if j%2 == 0:
                string += name[n]
                n += 1
            else:
                string += delims[d]
                d += 1

        full_names[i] = string

    # palauta nimet
    return full_names
