import pygame as pyg
import time

class GridWorldUI:

    def __init__(self, grid, terminals, size = 50, flag = 'V'):
        self.size = size
        self.grid = grid
        self.flag = flag
        self.terminals = terminals
        self.font = None
        self.display = None

        pyg.init()

    def initScene(self, title):
        self.font = pyg.font.SysFont('', int(self.size*0.2))
        self.display = pyg.display.set_mode((self.size*(len(self.grid[0])+2), self.size*(len(self.grid)+2)),pyg.RESIZABLE)
        pyg.display.set_caption(title)

    def text_on_screen(self, position, text):
        text_screen = self.font.render(text, True, (255,255,255))
        self.display.blit(text_screen, position)

    def updateScene(self, rl):
        V_val = rl.getV()
        Pi_val = rl.getPi()
        Q_val = rl.getQ()
        state = rl.getState()

        self.drawScene(V_val, Pi_val, Q_val, state)
        pyg.display.update()
        time.sleep(0.1)

    def drawScene(self, V_val, Pi_val, Q_val, state):
        self.display.fill((0,0,0))
        # Draw grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):

                if self.grid[i][j] in self.terminals:
                    self.renderTerminalState(V_val[self.grid[i][j]], i, j)
                elif self.grid[i][j] == 'W':
                    pyg.draw.rect(self.display, (128, 128, 128), [(j+1)*self.size, (i+1)*self.size, self.size, self.size])
                else:
                    if (self.flag == 'V'):
                        self.displayVFuncValue(V_val, i, j)
                        self.displayPolicy(Pi_val, i, j)
                    else:
                        self.displayQFuncValues(Q_val, i, j)

                if (self.grid[i][j] == state):
                    self.renderPlayer(i, j)

                pyg.draw.rect(self.display, (255, 255, 255), [(j+1)*self.size, (i+1)*self.size, self.size, self.size], 2)

    def renderPlayer(self, i, j):
        pyg.draw.circle(self.display, (0, 50, 255), [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2], self.size/10)

    def renderTerminalState(self, V_val, i, j):
        if V_val < 0:
            pyg.draw.rect(self.display, (255, 0, 0), [(j+1)*self.size, (i+1)*self.size, self.size, self.size])
            pyg.draw.rect(self.display, (255, 255, 255), [(j+1)*self.size+self.size/10, (i+1)*self.size+self.size/10, self.size-self.size/5, self.size-self.size/5], 2)
        elif V_val > 0:
            pyg.draw.rect(self.display, (0, 255, 0), [(j+1)*self.size, (i+1)*self.size, self.size, self.size])
            pyg.draw.rect(self.display, (255, 255, 255), [(j+1)*self.size+self.size/10, (i+1)*self.size+self.size/10, self.size-self.size/5, self.size-self.size/5], 2)
            # self.text_on_screen([(j+1)*self.size+int(self.size*0.4), (i+1)*self.size+int(self.size*0.4)], str(round(V_val[self.grid[i][j]], 2)) )
        else:
            pyg.draw.rect(self.display, (255, 255, 255), [(j+1)*self.size+self.size/10, (i+1)*self.size+self.size/10, self.size-self.size/5, self.size-self.size/5], 2)

        self.text_on_screen([(j+1)*self.size+int(self.size*0.4), (i+1)*self.size+int(self.size*0.4)], str(round(V_val, 2)))

    def displayVFuncValue(self, V_val, i, j):
        if self.grid[i][j] != 'W':
            st = str(round(V_val[self.grid[i][j]], 2))
        else:
            st = ' '
        self.text_on_screen([(j+1)*self.size+int(self.size*0.3), (i+1)*self.size+int(self.size*0.4)], st)

    def displayQFuncValues(self, Q_val, i, j):
        if self.grid[i][j] != 'W':
            # LEFT
            if (Q_val[self.grid[i][j]][0][0] <  0):
                pyg.draw.polygon(self.display, (255, 0, 0), [[(j+1)*self.size, (i+1)*self.size], [(j+1)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])
            elif (Q_val[self.grid[i][j]][0][0] >  0):
                pyg.draw.polygon(self.display, (0, 255, 0), [[(j+1)*self.size, (i+1)*self.size], [(j+1)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])

            # UP
            if (Q_val[self.grid[i][j]][1][0] <  0):
                pyg.draw.polygon(self.display, (255, 0, 0), [[(j+1)*self.size, (i+1)*self.size], [(j+2)*self.size, (i+1)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])
            elif (Q_val[self.grid[i][j]][1][0] >  0):
                pyg.draw.polygon(self.display, (0, 255, 0), [[(j+1)*self.size, (i+1)*self.size], [(j+2)*self.size, (i+1)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])

            # RIGHT
            if (Q_val[self.grid[i][j]][3][0] <  0):
                pyg.draw.polygon(self.display, (255, 0, 0), [[(j+1)*self.size, (i+2)*self.size], [(j+2)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])
            elif (Q_val[self.grid[i][j]][3][0] >  0):
                pyg.draw.polygon(self.display, (0, 255, 0), [[(j+1)*self.size, (i+2)*self.size], [(j+2)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])

            # DOWN
            if (Q_val[self.grid[i][j]][2][0] <  0):
                pyg.draw.polygon(self.display, (255, 0, 0), [[(j+2)*self.size, (i+1)*self.size], [(j+2)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])
            elif (Q_val[self.grid[i][j]][2][0] >  0):
                pyg.draw.polygon(self.display, (0, 255, 0), [[(j+2)*self.size, (i+1)*self.size], [(j+2)*self.size, (i+2)*self.size], [(j+1)*self.size+self.size/2, (i+1)*self.size+self.size/2]])


            pyg.draw.line(self.display, (255,255,255), [(j+1)*self.size, (i+1)*self.size], [(j+2)*self.size, (i+2)*self.size], 2)
            pyg.draw.line(self.display, (255,255,255), [(j+2)*self.size, (i+1)*self.size], [(j+1)*self.size, (i+2)*self.size], 2)

            st = str(round(Q_val[self.grid[i][j]][0][0], 2))
            self.text_on_screen([(j+1)*self.size+int(self.size*0.1), (i+1)*self.size+int(self.size*0.4)], st)
            st = str(round(Q_val[self.grid[i][j]][1][0], 2))
            self.text_on_screen([(j+1)*self.size+int(self.size*0.3), (i+1)*self.size+int(self.size*0.1)], st)
            st = str(round(Q_val[self.grid[i][j]][2][0], 2))
            self.text_on_screen([(j+1)*self.size+int(self.size*0.65), (i+1)*self.size+int(self.size*0.4)], st)
            st = str(round(Q_val[self.grid[i][j]][3][0], 2))
            self.text_on_screen([(j+1)*self.size+int(self.size*0.3), (i+1)*self.size+int(self.size*0.8)], st)
        else:
            st = ' '
            self.text_on_screen([(j+1)*self.size+int(self.size*0.3), (i+1)*self.size+int(self.size*0.4)], st)

    def displayPolicy(self, Pi_val, i, j):
        if (type(self.grid[i][j]) == int):

            if (Pi_val[self.grid[i][j]] == 'UP'):
                pyg.draw.polygon(self.display, (255, 255, 255), [[(j+1)*self.size+self.size/2, (i+1)*self.size+int(self.size*0.05)],
                                                      [(j+1)*self.size+int(self.size*0.55), (i+1)*self.size+int(self.size*0.1)],
                                                      [(j+1)*self.size+int(self.size*0.45), (i+1)*self.size+int(self.size*0.1)]])
            elif (Pi_val[self.grid[i][j]] == 'DOWN'):
                pyg.draw.polygon(self.display, (255, 255, 255), [[(j+1)*self.size+self.size/2, (i+1)*self.size+int(self.size*0.95)],
                                                      [(j+1)*self.size+int(self.size*0.55), (i+1)*self.size+int(self.size*0.9)],
                                                      [(j+1)*self.size+int(self.size*0.45), (i+1)*self.size+int(self.size*0.9)]])
            elif (Pi_val[self.grid[i][j]] == 'LEFT'):
                pyg.draw.polygon(self.display, (255, 255, 255), [[(j+1)*self.size+int(self.size*0.05), (i+1)*self.size+self.size/2],
                                                      [(j+1)*self.size+int(self.size*0.1), (i+1)*self.size+int(self.size*0.55)],
                                                      [(j+1)*self.size+int(self.size*0.1), (i+1)*self.size+int(self.size*0.45)]])
            else:
                # 'RIGHT'
                pyg.draw.polygon(self.display, (255, 255, 255), [[(j+1)*self.size+int(self.size*0.95), (i+1)*self.size+self.size/2],
                                                      [(j+1)*self.size+int(self.size*0.9), (i+1)*self.size+int(self.size*0.55)],
                                                      [(j+1)*self.size+int(self.size*0.9), (i+1)*self.size+int(self.size*0.45)]])

    def getUserEvent(self):

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                quit()
            elif event.type == pyg.KEYDOWN:
                if event.key == pyg.K_DOWN:
                    return 'K_DOWN'
                elif event.key == pyg.K_RIGHT:
                    return 'K_RIGHT'
                elif event.key == pyg.K_UP:
                    return 'K_UP'
                elif event.key == pyg.K_LEFT:
                    return 'K_LEFT'
                elif event.key == pyg.K_q:
                    return 'K_q'
                elif event.key == pyg.K_v:
                    return 'K_v'
                elif event.key == pyg.K_r:
                    return 'K_r'
                elif event.key == pyg.K_e:
                    return 'K_e'
                elif event.key == pyg.K_s:
                    return 'K_s'

        return 'Invalid'

    def setFlag(self, flag):
        self.flag = flag
