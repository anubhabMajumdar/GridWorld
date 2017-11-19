import copy
import time
import sys

lastDiff = -1

class GridWorld:
    def __init__(self, r, c, goals, goalRewards, alpha=0.9):
        self.row = r
        self.col = c
        self.goals = goals
        self.goalRewards = goalRewards
        self.alpha = alpha
        self.V = {}
        self.Q = {}
        self.P = {}

        self.initV()
        self.determineQ()
        self.determinePolicy()

    def initV(self):
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                self.V[(i, j)] = 0
        for goal, goalReward in zip(self.goals, self.goalRewards):
            self.V[goal] = goalReward

    def initP(self):
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                if i == self.row:
                    self.P[(i, j)] = 'S'
                else:
                    self.P[(i, j)] = 'N'

    def determineQ(self):
        def checkValidCoordinate(i, j):
            return 0 < i <= self.row and 0 < j <= self.col
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                self.Q[(i, j)] = {}
                if checkValidCoordinate(i - 1, j):
                    self.Q[(i, j)]['S'] = self.V[(i-1, j)]
                else:
                    self.Q[(i, j)]['S'] = -1 * sys.maxint

                if checkValidCoordinate(i + 1, j):
                    self.Q[(i, j)]['N'] = self.V[(i + 1, j)]
                else:
                    self.Q[(i, j)]['N'] = -1 * sys.maxint

                if checkValidCoordinate(i, j - 1):
                    self.Q[(i, j)]['W'] = self.V[(i, j - 1)]
                else:
                    self.Q[(i, j)]['W'] = -1 * sys.maxint

                if checkValidCoordinate(i, j + 1):
                    self.Q[(i, j)]['E'] = self.V[(i, j + 1)]
                else:
                    self.Q[(i, j)]['E'] = -1 * sys.maxint

    def determinePolicy(self):
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                qvals = self.Q[(i, j)].items()
                m = max(qvals, key=lambda x: x[-1])
                self.P[(i, j)] = m[0]

    def determineV(self):
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                if (i, j) in self.goals:
                    continue
                qvals = self.Q[(i, j)].items()
                m = max(qvals, key=lambda x: x[-1])
                self.V[(i, j)] = m[1]

    def update(self):
        def checkValidCoordinate(i, j):
            return 0 < i <= self.row and 0 < j <= self.col
        valueFunctionCopy = copy.deepcopy(self.V)
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                if (i, j) in self.goals:
                    continue
                temp = 0
                if checkValidCoordinate(i - 1, j):
                    temp += 0.25 * self.V[(i-1, j)]

                if checkValidCoordinate(i + 1, j):
                    temp += 0.25 * self.V[(i + 1, j)]

                if checkValidCoordinate(i, j - 1):
                    temp += 0.25 * self.V[(i, j - 1)]

                if checkValidCoordinate(i, j + 1):
                    temp += 0.25 * self.V[(i, j + 1)]
                valueFunctionCopy[(i, j)] = round(temp, 2)
        self.V = valueFunctionCopy

    def updateQ(self):
        def checkValidCoordinate(i, j):
            return 0 < i <= self.row and 0 < j <= self.col
        QFunctionCopy = copy.deepcopy(self.Q)
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                if (i, j) in self.goals:
                    continue
                curP = self.P[(i, j)]
                if curP == 'N':
                    m = self.V[(i + 1, j)]
                elif curP == 'S':
                    m = self.V[(i - 1, j)]
                elif curP == 'E':
                    m = self.V[(i, j + 1)]
                elif m == 'W':
                    m = self.V[(i, j - 1)]
                QFunctionCopy[(i, j)][curP] = (1 - self.alpha) * QFunctionCopy[(i, j)][curP] + self.alpha * 0.9 * m
        self.Q = QFunctionCopy

    def run(self):
        def checkConvergence(d1, d2):
            diff = 0
            for i in range(1, self.row + 1):
                for j in range(1, self.col + 1):
                    if d1[(i, j)] != d2[(i, j)]:
                        diff += abs(d1[(i, j)] - d2[(i, j)])
                        # return False
            print "Error = ", diff
            return diff == 0
        previousV = copy.deepcopy(self.V)
        self.update()
        self.pp()
        while not checkConvergence(previousV, self.V):
            previousV = copy.deepcopy(self.V)
            self.update()
            self.pp()
            # time.sleep(1)
        self.determineQ()
        self.determinePolicy()
        self.ppQ()
        self.ppPolicy()

    def runQ(self):
        def checkConvergence(d1, d2):
            global lastDiff
            diff = 0
            flag = True
            for i in range(1, self.row + 1):
                for j in range(1, self.col + 1):
                    if d1[(i, j)] != d2[(i, j)]:
                        diff += abs(d1[(i, j)] - d2[(i, j)])
                        flag = False
            print "Error = ", diff
            if lastDiff == diff:
                return True
            lastDiff = diff
            return flag
        def checkConvergencePolicy(p1, p2):
            for i in range(1, self.row + 1):
                for j in range(1, self.col + 1):
                    if p1[(i, j)] != p2[(i, j)]:
                        return False
            return True
        self.initP()
        # self.ppPolicy()
        previousV = copy.deepcopy(self.V)
        # previousP = copy.deepcopy(self.P)
        self.updateQ()
        self.determineV()
        self.determineQ()
        self.determinePolicy()
        # self.ppPolicy()
        while not checkConvergence(previousV, self.V):
            previousV = copy.deepcopy(self.V)
            # previousP = copy.deepcopy(self.P)
            self.updateQ()
            self.determineV()
            self.determineQ()
            self.determineQ()
            self.determinePolicy()
            self.ppPolicy()
            time.sleep(1)
        self.ppQ()
        self.ppPolicy()



    def pp(self):
        for i in range(self.row, 0, -1):
            for j in range(1, self.col+1):
                print self.V[(i, j)], "\t",
            print "\n"
        print "----------------------------------------------"

    def ppPolicy(self):
        for i in range(self.row, 0, -1):
            for j in range(1, self.col + 1):
                if (i, j) in self.goals:
                    print "X", "\t",
                else:
                    print self.P[(i, j)], "\t",
            print "\n"

    def ppQ(self):
        for i in range(1, self.row + 1):
            for j in range(1, self.col+1):
                print i, j, "-->", self.Q[(i, j)]

# grid = GridWorld(5, 4, [(5, 4)], [100], 0.5)
grid = GridWorld(5, 4, [(5, 4), (1, 4)], [100, -100], 0.1)
grid.run()
# grid.runQ()
grid.pp()
