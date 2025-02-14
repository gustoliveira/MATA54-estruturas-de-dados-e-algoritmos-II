import random
from benchmark import benchmark

elements = int(input("Enter elements variaty size: "))
input = int(input("Enter input size: "))

data = [random.randint(1, elements) for _ in range(input)]

benchmark(data)

