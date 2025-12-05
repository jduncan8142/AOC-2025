"""
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a
cafeteria on the other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to
put the wreaths up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!"
another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory
management system, they can't figure out which of their ingredients are fresh and which are
spoiled. When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges,
a blank line, and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32

The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all
fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this
example, this is done as follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.

So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available
ingredient IDs are fresh?
"""

"""
--- Part Two ---

The Elves start bringing their spoiled inventory to the trash chute at the 
back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves 
would like to know all of the IDs that the fresh ingredient ID ranges 
consider to be fresh. An ingredient ID is still considered fresh if it is 
in any range.

Now, the second section of the database (the available ingredient IDs) is 
irrelevant. Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18

The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 
11, 12, 13, 14, 15, 16, 17, 18, 19, and 20. So, in this example, the fresh 
ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to 
be fresh according to the fresh ingredient ID ranges?
"""

input_file = "puzzles/inputs/day5.txt"

# Read the input file
with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

# Find the blank line that separates ranges from ingredient IDs
blank_line_idx = lines.index("")

# Parse the fresh ID ranges
ranges = []
for i in range(blank_line_idx):
    start, end = map(int, lines[i].split("-"))
    ranges.append((start, end))

# Parse the available ingredient IDs
ingredient_ids = []
for i in range(blank_line_idx + 1, len(lines)):
    if lines[i]:
        ingredient_ids.append(int(lines[i]))

# Check which ingredient IDs are fresh
fresh_count = 0
for ingredient_id in ingredient_ids:
    is_fresh = False
    for start, end in ranges:
        if start <= ingredient_id <= end:
            is_fresh = True
            break
    if is_fresh:
        fresh_count += 1

print(f"Part 1: Number of fresh ingredient IDs: {fresh_count}")


# Part 2: Count total unique ingredient IDs in all ranges
# Merge overlapping ranges to avoid double-counting
def merge_ranges(ranges):
    """Merge overlapping ranges and return list of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # If current range overlaps with the last merged range, merge them
        if current_start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))

    return merged


# Merge the ranges
merged_ranges = merge_ranges(ranges)

# Count total IDs in merged ranges
total_fresh_ids = 0
for start, end in merged_ranges:
    total_fresh_ids += end - start + 1

print(f"Part 2: Total ingredient IDs considered fresh: {total_fresh_ids}")
