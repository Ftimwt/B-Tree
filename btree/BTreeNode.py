class BTreeNode:
    def __init__(self, max_degree, is_leaf=True):
        self.max_degree = max_degree
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.is_leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == self.max_degree - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = (self.max_degree + 1) // 2
        node = self.children[i]
        new_node = BTreeNode(self.max_degree, node.is_leaf)
        mid_key = node.keys[t - 1]

        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]

        if not node.is_leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]

        self.children.insert(i + 1, new_node)
        self.keys.insert(i, mid_key)
