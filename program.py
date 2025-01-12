import re

from btree.BTree import BTree


def print_btree_pretty(node, level=0, prefix="Root: "):
    # Print the current node's keys
    print(" " * (level * 4) + prefix + "[" + " | ".join(map(str, node.keys)) + "]")
    if not node.is_leaf:
        # Iterate through children, showing the branching structure
        for i, child in enumerate(node.children):
            child_prefix = f"Child-{i + 1}: "
            print_btree_pretty(child, level + 1, prefix=child_prefix)


def print_btree(node, level=0):
    print(" " * (level * 4) + " | ".join(map(str, node.keys)))
    if not node.is_leaf:
        for child in node.children:
            print_btree(child, level + 1)


if __name__ == "__main__":
    maxDeg = int(input("Enter maximum degree: "))

    btree = BTree(maxDeg)

    print("""
Available commands:
add %d
delete %d
""")

    while True:
        key = input("cmd: ").lower()
        if key == "exit":
            print("bye")
            break

        values = re.findall(r'(add|delete) (\d+)', key)
        if len(values) < 1:
            continue
        values = values[0]

        if values[0] == "add":
            btree.insert(int(values[1]))
        if values[0] == "delete":
            btree.delete(int(values[1]))

        btree.pretty()
