puzzle_size = 4

class Cell(object):

    def __init__(self, x, y, formula, possible, actual, cluster_size):
        self.x = x
        self.y = y
        self.formula = formula #should be (operator, value) - or maybe just two vars.
        self.possible = possible
        self.actual = actual
        self.cluster_size = cluster_size

    # def find_possible(cell):
    #     possible_list = []
    #     for x in range(cluster_size):
    #         possible_list.append([])
    #     if cell.formula[0] = "+":
    #         for x in xrange(1, (puzzle_size + 1) // self.cluster_size):







class CellCluster(object):

    def __init__(self, cells, formula): ## do we need possible and actual here?
        self.cells = cells
        self.formula = formula



def find_addition_values(puzzle_size, cluster_sum, cluster_size):
    possible_values = []
    for x in range(cluster_size):

# start with range of lowest possible values, then slowly iterate up one at a
# time to find possible sums. Iterate order should be: iterate highest value all
# the way up until we hit either the sum, or the puzzle size cap.
# Assuming we hit sum, then we iterate up the [-2] value and down the [-1] value
# until they are within one of each other. Then we do the same with [-3] and [-2]
# and so on, all the way down to [-cluster_size]
# this will give us cases with duplicates (such as [3, 1] and [2, 2] both adding to
# 4), but this is okay. We can reject these later, and they might be useful for
# cases where a cluster exists in multiple rows/columns.
    test_values = range(cluster_size)
    if sum(x for x in test_values) == cluster_sum:
        possible_values.append(test_values)
    elif sum(x for x in test_values) < cluster_sum:

    for x in range(sum // cluster_size):
        test_values = range()
