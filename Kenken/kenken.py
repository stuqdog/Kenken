puzzle_size = 4

class Cell(object):

    def __init__(self, x, y, formula, possible, actual, cluster_size):
        self.x = x
        self.y = y
        self.formula = formula # should be (operator, value)
        self.possible = possible # we may just want this to be an empty list initially
        self.actual = actual
        self.cluster_size = cluster_size


class CellCluster(object):

    def __init__(self, cells, formula, cluster_size, possible): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula
        self.cluster_size = cluster_size
        self.possible = possible

    def set_possible_ints(self):
        for cell in self.cells:
            for combo in self.possible:
                for i in combo:
                    if i not in cell.possible:
                        cell.possible.append(i)

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
        self.set_possible_ints()

    def find_subtraction_values(self):
        for x in range(self.formula[1] + 1, puzzle_size + 1):
            self.possible.append([x - self.formula[1], x])
        self.set_possible_ints()

    def find_division_values(self):
        for x in range(1, puzzle_size / self.formula[1] + 1):
            self.possible.append([x, x * self.formula[1]])
        self.set_possible_ints()
