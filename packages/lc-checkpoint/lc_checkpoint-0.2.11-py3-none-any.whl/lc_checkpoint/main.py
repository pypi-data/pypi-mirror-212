import os
import pickle
import math
import numpy as np
import torch.optim as optim
import torch.nn as nn
import dahuffman

__all__ = ['initialize', 'compress_data', 'decode_data', 'save_checkpoint', 'load_checkpoint', 'calculate_compression_rate']

net = None
optimizer = None
criterion = None
checkpoint_dir = None
num_buckets = None
num_bits = None
prev_state_dict = None

def initialize(model, optimizer, criterion, checkpoint_dir, num_buckets, num_bits):
    net = model
    optimizer = optimizer
    criterion = criterion
    checkpoint_dir = checkpoint_dir
    os.makedirs(checkpoint_dir, exist_ok=True)
    num_buckets = num_buckets
    num_bits = num_bits
    prev_state_dict = net.state_dict()

def compress_data(δt, num_bits=num_bits, k=num_buckets, treshold=True):
    sign = np.sign(δt)
    x_abs = np.abs(δt)
    exponent = np.floor(np.log2(x_abs))
    mantissa = x_abs / (2 ** exponent)
    quantized = sign * mantissa * (2 ** exponent)
    smallest_value = 2 ** (-num_bits)
    quantized = np.round(quantized / smallest_value) * smallest_value
    
    the_sign = np.zeros_like(δt)
    the_sign[δt < 0] = 1

    grouped_quantized = {}
    for i in range(len(δt)):
        key = (the_sign[i], int(exponent[i]))
        if key not in grouped_quantized:
            grouped_quantized[key] = []
        grouped_quantized[key].append(quantized[i])

    sorted_keys = sorted(grouped_quantized.keys(), key=lambda x: x[1])

    if treshold is not None:
        # Priority promotion
        e_values = set([key[1] for key in sorted_keys])
        e_priority = sorted(list(e_values), reverse=True)[:treshold]
        new_keys = []
        for key in sorted_keys:
            if key[1] in e_priority:
                new_keys.append(key)
            else:
                new_key = (key[0], 0)
                if new_key not in grouped_quantized:
                    grouped_quantized[new_key] = []
                grouped_quantized[new_key] += grouped_quantized[key]
        sorted_keys = sorted(new_keys, key=lambda x: x[1])

    num_keys = len(sorted_keys)
    bucket_size = max(num_keys // k, 1)
    buckets = [sorted_keys[i:i+bucket_size] for i in range(0, num_keys, bucket_size)]

    # Merge buckets
    if len(buckets) < k-1:
        merged_bucket = []
        for bucket in buckets[k-1:]:
            merged_bucket += bucket
        buckets = buckets[:k-1] + [merged_bucket]

    bucket_means = []
    for i, bucket in enumerate(buckets):
        bucket_mean = 0
        bucket_len = len(bucket)
        if bucket_len > 0:
            for key in bucket:
                values = [round(val, 2) for val in grouped_quantized[key]]
                bucket_mean += sum(values) / len(values)
            bucket_mean /= bucket_len
        bucket_means.append(bucket_mean)
        
    new_δt = np.zeros_like(exponent)
    for i, bucket in enumerate(buckets):
        if len(bucket) > 0:
            bucket_mean = bucket_means[i]
            base_key = bucket[0][1]
            new_δt[(the_sign == bucket[0][0]) & (exponent == base_key)] = bucket_mean
    
    # Encode new_δt using Huffman coding
    encoder = dahuffman.HuffmanCodec.from_data(new_δt)
    encoded = encoder.encode(new_δt)
    
    return encoded

def decode_data(encoded):
    codec = dahuffman.HuffmanCodec.from_data(encoded)
    int_list = codec.decode(encoded)
    int_list = [int(x) for x in int_list]
    new_δt = np.array(int_list) / 100.0
    return new_δt

def save_checkpoint(filename, compressed_data, epoch, iteration):
    # Save the compressed data and epoch number to a file
    if not os.path.exists('checkpoints/lc-checkpoint'):
        os.makedirs('checkpoints/lc-checkpoint')
    filename = os.path.join('checkpoints/lc-checkpoint', 'lc_checkpoint_epoch{}_iter{}.pt'.format(epoch, iteration))
    with open(filename, 'wb') as f:
        pickle.dump((compressed_data, epoch), f)

def load_checkpoint(filename):
    # Load the compressed data and epoch number from a file
    with open(filename, 'rb') as f:
        compressed_data, epoch = pickle.load(f)
    compressed_data = decode_data(compressed_data)  # decode the binary data
    return compressed_data, epoch

def calculate_compression_rate(prev_state_dict, num_bits=num_bits, num_buckets=num_buckets):
    num_elements = len(prev_state_dict)
    compression_rate = num_elements * math.log(num_buckets, 2) + num_buckets * num_bits
    return compression_rate