from random import choice, randint
from game import Game
import pandas as pd
import numpy as np
def getStatByLevel(name,p1=None,p2=None):
    # Chỉnh sửa 2 cái này để chạy
    level = "random"
    scale = 100
    first = True

    thinking =  []
    number_of_move = []
    total_thinking_time = []
    res = [] 
    max_time = [] 
    min_time = []
    seq = []
    for i in range(scale):
        game = Game()
        if p1 is None and p2 is None:
            _m,thinking,result = game.statistic(first,level)
        else:
            _m,thinking,result = game.statistic(first,level,p1,p2)    
        print(i)
        print(result)        
        print(_m)
        seq.append(",".join(str(x) for x in thinking))
        size = len(thinking)
        res.append(result)
        thinking = np.array(thinking,dtype=np.float32)
        number_of_move.append(size)
        total_thinking_time.append(np.sum(thinking))
        max_time.append(np.max(thinking))
        min_time.append(np.min(thinking))
    
    df = pd.DataFrame({ "result":res
                        ,"max_time":max_time
                        ,"min_time":min_time
                        ,"total_thinking_time":total_thinking_time
                        ,"total_move":number_of_move
                        ,"thinking_time":seq})

    df.to_csv("statistic/{}_{}_{}.csv".format("NB","first" if first else "second",name ))
    
###################### DATABASE GENERATOR #######################
from pandas import read_csv
import pandas as pd
from random import choice, randint
from game import Game

def createLevelDataset(level,scale):
    move_string = []
    res = []
    turns = []
    for i in range(scale):
        first = choice([False, True])
        turns.append(first)
        game = Game()
        moves,_,result = game.statistic(first,level,level,level)
        move_string.append(moves)
        res.append(result)
        
    df = pd.DataFrame({  "result":res
                        ,"moves":move_string
                        })

    df.to_csv("dataset/{}_{}.csv".format(level,scale))

def createRandomDataset(scale):
    move_string = []
    res = []
    for i in range(scale):
        game = Game()
        moves,_,result = game.statistic(True,"random")
        move_string.append(moves)
        res.append(result)
        
    df = pd.DataFrame({"result":res
                        ,"moves":move_string
                        })

    df.to_csv("dataset/{}_{}.csv".format("random",scale))


if __name__ == "__main__":
    # createLevelDataset("naiveBayes",500) # gen for P2
    getStatByLevel("NB","naiveBayes","naiveBayes")