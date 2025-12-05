"""
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for
Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer
in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way
to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're
pretty sure there's a cafeteria on the other side of the back wall. If we could break through the
wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those
big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to
break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful
diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the
eight adjacent positions. If you can figure out which rolls of paper the forklifts can access,
they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Consider your complete diagram of the paper roll locations. How many rolls of paper can be
accessed by a forklift?
"""

"""
--- Part Two ---

Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper 
is removed, the forklifts might be able to access more rolls of paper, which they might also be 
able to remove. How many total rolls of paper could the Elves remove if they keep repeating 
this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper 
as possible, using highlighted @ to indicate that a roll of paper is about to be removed, and 
using x to indicate that a roll of paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 
rolls of paper can be removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves 
and their forklifts?
"""

input_file = "puzzles/inputs/day4.txt"

# Read the input file
with open(input_file, "r") as f:
    grid = [line.strip() for line in f.readlines()]

rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0


# Part 1: Count rolls that can be accessed (fewer than 4 adjacent rolls)
def count_adjacent_rolls(grid, row, col):
    """Count the number of rolls (@) in the 8 adjacent positions."""
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == "@":
                    count += 1
    return count


accessible_rolls = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "@":
            adjacent = count_adjacent_rolls(grid, r, c)
            if adjacent < 4:
                accessible_rolls += 1

print(f"Part 1: Number of rolls that can be accessed: {accessible_rolls}")


# Part 2: Simulate removing accessible rolls repeatedly
def find_accessible_rolls(grid):
    """Find all rolls that can currently be accessed."""
    accessible = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "@":
                adjacent = count_adjacent_rolls(grid, r, c)
                if adjacent < 4:
                    accessible.append((r, c))
    return accessible


# Create a mutable copy of the grid
grid_copy = [list(row) for row in grid]
total_removed = 0

while True:
    accessible = find_accessible_rolls(grid_copy)
    if not accessible:
        break

    # Remove all accessible rolls
    for r, c in accessible:
        grid_copy[r][c] = "."

    total_removed += len(accessible)

print(f"Part 2: Total rolls that can be removed: {total_removed}")
