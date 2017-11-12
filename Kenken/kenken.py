"""
###############################################################################
# TO DO:                                                                      #
# 1. Find combinations based on formula - PROBABLY DONE, CHECK * FORMULA -    #
# 2. Logic for reducing from possible to actual.                              #
# 3. As a first step, We can reduce some options. (4, 4, 4, 4) is not a valid #
#    solution to +16, e.g. This will be a bigger problem in multiplication    #
#    Need to keep track of how much x/y variation there is in the cluster.    #
#    Lower of the two (+1) is the max number of copies of any given digit     #
# 4. From there, we need a number of methods for reducing. There will         #
#    likely be a lot of them. Will need to look at cluster, but also row and  #
#    column.                                                                  #
###############################################################################
"""

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


size = int(input("What is the puzzle size? \n > "))
while size > 9 and size < 3:
    print("Size must be a number between 3 and 9, inclusive.")
    size = int(input("What is the puzzle size? \n > "))

defined_cells = {}



def visual_display():
    cell_number = 1

    top = " _____" * size
    mid_cell = "|" + "     |" * size
    mid_cell_bottom = "|" + "_____|" * size

    puzzle = top + "\n"

    for row in range(size):
        puzzle += (mid_cell + "\n") * 2
        mid_cell_num = ''
        for column in range(size):
            if cell_number in defined_cells:
                if defined_cells[cell_number] < 10:
                    mid_cell_num += " g{}  |".format(defined_cells[cell_number])
                else:
                    mid_cell_num += " g{} |".format(defined_cells[cell_number])
            else:
                if cell_number < 10:
                    mid_cell_num += "  {}  |".format(cell_number)
                else:
                    mid_cell_num += " {}  |".format(cell_number)
            cell_number += 1
        mid_cell_num = "|" + mid_cell_num
        puzzle += mid_cell_num + "\n"
        puzzle += mid_cell + "\n"
        puzzle += mid_cell_bottom + "\n"
    return puzzle


def check_if_legal(cluster):
    """This logic can be approved. Do research to avoid doubling work (1 is next to 2, do we really need to also confirm that 2 is next to 1?) and also to avoid creating false groups (1 is next to 2 and 15 is next to 16, but 1, 2, 15, 16 is not a vaild group)"""
    if len(cluster) == 1:
        return True
    for cell in cluster:
        if any(int(c) == int(cell) + size for c in cluster):
            pass
        elif any(int(c) == int(cell) - size for c in cluster):
            pass
        elif int(cell) % size != 1 and any(int(c) ==
                                           int(cell) - 1 for c in cluster):
            pass
        elif int(cell) % size != 0 and any(int(c) ==
                                           int(cell) + 1 for c in cluster):
            pass
        else:
            return False
    return True


def create_clusters():
    """We should use try/except here to avoid crashes and lost progress due to
    input mistakes"""
    cluster_num = 1
    while any(x not in defined_cells for x in range(1, size ** 2 + 1)):
        new_cluster = input("""Please enter the members of a cell,
                             \rdivided by commas.\n >""").strip().split(',')
        while any(int(c) not in set(range(1, size ** 2 + 1)) for c in new_cluster):
            new_cluster = input("""Invalid input. Cells must be in numeric form,
                   \rseparated by commas. Try again!\n >""").strip().split(',')
        while any(int(cell) in defined_cells for cell in new_cluster):
            new_cluster = input("""Invalid input. Cells cannot be in
                     \rmultiple clusters. Try again!\n >""").strip().split(',')
        while check_if_legal(new_cluster) == False:
            new_cluster = input("""Invalid input. Cells must be connected either
            \rvertically or horizontally. Try again!\n >""").strip().split(',')

        for cell in new_cluster:
            defined_cells[int(cell)] = cluster_num
        cluster_num += 1
        print(visual_display())


print(visual_display())
create_clusters()
