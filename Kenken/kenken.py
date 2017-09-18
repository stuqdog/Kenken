puzzle_size = 3

class Cell(object):

    def __init__(self, x, y, formula, possible, actual, cluster_size):
        self.x = x
        self.y = y
        self.formula = formula #should be (operator, value) - or maybe just two vars.
        self.possible = possible
        self.actual = actual
        self.cluster_size = cluster_size

    def find_possible(cell):
        if cell.formula[0] = "+":
            for x in xrange(1, puzzle_size + 1):



class CellCluster(object):

    def __init__(self, cells, formula): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula
