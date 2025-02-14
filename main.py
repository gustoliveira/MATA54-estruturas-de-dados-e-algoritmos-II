import random
import matplotlib.pyplot as plt
import numpy as np
from benchmark import benchmark
from cms import CountMinSketch

# Dados simulados de precisão
x = np.linspace(0, 1000, 100)  # número de elementos
cms_precision = 1 - (0.01 * np.log(x))  # precisão do CMS
hash_precision = np.ones(100)  # Hash Table mantém 100% até limite
bst_precision = np.ones(100) * 0.95  # BST com precisão constante

epsilon = 0.00075 # width = 1000
delta = 0.0001 # depth = 10
cms = CountMinSketch(epsilon, delta)

memory_cms = []
memory_hash = []
memory_bst = []

entrada = []

init = 4500
while True:
    init = init + 500
    if init >= 50000:
        break

    data = [random.randint(1, init) for _ in range(500000)]
    bm = benchmark(data, cms)

    entrada.append(init)
    memory_cms.append(bm['memory'][0])
    memory_hash.append(bm['memory'][1])
    memory_bst.append(bm['memory'][2])

# # Dados simulados de uso de memória
# memory_cms = np.log(x) * 100  # CMS cresce logaritmicamente
# memory_hash = x * 10  # Hash Table cresce linearmente
# memory_bst = x * np.log2(x)  # BST cresce n*log(n)

plt.figure(figsize=(10, 6))
plt.plot(x, memory_cms, 'r--', label='Count-Min Sketch')
plt.plot(x, memory_hash, 'b-', label='Hash Table')
plt.plot(x, memory_bst, 'g:', label='BST')

plt.xlabel('Número de Elementos')
plt.ylabel('Uso de Memória (KB)')
plt.title('Comparação de Uso de Memória')
plt.legend()
plt.grid(True)
plt.show()
