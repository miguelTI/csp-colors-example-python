class Node:

    def __init__(self, state):
        self.state = state
        self.depth = 0
        self.children = []
        self.parent = None

    def add_child(self, childNode):
        self.children.append(childNode)
        childNode.parent = self
        childNode.depth = self.depth + 1

    def print_tree(self):
        print self.depth, " - ", self.state.assignment
        for child in self.children:
            child.print_tree()
