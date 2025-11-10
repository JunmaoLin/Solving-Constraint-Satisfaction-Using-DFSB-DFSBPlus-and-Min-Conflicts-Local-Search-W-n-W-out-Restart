"""
Output:
- On success: each variable’s color (0..K-1), one per line.
- On failure (no solution found after iteration cap): "No answer."
"""

import sys
import random
import time

if len(sys.argv) != 4:
    sys.stderr.write("python minconflicts.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be integer")
    sys.exit(2)

# read input
with open(input_file, 'r') as f:
    first_line = list(map(int, f.readline().split()))
    N, M, K = first_line
    edges = [tuple(map(int, line.split())) for line in f]

# build neighbor graph
neighbors = {i: [] for i in range(N)}
for a, b in edges:
    neighbors[a].append(b)
    neighbors[b].append(a)


def conflicting_vars(assign):
    # return list of variables currently in conflict
    bad = []
    for i in range(N):
        for j in neighbors[i]:
            if assign[i] == assign[j]:
                bad.append(i)
                break
    return bad

def min_conflict_color(var, assign):
    # return color (0..K-1) minimizing conflicts for variable var
    best_color, best_conflicts = assign[var], N + 1
    for c in range(K):
        conflicts = sum(1 for j in neighbors[var] if assign[j] == c)
        if conflicts < best_conflicts:
            best_color, best_conflicts = c, conflicts
    return best_color

def min_conflicts_basic(max_steps=500000):
    assign = [random.randint(0, K - 1) for _ in range(N)]
    for step in range(max_steps):
        bad = conflicting_vars(assign)
        if not bad:
            return assign
        var = random.choice(bad)
        assign[var] = min_conflict_color(var, assign)
    return None


# Min-Conflicts Local Search with Restarts (MCLS-R)
# Used def min_conflicts_basic(max_steps=500000) as a reference
def min_conflicts_restart(max_steps=500000, max_restarts=100):
    totalSteps = 0
    peakMemoryUsage = 0

    # Terminate after max_restarts
    for restart in range(max_restarts):
        assign = [random.randint(0, K - 1) for _ in range(N)]

        # Update peak memory usage after each assignment
        currentMemoryUsage = sys.getsizeof(assign)
        if currentMemoryUsage > peakMemoryUsage:
            peakMemoryUsage = currentMemoryUsage

        # Reference code from min_conflicts_basic
        for step in range(max_steps):
            bad = conflicting_vars(assign)
            if not bad:
                # return assign
                return assign, totalSteps + step, peakMemoryUsage
            var = random.choice(bad)
            assign[var] = min_conflict_color(var, assign)

            # Update peak memory usage after each assignment
            currentMemoryUsage = sys.getsizeof(assign) + sys.getsizeof(bad)
            if currentMemoryUsage > peakMemoryUsage:
                peakMemoryUsage = currentMemoryUsage

        # Total steps after each restart
        totalSteps += max_steps
    return None, totalSteps, peakMemoryUsage  # failed to find solution



# mode 0 MCRS
if mode == 0:
    solution = min_conflicts_basic()
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")

# mode 1 MCRS with restart  You should implement here
else:

    startTime = time.perf_counter()

    solution, totalSteps, peakMemoryUsage = min_conflicts_restart()

    endTime = time.perf_counter()
    elapsedTime = (endTime - startTime) * 1000  # Convert to milliseconds

    print("Time Used (ms): ", elapsedTime)
    print("Total steps taken: ", totalSteps)
    print("Memory Used (bytes): ", peakMemoryUsage)

    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")

        # out.write("Time Used (ms): " + str(elapsedTime) + "\n")
        # out.write("Total steps taken: " + str(totalSteps) + "\n")
        # out.write("Memory Used (bytes): " + str(peakMemoryUsage) + "\n")

    # sys.stderr.write("MODE=1 (MCLS-R) not implemented in this starter. Please implement restart logic. You can comment out this line\n")
