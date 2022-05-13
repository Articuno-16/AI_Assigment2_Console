from game import Game
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # Chỉnh sửa 2 cái này để chạy
    level = "easy"
    scale = 10
    first = False

    thinking =  []
    number_of_move = []
    total_thinking_time = []
    res = [] 
    max_time = [] 
    min_time = []
    seq = []
    for i in range(scale):
        game = Game()
        thinking,result = game.statistic(first,level)
        seq.append(",".join(str(x) for x in thinking))
        size = len(thinking)
        res.append(result)
        thinking = np.array(thinking,dtype=np.float32)
        number_of_move.append(size)
        total_thinking_time.append(np.sum(thinking))
        max_time.append(np.max(thinking))
        print(np.amin(thinking))
        min_time.append(np.min(thinking))
    
    df = pd.DataFrame({ "result":res
                        ,"max_time":max_time
                        ,"min_time":min_time
                        ,"total_thinking_time":total_thinking_time
                        ,"total_move":number_of_move
                        ,"thinking_time":seq})

    df.to_csv("statistic/{}_{}.csv".format(level,"first" if first else "second" ))
