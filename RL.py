import copy
import random
import time

import gridworld as gw
from gridworld.worlds import actions, actionList

'''
    Implements RL, Value Interation Method
    Policy Evaluation and Policy Extraction
    Grid World, 'W' = Wall
'''

class RL:

    def __init__(self, Q, V, T, R, Pi, terminals, startState, actions, GRID, gamma = 1.0, alpha = 0.5, eps = 0.2):
        self.Q = Q
        self.V = V
        self.T = T
        self.R = R
        self.Pi = Pi
        self.terminals = terminals
        self.actions = actions
        self.GRID = GRID
        self.startState = startState
        self.gamma = gamma
        self.alpha = alpha
        self.eps = eps
        self.state = self.startState

    def computeQValues(self):
        for state in self.Q:
            for action in self.actions:
                Tval = self.T(self.Q, state, action)
                self.Q[state][actions[action]][0] = sum([t*(self.R(state, action, s) + self.gamma*self.V[s]) for (t,s) in Tval])

    def ValueIteration(self):
        self.computeQValues()

        for state in self.Q:
            Qmax = self.getMaxQValue(state)
            # update Value function
            self.V[state] = Qmax[0]
            # update Policy function
            self.Pi[state] = self.getAction(Qmax[1])

    def PolicyIteration(self):
        V1 = self.V.copy()

        for state in self.Pi:
            Tval = self.T(self.Q, state, self.Pi[state])
            V1[state] = sum([t*(self.R(state, self.Pi[state], s) + self.gamma*self.V[s]) for (t,s) in Tval])

        self.V = V1.copy()

    def PolicyExtraction(self):
        self.computeQValues()

        for state in self.Pi:
            self.updatePolicy(state)

    def VTemporalDiffLearning(self, action, state1):
        sample = self.R(self.state, action, state1) + self.gamma*self.V[state1]
        self.V[self.state] += self.alpha*(sample - self.V[self.state])

    def QTemporalDiffLearning(self, action, state1):
        Qmax = self.getMaxQValue(state1)
        sample = self.R(self.state, action, state1) + self.gamma*Qmax[0]

        if (self.state in self.terminals):
            self.Q[self.state][0][0] += self.alpha*(sample - self.Q[self.state][self.actions[action]][0])
            self.Q[self.state][1][0] += self.alpha*(sample - self.Q[self.state][self.actions[action]][0])
            self.Q[self.state][2][0] += self.alpha*(sample - self.Q[self.state][self.actions[action]][0])
            self.Q[self.state][3][0] += self.alpha*(sample - self.Q[self.state][self.actions[action]][0])
        else:
            self.Q[self.state][self.actions[action]][0] += self.alpha*(sample - self.Q[self.state][self.actions[action]][0])

        self.updatePolicy(self.state)

    def updatePolicy(self, state):
        Qmax = self.getMaxQValue(state)
        self.Pi[state] = self.getAction(Qmax[1])

    def getMaxQValue(self, state):
        if (state == 'E'):
            return (0.0, 1)
        return max([(q, idx) for idx,(q, _) in enumerate(self.Q[state])], key = lambda item:item[0])

    def getAction(self, code):
        return [action for action in actions if actions[action] == code][0]

    def updateState(self, action):
        state1 = 0
        if (self.state != 'E'):
            Tval = self.T(self.Q, self.state, action)
            state1 = Tval[0][1]
            self.VTemporalDiffLearning(action, state1)
            self.QTemporalDiffLearning(action, state1)
            self.state = state1

    def setState(self, state):
        if (self.state == 'E'):
            self.state = state

    def resetState(self):
        if (self.state == 'E'):
            self.state = self.startState

    def updateCurrentState(self):
        rand = random.random()
        action = self.Pi[self.state]

        if (rand < self.eps):
            randAct = random.randint(0, len(actionList) - 1)
            action = actionList[randAct]

        self.updateState(action)

    def __str__(self):
        output = ""
        for row in self.GRID:
            for col in row:
                if col != 'W':
                    output += str(round(self.V[col], 2))+' | '
                else:
                    output += ' W  | '
            output += "\n"

        return output

    def PrintPi(self):
        print self.Pi

    def getV(self):
        return self.V

    def getQ(self):
        return self.Q

    def getPi(self):
        return self.Pi

    def getState(self):
        return self.state

    def updateEpsilon(self, delta):
        self.eps += delta
        if (self.eps <= 0):
            self.eps = 0

    def getEpsilon(self):
        return self.eps

def Main(rl, game):
    game.initScene('RL: Grid World')
    game.updateScene(rl)

    while True:
        event = game.getUserEvent()

        if event != 'Invalid':
            if event == 'K_DOWN':
                rl.updateState('DOWN')
            elif event == 'K_RIGHT':
                rl.updateState('RIGHT')
            elif event == 'K_UP':
                rl.updateState('UP')
            elif event == 'K_LEFT':
                rl.updateState('LEFT')
            elif event == 'K_q':
                game.setFlag('Q')
            elif event == 'K_v':
                game.setFlag('V')
            elif event == 'K_r':
                rl.resetState()
            elif event == 'K_e':
                rl.updateEpsilon(-0.1)
            elif event == 'K_s':
                for _ in xrange(100000):
                    rl.updateCurrentState()
                    if (rl.getState() == 'E'):
                        rl.resetState()

            game.updateScene(rl)

        rl.updateCurrentState()
        game.updateScene(rl)

        if (rl.getState() == 'E'):
            rl.resetState()
            game.updateScene(rl)

if __name__ == '__main__':
    grid, terminals, R, T, startState = gw.worlds.cliff_grid()
    V, Q, Pi = gw.utils.initParameters(grid, actionList, terminals)

    rl = RL(Q, V, T, R, Pi, terminals, startState, actions, grid, gamma = 0.8, alpha = 0.2, eps = 0.8)
    game = gw.gridworld_display.GridWorldUI(grid, terminals, size = 150)

    Main(rl, game)
