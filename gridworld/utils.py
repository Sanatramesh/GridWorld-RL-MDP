

def go(grid, action, i, j):
    i1 = 0
    j1 = 0
    if (action == 'UP'):
        i1 = i - 1
        j1 = j
    elif (action == 'DOWN'):
        i1 = i + 1
        j1 = j
    elif (action == 'LEFT'):
        i1 = i
        j1 = j - 1
    elif (action == 'RIGHT'):
        i1 = i
        j1 = j + 1

    if (i1 < 0 or i1 >= len(grid)):
        i1 = i

    if (j1 < 0 or j1 >= len(grid[0])):
        j1 = j

    if (grid[i1][j1] == 'W'):
        i1 = i
        j1 = j

    return i1, j1

def initParameters(grid, actionList, terminals):
    V = {}
    Q = {}
    Pi = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'W':
                continue
            elif grid[i][j] in terminals:
                V[grid[i][j]] = 0.0
                Pi[grid[i][j]] = actionList[0]
                Q[grid[i][j]] = []

                for action in actionList:
                    Q[grid[i][j]].append([0.0, 'E'])

            else:
                V[grid[i][j]] = 0.0
                Pi[grid[i][j]] = actionList[0]
                Q[grid[i][j]] = []

                for action in actionList:
                    i1, j1 = go(grid, action, i, j)
                    Q[grid[i][j]].append([0.0, grid[i1][j1]])

    V['E'] = 0.0

    return V, Q, Pi
