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






'''
This works right now, which is cool. But needs more functionality. Want to allow people to select which numbers are in a group, and then define what that group's function is. How we can do this:

1) Create a defined_cells dictionary.
2) If a cell is in the defined_cells dict, then instead of printing the cell_number in the display formatting, we print group, or formula, or something like that.
  a) We could probably set it up to do both on different rows, though that will complicate a bit the printing.
3) Create a new function that allows to create new ones. It'll just ask people to say which cells are in a group, and what the group formula is.
  In this function call, we need to limit the number of clusters that are legal to create. Can't so cells 1, 6, and 24, e.g. Make sure all cells are either one away from each other, or (size) away from each other. But also account for things being along the edge. e.g., in a size 6, cells 6 and 7 can't be legally connected.'''

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
        # print(mid_cell)
        # print(mid_cell)
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

puzzle = visual_display()
print(puzzle)

def create_cluster(cluster_num):
    new_cluster = input("""Please enter the members of a cell,
                             \rdivided by commas.\n >""").strip().split(',')
    while any(int(c) not in set(range(1, size ** 2 + 1)) for c in new_cluster):
        new_cluster = input("""Invalid input. Cells must be in numeric form,
                \rseparated by commas. Try again!\n >""").strip().split(',')
    while any(int(cell) in defined_cells for cell in new_cluster):
        new_cluster = input("""Invalid input. Cells cannot be in
                   \rmultiple clusters. Try again!\n >""").strip().split(',')

    for cell in new_cluster:
        defined_cells[int(cell)] = cluster_num

cluster_number = 1
while any(x not in defined_cells for x in range(1, size ** 2 + 1)):
    create_cluster(cluster_number)
    cluster_number += 1
    print(visual_display())
