puzzle_size = 4

class Cell(object):

    def __init__(self, x, y, formula, possible, actual, cluster_size):
        self.x = x
        self.y = y
        self.formula = formula #should be (operator, value) - or maybe just two vars.
        self.possible = possible
        self.actual = actual
        self.cluster_size = cluster_size
        self.possible_ints = []

    # def find_possible(self):
    #      possible_list = []
    #      for x in range(cluster_size):
    #          possible_list.append([])
    #      if cell.formula[0] == "+":
    #          pass
             # for x in xrange(1, (puzzle_size + 1) // self.cluster_size):

    def find_addition_values(self):
        test_values = [1] * self.cluster_size
            # Iterate up one at a time, starting with top values, until we reach
            # the sum we're looking for.
        for x in range(1, self.cluster_size + 1):
            while test_values[-x] < puzzle_size:
                test_values[-x] += 1
                if sum(test_values) == self.formula[1]:
                    self.possible.append(test_values[:])
                    break
            if sum(test_values) == self.formula[1]:
                break

        # Once we have reached sum, we lower the top value and raise lower
        # values to find other possible combinations that reach the sum.
        for x in range(1, self.cluster_size):
            print test_values
            while abs(test_values[-x] - test_values[-x - 1]) > 1:
                test_values[-x] -= 1
                test_values[-x - 1] += 1
                self.possible.append(test_values[:])

        for combo in self.possible:
            for i in combo:
                if i not in self.possible_ints:
                    self.possible_ints.append(i)


class CellCluster(object):

    def __init__(self, cells, formula): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula
