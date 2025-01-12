class BTreeNode:
    def __init__(self, max_degree, is_leaf=True):
        self.max_degree = max_degree
        self.keys: list = []
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

    def find_key(self, key):
        """Find the index of the key or the child where it should be."""
        for i, k in enumerate(self.keys):
            if k >= key:
                return i
        return len(self.keys)

    def delete(self, key):
        idx = self.find_key(key)

        # Case 1: Key is in this node
        if idx < len(self.keys) and self.keys[idx] == key:
            if self.is_leaf:
                # Case 1a: Key is in a leaf node
                self.keys.pop(idx)
            else:
                # Case 1b: Key is in an internal node
                self.delete_from_internal_node(idx)
        else:
            # Key is not in this node
            if self.is_leaf:
                # Case 2: Key is not in the tree
                print(f"Key {key} is not in the tree.")
                return

            # Ensure the child has enough keys
            child = self.children[idx]
            if len(child.keys) < (self.max_degree + 1) // 2:
                self.fill_child(idx)

            # Recursively delete the key
            if idx >= len(self.keys) and len(self.children) > idx + 1:
                self.children[idx].delete(key)
            else:
                self.children[idx].delete(key)

    def delete_from_internal_node(self, idx):
        """Delete a key from an internal node."""
        key = self.keys[idx]

        if len(self.children[idx].keys) >= (self.max_degree + 1) // 2:
            # Case 2a: Replace with the predecessor
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].delete(pred)
        elif len(self.children[idx + 1].keys) >= (self.max_degree + 1) // 2:
            # Case 2b: Replace with the successor
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].delete(succ)
        else:
            # Case 2c: Merge the key and the two children
            self.merge(idx)
            self.children[idx].delete(key)

    def get_predecessor(self, idx):
        """Get the predecessor of a key."""
        current = self.children[idx]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def get_successor(self, idx):
        """Get the successor of a key."""
        current = self.children[idx + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def fill_child(self, idx):
        """Ensure the child at idx has at least (t - 1) keys."""
        if idx > 0 and len(self.children[idx - 1].keys) >= (self.max_degree + 1) // 2:
            self.borrow_from_prev(idx)
        elif idx < len(self.children) - 1 and len(self.children[idx + 1].keys) >= (self.max_degree + 1) // 2:
            self.borrow_from_next(idx)
        else:
            if idx < len(self.children) - 1:
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        """Borrow a key from the previous sibling."""
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())

        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        """Borrow a key from the next sibling."""
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx):
        """Merge child[idx] and child[idx + 1]."""
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])
        child.keys.extend(sibling.keys)
        if not child.is_leaf:
            child.children.extend(sibling.children)

        self.keys.pop(idx)
        self.children.pop(idx + 1)
