import random
from benchmark import benchmark
from cms import CountMinSketch

epsilon = 0.002719 # width = 1000
delta = 0.99 # depth = 10
cms = CountMinSketch(epsilon, delta)

data = [random.randint(1, 5000) for _ in range(10000)]

benchmark(data, cms)

print("Error Bound: {:.2f}".format(cms.get_error_bound(len(data))))
