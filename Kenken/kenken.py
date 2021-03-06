"""
###############################################################################
# TO DO:                                                                      #
# 1. Logic for reducing from possible to actual.                              #
# 1b.In reduce_x_y, need to say if only one cell can possibly be n, then      #
#    that cell is definitely n, even if theoretically it could be m           #
#    Trying to do this at bottom of reduce_x_y, but not working. Why?         #
#    --SOLVED-- Needed to also confirm that we hadn't already solved for n    #
# 1c.If i cells have identical possibles of len(i), then no other cell in the #
#    row or column can have one of those values.                              #
# 1d.Conflicts. If a x5 exists in a row, and a cell in that row is part of a  #
#    vertical +6, we know that the (1, 5) possible isn't actually possible.   #
# 2. Fix update_cells, specifically at the top. Need to confirm that the      #
#    formula type is legitimate even after it is being reset.                 #
# 3. Significant refactor, but: maybe we should convert possible from a list  #
#    to a collections Counter? Will definitely make some of this easier and   #
#    faster. Thinking right now in particular the incomplete code snipped at  #
#    bottom of "reduce_x_y".
###############################################################################
"""


import itertools
from collections import Counter

class Cell(object):
    def __init__(self, x, y, visual):
        self.x = x
        self.y = y
        self.visual = visual
        self.formula = None
        self.cluster = None
        self.actual = None
        self.possible_combos = []
        self.possible = []


class Cluster(object):
    def __init__(self, formula):
        self.cells = []
        self.size = 0
        self.formula = formula
        self.possible = []
        self.minimum_unique_digits = 0


    def find_values(self):
        if self.formula[0] == '+':
            self.find_addition_values()
        elif self.formula[0] == '-':
            self.find_subtraction_values()
        elif self.formula[0] == '*':
            self.find_multiplication_values()
        elif self.formula[0] == '/':
            self.find_division_values()
        elif self.formula[0] == '=':
            self.set_single_value()
        else:
            print("Ruh roh")
        arr_ = (["x{}".format(cell.x) for cell in self.cells]
                 + ["y{}".format(cell.y) for cell in self.cells])
        self.min_digits = Counter(arr_).most_common()[0][1]
        self.possible = [x for x in self.possible if len(set(x))
                         >= self.min_digits]

    def find_addition_values(self):
        arr = list(range(1, size + 1)) * self.size
        possible_long = list(set(x for x in itertools.combinations(
               arr, self.size) if sum(x) == self.formula[1]))
        possible_long = [sorted(x) for x in possible_long]
        for x in possible_long:
            if x not in self.possible:
                self.possible.append(x)

    def find_subtraction_values(self):
        for x in range(self.formula[1] + 1, size + 1):
            self.possible.append([x - self.formula[1], x])

    def find_division_values(self):
        for x in range(1, size // self.formula[1] + 1):
            self.possible.append([x, x * self.formula[1]])

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
            possible_long = list(set(y for y in itertools.combinations(
                arr, self.size) if self.check_multiplication_value(y)
                == self.formula[1]))
            possible_long = [sorted(x) for x in possible_long]
            for x in possible_long:
                if x not in self.possible:
                    self.possible.append(x)

    def set_single_value(self):
        self.cells[0].possible = [self.formula[1]]

    def set_possible_ints(self):
        for cell in self.cells:
            for combo in self.possible:
                cell.possible += combo
            cell.possible = list(set(cell.possible))

    def reduce_possible(self):
        solved = [cell.actual for cell in self.cells if cell.actual != None]
        self.possible = [combo for combo in self.possible if all(
                      Counter(combo)[x] >= Counter(solved)[x] for x in solved)]
        for cell in self.cells:
            if len(cell.possible) == 1:
                cell.actual = cell.possible[0]
                cell.possible = []
                solved.append(cell.actual)
                for cell_ in self.cells:
                    if cell.actual in cell_.possible and (cell.x == cell_.x or
                    cell.y == cell_.y):
                        del cell_.possible[cell_.index(cell.actual)]
            for q in range(1, size+1): #######
                if q in cell.possible and all(q not in y for y in self.possible):
                    cell.possible.remove(q) ########


def create_layout():
    cell_number = 1
    layout = []
    for row in range(size):
        layout.append([])
        for column in range(size):
            layout[-1].append(Cell(column, row, str(cell_number).rjust(3)))
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
    '''refactor likely useful here. Seems awkward that we have to construct a
    new 2d array each time we want to check legality. We can probably make this
    more efficient.
    '''
    legality_test = [[0] * size for x in range(size)]
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
    formula_type = input("Please enter formula type: +, -, *, /, or =\n> ")
    while formula_type.lower() not in {'+', '-', '*', '/', '='}:
        formula_type = input("Please enter formula type: +, -, *, /, or =\n> ")

    while formula_type in ['-', '/'] and len(cluster_string) != 2:
        formula_type = input("""Division and subtraction clusters can only
          \rbe two values. Please try again. \n> """)
        while formula_type.lower() not in {'+', '-', '*', '/', '='}:
            formula_type = input("Please enter formula type: +, -, *, /, or =\n> ")

    while (formula_type.lower() != '=' and len(cluster_string) == 1) or (
           formula_type.lower() == '=' and len(cluster_string) != 1):
        formula_type = input("""Cluster size can be one if and only if the
                \rformula type is '='! Please try again.\n> """)
        while formula_type.lower() not in {'+', '-', '*', '/', '='}:
            formula_type = input("Please enter formula type: +, -, *, /, or =\n> ")

    formula_val = int(input("Please enter formula value as an integer\n> "))
    create_new_cluster((formula_type, formula_val), cluster_string)

def create_new_cluster(formula, cluster_string):
    new_cluster = Cluster(formula)
    for cell in cluster_string:
        new_cell = layout[(cell - 1) // size][(cell - 1) % size]
        new_cell.visual = ("g{}".format(str(group_number))).rjust(3)
        new_cell.formula = formula
        new_cell.cluster = group_number
        new_cluster.cells.append(new_cell)
        new_cluster.size += 1
    clusters.append(new_cluster)


def reduce_x_y(val):
    row = [layout[x][val] for x in range(size)]
    solved = [cell.actual for cell in row if cell.actual != None]
    for i in range(1, size+1):
        if sum(1 for cell in row if i in cell.possible) == 1 and i not in solved:
            for cell in row:
                if i in cell.possible:
                    cell.actual = i
                    cell.possible = []
    for cell in row:
        cell.possible = [x for x in cell.possible if x not in solved]
        if len(cell.possible) == 1:
            cell.actual = cell.possible[0]
            cell.possible = []
            solved.append(cell.actual)
    column = [layout[val][y] for y in range(size)]
    solved = [cell.actual for cell in column if cell.actual != None]
    for i in range(1, size+1):
        if sum(1 for cell in column if i in cell.possible) == 1 and i not in solved:
            for cell in column:
                if i in cell.possible:
                    cell.actual = i
                    cell.possible = []
    for cell in column:
        cell.possible = [y for y in cell.possible if y not in solved]
        if len(cell.possible) == 1:
            cell.actual = cell.possible[0]
            cell.possible = []
            solved.append(cell.actual)

    ##################
    # for _ in range(2, size):
    #     combo_solve = [x for x in itertools.combinations(row/column, _) if
    #                    all(y.possible == x[0].possible for y in x) and
    #                    len(x[0].possible) == _]
    #     for z in [x for x row/column if x not in combo_solve]:
    #         for i in combo_solve[0].possible:
    #             if i in z.possible:
    #                 z.possible.remove(i)
    '''Ohhhhhh boy this (above ^^^) is ugly as heck. Gotta clean it up, but it's
    the core logic at least.'''
    #################


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
    cluster_string = [int(cells) for cells in cluster_string]
    while any(layout[(cells - 1) // size][(cells - 1) % size].cluster
              != None for cells in cluster_string):
        cluster_string = input("Can't reuse cells, try again!\n> "
                               ).strip().split(',')
        cluster_string = [int(cells) for cells in cluster_string]
    while check_if_legal(cluster_string) == False:
        cluster_string = input("All cells in a cluster must be connected!\n> "
                               ).strip().split(',')
        cluster_string = [int(cells) for cells in cluster_string]
    update_cells(cluster_string, group_number)
    group_number += 1
    print(visual_layout(layout))

for cluster in clusters:
    cluster.find_values()
    cluster.reduce_possible()
    cluster.set_possible_ints()

counts = 0
while any(cell.actual == None for cell in cell_generator()):
    for cluster in clusters:
        cluster.reduce_possible()
    for row_or_column in range(size):
        reduce_x_y(row_or_column)
    counts += 1
    if counts > 8000:
        break

for cell in cell_generator():
    cell.actual = 0 if not cell.actual else cell.actual
    cell.visual = " {} ".format(cell.actual)

print(visual_layout(layout))
