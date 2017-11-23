"""
###############################################################################
# TO DO:                                                                      #
# 1. Find combinations based on formula - PROBABLY DONE, CHECK * FORMULA -    #
# 2. Logic for reducing from possible to actual.                              #
# 2a.As a first step, We can reduce some options. (4, 4, 4, 4) is not a valid #
#    solution to +16, e.g. This will be a bigger problem in multiplication    #
#    Need to keep track of how much x/y variation there is in the cluster.    #
#    Lower of the two (+1) is the max number of copies of any given digit     #
# 2b.From there, we need a number of methods for reducing. There will         #
#    likely be a lot of them. Will need to look at cluster, but also row and  #
#    column.                                                                  #
# 3. Fix group making. subtraction and division shouldn't be allowed to be    #
#    more than two numbers, e.g. ---THIS SHOULD BE DONE---                    #
# 4. Fix update_cells, specifically at the top. Need to confirm that the      #
#    formula type is legitimate even after it is being reset.                 #
# 5. MULTIPLICATION ISN'T WORKING. Fix IT FIXIT FIXITIFIXTIIFXITIFXITIERNST   #
###############################################################################
"""

import itertools

class Cell(object):
    def __init__(self, x, y, visual):
        self.x = x
        self.y = y
        self.visual = visual
        self.formula = None
        self.cluster = None
        self.actual = None
        self.possible = []

class Cluster(object):
    def __init__(self, formula, cells=[], size=0, possible=[]):
        self.cells = cells
        self.size = size
        self.formula = formula
        self.possible = possible

    def set_possible_ints(self):
        pass
        for cell in self.cells:
            for combo in self.possible:
                for i in combo:
                    if i not in cell.possible:
                        cell.possible.append(i)

    def find_values(self):
        if self.formula[0] == '+':
            self.find_addition_values()
        if self.formula[0] == '-':
            self.find_subtraction_values()
        if self.formula[0] == '*':
            self.find_multiplication_values()
        if self.formula[0] == '/':
            self.find_division_values()
        if self.formula[0] == 'none':
            self.set_single_value()


    def find_addition_values(self):
        arr = list(range(1, size + 1)) * self.size
        possible_long = list(set(x for x in itertools.combinations(
               arr, self.size) if sum(x) == self.formula[1]))
        possible_long = [sorted(x) for x in possible_long]
        self.possible = [] # Why don't we just do this with another set?
                            # Running into trouble trying it. Gotta figure out why.
        for x in possible_long:
            if x not in self.possible:
                self.possible.append(x)
        self.set_possible_ints()


    def find_subtraction_values(self):
        for x in range(self.formula[1] + 1, size + 1):
            self.possible.append([x - self.formula[1], x])
        self.set_possible_ints()

    def find_division_values(self):
        for x in range(1, size / self.formula[1] + 1):
            self.possible.append([x, x * self.formula[1]])
        self.set_possible_ints()

    def check_multiplication_value(self, arr):
        check = 1
        for x in arr:
            check *= x
        return check

    def find_multiplication_values(self):
        arr = []
        for x in range(1, size + 1):
            if self.formula[1] % x == 0:
                arr += [x] * self.size
            possible_long = list(set(x for x in itertools.combinations(
                arr, self.size) if self.check_multiplication_value(x)
                == self.formula[1]))

    def set_single_value(self):
        self.cells[0].actual = self.formula[1]
        self.cells[0].possible = self.formula[1]

def create_layout():
    cell_number = 1
    layout = []
    for row in range(size):
        layout.append([])
        for column in range(size):
            if cell_number < 10:
                layout[-1].append(Cell(column, row, '  ' + str(cell_number)))
            else:
                layout[-1].append(Cell(column, row, ' ' + str(cell_number)))
            cell_number += 1
    return layout


def cell_generator():
    for row in layout:
        for cell in row:
            yield cell


def visual_layout(layout):
    top = " _____" * size
    mid_cell = "|" + "     |" * size
    mid_cell_bottom = "|" + "_____|" * size

    puzzle = top + "\n"

    for column in range(size):
        puzzle += (mid_cell + "\n") * 2
        mid_cell_num = ''
        for row in range(size):
            mid_cell_num += " {} |".format(layout[column][row].visual)
        mid_cell_num = "|" + mid_cell_num
        puzzle += mid_cell_num + "\n"
        puzzle += mid_cell + "\n"
        puzzle += mid_cell_bottom + "\n"
    return puzzle


def check_if_legal(cluster):
    legality_test = []
    for x in range(size):
        legality_test.append([0] * size)
    for cell in cluster:
        legality_test[(cell - 1) // size][(cell - 1) % size] = 1
    connected_positions = [((cell - 1) // size, (cell - 1) % size)]
    while True:
        stop_test = True
        for entry in connected_positions:
            test_pos = [(entry[0] + 1, entry[1]), (entry[0] - 1, entry[1]),
                        (entry[0], entry[1] - 1), (entry[0], entry[1] + 1)]
            for pos in test_pos:
                if pos[0] < 0 or pos[1] < 0 or pos[0] == size or pos[1] == size:
                    pass
                else:
                    if legality_test[pos[0]][pos[1]] == 1 and (
                          (pos[0], pos[1]) not in connected_positions):
                        stop_test = False
                        connected_positions.append((pos[0], pos[1]))
        if stop_test == True:
            break
    if len(connected_positions) == len(cluster):
        return True
    else:
        return False


def update_cells(cluster_string, group_number):
    formula_type = input("Please enter formula type: +, -, *, /, or none\n> ")
    while formula_type.lower() not in {'+', '-', '*', '/', 'none'}:
        formula_type = input("Please enter formula type: +, -, *, /, or none\n> ")

    while formula_type in ['-', '/'] and len(cluster_string) != 2:
        formula_type = input("""Division and subtraction clusters can only
          \rbe two values. Please try again. \n> """)
        while formula_type.lower() not in {'+', '-', '*', '/', 'none'}:
            formula_type = input("Please enter formula type: +, -, *, /, or none\n> ")

    while (formula_type.lower() != 'none' and len(cluster_string) == 1) or (
           formula_type.lower() == 'none' and len(cluster_string) != 1):
        formula_type = input("""Cluster size can be one if and only if the
                \rformula type is 'none'! Please try again.\n> """)
        while formula_type.lower() not in {'+', '-', '*', '/', 'none'}:
            formula_type = input("Please enter formula type: +, -, *, /, or none\n> ")

    formula_val = int(input("Please enter formula value as an integer\n> "))
    create_new_cluster((formula_type, formula_val), cluster_string)

def create_new_cluster(formula, cluster_string):
    new_cluster = Cluster((formula))
    for cell in cluster_string:
        new_cell = layout[(cell - 1) // size][(cell - 1) % size]
        if group_number < 10:
            new_cell.visual = " g{}".format(str(group_number))
        else:
            new_cell.visual = "g{}".format(str(group_number))
        new_cluster.cells.append(new_cell)
        new_cluster.size += 1
        new_cell.formula = formula
        new_cell.cluster = group_number
    clusters.append(new_cluster)


size = int(input("What is the puzzle size?\n> "))
while size < 3 and size > 9:
    size = int(input("Puzzle size must be between 3 and 9. Try again!\n> "))

clusters = []

layout = create_layout()
print(visual_layout(layout))
group_number = 1

while any(cell.cluster == None for cell in cell_generator()):
    cluster_string = input("List cells in a cluster, divided by commas.\n> "
                           ).strip().split(',')
    cluster_string = [int(cell) for cell in cluster_string]
    while any(layout[(cell - 1) // size][(cell - 1) % size].cluster
              != None for cell in cluster_string):
        cluster_string = input("Can't reuse cells, try again!\n> "
                               ).strip().split(',')
        cluster_string = [int(cell) for cell in cluster_string]
    while check_if_legal(cluster_string) == False:
        cluster_string = input("All cells in a cluster must be connected!\n> "
                               ).strip().split(',')
        cluster_string = [int(cell) for cell in cluster_string]
    update_cells(cluster_string, group_number)
    group_number += 1
    print(visual_layout(layout))

for cluster in clusters:
    cluster.find_values()
    print(cluster.possible)
