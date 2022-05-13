from copy import deepcopy
NUM_SQUARE = 12
QUAN_1 = 5
QUAN_2 = 11
INF = 70
def finished(state):
    return state[5] == [0, 0] and state[11] == [0, 0]
    
# Check Nợ quân: (new_state, new_point)
def handleBorrowStack(state, cur_point):
    state, player_score = deepcopy(state), deepcopy(cur_point)
    if not any([i[0] for i in state[0:QUAN_1]]):
        player_score[0] -= 5

        for i in range(0,QUAN_1):
            state[i][0] = 1
    
    if not any([i[0] for i in state[QUAN_1+1:QUAN_2]]):
        player_score[1] -= 5

        for i in range(QUAN_1+1,QUAN_2):
            state[i][0] = 1
    return state, player_score

# Generate next possible move foreach player
# Input: state, move, cur_point_, player_id
# Output: (new_state, new_point)
def performNextMove(state__, move , cur_point_, id): # Khởi tạo bước đi trong bàn cờ
    state , cur_point = deepcopy(state__), deepcopy(cur_point_)
    # direction: 1 for RIGHT and 2 for LEFT
    direction = 1 if move[1] == 'Right' else -1
    cur_pos = move[0]
    next_pos = (cur_pos + direction) % NUM_SQUARE

    # Each of next positions get +1 prawn
    for _ in range(state[cur_pos][0]):
        state[next_pos][0] += 1
        next_pos = (next_pos + direction) % NUM_SQUARE
    state[cur_pos][0] //= NUM_SQUARE

    while True:
        # if next_pos is a King's spot or (next_pos and next of next_pos are empty)
        # -> No more consecutive pick-up and point not increased
        if next_pos == QUAN_1 or next_pos == QUAN_2 or (state[next_pos][0] == 0 and state[(next_pos + direction) % NUM_SQUARE][0] == 0 and
                                state[(next_pos + direction) % NUM_SQUARE][1] != 1):
                                return state , cur_point
                            
        # else if next_pos is empty and (next of next_pos is not empty)
        # -> point increased
        elif state[next_pos][0] == 0 and (
            state[(next_pos + direction) % NUM_SQUARE][0] or state[(next_pos + direction) % NUM_SQUARE][1] == 1
        ):
            # reset the current point and state for (next of next_pos)
            cur_point[id] += state[(next_pos + direction) % NUM_SQUARE][0]
            state[(next_pos + direction) % NUM_SQUARE][0] = 0
            # check if we ate the King
            if state[(next_pos + direction) % NUM_SQUARE][1] == 1:
                cur_point[id] += 10
                state[(next_pos + direction) % NUM_SQUARE][1] = 0
            # double tap
            if state[(next_pos + direction*2) % NUM_SQUARE][0] == 0 and state[(next_pos + direction * 2) % NUM_SQUARE][1] != 1:
                next_pos = (next_pos + direction * 2) % NUM_SQUARE
                
        # else: next pos is not empty and not a King's spot
        # -> continue running
        else:
            cur_pos = next_pos
            for _ in range(state[cur_pos][0]):
                state[next_pos][0] += 1 
                next_pos = (next_pos + direction) % NUM_SQUARE
            state[cur_pos][0] //= NUM_SQUARE