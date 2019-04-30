import numpy
import string
import random
import math
import itertools
from heapq import heappush, heappop, heapify

def huffman_code(symbol_probability):
    # Base case of only two symbols
    if(len(symbol_probability) == 2):
        huff_code = {}
        keys = list(symbol_probability.keys())
        huff_code[keys[0]] = '0'
        huff_code[keys[1]] = '1'
        return huff_code

    # Create a new distribution by merging lowest prob. pair
    symbol_prob_copy = symbol_probability.copy()
    lowest_1, lowest_2 = lowest_prob_pair(symbol_probability)
    
    # Remove lowest probability from dict
    prob_lowest_1, prob_lowest_p2 = symbol_prob_copy.pop(lowest_1), symbol_prob_copy.pop(lowest_2)

    # Recompute the sum of probabilities of the two lowest probability codes combined
    symbol_prob_copy[lowest_1 + lowest_2] = prob_lowest_1 + prob_lowest_p2

    # Recursion
    huff_code = huffman_code(symbol_prob_copy)

    # Construct new code 
    lowest_code = huff_code.pop(lowest_1 + lowest_2)
    huff_code[lowest_1], huff_code[lowest_2] = lowest_code + '0', lowest_code + '1'

    return huff_code

def improved_huffman_code(symbol_probability):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[prob, [symbol, ""]] for symbol, prob in symbol_probability.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for low_pair in lo[1:]:
            low_pair[1] = '0' + low_pair[1]
        for high_pair in hi[1:]:
            high_pair[1] = '1' + high_pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
 

def lowest_prob_pair(symbol_probability):
    '''Return pair of symbols from distribution p with lowest probabilities.'''
    sorted_prob = sorted(symbol_probability.items(), key=lambda x: x[1])

    # # Add randomization for expectation computation
    # if sorted_prob[0][1] == sorted_prob[1][1]:
    #     if random.random() < 0.5:
    #         return sorted_prob[0][0], sorted_prob[1][0]
    #     else:
    #         return sorted_prob[1][0], sorted_prob[0][0]

    return sorted_prob[0][0], sorted_prob[1][0]



if __name__ == '__main__':
    expected_average_length = 0

    file = open("text.txt","r") 
    text = file.read().lower()
    text_length = len(text)
    unique_symbols = list(set(text))
    normal_symbols = list(string.digits + string.ascii_lowercase)
    special_symbols = [c for c in unique_symbols if c not in normal_symbols]
    nb_chars = len(unique_symbols)


    #==================== HUFFMAN CODING ======================#
    print('#==================== HUFFMAN CODING ======================#')

    # Computing probability of each unique symbol
    symbol_probability = {}

    for c in unique_symbols:
        symbol_probability[c] = text.count(c)/text_length

    # Computing the huffman code
    huff_code = huffman_code(symbol_probability)

    # Printing probability and code for each symbol
    sorted_prob = reversed(sorted(symbol_probability.items(), key=lambda x: x[1]))
    print("Symbol \t Probability \t Code")
    for symbol, prob in sorted_prob:
        code = huff_code[symbol]
        if symbol == '\n':
            print("enter \t {:.6f} \t {}".format(prob, code))
        else:
            print("{} \t {:.6f} \t {}".format(symbol, prob, code))
        expected_average_length += prob * len(code)

    # Encode the text
    # Don't mix up symbols '0' and '1' with encoded symbols
    encoded_text = text
    encoded_text = encoded_text.replace('1', '!!!one!!!')
    encoded_text = encoded_text.replace('0', huff_code['0'])
    encoded_text = encoded_text.replace('!!!one!!!', huff_code['1'])
    for symbol in unique_symbols:
        if symbol != '0' and symbol != '1':
            encoded_text = encoded_text.replace(symbol, huff_code[symbol])


    print("Special characters : ", special_symbols)
    print("Number of unique characters in the text: ",nb_chars)
    print("Length of encoded text is : ", len(encoded_text))

    print("Total length of text is {} chars, so {} bits assuming unicode encoding (32 bit per char)".format(len(text), len(text)*32))
    print("Expected average length of encoded text is ceil({:.3f}) = {} bits".format(expected_average_length, math.ceil(expected_average_length)))
    print("Empirical average length of encoded text is ceil({:.3f}) = {} bits".format(len(encoded_text)/len(text), math.ceil(len(encoded_text)/len(text))))
    print("Compression rate is (assuming 8 bit per symbol) ", len(text) * 8 /len(encoded_text))
    print("Compression rate is (assuming 32 bit per symbol) ", len(text) * 32 /len(encoded_text))

    #==================== IMPROVED HUFFMAN CODING ======================#
    print('#====================IMPROVED HUFFMAN CODING ======================#')

    huff_code = {}
    expected_average_length_pairs = 0  
    unique_symbol_pairs = [char_1+char_2 for char_1 in unique_symbols for char_2 in unique_symbols]

    # Computing probability of each unique symbol pair
    symbol_pairs_probability = {}
    for pair in unique_symbol_pairs:
        symbol_pairs_probability[pair] = text.count(pair)/text_length

    # Computing the Huffman code
    huff_code_list = improved_huffman_code(symbol_pairs_probability)


    print("Symbol \t Probability")
    for item in huff_code_list:
        symbol = item[0]
        code = item[1]

        # Transforming into a dictionnary
        for item in huff_code_list:
            huff_code[item[0]] = item[1] 

        prob = symbol_pairs_probability[symbol]
        if prob != 0:
            if symbol == '\n':
                print("enter \t {:.8f}".format(prob))
            else:
                print("{} \t {:.8f}".format(symbol, prob))
            expected_average_length_pairs += prob * len(code)


    # Encode the text
    # Don't mix up symbols '0' and '1' with encoded symbols
    encoded_text_pairs = text
    encoded_text_pairs = encoded_text_pairs.replace('11', '!!!one!!!')
    encoded_text_pairs = encoded_text_pairs.replace('00', huff_code['00'])
    encoded_text_pairs = encoded_text_pairs.replace('!!!one!!!', huff_code['11'])
    for symbol_pair in unique_symbol_pairs:
        if symbol_pair != '00' and symbol_pair != '11':
            encoded_text_pairs = encoded_text_pairs.replace(symbol_pair, huff_code[symbol_pair])

    print("Length of encoded text is : ", len(encoded_text_pairs))
    print("Expected average length of encoded text is ceil({:.3f}) = {} bits".format(expected_average_length_pairs, math.ceil(expected_average_length_pairs)))
    print("Empirical average length of encoded text is ceil({:.3f}) = {} bits".format(len(encoded_text_pairs)/len(text), math.ceil(len(encoded_text_pairs)/len(text))))
    print("Compression rate is (assuming 8 bit per symbol) ", len(text) * 8 /len(encoded_text_pairs))
    print("Compression rate is (assuming 32 bit per symbol) ", len(text) * 32 /len(encoded_text_pairs))







    