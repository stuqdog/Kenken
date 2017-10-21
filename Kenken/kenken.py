import itertools
puzzle_size = 8

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
        pass
        for cell in self.cells:
            for combo in self.possible:
                for i in combo:
                    if i not in cell.possible:
                        cell.possible.append(i)



    def find_addition_values(self):
        arr = list(range(1, puzzles_size + 1)) * self.cluster_size
        possible_long = list(set(x for x in itertools.combinations(
               arr, self.cluster_size) if sum(x) == self.formula[1]))
        possible_long = [sorted(x) for x in possible_long]
        self.possible = [] # Why don't we just do this with another set?
                            # Running into trouble trying it. Gotta figure out why.
        for x in possible_long:
            if x not in self.possible:
                self.possible.append(x)
        self.set_possible_ints()


    def find_subtraction_values(self):
        for x in range(self.formula[1] + 1, puzzle_size + 1):
            self.possible.append([x - self.formula[1], x])
        self.set_possible_ints()

    def find_division_values(self):
        for x in range(1, puzzle_size / self.formula[1] + 1):
            self.possible.append([x, x * self.formula[1]])
        self.set_possible_ints()

    def check_multiplication_value(self, arr):
        check = 1
        for x in arr:
            check *= x
        return check

    def find_multiplication_values(self):
        arr = []
        for x in range(1, puzzle_size + 1):
            if self.formula[1] % x == 0:
                arr += [x] * self.cluster_size
            possible_long = list(set(x for x in itertools.combinations(
                arr, self.cluster_size) if self.check_multiplication_value(x)
                == self.formula[1]))
