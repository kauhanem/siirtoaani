from math import floor
import random

def stv(path=None,ballots=None,candidates=None,tie_breaking="backwards",):
    if path:
        ballots = {}
        with open(path,"r",encoding="utf-8") as f:
            for line in f:
                values = line.replace("\n","").split(",")
                voter = values[0]
                votes = values[1:]
                if voter != "":
                    ballots[voter] = votes
        f.close()

    results = {}
    
    for voter in ballots:
        candidate = ballots[voter][0]
        if candidate in results:
            results[candidate][0] += 1
        else:
            results[candidate] = [1]
    
    # print(ballots)
    eliminated = []
    for voter in ballots:
        rm = []
        for v in ballots[voter]:
            if v not in results:
                rm.append(v)
                if v not in eliminated:
                    eliminated.append(v)
        [ballots[voter].remove(c) for c in rm]
    
    # print(results)
    # print()

    [print(f"Candidate {e} didn't get any votes on the first round, and is eliminated.") for e in eliminated]
    # print(ballots)

    ready = False
    i = 0
    empty_ballots = []
    while not ready:
        i += 1
        total_votes = len(ballots)
        threshold = floor(total_votes/2) + 1
        empty = len(empty_ballots)
        
        print("- "*50)
        print(f"Round {i}.")
        print(f"Votes now:")
        [print(f"{V}: {results[V][-1]}") for V in results]
        print(f"Total: {total_votes}, empty ballots: {empty}, threshold: {threshold}.\n")
         
        # Winner determination

        if len(results) == 2:
            win_cand = []
            for win in results:
                win_cand.append(win)

            cand_1_votes = results[win_cand[0]][-1]
            cand_2_votes = results[win_cand[1]][-1]

            # Tie-Breaking
            if cand_1_votes == cand_2_votes:
                print("Tie-breaking")
                if tie_breaking == "random":
                    winner = random.choice(win_cand)
                    print(f"Coin toss between {win_cand}.")
                    ready = True
                    
                elif tie_breaking == "backwards":
                    toss = True

                    if i > 1:
                        print(f"Cand. 1 {win_cand[0]} votes: {results[win_cand[0]]}")
                        print(f"Cand. 2 {win_cand[1]} votes: {results[win_cand[1]]}\n")
                        for t in range(-2,-i-1,-1):
                            cand_1_votes = results[win_cand[0]][t]
                            cand_2_votes = results[win_cand[1]][t]

                            print(f"i: {t}")
                            print(f"round: {i - (abs(t)-2)}")
                            print(f"Cand. 1 {win_cand[0]} votes: {cand_1_votes}")
                            print(f"Cand. 2 {win_cand[1]} votes: {cand_2_votes}\n")
                                
                            if cand_1_votes > cand_2_votes:
                                winner = win_cand[0]
                                toss = False
                                break
                            elif cand_1_votes < cand_2_votes:
                                winner = win_cand[1]
                                toss = False
                                break

                        if toss:
                            print(f"Coin toss between {win_cand[0]} and {win_cand[1]}.")
                            winner = random.choice(win_cand)
                
                # Toisella enemmän
            elif cand_1_votes > cand_2_votes:
                winner = win_cand[0]
            else:
                winner = win_cand[1]
        
        low = []
        for candidate in results:
            c_votes = results[candidate][-1]
            results[candidate].append(c_votes)
        
            if c_votes >= threshold:
                winner = candidate
                print(f"Winner is {winner} with {results[winner][-1]} votes.")
                ready = True
                break
            
            if not low:
                low.append(candidate)
            
            elif c_votes == results[low[0]][-1]:
                low.append(candidate)

            elif c_votes < results[low[0]][-1]:
                low.clear()
                low.append(candidate)
        
        if not ready:
            if len(low) == 1:
                loser = low[0]
            else:
                print("Tie-breaking")
                if tie_breaking == "random":
                    loser = random.choice(low)
                    print(f"Coin toss between {low}.")

                elif tie_breaking == "backwards":                
                    low_tb = low

                    if i > 1:
                        l = low
                        for t in range(-3,-i-1,-1):
                            low_tb = []

                            print(f"i: {t}")
                            print(f"round: {i - (abs(t)-2)}")
                            for cand in l:
                                tb_votes = results[cand][t]
                                print(f"{cand}, {results[cand]}")
                                print(f"votes on round {i - (abs(t)-2)}: {tb_votes}")
                                print(f"low: {low_tb}\n")

                                if not low_tb:
                                    low_tb.append(cand)
                    
                                elif tb_votes == results[low_tb[0]][t]:
                                    low_tb.append(cand)

                                elif tb_votes < results[low_tb[0]][t]:
                                    low_tb.clear()
                                    low_tb.append(cand)
                        
                            if len(low_tb) == 1:
                                # print("Lone loser.")
                                loser = low_tb[0]
                                break
                            # elif len(l) == len(low_tb):
                            #     break
                            else:
                                l = low_tb

                    if len(low_tb) > 1:
                        print(f"Coin toss between {low_tb}.")
                        loser = random.choice(low_tb)

            print(f"Loser is {loser} with {results[loser][-1]} votes.")
            results.pop(loser)
            
            rm = []
            for voter in ballots:
                if loser in ballots[voter]:
                    if loser == ballots[voter][0] and len(ballots[voter]) > 1:
                        # print(f"{voter} voted for {ballots[voter][0]}.")
                        # print(f"Whole ballot: {ballots[voter]}")
                        results[ballots[voter][1]][-1] += 1
                        # print(f"Now the vote goes to {ballots[voter][1]}.")
                        
                    # print(f"Removing {loser} from {voter}'s ballot.")
                    ballots[voter].remove(loser)
                    # print(f"Ballot after: {ballots[voter]}")
                    
                    if len(ballots[voter]) == 0:
                        # print(f"{voter}'s ballot is now empty.")
                        empty_ballots.append(voter)
                        rm.append(voter)
                    # print()
            [ballots.pop(v) for v in rm]
    print("- "*50,"\n")