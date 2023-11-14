from source.tree import Tree, Node
from source.objects import Card

def test_tree_node():
    tree = Tree(4)
    node = tree.create_node(2,None)
    assert isinstance(node, Node)

    node_son = tree.create_node(10, node)
    assert node_son.parent == node

    tree.add_node(node_son,3)
    assert tree.levels_of_tree[3] == [node_son]

    tree.add_sons(3)
    assert node.list_of_sons[0] == 10

def test_init_card():
    card = Card("9H",0,None)
    assert card.lock == False


