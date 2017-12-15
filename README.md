# Solve Sudoku with AI

## Synopsis

In this project, I extended the Sudoku-solving agent developed in classroom lectures to solve _diagonal_ Sudoku puzzles. A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

## Quickstart Guide

### Activate the aind environment (OS X or Unix/Linux)
    
    `$ source activate aind`

### Activate the aind environment (Windows)

    `> activate aind`

### Run the code & visualization

    `(aind)$ python solution.py`

### Run the local test suite

    `(aind)$ python -m unittest -v`

### Run the remote test suite & submit the project

    `(aind)$ udacity submit`


## Visualization

**Note:** The `pygame` library is required to visualize your solution -- however, the `pygame` module can be troublesome to install and configure. It should be installed by default with the AIND conda environment, but it is not reliable across all operating systems or versions. Please refer to the pygame documentation [here](http://www.pygame.org/download.shtml), or discuss among your peers in the slack group or discussion forum if you need help.

Running `python solution.py` will automatically attempt to visualize your solution, but you mustuse the provided `assign_value` function (defined in `utils.py`) to track the puzzle solution progress for reconstruction during visuzalization.
