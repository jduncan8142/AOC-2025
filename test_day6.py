test_lines = ["123 328  51 64 ", " 45 64  387 23 ", "  6 98  215 314", "*   +   *   +  "]

# Part 2 logic
max_width = max(len(line) for line in test_lines)
padded_lines = [line.ljust(max_width) for line in test_lines]

print("Padded lines:")
for i, line in enumerate(padded_lines):
    print(f"Row {i}: '{line}' (len={len(line)})")

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

    print(f"\nProblem from col {col} to {end_col - 1}")

    # Extract the problem from this column range
    problem_numbers = []
    operation = None

    # Process each column in this problem range, from right to left
    for c in range(end_col - 1, col - 1, -1):
        print(f"  Column {c}:", end=" ")
        # Read this column top to bottom to form a number
        digits = []
        found_operation = False
        for row in range(len(padded_lines)):
            char = padded_lines[row][c]
            print(f"'{char}'", end="")
            if char in ["+", "*"]:
                operation = char
                found_operation = True
                # Don't break - continue reading
            elif char.isdigit():
                digits.append(char)

        print()

        if digits:
            # Form number from digits (top to bottom)
            number = int("".join(digits))
            print(f"    -> number: {number}")
            problem_numbers.append(number)

        if found_operation:
            print(f"    -> operator: {operation}")
            break

    if problem_numbers and operation:
        problems.append((problem_numbers, operation))
        print(f"  Problem: {' {operation} '.join(map(str, problem_numbers))} = ", end="")
        if operation == "+":
            result = sum(problem_numbers)
        else:
            result = 1
            for num in problem_numbers:
                result *= num
        print(result)

    col = end_col

print("\nExpected:")
print("The rightmost problem is 4 + 431 + 623 = 1058")
print("The second problem from the right is 175 * 581 * 32 = 3253600")
print("The third problem from the right is 8 + 248 + 369 = 625")
print("Finally, the leftmost problem is 356 * 24 * 1 = 8544")
print("Grand total: 3263827")
