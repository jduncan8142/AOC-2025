"""
--- Day 12: Christmas Tree Farm ---
You're almost out of time, but there can't be much left to decorate. Although there are no stairs, elevators, escalators, tunnels, chutes, teleporters, firepoles, or conduits here that would take you deeper into the North Pole base, there is a ventilation duct. You jump in.

After bumping around for a few minutes, you emerge into a large, well-lit cavern full of Christmas trees!

There are a few Elves here frantically decorating before the deadline. They think they'll be able to finish most of the work, but the one thing they're worried about is the presents for all the young Elves that live here at the North Pole. It's an ancient tradition to put the presents under the trees, but the Elves are worried they won't fit.

The presents come in a few standard but very weird shapes. The shapes and the regions into which they need to fit are all measured in standard units. To be aesthetically pleasing, the presents need to be placed into the regions in a way that follows a standardized two-dimensional unit grid; you also can't stack presents.

As always, the Elves have a summary of the situation (your puzzle input) for you. First, it contains a list of the presents' shapes. Second, it contains the size of the region under each tree and a list of the number of presents of each shape that need to fit into that region. For example:

0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
The first section lists the standard present shapes. For convenience, each shape starts with its index and a colon; then, the shape is displayed visually, where # is part of the shape and . is not.

The second section lists the regions under the trees. Each line starts with the width and length of the region; 12x5 means the region is 12 units wide and 5 units long. The rest of the line describes the presents that need to fit into that region by listing the quantity of each shape of present; 1 0 1 0 3 2 means you need to fit one present with shape index 0, no presents with shape index 1, one present with shape index 2, no presents with shape index 3, three presents with shape index 4, and two presents with shape index 5.

Presents can be rotated and flipped as necessary to make them fit in the available space, but they have to always be placed perfectly on the grid. Shapes can't overlap (that is, the # part from two different presents can't go in the same place on the grid), but they can fit together (that is, the . part in a present's shape's diagram does not block another present from occupying that space on the grid).

The Elves need to know how many of the regions can fit the presents listed. In the above example, there are six unique present shapes and three regions that need checking.

The first region is 4x4:

....
....
....
....
In it, you need to determine whether you could fit two presents that have shape index 4:

###
#..
###
After some experimentation, it turns out that you can fit both presents in this region. Here is one way to do it, using A to represent one present and B to represent the other:

AAA.
ABAB
ABAB
.BBB
The second region, 12x5: 1 0 1 0 2 2, is 12 units wide and 5 units long. In that region, you need to try to fit one present with shape index 0, one present with shape index 2, two presents with shape index 4, and two presents with shape index 5.

It turns out that these presents can all fit in this region. Here is one way to do it, again using different capital letters to represent all the required presents:

....AAAFFE.E
.BBBAAFFFEEE
DDDBAAFFCECE
DBBB....CCC.
DDD.....C.C.
The third region, 12x5: 1 0 1 0 3 2, is the same size as the previous region; the only difference is that this region needs to fit one additional present with shape index 4. Unfortunately, no matter how hard you try, there is no way to fit all of the presents into this region.

So, in this example, 2 regions can fit all of their listed presents.

Consider the regions beneath each tree and the presents the Elves would like to fit into each of them. How many of the regions can fit all of the presents listed?
"""

"""
--- Part Two ---
"""

input_file = "puzzles/inputs/day12.txt"


def parse_input(filename):
    """Parse shapes and regions from input file."""
    with open(filename) as f:
        lines = [line.rstrip() for line in f]

    # Parse shapes
    shapes = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' in line and 'x' not in line:
            # This is a shape definition
            shape_id = int(line.rstrip(':'))
            shape = []
            i += 1
            while i < len(lines) and lines[i] and 'x' not in lines[i] and ':' not in lines[i]:
                shape.append(list(lines[i]))
                i += 1
            shapes[shape_id] = shape
        elif 'x' in line and ':' in line:
            # This is a region - break to parse regions
            break
        else:
            i += 1

    # Parse regions
    regions = []
    for j in range(i, len(lines)):
        line = lines[j]
        if 'x' in line and ':' in line:
            parts_line = line.split(': ')
            dims = parts_line[0].split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts_line[1].split()))
            regions.append((width, height, counts))

    return shapes, regions


def get_shape_coords(shape):
    """Get list of (row, col) coordinates where shape has '#'."""
    coords = []
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell == '#':
                coords.append((r, c))
    return coords


def normalize_coords(coords):
    """Normalize coordinates to start at (0, 0)."""
    if not coords:
        return []
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return sorted([(r - min_r, c - min_c) for r, c in coords])


def rotate_90(coords):
    """Rotate coordinates 90 degrees clockwise."""
    return normalize_coords([(c, -r) for r, c in coords])


def flip_horizontal(coords):
    """Flip coordinates horizontally."""
    return normalize_coords([(r, -c) for r, c in coords])


def get_all_orientations(shape):
    """Get all unique orientations (rotations and flips) of a shape."""
    coords = get_shape_coords(shape)
    coords = normalize_coords(coords)

    orientations = set()
    current = coords

    # Try all 4 rotations
    for _ in range(4):
        orientations.add(tuple(current))
        current = rotate_90(current)

    # Flip and try all 4 rotations
    current = flip_horizontal(coords)
    for _ in range(4):
        orientations.add(tuple(current))
        current = rotate_90(current)

    return [list(o) for o in orientations]


def can_place(grid, coords, r_offset, c_offset):
    """Check if shape can be placed at given offset."""
    height, width = len(grid), len(grid[0])
    for r, c in coords:
        nr, nc = r + r_offset, c + c_offset
        if nr < 0 or nr >= height or nc < 0 or nc >= width:
            return False
        if grid[nr][nc] != '.':
            return False
    return True


def place_shape(grid, coords, r_offset, c_offset, marker):
    """Place shape on grid with given marker."""
    for r, c in coords:
        grid[r + r_offset][c + c_offset] = marker


def remove_shape(grid, coords, r_offset, c_offset):
    """Remove shape from grid."""
    for r, c in coords:
        grid[r + r_offset][c + c_offset] = '.'


def get_shape_size(shape):
    """Get the number of filled cells in a shape."""
    return sum(1 for row in shape for cell in row if cell == '#')


def solve_region(width, height, shapes, counts):
    """Try to fit all required presents into the region using backtracking."""
    # Quick check: do we have enough space?
    total_cells_needed = sum(get_shape_size(shapes[i]) * counts[i] for i in range(len(counts)))
    if total_cells_needed > width * height:
        return False

    grid = [['.' for _ in range(width)] for _ in range(height)]

    # Build list of presents to place, sorted by size (largest first for better pruning)
    presents = []
    for shape_id, count in enumerate(counts):
        for _ in range(count):
            presents.append((get_shape_size(shapes[shape_id]), shape_id))

    presents.sort(reverse=True)  # Place larger pieces first
    presents = [shape_id for _, shape_id in presents]

    # Precompute all orientations for each shape
    all_orientations = {}
    for shape_id in shapes:
        all_orientations[shape_id] = get_all_orientations(shapes[shape_id])

    def backtrack(present_idx):
        if present_idx == len(presents):
            return True  # All presents placed successfully

        shape_id = presents[present_idx]
        orientations = all_orientations[shape_id]

        # Find the first empty cell - we'll try to place pieces covering this cell
        first_empty_r, first_empty_c = None, None
        for r in range(height):
            for c in range(width):
                if grid[r][c] == '.':
                    first_empty_r, first_empty_c = r, c
                    break
            if first_empty_r is not None:
                break

        if first_empty_r is None:
            # No empty cell but more presents to place
            return False

        # Try each orientation
        for coords in orientations:
            # Only try placements that would cover the first empty cell
            # This dramatically reduces the search space
            for dr, dc in coords:
                r_offset = first_empty_r - dr
                c_offset = first_empty_c - dc
                if can_place(grid, coords, r_offset, c_offset):
                    place_shape(grid, coords, r_offset, c_offset, str(present_idx))
                    if backtrack(present_idx + 1):
                        return True
                    remove_shape(grid, coords, r_offset, c_offset)

        return False

    return backtrack(0)


# Solve Part 1
shapes, regions = parse_input(input_file)

solvable_count = 0
for idx, (width, height, counts) in enumerate(regions):
    if (idx + 1) % 100 == 0:
        print(f"Progress: {idx+1}/{len(regions)}, solvable so far: {solvable_count}", flush=True)
    if solve_region(width, height, shapes, counts):
        solvable_count += 1

print(f"Part 1: {solvable_count}")
