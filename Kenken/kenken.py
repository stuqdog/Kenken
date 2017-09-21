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

        #But to solve the problem discussed above, we need to repeat this
        #process over and over until all values are within one of the values
        #next to them.

        #Well, this doesn't quite solve it either. We're definitely still missing
        #combinations.
"""After doing this by hand, it seems like a possible method may be:
1. set the [-1] entry at puzzle size, set everything else at 1
2. if we're over sum, iterate down top value until we reach sum (if this happens,
then we have our solution immediately)
3. Then, set [-2] to whatever it needs to be to reach sum (or to [-1] val if
that's not high enough to reach the sum)


1. Okay so find the solution that best prioritized low values early (in the case
of 4 +17, that would be 1/1/7/8.). Add that to the possible solutions.
2. Then, for entry [-2], add one, and subtract one from [-1]. If it's not in possible
   solutions (in this case it's 1/1/8/7 which is in possible_solutions), then we add that
   to possible solutions. Then we add 2, then 3, etc. etc. until [-2] == puzzle size
   (so in this case, we only do it once).
3. Then we repeat the process, but start at [-3]. Add one, subtract one from [-1] and then
   [-2], and each time add the result to possible_solutions if it's not there already, and then
   do that with +/- 2, then 3, etc. until [-3] equal puzzle size.
      The order ([-1] first, then [-2]) is important. Once an entry reaches value [0],
      we know the math is going too far. But we don't want to miss anything. So start with
      the higher numbers. <-- This is wrong. See n.b. below.
4. then we go back to [-4] (not in this case, but you get the idea) and keep going back until
   we reach an entry where its value is the same as [0]. Once we reach that point, we do the whole
   +/- loop one more time, but don't bother going back to the previous index.
5. At this point, we've done everything where smallest value is 1. So now we repeat the
   whole process, but say 1 isn't allowed (so prioritize low early values, where 2 is the
   lowest value and 1 is not allowed).
6. Then we repeat that whole process until 3 * whatever our starting value is is >= sum.

N.b.: This doesn't work at all. If we have 1, 2, 7, 7, it isn't capturing 1, 4, 6, 6.
    OR MAYBE TI DOES??? Just not at the ones level.

n.b.b.: After running through this by hand, it missed 3 4 5 5. Seemed to capture everything
    else for the (4, +17) cluster. So, getting closer, but this still isn't it. Time to
    try to come up with something better.
"""

        while True:
            for x in range(1, self.cluster_size):
                print test_values
                while abs(test_values[-x] - test_values[-x - 1]) > 1:
                    test_values[-x] -= 1
                    test_values[-x - 1] += 1
                    self.possible.append(test_values[:])
            if all(abs(test_values[x] - test_values[x + 1]) <= 1
                   for x in range(self.cluster_size - 1)):
                break
        self.set_possible_ints()

    def find_subtraction_values(self):
        for x in range(self.formula[1] + 1, puzzle_size + 1):
            self.possible.append([x - self.formula[1], x])
        self.set_possible_ints()

    def find_division_values(self):
        for x in range(1, puzzle_size / self.formula[1] + 1):
            self.possible.append([x, x * self.formula[1]])
        self.set_possible_ints()


def sum_test(cluster_size, cluster_sum, puzzle_size):
    test = [1] * cluster_size
    for i, x in enumerate(reversed(test)):
