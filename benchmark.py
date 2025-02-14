import time
import sys
import random
from bst import BST
from cms import CountMinSketch

def benchmark(data, cms):
    # Benchmark Insertion Times

    # 1. Count-Min Sketch
    t0 = time.perf_counter()
    for item in data:
        cms.add(item)
    t1 = time.perf_counter()
    cms_insertion_time = t1 - t0

    # 2. Hash Table (Dictionary)
    hash_table = {}
    t0 = time.perf_counter()
    for item in data:
        hash_table[item] = hash_table.get(item, 0) + 1
    t1 = time.perf_counter()
    hash_insertion_time = t1 - t0

    # 3. BST
    bst = BST()
    t0 = time.perf_counter()
    for item in data:
        bst.insert(item)
    t1 = time.perf_counter()
    bst_insertion_time = t1 - t0

    # Benchmark Query Times for 100 random keys
    test_keys = random.sample(list(set(data)), 100)
    cms_results = {}
    hash_results = {}
    bst_results = {}

    t0 = time.perf_counter()
    for key in test_keys:
        cms_results[key] = cms.estimate(key)
    t1 = time.perf_counter()
    cms_query_time = t1 - t0

    t0 = time.perf_counter()
    for key in test_keys:
        hash_results[key] = hash_table.get(key, 0)
    t1 = time.perf_counter()
    hash_query_time = t1 - t0

    t0 = time.perf_counter()
    for key in test_keys:
        bst_results[key] = bst.query(key)
    t1 = time.perf_counter()
    bst_query_time = t1 - t0

    errors = []
    for key in test_keys:
        exact = hash_results[key]
        estimate = cms_results[key]
        errors.append(estimate - exact)
    avg_error = sum(errors) / len(errors)

    # --- Benchmarking Space Usage ---
    cms_memory = cms.table.nbytes + deep_getsizeof(cms.hash_functions)
    hash_memory = deep_getsizeof(hash_table)
    bst_memory = deep_getsizeof(bst)

    return {
        "memory": [cms_memory, hash_memory, bst_memory],
        "error": avg_error,
        "insertion_time": [cms_insertion_time, hash_insertion_time, bst_insertion_time],
        "query_time": [cms_query_time, hash_query_time, bst_query_time]
    }

def deep_getsizeof(obj, seen=None):
    """Recursively compute the memory footprint of an object and its contents."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    if isinstance(obj, dict):
        size += sum(deep_getsizeof(k, seen) for k in obj.keys())
        size += sum(deep_getsizeof(v, seen) for v in obj.values())
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        try:
            size += sum(deep_getsizeof(i, seen) for i in obj)
        except TypeError:
            pass
    elif hasattr(obj, '__dict__'):
        size += deep_getsizeof(obj.__dict__, seen)
    return size

