import sys
import time

statesExplored = 0
peakMemoryUsage = 0

"""
Output:
- On success: writes the color for each variable (0..K-1), one per line.
- On failure (no solution found): "No answer."

"""
if len(sys.argv) != 4:
    sys.stderr.write(" python dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be an integer")
    sys.exit(2)


# problem definition
no_of_variables = None
no_of_constraints = None
no_of_colors = None
constraints = []  # list of [a, b] pairs

with open(input_file, 'r') as f:
    first = f.readline().split()
    no_of_variables = int(first[0])
    no_of_constraints = int(first[1])
    no_of_colors = int(first[2])
    for line in f:
        a, b = map(int, line.split())
        constraints.append((a, b))

# using dictionary for faster lookup for neighbors and constraints
# inspiration from minconflicts.py
# Ex: {
        # 0: {1},
        # 1: {0, 2},
        # 2: {1},
        # 3: {4},
        # 4: {3}
#   }
neighbors = {i: set() for i in range(no_of_variables)}
for a, b in constraints:
    neighbors[a].add(b)
    neighbors[b].add(a)

# DFS-B (backtracking)
# Ultimately, you need check for if assigning val to var breaks any constraints-------
def consistent(var, val, assignment):
    # Check if assigning var=val is consistent with current partial assignment
    # Only check constraints where both ends are assigned (including the proposed var)
    for (a, b) in constraints:
        x = assignment.get(a, None) if a != var else val
        y = assignment.get(b, None) if b != var else val
        if x is not None and y is not None and x == y:
            return False
    return True

def dfs_backtrack(assignment):
    # recursive backtracking on variables in index order (0..N-1)
    if len(assignment) == no_of_variables:
        return assignment
    var = len(assignment)  # next variable by index order
    for val in range(no_of_colors):
        if consistent(var, val, assignment):
            assignment[var] = val
            res = dfs_backtrack(assignment)
            if res is not None:
                return res
            # backtrack
            del assignment[var]
    return None

# Functions for DFS-B++ : variable ordering, value order, and forward-checking -------------

# Variable Ordering - Most Constrained Variable
def mostConstrainedVariable(assignment, domains):
    # Find the variable with the least remaining values in its domain

    # Get a list of unassigned variables
    unassignedVars = []
    for var in range(no_of_variables):
        if var not in assignment:
            unassignedVars.append(var)
    # If there are no unassigned variables left
    if not unassignedVars:
        return None
    
    # Select variable with the smallest domain
    mcv = unassignedVars[0]
    smallestDomainSize = len(domains[unassignedVars[0]])
    for var in unassignedVars:
        if len(domains[var]) < smallestDomainSize:
            smallestDomainSize = len(domains[var])
            mcv = var
    return mcv

# Value Ordering - Least Constraining Value (LCV)
def leastConstrainingValue(var, assignment, domains):
    # Find the value that has the least impact on the domains of neighboring variables
    counts = []
    for val in domains[var]:
        # Ex: if var=0, val=0,1,2
        numOfConstraints = 0

        # Check neighbor variables

        # for (a, b) in constraints:
        #     # Ex:(a=0, b=1)
        #     neighbor = None
        #     # If neighbor is unassigned and has val in its domain, it will be constrained
        #     if (a == var and b not in assignment):
        #         neighbor = b
        #     elif (b == var and a not in assignment):
        #         neighbor = a
        #     # If neighbor exists and val is in its domain, increment count
        #     if (neighbor is not None and val in domains[neighbor]):
        #         numOfConstraints += 1
        # counts.append((val, numOfConstraints))

        # Reprogrammed for faster lookup using neighbors dictionary
        for neighbor in neighbors[var]:
            if neighbor not in assignment and val in domains[neighbor]:
                numOfConstraints += 1
        counts.append((val, numOfConstraints))

    # Sort the values based on the second index (number of constraints imposed)
    # Ex: [(0,2), (1,1), (2,3)]  --> [(1,1), (0,2), (2,3)]
    counts.sort(key=lambda value: value[1])
    # Return the ordered values based on least constraining value
    valueOrdering = []
    for val, numOfConstraints in counts:
        valueOrdering.append(val)
    return valueOrdering

# Forward Checking
# Idea: When a variable is assigned a value Prune incompatible values from its neighbors
# Implemented based on lecture slide constraint-satisfaction-part-IIa-b
def forwardChecking(xi, a, assignment, domains):
    # xi = variable, a = assigned value

    # Create a copy of current domains to restore for backtracking
    copyOfDomains = {v: list(domains[v]) for v in domains}

    # For all neighbors xj of xi
    for (x1, x2) in constraints:
        xj = None
        if x1 == xi and x2 not in assignment:
            xj = x2
        elif x2 == xi and x1 not in assignment:
            xj = x1
        # For all G in domain(xj)
        if xj is not None:
            for g in list(domains[xj]):
                # if xi=a and xj=b is incompatible, remove G from domain(xj)
                if g == a:  # neighbor cannot have same value
                    domains[xj].remove(g)
                    # if domain of xj is empty, then there is no available value
                    if len(domains[xj]) == 0:
                        return None  
    return copyOfDomains

# Using def dfs_backtrack(assignment) as reference
def dfs_backtrack_plus_plus(assignment, domains):
    global statesExplored
    statesExplored += 1 # Count the number of states explored

    updatePeakMemoryUsage(assignment, domains) # for finding peak memory usage, may affect time used

    if len(assignment) == no_of_variables:
        return assignment
    # var = len(assignment)  # next variable by index order
    var = mostConstrainedVariable(assignment, domains) # next variable by most constrained variable
    if var is None:
        return None
    
    # for val in range(no_of_colors):
    #     if consistent(var, val, assignment):
    #         assignment[var] = val
    #         res = dfs_backtrack(assignment)
    #         if res is not None:
    #             return res
    #         # backtrack
    #         del assignment[var]

    for val in leastConstrainingValue(var, assignment, domains):
        if consistent(var, val, assignment):
            assignment[var] = val

            # Forward Checking to prune domains of neighbors
            copyOfDomains = forwardChecking(var, val, assignment, domains)
            if copyOfDomains is not None:  # no dead ends
                result = dfs_backtrack_plus_plus(assignment, domains)
                if result is not None:
                    return result
                
            # Backtrack: restore domains and remove assignment
            if copyOfDomains is not None:
                for variable in domains:
                    domains[variable] = copyOfDomains[variable]
            del assignment[var]
    return None
# End of functions for DFS-B++ ------------------------------------------------------------

# Memory Tracking -------------------------------------------------------------------------
def updatePeakMemoryUsage(assignment, domains):
    global peakMemoryUsage
    currentMemory = sys.getsizeof(assignment) + sys.getsizeof(domains)
    
    for val in assignment.values():
        currentMemory += sys.getsizeof(val)
    for domain_list in domains.values():
        currentMemory += sys.getsizeof(domain_list)
        for val in domain_list:
            currentMemory += sys.getsizeof(val)
    
    if currentMemory > peakMemoryUsage:
        peakMemoryUsage = currentMemory

# End of Memory Tracking ------------------------------------------------------------------

# mode 0 dfsb
if mode == 0:
    solution = dfs_backtrack({})
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")

# mode 1 dfsb++  You should implement here
else:
    # Initialize domains for each variable (0..K-1)
    # Ex: 0: [0, 1, 2],  
    #     1: [0, 1, 2],  
    #     2: [0, 1, 2]  
    domains = {}
    for i in range(no_of_variables):
        domains[i] = list(range(no_of_colors))

    # "Use time.perf counter() for high-precision time measurement in milliseconds." From assignment PDF
    startTime = time.perf_counter()
    peakMemoryUsage = 0
    statesExplored = 0

    solution = dfs_backtrack_plus_plus({}, domains)

    # Calculate time used in milliseconds
    endTime = time.perf_counter()
    elapsedTime = (endTime - startTime) * 1000  # Convert to milliseconds

    print("States Explored: ", statesExplored)
    print("Time Used (ms): ", elapsedTime) # calculating peak memory usage may effect time used
    print("Memory Used (bytes): ", peakMemoryUsage)

    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")

        # out.write("States Explored: " + str(statesExplored) + "\n")
        # out.write("Time Used (ms): " + str(elapsedTime) + "\n") # calculating peak memory usage may effect time used
        # out.write("Memory Used (bytes): " + str(peakMemoryUsage) + "\n")

    # sys.stderr.write("MODE=1 (DFS-B++) is intentionally not included in this starter. Please implement it. You can comment out this line\n")
