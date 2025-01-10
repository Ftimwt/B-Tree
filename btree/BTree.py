from btree.BTreeNode import BTreeNode


class BTree:
    def __init__(self, max_degree):
        self.max_degree = max_degree
        self.root = BTreeNode(max_degree)

    def insert(self, key):
        root = self.root
        if len(root.keys) == self.max_degree - 1:
            new_root = BTreeNode(self.max_degree, is_leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0)
            self.root = new_root
        self.root.insert_non_full(key)

    def pretty(self, node=None, level=0, prefix="Root: "):
      # Print the current node's keys
      if node == None:
          node = self.root
      print(" " * (level * 4) + prefix + "[" + " | ".join(map(str, node.keys)) + "]")
      if not node.is_leaf:
          # Iterate through children, showing the branching structure
          for i, child in enumerate(node.children):
              child_prefix = f"Child-{i+1}: "
              self.pretty(child, level + 1, prefix=child_prefix)

