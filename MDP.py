import copy
import pygame as pyg

import gridworld as gw
from gridworld.worlds import actions, actionList

'''
    Implements an MDP, Value Interation Method
    Policy Evaluation and Policy Extraction
    Grid World, 'W' = Wall
'''

class MDP:

    def __init__(self, Q, V, T, R, Pi, actions, GRID, gamma = 1.0):
        self.Q = Q
        self.V = V
        self.T = T
        self.R = R
        self.Pi = Pi
        self.actions = actions
        self.GRID = GRID
        self.gamma = gamma

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

    def updatePolicy(self, state):
        Qmax = self.getMaxQValue(state)
        self.Pi[state] = self.getAction(Qmax[1])

    def getMaxQValue(self, state):
        if (state == 'E'):
            return (0.0, 1)
        return max([(q, idx) for idx,(q, _) in enumerate(self.Q[state])], key = lambda item:item[0])

    def getAction(self, code):
        return [action for action in actions if actions[action] == code][0]

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
        return -1

def Main(mdp, game):
    game.initScene('Markov Decision Process: Grid World')
    game.updateScene(mdp)
    
    while True:
        event = game.getUserEvent()

        if event != 'Invalid':
            if event == 'K_DOWN':
                for i in range(100):
                    print 'Iteration ...... ',i+1
                    mdp.ValueIteration()
            elif event == 'K_RIGHT':
                mdp.ValueIteration()
            elif event == 'K_UP':
                for i in range(5):
                    print 'Iteration ...... ',i+1
                    mdp.PolicyIteration()
                mdp.PolicyExtraction()
            elif event == 'K_q':
                game.setFlag('Q')
            elif event == 'K_v':
                game.setFlag('V')

            game.updateScene(mdp)

if __name__ == '__main__':
    grid, terminals, R, T, startState = gw.worlds.cliff_grid()
    V, Q, Pi = gw.utils.initParameters(grid, actionList, terminals)

    mdp = MDP(Q, V, T, R, Pi, actions, grid)
    game = gw.gridworld_display.GridWorldUI(grid, terminals, size = 150)

    Main(mdp, game)
