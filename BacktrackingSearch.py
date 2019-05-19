from State import State
from Node import Node
import CSP
from TreePlot import TreePlot


class BacktrackingSearch():
    def search(self):
        initial_state = State()
        root_node = Node(initial_state)
        treeplot = TreePlot()
        treeplot.generate_diagram(root_node, root_node)
        self.perform_backtrack_search(root_node, root_node)

    def perform_backtrack_search(self, root_node, node):
        print "-- proc --", node.state.assignment
        if node.state.check_goal_state():
            print "Reached goal state"
            return True
        else:
            if node.state.forward_check():
                variable = node.state.select_unassignet_variable()
                for value in node.state.order_domain_values(variable):
                    if CSP.check_constraints(node.state.assignment, variable, value):
                        child_node = Node(State(node.state.assignment, variable, value))
                        node.add_child(child_node)
                        treeplot = TreePlot()
                        treeplot.generate_diagram(root_node, child_node)

                        result = self.perform_backtrack_search(root_node, child_node)
                        if result is True:
                            return True
            return False
