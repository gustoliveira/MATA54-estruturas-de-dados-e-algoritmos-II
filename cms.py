import numpy as np
import math

class CountMinSketch:
    def __init__(self, epsilon, delta):
        """
        :param epsilon: Fator de erro na estimativa de frequência
        :param delta: Probabilidade de erro
        """
        self.epsilon = epsilon
        self.delta = delta
        
        # Calcula a largura e a profundidade com base em epsilon e delta
        self.width = math.ceil(math.e / epsilon)
        self.depth = math.ceil(math.log(1 / delta))
        
        self.table = np.zeros((self.depth, self.width), dtype=int)
        self.hash_functions = [
            lambda x, s=seed: hash((s, x)) % self.width for seed in range(self.depth)
        ]

    def add(self, key):
        for i in range(self.depth):
            self.table[i][self.hash_functions[i](key)] += 1

    def estimate(self, key):
        return min(self.table[i][self.hash_functions[i](key)] for i in range(self.depth))

    def get_error_bound(self, elements):
        """
        Retorna o limite de erro teórico.
        """
        return self.epsilon * elements

