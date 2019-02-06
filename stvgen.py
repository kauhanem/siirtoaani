import numpy as np
from scipy import stats
from finns import finngen
import csv
import random

def stvgen(candidates,voters,max_votes=None,name=None):
    candidates = finngen(candidates)
    voters = finngen(voters)
    
    ballots = []

    if not max_votes:
        max_votes = len(candidates)

    for voter in voters:
        result = [voter]
        result += random.sample(candidates,random.randrange(1,max_votes))
        ballots.append(result)
    
    if name:
        with open(f"{name}.csv",'w',encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerows(ballots)
        f.close()

    temp = {}
    for line in ballots:
        temp[line[0]] = line[1:]
    ballots = temp

    return ballots