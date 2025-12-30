from copy import deepcopy
from typing import Any
import time

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
# input_file = "puzzles/inputs/day12_v2.txt"


def parse_input(filename):
    """Parse shapes and regions from input file."""
    with open(filename) as f:
        lines = [line.rstrip() for line in f]

    # Parse shapes
    shapes = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and "x" not in line:
            # This is a shape definition
            shape_id = int(line.rstrip(":"))
            shape = []
            i += 1
            while i < len(lines) and lines[i] and "x" not in lines[i] and ":" not in lines[i]:
                shape.append(list(lines[i]))
                i += 1
            shapes[shape_id] = shape
        elif "x" in line and ":" in line:
            # This is a region - break to parse regions
            break
        else:
            i += 1

    # Parse regions
    regions = []
    for j in range(i, len(lines)):
        line = lines[j]
        if "x" in line and ":" in line:
            parts_line = line.split(": ")
            dims = parts_line[0].split("x")
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts_line[1].split()))
            regions.append((width, height, counts))

    return shapes, regions


class Shape:
    """Class representing a shape with its transformations."""

    def __init__(self, grid, id, generate_transforms=True) -> None:
        self.shape_id = id
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.center_row = self.height // 2
        self.transformations: list[Shape] | None = None
        if generate_transforms:
            self.transformations = self.generate_transformations()

    def rotate(self, grid) -> list[list[Any]]:
        """Rotate the shape 90 degrees clockwise."""
        return [list(row) for row in zip(*grid[::-1])]

    def flip(self, grid) -> list[list[Any]]:
        """Flip the shape horizontally."""
        return [row[::-1] for row in grid]

    def generate_transformations(self) -> list["Shape"]:
        """Generate new Shape objects for all unique transformations of the base shape."""
        _transformations = set()
        _current = self.grid
        for _ in range(4):
            _current = self.rotate(_current)
            _transformations.add(tuple(map(tuple, _current)))
            _flipped = self.flip(_current)
            _transformations.add(tuple(map(tuple, _flipped)))
        return [
            Shape(grid=[list(row) for row in t], id=self.shape_id, generate_transforms=False) for t in _transformations
        ]

    def __repr__(self) -> str:
        r = ""
        r += f"Shape(id={self.shape_id}, width={self.width}, height={self.height})"
        for row in self.grid:
            r += "\n" + "".join(row)
        return r

    def print_grid(self) -> None:
        """Print the shape grid."""
        for row in self.grid:
            print("".join(row))
        print()

    def print_grid_with_qty(self, quantity: int) -> None:
        """Print the shape grid with quantity."""
        for idx, row in enumerate(self.grid):
            if idx == self.center_row:
                print("".join(row), end=f"    x {quantity}\n")
            else:
                print("".join(row))
        print()


class Region:
    """Class representing a region to fit shapes into."""

    def __init__(self, width: int, height: int, counts: list[int]) -> None:
        self.width = width
        self.height = height
        self.grid = [["." for _ in range(width)] for _ in range(height)]
        self.shape_list: list[Shape] = []
        self.counts = counts

    def can_place(self, shape: Shape, x: int, y: int) -> bool:
        """Check if a shape can be placed at position (x, y)."""
        for dy in range(shape.height):
            for dx in range(shape.width):
                if shape.grid[dy][dx] == "#":
                    if y + dy >= self.height or x + dx >= self.width or self.grid[y + dy][x + dx] == "#":
                        return False
        return True

    def place(self, shape: Shape, x: int, y: int, marker: str) -> None:
        """Place or remove a shape at position (x, y) with the given marker."""
        for dy in range(shape.height):
            for dx in range(shape.width):
                if shape.grid[dy][dx] == "#":
                    self.grid[y + dy][x + dx] = marker


class SolverLimitExceeded(Exception):
    """Exception raised when solver exceeds time or attempt limits."""

    pass


class Solver:
    """Class to solve the region fitting problem."""

    def __init__(
        self, region: Region, max_attempts: int = 1_000_000, max_runtime: float = 120.0, print_interval: float = 5.0
    ) -> None:
        self.solution_found: bool = False
        self.region: Region = region
        self.shape_list: list[Shape] = deepcopy(region.shape_list)
        self.start_time: float = 0
        self.last_print_time: float = 0
        self.attempt_count: int = 0
        self.max_attempts: int = max_attempts
        self.max_runtime: float = max_runtime
        self.print_interval: float = print_interval
        self.limit_check_interval: int = 100  # Check limits every N attempts for performance

    def solve(self) -> bool:
        """Attempt to solve the region fitting problem."""
        try:
            self.start_time = time.time()
            self.last_print_time = self.start_time
            print(f"  Starting backtracking algorithm for {len(self.shape_list)} shapes...")
            print(f"  Limits: max_attempts={self.max_attempts:,}, max_runtime={self.max_runtime}s")
            self.solution_found = self._backtrack(0)
            elapsed = time.time() - self.start_time
            if self.solution_found:
                print(
                    f"  [SUCCESS] Solution found in {elapsed:.2f} seconds ({self.attempt_count:,} placement attempts)"
                )
            else:
                print(
                    f"  [FAILED] No solution found after {elapsed:.2f} seconds ({self.attempt_count:,} placement attempts)"
                )
            return self.solution_found
        except SolverLimitExceeded:
            elapsed = time.time() - self.start_time
            print(f"  [LIMIT EXCEEDED] Stopped after {elapsed:.2f} seconds ({self.attempt_count:,} placement attempts)")
            return False
        except Exception as e:
            elapsed = time.time() - self.start_time
            print(f"  [ERROR] Solving failed after {elapsed:.2f} seconds: {e}")
            return False

    def _backtrack(self, shape_index: int) -> bool:
        """Backtracking algorithm to place shapes with all transformations."""
        if shape_index >= len(self.shape_list):
            return True  # All shapes placed successfully

        _shape = self.shape_list[shape_index]

        # Try all transformations of this shape
        transformations_to_try = _shape.transformations if _shape.transformations else [_shape]

        for trans_idx, transformation in enumerate(transformations_to_try):
            for y in range(self.region.height):
                for x in range(self.region.width):
                    if self.region.can_place(shape=transformation, x=x, y=y):
                        self.attempt_count += 1

                        # Check limits periodically for performance (not every attempt)
                        if self.attempt_count % self.limit_check_interval == 0:
                            current_time = time.time()
                            elapsed = current_time - self.start_time

                            if self.attempt_count >= self.max_attempts:
                                raise SolverLimitExceeded(f"Max attempts ({self.max_attempts:,}) reached")

                            if elapsed >= self.max_runtime:
                                raise SolverLimitExceeded(f"Max runtime ({self.max_runtime}s) exceeded")

                            # Print status update
                            if current_time - self.last_print_time >= self.print_interval:
                                print(
                                    f"  [{elapsed:.1f}s] Placing shape {shape_index + 1}/{len(self.shape_list)} "
                                    f"(Transform {trans_idx + 1}/{len(transformations_to_try)}, "
                                    f"Pos ({x},{y}), {self.attempt_count:,} attempts)"
                                )
                                self.last_print_time = current_time

                        self.region.place(shape=transformation, x=x, y=y, marker="#")
                        if self._backtrack(shape_index + 1):
                            return True
                        self.region.place(shape=transformation, x=x, y=y, marker=".")  # Backtrack

        return False


if __name__ == "__main__":
    # Solve Part 1
    solvable_count = 0
    shapes, regions = parse_input(input_file)
    # Create Shape objects
    shape_objects = {idx: Shape(shape, idx) for idx, shape in shapes.items()}
    # Create Region objects
    region_objects = [Region(width, height, counts) for width, height, counts in regions]
    # Populate shape_list for each region with the corresponding Shape objects to be placed
    for region in region_objects:
        # region.shape_list = [shape_objects[idx] for idx, count in enumerate(region.counts) if count > 0]
        for idx, count in enumerate(region.counts):
            if count > 0:
                for _ in range(count):
                    region.shape_list.append(shape_objects[idx])

    # Print the current view of shapes and regions
    for idx, shape in shape_objects.items():
        print(f"Shape {idx}:")
        shape.print_grid()

    for idr, region in enumerate(region_objects):
        print(f"Region {idr + 1}: {region.width}x{region.height}, counts: {region.counts}")
        print(f"Region Shapes List: {[shape.shape_id for shape in region.shape_list]}")
        print("Shapes to place:")
        for shape_idx, shape in shape_objects.items():
            if region.counts[shape_idx] > 0:
                shape.print_grid_with_qty(region.counts[shape_idx])

    # Try to solve each region
    unsolvable_regions = []
    for region_idx, region in enumerate(region_objects):
        if region.shape_list:
            print(f"\n{'=' * 70}")
            print(f"Trying to solve Region {region_idx + 1}: {region.width}x{region.height}, counts: {region.counts}")
            print(f"{'=' * 70}")
            solver = Solver(region, max_runtime=30.0, print_interval=10.0, max_attempts=1_000_000)
            if solver.solve():
                solvable_count += 1
                print(f"Region {region_idx + 1} is solvable.\n")
            else:
                unsolvable_regions.append(region_idx + 1)
                print(f"Region {region_idx + 1} is NOT solvable.\n")
        else:
            print(f"Region {region_idx + 1}: {region.width}x{region.height} has no shapes to place.")

    # Print summary
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total regions: {len(region_objects)}")
    print(f"Solvable regions: {solvable_count}")
    print(f"Unsolvable regions: {len(unsolvable_regions)}")
    if unsolvable_regions:
        print(f"\nUnsolvable region numbers: {unsolvable_regions}")
    print(f"{'=' * 70}")
