import copy
import time

class GridWorld:
    def __init__(self, r, c, goals, goalReward):
        self.row = r
        self.col = c
        self.goals = goals
        self.goalReward = goalReward
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
        for goal in self.goals:
            self.V[goal] = self.goalReward

    def determineQ(self):
        def checkValidCoordinate(i, j):
            return 0 < i <= self.row and 0 < j <= self.col
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                self.Q[(i, j)] = {}
                if checkValidCoordinate(i - 1, j):
                    self.Q[(i, j)]['S'] = self.V[(i-1, j)]
                else:
                    self.Q[(i, j)]['S'] = -1

                if checkValidCoordinate(i + 1, j):
                    self.Q[(i, j)]['N'] = self.V[(i + 1, j)]
                else:
                    self.Q[(i, j)]['N'] = -1

                if checkValidCoordinate(i, j - 1):
                    self.Q[(i, j)]['W'] = self.V[(i, j - 1)]
                else:
                    self.Q[(i, j)]['W'] = -1

                if checkValidCoordinate(i, j + 1):
                    self.Q[(i, j)]['E'] = self.V[(i, j + 1)]
                else:
                    self.Q[(i, j)]['E'] = -1

    def determinePolicy(self):
        for i in range(1, self.row+1):
            for j in range(1, self.col+1):
                qvals = self.Q[(i, j)].items()
                m = max(qvals, key=lambda x: x[-1])
                self.P[(i, j)] = m[0]

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

    def run(self):
        def checkConvergence(d1, d2):
            diff = 0
            for i in range(1, self.row + 1):
                for j in range(1, self.col + 1):
                    if d1[(i, j)] != d2[(i, j)]:
                        diff += abs(d1[(i, j)] - d2[(i, j)])
                        # return False
            print diff
            return diff == 0
        previousV = copy.deepcopy(self.V)
        self.update()
        self.pp()
        while not checkConvergence(previousV, self.V):
            previousV = copy.deepcopy(self.V)
            self.update()
            # self.pp()
            # time.sleep(1)
        self.determineQ()
        self.determinePolicy()
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

grid = GridWorld(5, 4, [(5, 4), (1, 4)], 100)
grid.run()
