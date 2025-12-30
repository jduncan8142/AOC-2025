"""
--- Day 9: Movie Theater ---
You slide down the firepole in the corner of the playground and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid (your puzzle input).

For example:

7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
Showing red tiles as # and other tiles as ., the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............
You can choose any two red tiles as the opposite corners of your rectangle; your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O) with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............
Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............
You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............
Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?
"""

"""
--- Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

Using the same example as before, the tiles marked X would be green:

..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............
In addition, all of the tiles inside this loop of red and green tiles are also green. So, in this example, these are the green tiles:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
The remaining tiles are never red nor green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green. This significantly limits your options.

For example, you could make a rectangle out of red and green tiles with an area of 15 between 7,3 and 11,1:

..............
.......OOOOO..
.......OOOOO..
..#XXXXOOOOO..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXXOXX..
.........OXX..
.........OX#..
..............
The largest rectangle you can make in this example using only red and green tiles has area 24. One way to do this is between 9,5 and 2,3:

..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?
"""

input_file = "puzzles/inputs/day9.txt"


def parse_input(filename):
    """Parse the input file to get list of red tile coordinates."""
    coords = []
    with open(filename) as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            coords.append((x, y))
    return coords


def point_in_polygon(point, polygon):
    """Ray casting algorithm to determine if a point is inside a polygon."""
    x, y = point
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def get_green_edge_tiles(coords):
    """Find green tiles on edges between consecutive red tiles."""
    green_tiles = set()
    for i in range(len(coords)):
        p1 = coords[i]
        p2 = coords[(i + 1) % len(coords)]
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                green_tiles.add((x1, y))
        elif y1 == y2:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                green_tiles.add((x, y1))
    return green_tiles


def is_rectangle_valid_sampled(min_x, max_x, min_y, max_y, coords, red_tiles, green_edge_tiles, cache):
    """Check if rectangle is valid using sampling for large rectangles."""
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    area = width * height

    # For small rectangles, check every tile
    if area <= 10000:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                tile = (x, y)
                if tile in red_tiles or tile in green_edge_tiles:
                    continue
                if tile not in cache:
                    cache[tile] = point_in_polygon(tile, coords)
                if not cache[tile]:
                    return False
        return True

    # For larger rectangles, sample points in a grid (100x100 sampling)
    sample_step = max(width // 100, height // 100, 5)
    for x in range(min_x, max_x + 1, sample_step):
        for y in range(min_y, max_y + 1, sample_step):
            tile = (x, y)
            if tile in red_tiles or tile in green_edge_tiles:
                continue
            if tile not in cache:
                cache[tile] = point_in_polygon(tile, coords)
            if not cache[tile]:
                return False

    # Also check corners
    for x in [min_x, max_x]:
        for y in [min_y, max_y]:
            tile = (x, y)
            if tile in red_tiles or tile in green_edge_tiles:
                continue
            if tile not in cache:
                cache[tile] = point_in_polygon(tile, coords)
            if not cache[tile]:
                return False

    return True


def find_largest_rectangle(coords):
    """Find the largest rectangle using any two red tiles as opposite corners."""
    max_area = 0

    # Try all pairs of coordinates as opposite corners
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            # Calculate area of rectangle with these as opposite corners
            # Area includes all tiles from min to max coordinates (inclusive)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height

            max_area = max(max_area, area)

    return max_area


def find_largest_valid_rectangle(coords, red_tiles, green_edge_tiles):
    """Find largest rectangle using only red and green tiles."""
    cache = {}
    max_area = 0

    # Generate all candidates
    candidates = []
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            candidates.append((area, min_x, max_x, min_y, max_y))

    # Sort by area descending
    candidates.sort(reverse=True)

    # Check candidates starting from largest
    for area, min_x, max_x, min_y, max_y in candidates:
        if area <= max_area:
            break

        if is_rectangle_valid_sampled(min_x, max_x, min_y, max_y, coords, red_tiles, green_edge_tiles, cache):
            max_area = area

    return max_area


# Part 1
coords = parse_input(input_file)
part1 = find_largest_rectangle(coords)
print(f"Part 1: {part1}")

# Part 2
red_tiles = set(coords)
green_edge_tiles = get_green_edge_tiles(coords)
part2 = find_largest_valid_rectangle(coords, red_tiles, green_edge_tiles)
print(f"Part 2: {part2}")
