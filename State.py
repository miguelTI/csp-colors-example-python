import CSP
import collections
import numpy as np
import copy


class State:
    def __init__(self, assignment = None, possible_values = None, variable = None, value = None):
        if assignment is None:
            self.assignment = self.get_initial_state()
            self.possible_values = collections.OrderedDict()
            for variable in CSP.variables:
                self.possible_values[variable] = copy.deepcopy(CSP.domain_values)
        else:
            assignment1 = copy.deepcopy(assignment)
            assignment1[variable] = value
            self.assignment = assignment1

            possible_values1 = copy.deepcopy(possible_values)
            possible_values1[variable] = [value]

            for neighbour in CSP.constraints[variable]:
                if neighbour not in self.assignment:
                    if value in possible_values1[neighbour]:
                        possible_values1[neighbour].remove(value)

            self.possible_values = possible_values1

    def get_initial_state(self):
        return collections.OrderedDict()

    def find_possible_values_count(self, variable):
        count = 0
        for value in CSP.domain_values:
            if CSP.check_constraints(self.assignment, variable, value):
                count += 1
        return count

    def find_constraints_count(self, variable):
        count = 0
        for neighbour in CSP.constraints[variable]:
            if neighbour not in self.assignment:
                count += 1
        return count

    def select_unassignet_variable(self):
        remaining_values = {}
        for variable in CSP.variables:
            if variable not in self.assignment:
                remaining_values[variable] = self.find_possible_values_count(variable)

        min_val = min(remaining_values.itervalues())
        min_variables = [k for k, v in remaining_values.iteritems() if v == min_val]

        print "Remaining values", remaining_values
        print "Min Variables", min_variables

        if len(min_variables) > 0:
            constraint_counts = {}
            for variable in min_variables:
                constraint_counts[variable] = self.find_constraints_count(variable)

            max_val = max(constraint_counts.itervalues())
            max_con_var = [k for k, v in constraint_counts.iteritems() if v == max_val]

            print "Constrain Counts", constraint_counts
            print "Max Val", max_val
            print "Max Con Var", max_con_var

            return max_con_var[0]

    def order_domain_values(self, variable):
        neighbour_values_counts = []
        for value in CSP.domain_values:
            if CSP.check_constraints(self.assignment, variable, value):
                neighbour_values_count = 0

                child_state = State(self.assignment, variable, value)

                for neighbour in CSP.constraints[variable]:
                    if neighbour not in self.assignment:
                        for value1 in CSP.domain_values:
                            if CSP.check_constraints(child_state.assignment, neighbour, value1):
                                neighbour_values_count += 1
                neighbour_values_counts.append(-neighbour_values_count)
            else:
                neighbour_values_counts.append(0)
        print "Neighbour Values Count", neighbour_values_counts

        sorted_counts = sorted(zip(neighbour_values_counts, CSP.domain_values))
        print "Sorted Counts", sorted_counts
        ordered_values = [x for (_, x) in sorted_counts]

        return ordered_values

    def check_goal_state(self):
        return len(self.assignment) == len(CSP.variables)

    def forward_check(self):
        for values in self.possible_values.itervalues():
            if len(values) == 0:
                return False
        return True

    def draw_state(self):
        image = np.zeros((7, 7, 3), np.uint8)
        for key in self.assignment:
            if self.assignment[key] == "red":
                channel_index = 0
            elif self.assignment[key] == "green":
                channel_index = 1
            else:
                channel_index = 2
            for (x, y) in CSP.positions[key]:
                image[x, y, channel_index] = 255
        return image

    def draw_possible_values(self):
        image = np.zeros((len(CSP.variables), 3, 3), np.uint8)
        for key in self.possible_values.keys():
            index = CSP.variables.index(key)
            if "red" in self.possible_values[key]:
                image[index, 0, 0] = 255
            if "green" in self.possible_values[key]:
                image[index, 1, 1] = 255
            if "blue" in self.possible_values[key]:
                image[index, 2, 2] = 255
        return image
