'''
Created on Jan 19, 2016

@author: Miranda Motsinger

I have tested this code with the given test cases and it passes all of them.
I understand that misrepresenting passing test cases is an academic
integrity violation.

Usage Example
% python cb.py 011011000000000
[5->0][0->3][3->5]
[1->8][2->9][9->7]
[2->9][1->8][9->7]
[5->3][3->0][0->5]

Description
Evaluates a Cracker Barrel puzzle given an initial configuration of
peg positions, mapped as follows:

       0
     1   2
    3  4  5
   6  7  8  9
 10 11 12 13 14
 
 Given the positions, this program recursively finds and prints all possible
 solutions line-by-line. Solutions are shown as the series of jumps required
 to reach the final desired single-peg state.
'''

import sys

# Hardcoded list of tuples representing all possible jump paths.
# Indexes represent outer, inner, and outer respectively. Source and destination
# are not differentiated here.
paths = [[0, 1, 3], [0, 2, 5], [1, 3, 6], [1, 4, 8], [2, 4, 7], [2, 5, 9],
         [3, 4, 5], [3, 6, 10], [3, 7, 12], [4, 7, 11], [4, 8, 13], [5, 8, 12],
         [5, 9, 14], [6, 7, 8], [7, 8, 9], [10, 11, 12], [11, 12, 13],
         [12, 13, 14]]


# A path can be jumped if its inner hole has a peg and if either but not
# both outer holes have a peg.
def canJump(holes, path):
    return holes[path[1]] and (holes[path[0]] ^ holes[path[2]])


# Reverses peg status of all holes in a path. Handily serves as both a jump
# and an undo of a previous jump, assuming it's only called on a valid path.
def jumpOrUndo(holes, path):
    holes[path[0]] = not holes[path[0]]
    holes[path[1]] = not holes[path[1]]
    holes[path[2]] = not holes[path[2]]


# Board is solved if one or fewer pegs remains.
def solved(holes):
    return sum(holes) <= 1


# Creates solution string by iterating along moveList.
def printSolution(moveList):
    s = ""
    for source, dest in moveList:
        s += "[" + str(source) + "->" + str(dest) + "]"

    print(s)


# Recursive solve function. holes is the list of holes (board state) and
# moveList stores the indexes of sources and targets in previously-done jumps.
def solve(holes, moveList=[]):

    # Base (solution) case
    if solved(holes):
        printSolution(moveList)
        return

    # Tries each path one at a time until a legal jump is found.
    for path in paths:
        if canJump(holes, path):

            # Need to find which hole is the source and which the destination
            # by checking peg location.
            if holes[path[0]]:
                moveList.append([path[0], path[2]])
            else:
                moveList.append([path[2], path[0]])

            # Do the jump, recurse with new board.
            jumpOrUndo(holes, path)
            solve(holes, moveList)

            # Reaching this code indicates backtracking. Undo previous move.
            jumpOrUndo(holes, path)
            moveList.pop()


def main(argv):
    # Reads in board state as a string and populates list holes w/its contents.
    board = argv[1]

    # Holes is a list of boolean values which represent whether the hole at that
    # index has a peg (True) or doesn't (False).
    holes = []

    # Populate holes, changing char representations of peg state into booleans.
    for hole in board:
        if hole == '1':
            holes.append(True)
        elif hole == '0':
            holes.append(False)

    solve(holes)


if __name__ == "__main__":
    main(sys.argv)