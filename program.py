from btree.BTree import BTree


def print_btree_pretty(node, level=0, prefix="Root: "):
    # Print the current node's keys
    print(" " * (level * 4) + prefix + "[" + " | ".join(map(str, node.keys)) + "]")
    if not node.is_leaf:
        # Iterate through children, showing the branching structure
        for i, child in enumerate(node.children):
            child_prefix = f"Child-{i+1}: "
            print_btree_pretty(child, level + 1, prefix=child_prefix)

def print_btree(node, level=0):
    print(" " * (level * 4) + " | ".join(map(str, node.keys)))
    if not node.is_leaf:
        for child in node.children:
            print_btree(child, level + 1)



if __name__ == "__main__":
    max = int(input("Enter maximum degree: "))

    btree = BTree(max)

    keys = input("Enter numbers: (separate with comma) ").split(',')

    for key in keys:
        btree.insert(int(key))

    btree.pretty()