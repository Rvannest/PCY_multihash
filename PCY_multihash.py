import time
from collections import defaultdict

each_baskets = []

text_path = ""

# define chunks and thresholds
set_thresholds = [0.01, 0.05, 0.10]  # 1%, 5%, 10% thresholds
set_sizes_of_dataset = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 1%, 5%, 10% data


with open(text_path, 'r') as text:
    for line in text:
        create_singlebasket = [int(item) for item in line.strip().split()]
        each_baskets.append(create_singlebasket)


# hash functions
def hash_pair(pair, number_of_buckets, hash_function=1):
    if hash_function == 1:
        return sum(pair) % number_of_buckets
    else:  # different hash function
        return (pair[0] * pair[1]) % number_of_buckets


# MultiHash PCY function
def multihash_pcy(each_baskets, supp_threshold, number_of_buckets):
    # First Pass
    single_itemcount = defaultdict(int)
    count_of_buckets_1 = defaultdict(int)
    count_of_buckets_2 = defaultdict(int)
    
    for basket in each_baskets:
        for item in basket:
            single_itemcount[item] += 1
        
        for i in range(len(basket)):
            for j in range(i+1, len(basket)):
                pair = tuple(sorted((basket[i], basket[j])))
                count_of_buckets_1[hash_pair(pair, number_of_buckets, hash_function=1)] += 1
                count_of_buckets_2[hash_pair(pair, number_of_buckets, hash_function=2)] += 1
                
    # Second Pass
    pair_counts = defaultdict(int)
    frequent_single_items = set()
    for k, v in single_itemcount.items():
        if v >= supp_threshold:
            frequent_single_items.add(k)
    
    for basket in each_baskets:
        for i in range(len(basket)):
            for j in range(i+1, len(basket)):
                pair = tuple(sorted((basket[i], basket[j])))
                if pair[0] in frequent_single_items and pair[1] in frequent_single_items:
                    if count_of_buckets_1[hash_pair(pair, number_of_buckets, hash_function=1)] >= supp_threshold and \
                       count_of_buckets_2[hash_pair(pair, number_of_buckets, hash_function=2)] >= supp_threshold:
                        pair_counts[pair] += 1
                    
    frequent_pair_items = set()
    for k, v in pair_counts.items():
        if v >= supp_threshold:
            frequent_pair_items.add(k)
    
    return frequent_pair_items



# loop chunk and threshold
for support_percentage in set_thresholds:
    for chunk_size in set_sizes_of_dataset:

        supp_threshold = (len(each_baskets) * support_percentage)
        
        select_basket_chunk = each_baskets[:int(len(each_baskets) * chunk_size)]
        
        # start time
        start_timer = time.time()
        
        number_of_buckets = 10037  # number of buckets
        find_frequent_itemsets = multihash_pcy(select_basket_chunk, supp_threshold, number_of_buckets)

        print(f"Frequent Itemsets: {find_frequent_itemsets}")

        execution_time = (time.time() - start_timer) * 1000
        print(f"Execution Time: {execution_time:.2f} ms --- Chunk size is {chunk_size:.2f} --- Support threshold is {support_percentage*100}%\n")
