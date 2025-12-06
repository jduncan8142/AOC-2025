"""
--- Day 6: Trash Compactor ---
After helping the Elves in the kitchen, you were taking a break and helping them re-enact a movie scene when you over-enthusiastically jumped into the garbage chute!

A brief fall later, you find yourself in a garbage smasher. Unfortunately, the door's been magnetically sealed.

As you try to find a way out, you are approached by a family of cephalopods! They're pretty sure they can get the door open, but it will take some time. While you wait, they're curious if you can help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math. The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.

However, the problems are arranged a little strangely; they seem to be presented next to each other in a very long horizontal list. For example:

123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

So, this worksheet contains four problems:

123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401
To check their work, cephalopod students are given the grand total of adding together all of the answers to the individual problems. In this worksheet, the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

Of course, the actual worksheet is much wider. You'll need to make sure to unroll it completely so that you can read the problems clearly.

Solve the problems on the math worksheet. What is the grand total found by adding together all of the answers to the individual problems?
"""

"""
--- Part Two ---

The big cephalopods come back to check on how things are going. When they see that your grand total doesn't match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)

Here's the example worksheet again:

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Reading the problems right-to-left one column at a time, the problems are now quite different:

The rightmost problem is 4 + 431 + 623 = 1058
The second problem from the right is 175 * 581 * 32 = 3253600
The third problem from the right is 8 + 248 + 369 = 625
Finally, the leftmost problem is 356 * 24 * 1 = 8544
Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

Solve the problems on the math worksheet again. What is the grand total found by adding together all of the answers to the individual problems?
"""

input_file = "puzzles/inputs/day6.txt"

# Read the input file
with open(input_file, "r") as f:
    lines = [line.rstrip("\n") for line in f.readlines()]

# Find the maximum width to handle all columns
max_width = max(len(line) for line in lines)

# Pad all lines to the same width
for i in range(len(lines)):
    lines[i] = lines[i].ljust(max_width)

# Extract problems column by column
problems = []
col = 0
while col < max_width:
    # Check if this column is a space column (separator)
    is_separator = all(lines[row][col] == " " for row in range(len(lines)))

    if not is_separator:
        # Extract this problem (starting at this column)
        problem_numbers = []
        operation = None

        # Read vertically until we hit the operation or end
        for row in range(len(lines)):
            cell = lines[row][col:].split()[0] if col < len(lines[row]) and lines[row][col] != " " else ""
            if cell in ["+", "*"]:
                operation = cell
                break
            elif cell:
                try:
                    problem_numbers.append(int(cell))
                except ValueError:
                    pass

        if problem_numbers and operation:
            problems.append((problem_numbers, operation))

        # Move to next non-space column
        col += 1
        while col < max_width and all(lines[row][col] == " " for row in range(len(lines))):
            col += 1
    else:
        col += 1

# Actually, let me reparse this properly by identifying problem columns
# A problem column contains numbers and ends with an operation symbol


# Better approach: split by columns of spaces
def extract_problems_from_grid(lines):
    if not lines:
        return []

    max_width = max(len(line) for line in lines)
    # Pad all lines
    padded_lines = [line.ljust(max_width) for line in lines]

    problems = []
    col = 0

    while col < max_width:
        # Skip leading spaces
        while col < max_width and all(padded_lines[row][col] == " " for row in range(len(padded_lines))):
            col += 1

        if col >= max_width:
            break

        # Find the end of this problem column (next full space column or end)
        end_col = col + 1
        while end_col < max_width:
            if all(padded_lines[row][end_col] == " " for row in range(len(padded_lines))):
                break
            end_col += 1

        # Extract the problem from this column range
        problem_text = []
        for row in range(len(padded_lines)):
            cell = padded_lines[row][col:end_col].strip()
            if cell:
                problem_text.append(cell)

        # Parse the problem
        if problem_text:
            operation = problem_text[-1] if problem_text[-1] in ["+", "*"] else None
            if operation:
                numbers = []
                for item in problem_text[:-1]:
                    try:
                        numbers.append(int(item))
                    except ValueError:
                        pass
                if numbers:
                    problems.append((numbers, operation))

        col = end_col

    return problems


problems = extract_problems_from_grid(lines)

# Calculate the result for each problem
grand_total = 0
for numbers, operation in problems:
    if operation == "+":
        result = sum(numbers)
    else:  # operation == '*'
        result = 1
        for num in numbers:
            result *= num
    grand_total += result

print(f"Part 1: Grand total: {grand_total}")


# Part 2: Read numbers as digits in columns, right-to-left
def extract_problems_part2(lines):
    if not lines:
        return []

    max_width = max(len(line) for line in lines)
    # Pad all lines
    padded_lines = [line.ljust(max_width) for line in lines]

    problems = []
    col = 0

    while col < max_width:
        # Skip leading spaces
        while col < max_width and all(padded_lines[row][col] == " " for row in range(len(padded_lines))):
            col += 1

        if col >= max_width:
            break

        # Find the end of this problem column (next full space column or end)
        end_col = col + 1
        while end_col < max_width:
            if all(padded_lines[row][end_col] == " " for row in range(len(padded_lines))):
                break
            end_col += 1

        # Extract the problem from this column range
        # For part 2, we read digit by digit from each column, right-to-left
        problem_numbers = []
        operation = None

        # Process each column in this problem range, from right to left
        for c in range(end_col - 1, col - 1, -1):
            # Read this column top to bottom to form a number
            digits = []
            found_operation = False
            for row in range(len(padded_lines)):
                char = padded_lines[row][c]
                if char in ["+", "*"]:
                    operation = char
                    found_operation = True
                    # Don't break - continue to see if there are digits above
                elif char.isdigit():
                    digits.append(char)
                # Skip spaces within column

            # Add the number if we found digits (even if we also found an operator)
            if digits:
                # Form number from digits (top to bottom)
                number = int("".join(digits))
                problem_numbers.append(number)

            # Stop processing more columns if we found the operator
            if found_operation:
                break

        if problem_numbers and operation:
            problems.append((problem_numbers, operation))

        col = end_col

    return problems


problems_part2 = extract_problems_part2(lines)

# Note: Problems are found left-to-right, but result should be the same
# The key difference is that within each problem, we read columns right-to-left

# Calculate the result for each problem
grand_total_part2 = 0
for numbers, operation in problems_part2:
    if operation == "+":
        result = sum(numbers)
    else:  # operation == '*'
        result = 1
        for num in numbers:
            result *= num
    grand_total_part2 += result

print(f"Part 2: Grand total: {grand_total_part2}")
