class BSTNode:
    def __init__(self, key):
        self.key = key
        self.count = 1
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key == node.key:
            node.count += 1
        elif key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert_recursive(node.left, key)
        else:  # key > node.key
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert_recursive(node.right, key)

    def query(self, key):
        return self._query_recursive(self.root, key)

    def _query_recursive(self, node, key):
        if node is None:
            return 0
        if key == node.key:
            return node.count
        elif key < node.key:
            return self._query_recursive(node.left, key)
        else:
            return self._query_recursive(node.right, key)

