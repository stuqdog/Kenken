"""
To do:
-  We need a test to make sure that subtraction and division clusters are never
   more or less than two cells.
-  Need to actually make the logic of find_possible, lol :(
-  Relatedly, need to find a good way to test addition/multiplication clusters
   of more than two cells. Find efficient way to find how to take X numbers that
   sum/multiply to the resulting value, where X is cluster size.
-  Need to work out logic of reducing possible to actual
-  We need to actually just clean up the syntax of our tests here. Get a better
   understanding of how we're calling the functions in kenken.py.
     - I think we may have this fixed now. I'll have to fix up the logic enough
       to run these tests, and then find out!

"""

from nose.tools import *
from kenken import kenken

def test_addition():
    test_square = kenken.Cell(1, 1, ('+', 3), [], [], 2)
    test_square.find_addition_values()
    assert_equal(test_square.possible, [[1, 2]])

    test_square = kenken.Cell(1, 1, ('+', 5), [], [], 2)
    test_square.find_addition_values()
    assert_equal(test_square.possible, [[1, 4], [2, 3]])

def test_subtraction():
    test_square = kenken.Cell(1, 1, ('-', 3), [], [], 2)
    test_square.find_subtraction_values()
    assert_equal(test_square.possible, [[1, 4]])
#
# def test_multiplication():
#     test_square = Cell(1, 1, ('*', 12), [1, 2, 3, 4], [], 2)
#     test_square.find_possible()
#     assert_equal(test_square.possible, [3, 4])
#
def test_division():
    test_square = kenken.Cell(1, 1, ('/', 3), [], [], 2)
    test_square.find_division_values()
    assert_equal(test_square.possible, [[1, 3]])

    test_square = kenken.Cell(1, 1, ('/', 2), [], [], 2)
    test_square.find_division_values()
    assert_equal(test_square.possible, [[1, 2], [2, 4]])
