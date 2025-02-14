import time
import sys
import random
from bst import BST
from cms import CountMinSketch

def benchmark(data):
    # Benchmark Insertion Times

    # 1. Count-Min Sketch
    cms = CountMinSketch(width=2000, depth=10)
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

    print("Insertion Times:")
    print("Count-Min Sketch: {:.6f} seconds".format(cms_insertion_time))
    print("Hash Table      : {:.6f} seconds".format(hash_insertion_time))
    print("BST             : {:.6f} seconds".format(bst_insertion_time))

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

    print("\nQuery Times (for 100 keys):")
    print("Count-Min Sketch: {:.6f} seconds".format(cms_query_time))
    print("Hash Table      : {:.6f} seconds".format(hash_query_time))
    print("BST             : {:.6f} seconds".format(bst_query_time))

    # Compare CMS's estimation error for sample keys:
    errors = []
    for key in test_keys:
        exact = hash_results[key]
        estimate = cms_results[key]
        errors.append(estimate - exact)  # CMS should overestimate (never underestimate)
    avg_error = sum(errors) / len(errors)
    print("\nAverage Overestimate in CMS (should be >= 0): {:.3f}".format(avg_error))

    # --- Benchmarking Space Usage ---

    # CMS: Use the nbytes attribute for the numpy array,
    # plus the (small) overhead for the list of hash functions.
    cms_memory = cms.table.nbytes + deep_getsizeof(cms.hash_functions)

    # Hash Table: Use deep_getsizeof to capture the overall footprint.
    hash_memory = deep_getsizeof(hash_table)

    # BST: Use deep_getsizeof starting from the BST instance.
    bst_memory = deep_getsizeof(bst)

    print("\nMemory Usage:")
    print("Count-Min Sketch: {} bytes".format(cms_memory))
    print("Hash Table      : {} bytes".format(hash_memory))
    print("BST             : {} bytes".format(bst_memory))

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

