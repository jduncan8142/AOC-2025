"""
--- Day 10: Factory ---
Just across the hall, you find a large factory. Fortunately, the Elves here have plenty of time to decorate. Unfortunately, it's because the factory machines are all offline, and none of the Elves can figure out the initialization procedure.

The Elves do have the manual for the machines, but the section detailing the initialization procedure was eaten by a Shiba Inu. All that remains of the manual are some indicator light diagrams, button wiring schematics, and joltage requirements for each machine.

For example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets], one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.

To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on. The machine has the number of indicator lights shown, but its indicator lights are all initially off.

So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on, and the fourth to be off.

You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button, each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a negative number of times).

So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would change them to be [...##.] instead.

Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.

You can push each button as many times as you like. However, to save on time, you will need to determine the fewest total presses required to correctly configure all indicator lights for all machines in your list.

There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.
However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons ((0,2) and (0,1)) once each.

The second machine can be configured with as few as 3 button presses:

[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
One way to achieve this is by pressing the last three buttons ((0,4), (0,1,2), and (1,2,3,4)) once each.

The third machine has a total of six indicator lights that need to be configured correctly:

[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The fewest presses required to correctly configure it is 2; one way to do this is by pressing buttons (0,3,4) and (0,1,2,4,5) once each.

So, the fewest button presses required to correctly configure the indicator lights on all of the machines is 2 + 3 + 2 = 7.

Analyze each machine's indicator light diagram and button wiring schematics. What is the fewest button presses required to correctly configure the indicator lights on all of the machines?
"""

"""
--- Part Two ---
All of the machines are starting to come online! Now, it's time to worry about the joltage requirements.

Each machine needs to be configured to exactly the specified joltage levels to function properly. Below the buttons on each machine is a big lever that you can use to switch the buttons from configuring the indicator lights to increasing the joltage levels. (Ignore the indicator light diagrams.)

The machines each have a set of numeric counters tracking its joltage levels, one counter per joltage requirement. The counters are all initially set to zero.

So, joltage requirements like {3,5,4,7} mean that the machine has four counters which are initially 0 and that the goal is to simultaneously configure the first counter to be 3, the second counter to be 5, the third to be 4, and the fourth to be 7.

The button wiring schematics are still relevant: in this new joltage configuration mode, each button now indicates which counters it affects, where 0 means the first counter, 1 means the second counter, and so on. When you push a button, each listed counter is increased by 1.

So, a button wiring schematic like (1,3) means that each time you push that button, the second and fourth counters would each increase by 1. If the current joltage levels were {0,1,2,3}, pushing the button would change them to be {0,2,2,4}.

You can push each button as many times as you like. However, your finger is getting sore from all the button pushing, and so you will need to determine the fewest total presses required to correctly configure each machine's joltage level counters to match the specified joltage requirements.

Consider again the example from before:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
Configuring the first machine's counters requires a minimum of 10 button presses. One way to do this is by pressing (3) once, (1,3) three times, (2,3) three times, (0,2) once, and (0,1) twice.

Configuring the second machine's counters requires a minimum of 12 button presses. One way to do this is by pressing (0,2,3,4) twice, (2,3) five times, and (0,1,2) five times.

Configuring the third machine's counters requires a minimum of 11 button presses. One way to do this is by pressing (0,1,2,3,4) five times, (0,1,2,4,5) five times, and (1,2) once.

So, the fewest button presses required to correctly configure the joltage level counters on all of the machines is 10 + 12 + 11 = 33.

Analyze each machine's joltage requirements and button wiring schematics. What is the fewest button presses required to correctly configure the joltage level counters on all of the machines?
"""

input_file = "puzzles/inputs/day10.txt"


def parse_machine(line):
    """Parse a machine configuration line."""
    # Extract target state from [brackets]
    target_start = line.index("[") + 1
    target_end = line.index("]")
    target_str = line[target_start:target_end]
    target = [1 if c == "#" else 0 for c in target_str]

    # Extract buttons from (parentheses)
    buttons = []
    i = target_end + 1
    while i < len(line):
        if line[i] == "(":
            close = line.index(")", i)
            button_str = line[i + 1 : close]
            if button_str:  # Not empty
                button = [int(x) for x in button_str.split(",")]
                buttons.append(button)
            i = close + 1
        else:
            i += 1

    # Extract joltage requirements from {curly braces}
    joltage = []
    if "{" in line:
        jolt_start = line.index("{") + 1
        jolt_end = line.index("}")
        jolt_str = line[jolt_start:jolt_end]
        joltage = [int(x) for x in jolt_str.split(",")]

    return target, buttons, joltage


def gauss_eliminate_gf2(matrix, target):
    """
    Solve system of linear equations in GF(2) using Gaussian elimination.
    Returns the minimum number of button presses needed.
    """
    num_lights = len(target)
    num_buttons = len(matrix[0]) if matrix else 0

    if num_buttons == 0:
        # No buttons available
        return float("inf") if any(target) else 0

    # Build augmented matrix [A | b] where A is the button matrix and b is the target
    # Each row represents a light, each column represents a button
    aug = []
    for i in range(num_lights):
        row = matrix[i][:] + [target[i]]
        aug.append(row)

    # Gaussian elimination
    pivot_col = []
    current_row = 0

    for col in range(num_buttons):
        # Find pivot
        pivot_row = None
        for row in range(current_row, num_lights):
            if aug[row][col] == 1:
                pivot_row = row
                break

        if pivot_row is None:
            continue  # No pivot in this column, it's a free variable

        # Swap rows
        aug[current_row], aug[pivot_row] = aug[pivot_row], aug[current_row]
        pivot_col.append(col)

        # Eliminate
        for row in range(num_lights):
            if row != current_row and aug[row][col] == 1:
                for c in range(num_buttons + 1):
                    aug[row][c] ^= aug[current_row][c]

        current_row += 1

    # Check for inconsistency
    for row in range(current_row, num_lights):
        if aug[row][num_buttons] == 1:
            return float("inf")  # No solution

    # Back substitution to find solution with minimum button presses
    # Free variables are those not in pivot_col
    free_vars = [i for i in range(num_buttons) if i not in pivot_col]

    # Try all combinations of free variables to find minimum
    min_presses = float("inf")

    for mask in range(1 << len(free_vars)):
        solution = [0] * num_buttons

        # Set free variables
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1

        # Set pivot variables
        for i in range(len(pivot_col) - 1, -1, -1):
            col = pivot_col[i]
            # Find the row for this pivot
            row = i
            val = aug[row][num_buttons]
            for j in range(col + 1, num_buttons):
                val ^= aug[row][j] * solution[j]
            solution[col] = val

        # Count button presses
        presses = sum(solution)
        min_presses = min(min_presses, presses)

    return min_presses


def solve_machine(target, buttons):
    """Find minimum button presses for a machine (Part 1 - GF(2))."""
    num_lights = len(target)
    num_buttons = len(buttons)

    # Build matrix: matrix[light][button] = 1 if button affects light
    matrix = [[0] * num_buttons for _ in range(num_lights)]

    for button_idx, button in enumerate(buttons):
        for light in button:
            if light < num_lights:
                matrix[light][button_idx] = 1

    return gauss_eliminate_gf2(matrix, target)


def solve_joltage(joltage, buttons):
    """Find minimum button presses for joltage counters (Part 2 - integers)."""
    num_counters = len(joltage)
    num_buttons = len(buttons)

    if num_buttons == 0:
        return float('inf') if any(joltage) else 0

    # Build matrix: matrix[counter][button] = 1 if button affects counter
    matrix = [[0] * num_buttons for _ in range(num_counters)]

    for button_idx, button in enumerate(buttons):
        for counter in button:
            if counter < num_counters:
                matrix[counter][button_idx] = 1

    # Gaussian elimination (over integers, not GF(2))
    aug = []
    for i in range(num_counters):
        row = matrix[i][:] + [joltage[i]]
        aug.append(row[:])  # Make a copy

    # Forward elimination
    pivot_col = []
    current_row = 0

    for col in range(num_buttons):
        # Find pivot
        pivot_row = None
        for row in range(current_row, num_counters):
            if aug[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows
        aug[current_row], aug[pivot_row] = aug[pivot_row], aug[current_row]
        pivot_col.append(col)

        # Eliminate
        pivot_val = aug[current_row][col]
        for row in range(num_counters):
            if row != current_row and aug[row][col] != 0:
                factor = aug[row][col] / pivot_val
                for c in range(num_buttons + 1):
                    aug[row][c] -= factor * aug[current_row][c]

        current_row += 1

    # Check for inconsistency
    for row in range(current_row, num_counters):
        if abs(aug[row][num_buttons]) > 1e-9:
            return float('inf')

    # Find minimum over all valid free variable combinations
    free_vars = [i for i in range(num_buttons) if i not in pivot_col]

    # Try different combinations of free variables
    # Search up to a reasonable limit for each free variable
    min_presses = float('inf')
    max_free_val = max(joltage) if joltage else 0  # Upper bound for free variables

    def try_free_vars(free_idx, current_free_vals):
        nonlocal min_presses

        if free_idx == len(free_vars):
            # All free variables assigned, solve for pivot variables
            solution = [0] * num_buttons

            # Set free variables
            for i, var in enumerate(free_vars):
                solution[var] = current_free_vals[i]

            # Solve for pivot variables
            valid = True
            for i in range(len(pivot_col) - 1, -1, -1):
                col = pivot_col[i]
                row = i
                val = aug[row][num_buttons]
                for j in range(col + 1, num_buttons):
                    val -= aug[row][j] * solution[j]
                val = val / aug[row][col]

                # Check if valid (non-negative integer)
                if val < -1e-9 or abs(val - round(val)) > 1e-9:
                    valid = False
                    break
                solution[col] = round(val)
                if solution[col] < 0:
                    valid = False
                    break

            if valid:
                total = sum(solution)
                min_presses = min(min_presses, total)
            return

        # Try values for current free variable
        for val in range(max_free_val + 1):
            if sum(current_free_vals) + val + (len(free_vars) - free_idx - 1) * 0 >= min_presses:
                break  # Pruning: already too many presses
            try_free_vars(free_idx + 1, current_free_vals + [val])

    if len(free_vars) <= 5:  # Only do exhaustive search if few free variables
        try_free_vars(0, [])
    else:
        # Too many free variables, just try setting them to 0
        solution = [0] * num_buttons
        for i in range(len(pivot_col) - 1, -1, -1):
            col = pivot_col[i]
            row = i
            val = aug[row][num_buttons]
            for j in range(col + 1, num_buttons):
                val -= aug[row][j] * solution[j]
            solution[col] = val / aug[row][col]

        if all(s >= -1e-9 and abs(s - round(s)) < 1e-9 for s in solution):
            solution = [round(s) for s in solution]
            if all(s >= 0 for s in solution):
                min_presses = sum(solution)

    return min_presses


# Solve both parts
with open(input_file) as f:
    lines = f.readlines()

total_presses_part1 = 0
total_presses_part2 = 0

for line in lines:
    line = line.strip()
    if not line:
        continue

    target, buttons, joltage = parse_machine(line)

    # Part 1: Toggle lights (GF(2))
    min_presses_p1 = solve_machine(target, buttons)
    if min_presses_p1 != float("inf"):
        total_presses_part1 += min_presses_p1

    # Part 2: Increment counters (integers)
    min_presses_p2 = solve_joltage(joltage, buttons)
    if min_presses_p2 != float("inf"):
        total_presses_part2 += min_presses_p2

print(f"Part 1: {total_presses_part1}")
print(f"Part 2: {total_presses_part2}")
