"""
--- Day 11: Reactor ---
You hear some loud beeping coming from a hatch in the floor of the factory, so you decide to check it out. Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping: a large, toroidal reactor which powers the factory above. Some Elves here are hurriedly running between the reactor and a nearby server rack, apparently trying to fix something.

One of the Elves notices you and rushes over. "It's a good thing you're here! We just installed a new server rack, but we aren't having any luck getting the reactor to communicate with it!" You glance around the room and see a tangle of cables and devices running from the server rack to the reactor. She rushes off, returning a moment later with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
Each line gives the name of a device followed by a list of the devices to which its outputs are attached. So, bbb: ddd eee means that device bbb has two outputs, one leading to device ddd and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device, but rather that the issue is triggered by data following some specific path through the devices. Data only ever flows from a device through its outputs; it can't flow backwards.

After dividing up the work, the Elves would like you to focus on the devices starting with the one next to you (an Elf hastily attaches a label which just says you) and ending with the main output to the reactor (which is the device with the label out).

To help the Elves figure out which path is causing the issue, they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

Data could take the connection from you to bbb, then from bbb to ddd, then from ddd to ggg, then from ggg to out.
Data could take the connection to bbb, then to eee, then to out.
Data could go to ccc, then ddd, then ggg, then out.
Data could go to ccc, then eee, then out.
Data could go to ccc, then fff, then out.
In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?
"""

"""
--- Part Two ---
Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out
However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?
"""

input_file_path = "puzzles/inputs/day11.txt"


def parse_graph(filename):
    """Parse the input file and build a directed graph."""
    graph = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ")
            if len(parts) == 2:
                node = parts[0]
                outputs = parts[1].split()
                graph[node] = outputs
    return graph


def count_paths(graph, start, end, memo=None):
    """Count all paths from start to end using DFS with memoization."""
    if memo is None:
        memo = {}

    # Base case: reached the end
    if start == end:
        return 1

    # Check memo
    if start in memo:
        return memo[start]

    # If start node has no outputs, no path to end
    if start not in graph:
        memo[start] = 0
        return 0

    # Count paths through all neighbors
    total_paths = 0
    for neighbor in graph[start]:
        total_paths += count_paths(graph, neighbor, end, memo)

    memo[start] = total_paths
    return total_paths


def count_paths_with_required(graph, start, end, required_nodes):
    """
    Count paths from start to end that visit all required_nodes.
    Uses DFS with state tracking and memoization.
    """
    required_set = set(required_nodes)
    memo = {}

    def dfs(node, visited_required_frozen):
        # Check memo
        state = (node, visited_required_frozen)
        if state in memo:
            return memo[state]

        visited_required = set(visited_required_frozen)

        # Base case: reached the end
        if node == end:
            result = 1 if visited_required == required_set else 0
            memo[state] = result
            return result

        # If node has no outputs, can't reach end
        if node not in graph:
            memo[state] = 0
            return 0

        # Update visited required nodes if current node is required
        new_visited = visited_required.copy()
        if node in required_set:
            new_visited.add(node)

        # Count paths through all neighbors
        total = 0
        new_visited_frozen = frozenset(new_visited)
        for neighbor in graph[node]:
            total += dfs(neighbor, new_visited_frozen)

        memo[state] = total
        return total

    return dfs(start, frozenset())


# Part 1
graph = parse_graph(input_file_path)
paths_part1 = count_paths(graph, "you", "out")
print(f"Part 1: {paths_part1}")

# Part 2
paths_part2 = count_paths_with_required(graph, "svr", "out", ["dac", "fft"])
print(f"Part 2: {paths_part2}")
