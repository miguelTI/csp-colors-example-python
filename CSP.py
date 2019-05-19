# Variables of the CSP
variables = ["state1", "state2", "state3", "state4", "state5", "state6"]

# Possible values for each variable
domain_values = ["red", "green", "blue"]

# Problem specific details
positions = {}
positions["state1"] = [(1, 1), (2, 0), (2, 1), (3, 1)]
positions["state3"] = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)]
positions["state6"] = [(3, 2), (3, 3), (3, 4), (4, 3), (4, 4), (5, 4), (6, 4)]
positions["state5"] = [(0, 4), (1, 4), (1, 5), (2, 4), (2, 5), (2, 6), (3, 5), (3, 6)]
positions["state2"] = [(4, 5), (4, 6)]
positions["state4"] = [(5, 5), (5, 6), (6, 5)]

# Constraints graph
constraints = {}
constraints["state1"] = {"state3", "state6"}
constraints["state2"] = {"state4", "state5", "state6"}
constraints["state3"] = {"state1", "state5", "state6"}
constraints["state4"] = {"state2", "state6"}
constraints["state5"] = {"state2", "state3", "state6"}
constraints["state6"] = {"state1", "state2", "state3", "state4", "state5"}


def check_constraints(assignment, variable, value):
    neighbours = constraints[variable]
    for neighbour in neighbours:
        if neighbour in assignment:
            if assignment[neighbour] == value:
                return False
    return True
