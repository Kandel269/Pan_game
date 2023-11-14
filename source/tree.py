class Node():
    def __init__(self, power, parent,bot_move = None):
        self.power = power
        self.parent = parent
        self.bot_move = bot_move
        self.list_of_sons = []

    def new_son(self, node) -> None:
        self.list_of_sons.append(node)

class Tree():
    def __init__(self, max_lvl):
        self.levels_of_tree = dict()
        for lvl in range(max_lvl):
            self.levels_of_tree[lvl] = []

    def create_node(self, power, parent, bot_move = None) -> Node:
        return Node(power, parent,bot_move)

    def add_node(self, node, level) -> None:
        self.levels_of_tree[level].append(node)

    def add_sons(self, level, operation = None, last = False) -> None:
        for node in self.levels_of_tree[level]:
            if last:
                if node.list_of_sons:
                    node.power = operation(node.list_of_sons)
                    node.parent.new_son(node)
                else:
                    node.parent.new_son(node.power)
            elif operation and node.list_of_sons:
                node.power = operation(node.list_of_sons)
                node.parent.new_son(node.power)
            else:
                node.parent.new_son(node.power)