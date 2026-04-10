## 2026-04-14 - Optimized leads processing throughput with consolidated memoization and flattened unpacking
**Learning:** Consolidating multiple cleaning/normalization steps into a single memoized function significantly reduces function call overhead and multiple dictionary lookups in the `lru_cache`. Additionally, flattening the return values of helper functions in hot loops avoids the overhead of nested tuple unpacking. Direct `.lower()` calls can be faster than memoized versions for short, simple strings due to the overhead of the cache mechanism itself.
**Action:** Always look for opportunities to fuse related memoized operations and flatten return structures in performance-critical loops. Benchmark `lru_cache` against direct operations for simple transformations.

## 2026-04-15 - Micro-optimized string membership testing and verified streaming I/O efficiency
**Learning:** Using a pre-defined set () for identifying null-equivalent fields is slightly faster than multiple  conditions in Python. While batch writing via  is faster in isolation, the memory cost of O(N) storage can be a bottleneck for large datasets; pre-binding the  method provides a middle-ground throughput gain while maintaining O(1) memory scalability.
**Action:** Use sets for membership tests with multiple constants. Prioritize streaming I/O with method pre-binding over batching for data processing tasks unless the dataset is guaranteed to be small.

## 2026-04-15 - Micro-optimized string membership testing and verified streaming I/O efficiency
**Learning:** Using a pre-defined set (`NONE_SET = {'None', 'none', ''}`) for identifying null-equivalent fields is slightly faster than multiple `or` conditions in Python. While batch writing via `writerows` is faster in isolation, the memory cost of O(N) storage can be a bottleneck for large datasets; pre-binding the `writerow` method provides a middle-ground throughput gain while maintaining O(1) memory scalability.
**Action:** Use sets for membership tests with multiple constants. Prioritize streaming I/O with method pre-binding over batching for data processing tasks unless the dataset is guaranteed to be small.
