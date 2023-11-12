import time
import hashlib
from collections import defaultdict

def hash_pair_1(pair, num_buckets):
    hash_value = hashlib.md5(str(pair).encode()).hexdigest()
    return int(hash_value, 16) % num_buckets

def hash_pair_2(pair, num_buckets):
    hash_value = hashlib.sha256(str(pair).encode()).hexdigest()
    return int(hash_value, 16) % num_buckets

def multihash_pcy(baskets, support_threshold, num_buckets):
    # First Pass
    singleton_counts = defaultdict(int)
    bucket_counts_1 = defaultdict(int)
    bucket_counts_2 = defaultdict(int)
    
    for basket in baskets:
        for item in basket:
            singleton_counts[item] += 1
        
        for i in range(len(basket)):
            for j in range(i+1, len(basket)):
                pair = (basket[i], basket[j])
                bucket_1 = hash_pair_1(pair, num_buckets)
                bucket_counts_1[bucket_1] += 1
                
                bucket_2 = hash_pair_2(pair, num_buckets)
                bucket_counts_2[bucket_2] += 1
                
    # Second Pass
    frequent_pairs = set()
    frequent_singletons = {k for k, v in singleton_counts.items() if v >= support_threshold}
    
    for basket in baskets:
        basket_set = set(basket) & frequent_singletons
        for i, item1 in enumerate(basket_set):
            for item2 in basket_set:
                if item1 < item2:
                    pair = (item1, item2)
                    bucket_1 = hash_pair_1(pair, num_buckets)
                    bucket_2 = hash_pair_2(pair, num_buckets)
                    
                    if bucket_counts_1[bucket_1] >= support_threshold and bucket_counts_2[bucket_2] >= support_threshold:
                        if all(item in frequent_singletons for item in pair):
                            frequent_pairs.add(pair)
    
    return frequent_pairs

baskets = []

data_file_path = ""

with open(data_file_path, 'r') as file:
    for line in file:
        single_basket = [int(item) for item in line.strip().split()]
        baskets.append(single_basket)

chunk_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 1%, 5%, 10% of the data
thresholds = [1, 5, 10]  # 1%, 5%, 10% thresholds

for support_threshold_percentage in thresholds:
    for chunk_size in chunk_sizes:
        support_threshold = (len(baskets) * support_threshold_percentage) // 100
        
        baskets_chunk = baskets[:int(len(baskets) * chunk_size)]
        
        start_time = time.time()
        
        num_buckets = 10007
        frequent_itemsets = multihash_pcy(baskets_chunk, support_threshold, num_buckets)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"\nExecution Time: {execution_time:.2f} ms with a chunk size of {chunk_size:.2f} and {support_threshold_percentage}% threshold")
        
        print(f"Frequent Itemsets: {frequent_itemsets}\n")
