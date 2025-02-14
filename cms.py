import numpy as np

class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = np.zeros((depth, width), dtype=int)
        self.hash_functions = [
            lambda x, s=seed: hash((s, x)) % self.width for seed in range(depth)
        ]

    def add(self, key):
        for i in range(self.depth):
            self.table[i][self.hash_functions[i](key)] += 1

    def estimate(self, key):
        return min(self.table[i][self.hash_functions[i](key)] for i in range(self.depth))
