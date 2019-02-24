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

    century_char = {
        18: "+",
        19: "-",
        20: "A"
    }

    domain_f = np.arange(3,900)
    domain_m = np.arange(2,900)

    check_char = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
        16: "H",
        17: "J",
        18: "K",
        19: "L",
        20: "M",
        21: "N",
        22: "P",
        23: "R",
        24: "S",
        25: "T",
        26: "U",
        27: "V",
        28: "W",
        29: "X",
        30: "Y"
    }

    for i in range(names):
        name = []
        sex = dists["sex"].generate()

        month,year = dists["bday"].generate()

        if month == "2":
            if int(year) % 4 == 0 and (not int(year) % 100 == 0 or int(year) % 400 == 0):
                days = 29
            else:
                days = 28
        elif month in ["1","3","5","7","8","10","12"]:
            days = 31
        else:
            days = 30
                
        day = np.random.randint(1,days+1)

        for piece in name_format:
            if piece == "bday":
                p = str(day) + "." + str(month) + "." + str(year)

            elif piece == "id":
                if sex == "f":
                    domain = domain_f
                else:
                    domain = domain_m

                d = str(day)
                m = str(month)
                y = str(year)

                num = np.random.choice(domain,1)[0]
                n = str(num)
                
                p = "0"*(2-len(d)) + d
                p += "0"*(2-len(m)) + m 
                p += y[-2] + y[-1]

                P = p + "0"*(3-len(n)) + n
                
                p += century_char[int(year)//100]
                
                p += "0"*(3-len(n)) + n

                p += check_char[int(P)%31]

            else:
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
