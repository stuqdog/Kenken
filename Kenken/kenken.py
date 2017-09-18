class Cell(object):

    def __init__(self, x, y, formula, possible, actual):
        self.x = x
        self.y = y
        self.formula = formula
        self.possible = possible
        self.actual = actual


class CellCluster(object):

    def __init__(self, cells, formula): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula
