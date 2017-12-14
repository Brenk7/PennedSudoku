
from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# zip method enables iteration over two lists in parallel
diagonal_units = [[r + c for (r, c) in zip(rows, cols)], [r + c for (r, c) in zip(reversed(rows), cols)]]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # take a unitlist and iterate over each unit, looking for a set of twins,
    # then deducting the values from the other boxes in the unit
    for unit in unitlist:
        # initialize an empty list to hold our naked twin pairs
        naked_twins = []
        # iterate over each box in the unit
        for box in unit:
            # if the amount of possible values in the box is 2, we might have located a twin
            if len(values[box]) == 2:
                # loop through the unit's boxes again, looking to see if we can locate a twin
                for potential_twin in unit:
                    # if the potential twin is not the current box and values of the boxes match....
                    if potential_twin != box and values[box] == values[potential_twin]:
                        # double check that the pair is not already in our naked twins array
                        if [box, potential_twin] not in naked_twins and [potential_twin, box] not in naked_twins:
                            # add it!
                            naked_twins.append([box, potential_twin])
        # now that we have our naked_twins list complete, we can start removing their values from the other boxes in the unit
        for twins in naked_twins:
            # iterate over each box in the unit
            for box in unit:
                # iterate over each value contained in the first twin (since they are identical)
                for digit in values[twins[0]]:
                    # if the box is not one of the twins in the unit, deduct the twin's values
                    if box not in twins:
                        values = assign_value(values, box, values[box].replace(digit, ''))

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = naked_twins(values)
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # check to make sure the reduced puzzle is not solved/errored out
    if values is False:
        # errored?
        return False
    # The all() method returns True when all elements in the given iterable are true. If not, it returns False.
    # Does each value for the boxes dictionary have a length of 1?
    if all(len(values[box]) == 1 for box in boxes):
        # If sudoku is solved
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    # we are only concerned with the values contained in the box
    _, box = min((len(values[box]), box) for box in values if len(values[box]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and
    # if one returns a value (not False), return that answer!

    # iterate over each number in the box. Example 5 & 6 from '56'.
    for digit in values[box]:
        # create a shallow copy of the puzzle to test, our puzzle in the UpsideDown
        new_values = values.copy()
        # set the box in question to the experimental digit
        new_values[box] = digit
        # call the function (itself) to see if the Sudoku with this
        # missing test number will solve the puzzle.
        # Remember: when a thing is defined in terms of itself or of its type, it is recursive
        is_solved = search(new_values)
        # if it returns anything other than false, we are solved!
        if is_solved:
            # return the solved puzzle
            return is_solved


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
