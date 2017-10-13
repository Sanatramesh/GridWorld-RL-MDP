
actionList = ['LEFT', 'UP', 'RIGHT','DOWN']

actions = {'LEFT': 0,
             'UP': 1,
          'RIGHT': 2,
           'DOWN': 3}

# T(s, a, s')
def T(Q, state, action):
    if action == 'W':
        return [(0.0, state)]
    else:
        l = len(Q[state])
        return [( 0.8, Q[state][actions[action]][1] ), # Action
                ( 0.1, Q[state][actions[action] - 1][1] ), # Left to the Action
                ( 0.1, Q[state][(actions[action] + 1)%l][1] )] # Right to the Action

def simple_grid():
    # states config
    #   | 0 | 1 | 2 | G |
    #   | 3 | W | 4 | R |
    #   | 5 | 6 | 7 | 8 |
    #   G,R terminal states, W - Wall/Obstacle
    start = 5
    GRID = [[0, 1, 2, 'G'],
            [3, 'W', 4, 'R'],
            [5, 6, 7, 8]]

    terminals = ['G', 'R']
    rewards = {'G': 1.0, 'R': -1.0, 'live': -0.01}

    R = lambda s, a, s1: rewards[s] if (s1 == 'E' and s in terminals) else rewards['live']

    return GRID, terminals, R, T, start

def edge_grid():
    start = 5
    GRID = [['W',  1,  2,  3, 4 ],
            [  5,  6,  7,  8, 'G'],
            ['W','R1','R2','R3','W']]

    terminals = ['G', 'R1', 'R2', 'R3']
    rewards = {'G': 10.0, 'R1': -10.0, 'R2': -50.0, 'R3': -75.0, 'live': -0.01}

    R = lambda s, a, s1: rewards[s] if (s1 == 'E' and s in terminals) else rewards['live']

    return GRID, terminals, R, T, start

def bridge_grid():
    start = 2
    GRID = [['W', 'R6', 'R7', 'R8', 'R9', 'R10', 'W' ],
            [ 'G1',  2,  3,  4, 5, 6, 'G'],
            ['W','R1','R2','R3', 'R4', 'R5', 'W']]

    terminals = ['G', 'G1', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10' ]
    rewards = {'G': 10.0, 'G1': 1.0, 'R1': -10.0, 'R2': -10.0, 'R3': -10.0, 'R4': -10.0, 'R5': -10.0, 'R6': -10.0,
                'R7': -10.0,'R8': -10.0,'R9': -10.0, 'R10': -10.0, 'live': -0.01}

    R = lambda s, a, s1: rewards[s] if (s1 == 'E' and s in terminals) else rewards['live']

    return GRID, terminals, R, T, start

def cliff_grid():
    start = 10
    GRID = [[ 0,  1,  2,  3, 4 ],
            [ 5, 'W', 6,  7,  8],
            [ 9, 'W', 'G1', 'W', 'G'],
            [10, 11, 12, 13, 14],
            ['R4','R1','R2','R3','R5']]

    terminals = ['G', 'G1', 'R1', 'R2', 'R3', 'R4', 'R5']
    rewards = {'G': 10.0, 'G1': 1.0, 'R1': -10.0, 'R2': -10.0,'R3': -10.0,'R4': -10.0,'R5': -10.0, 'live': -0.01}

    R = lambda s, a, s1: rewards[s] if (s1 == 'E' and s in terminals) else rewards['live']

    return GRID, terminals, R, T, start
