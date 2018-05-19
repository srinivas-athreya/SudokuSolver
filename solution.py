
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
FirstDiagonal = [rows[i]+cols[i] for i in range(0,9)]
SecondDiagonal = [rows[8-i]+cols[i] for i in range(0,9)]
diagonal_units = [FirstDiagonal,SecondDiagonal]
unitlist = unitlist + diagonal_units
#print(row_units)

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


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
    # TODO: Implement this function!
    new_values = values
    for each_box in values:
        if len(values[each_box]) == 2:
            peersofbox = peers[each_box]
            stringtoeliminate = ''
            for each_peer in peersofbox:
                if set(values[each_peer]) == set(values[each_box]) and each_box != each_peer: #Naked Twin Found
                    TwinBoxes = (each_peer,each_box)
                    common_units = [a for a in units[each_box] for b in units[each_peer] if a==b]
                    stringtoeliminate = values[each_peer]
                    for each_unit in common_units:
                        for box in each_unit:
                            if box in TwinBoxes:
                                continue
                            else:
                                new_values[box] = ''.join([c for c in values[box] if c not in stringtoeliminate])
                    
    return new_values
    #raise NotImplementedError


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
    # TODO: Copy your code from the classroom to complete this function
    
    new_values = dict()
    for each_box in values:
        if len(values[each_box]) == 1:
            new_values[each_box] = values[each_box]
        #removed continue as suggested by the reviewer    
        peersofbox = peers[each_box]
        stringtoeliminate = ''
        for each_peer in peersofbox:
            if len(values[each_peer]) == 1 and values[each_peer] in values[each_box]:
                stringtoeliminate += values[each_peer]
            new_values[each_box] = ''.join([c for c in values[each_box] if c not in stringtoeliminate])    
    return new_values


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
    # TODO: Copy your code from the classroom to complete this function
    for each_unit in unitlist:
        all_values = [values[each_box] for each_box in each_unit]
        for each_box in each_unit:
            if len(values[each_box]) == 1:
                continue
            else:
                for each_value in values[each_box]:
                    count = 0
                    for i in all_values:
                        if each_value in i:
                            count+=1
                    if count == 1:
                        values[each_box] = each_value
                        break                
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
    # TODO: Copy your code from the classroom and modify it to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    
    raise NotImplementedError


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
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    possible_sols = 9
    solutions = None
    box_id = None
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
        
    for each_box in values:
        if len(values[each_box]) < possible_sols and len(values[each_box])>1:
            possible_sols = len(values[each_box])
            solutions = values[each_box]
            box_id = each_box
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for each_solution in solutions:
        new_sudoku = values.copy()
        new_sudoku[box_id] = each_solution
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    
    #raise NotImplementedError


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
    #print(units['A3'])
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
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
