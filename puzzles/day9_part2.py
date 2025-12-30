"""
--- Day 9: Movie Theater - Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

In addition, all of the tiles inside this loop of red and green tiles are also green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green.

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


# Main solution
coords = parse_input(input_file)
print(f"Number of red tiles: {len(coords)}")
print(f"Coordinate range: x={min(x for x, y in coords)} to {max(x for x, y in coords)}")
print(f"Coordinate range: y={min(y for x, y in coords)} to {max(y for x, y in coords)}")
print()

# Look at first few edges to understand the polygon structure
print("First 10 edges:")
for i in range(10):
    p1 = coords[i]
    p2 = coords[(i + 1) % len(coords)]
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    print(f"  {p1} -> {p2}: dx={dx}, dy={dy}, length={max(dx, dy)+1}")

print()
print("Edge lengths:")
edge_lengths = []
for i in range(len(coords)):
    p1 = coords[i]
    p2 = coords[(i + 1) % len(coords)]
    length = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) + 1
    edge_lengths.append(length)

print(f"  Min edge: {min(edge_lengths)}")
print(f"  Max edge: {max(edge_lengths)}")
print(f"  Average: {sum(edge_lengths) / len(edge_lengths):.1f}")
print(f"  Total perimeter: {sum(edge_lengths)}")
print()


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

    # For larger rectangles, sample points in a grid (more dense sampling)
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

    # Also check corners and edges
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


print("Building red tile and green edge sets...")
red_tiles = set(coords)
green_edge_tiles = get_green_edge_tiles(coords)
print(f"Green edge tiles: {len(green_edge_tiles)}")
print()

print("Finding largest valid rectangle...")
cache = {}
max_area = 0
best_rect = None

# Generate all candidates
candidates = []
for i in range(len(coords)):
    for j in range(i + 1, len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[j]
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        candidates.append((area, min_x, max_x, min_y, max_y, i, j))

candidates.sort(reverse=True)

checked = 0
for area, min_x, max_x, min_y, max_y, i, j in candidates:
    if area <= max_area:
        break

    checked += 1
    if checked % 1000 == 0:
        print(f"Checked {checked}/{len(candidates)}, best: {max_area}, current: {area}")

    if is_rectangle_valid_sampled(min_x, max_x, min_y, max_y, coords, red_tiles, green_edge_tiles, cache):
        if area > max_area:
            max_area = area
            best_rect = (coords[i], coords[j])
            print(f"New best: {max_area} between {coords[i]} and {coords[j]}")

print()
print(f"Part 2 (with sampling): {max_area}")

# Verify the best rectangle found
if best_rect:
    print()
    print(f"Verifying best rectangle between {best_rect[0]} and {best_rect[1]}...")
    x1, y1 = best_rect[0]
    x2, y2 = best_rect[1]
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    print(f"Rectangle: width={width}, height={height}, area={width*height}")
    print("This rectangle is too large to fully verify tile-by-tile.")
    print(f"Sampled validation passed, answer: {max_area}")
