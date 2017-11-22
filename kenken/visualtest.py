'''Okay, this looks like a working visual layout system! Also it's got some neat logic, it lets the user put in the formula, and the check_if_legal uses a BFS to confirm total connectivity. Need to bring over the reduction and start doing the actual math now! The fun part!'''

class Cell(object):
    def __init__(self, x, y, visual):
        self.x = x
        self.y = y
        self.visual = visual
        self.formula = None
        self.cluster = None

class Cluster(object):
    def __init__(self, formula, cells=[], size=0, possible=[]):
        self.cells = cells
        self.size = size
        self.formula = formula
        self.possible = possible


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
    formula_type = input("Please enter formula type: +, -, *, /, or none\n >")
    while formula_type not in {'+', '-', '*', '/', 'none'}:
        formula_type = input("Please enter formula type: +, -, *, /, or none\n >")
    formula_val = int(input("Please enter formula value as an integer\n >"))
    new_cluster = Cluster((formula_type, formula_val))
    for cell in cluster_string:
        new_cell = layout[(cell - 1) // size][(cell - 1) % size]
        if group_number < 10:
            new_cell.visual = " g{}".format(str(group_number))
        else:
            new_cell.visual = "g{}".format(str(group_number))
        new_cluster.cells.append(new_cell)
        new_cluster.size += 1
        new_cell.formula = (formula_type, formula_val)
        new_cell.cluster = group_number
    clusters[group_number] = new_cluster


size = int(input("What is the puzzle size? \n >"))
while size < 3 and size > 9:
    size = int(input("Puzzle size must be between 3 and 9. Try again! \n >"))

clusters = {}

layout = create_layout()
print(visual_layout(layout))
group_number = 1

while any(cell.cluster == None for cell in cell_generator()):
    cluster_string = input("List cells in a cluster, divided by commas.\n >"
                           ).strip().split(',')
    cluster_string = [int(cell) for cell in cluster_string]
    while any(layout[(cell - 1) // size][(cell - 1) % size].cluster
              != None for cell in cluster_string):
        cluster_string = input("Can't reuse cells, try again!\n >"
                               ).strip().split(',')
        cluster_string = [int(cell) for cell in cluster_string]
    while check_if_legal(cluster_string) == False:
        cluster_string = input("All cells in a cluster must be connected!\n >"
                               ).strip().split(',')
        cluster_string = [int(cell) for cell in cluster_string]
    update_cells(cluster_string, group_number)
    group_number += 1
    print(visual_layout(layout))

for cluster in clusters.values():
    print('size: {}. formula: {}'.format(cluster.size, cluster.formula))
