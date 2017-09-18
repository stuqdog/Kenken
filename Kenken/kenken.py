puzzle_size = 4

class Cell(object):

    def __init__(self, x, y, formula, possible, actual, cluster_size):
        self.x = x
        self.y = y
        self.formula = formula #should be (operator, value) - or maybe just two vars.
        self.possible = possible
        self.actual = actual
        self.cluster_size = cluster_size

    # def find_possible(self):
    #      possible_list = []
    #      for x in range(cluster_size):
    #          possible_list.append([])
    #      if cell.formula[0] == "+":
    #          pass
             # for x in xrange(1, (puzzle_size + 1) // self.cluster_size):

    def find_addition_values(self):
        possible_values = []
        # for x in range(cluster_size):

    # start with range of lowest possible values, then slowly iterate up one at a
    # time to find possible sums. Iterate order should be: iterate highest value all
    # the way up until we hit either the sum, or the puzzle size cap.
    # Assuming we hit sum, then we iterate up the [-2] value and down the [-1] value
    # until they are within one of each other. Then we do the same with [-3] and [-2]
    # and so on, all the way down to [-cluster_size]
    # this will give us cases with duplicates (such as [3, 1] and [2, 2] both adding to
    # 4), but this is okay. We can reject these later, and they might be useful for
    # cases where a cluster exists in multiple rows/columns.
        test_values = range(1, self.cluster_size + 1)
        if sum(x for x in test_values) == self.formula[1]:
            possible_values.append(test_values[:])
        elif sum(x for x in test_values) < self.formula[1]:
            for i in range(1, self.cluster_size + 1):
                while test_values[-1] < puzzle_size:
                    test_values[-i] += 1
                    if sum(x for x in test_values) == self.formula[1]:
                        possible_values.append(test_values[:])
                        while abs(test_values[-i]) - test_values[-i - 1] > 1:
                            test_values[-i] -= 1
                            test_values[-i - 1] += 1
                            possible_values.append(test_values[:])
                        break
                    if i == 1 and test_values[-1] == puzzle_size or (i != 1 and
                       abs(test_values[-i] - test_values[-i + 1]) in [0, 1]):
                        break


        self.possible = sorted(possible_values)





class CellCluster(object):

    def __init__(self, cells, formula): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula
