import numpy
import string
import random

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
    file = open("text.txt","r") 

    text = file.read().lower()
    text_length = len(text)
    unique_char = list(set(text))
    normal_chars = list(string.digits + string.ascii_lowercase)
    special_char = [c for c in unique_char if c not in normal_chars]
    nb_chars = len(unique_char)

    symbol_probability = {}

    # Computing probability of each unique character
    for c in unique_char:
        symbol_probability[c] = text.count(c)/text_length

    # Computing the huffman code
    huff_code = huffman_code(symbol_probability)

    # Printing probability and code for each character
    sorted_prob = reversed(sorted(symbol_probability.items(), key=lambda x: x[1]))
    print("Symbol \t Probability \t Code")
    for symbol, prob in sorted_prob:
        code = huff_code[symbol]
        if symbol == '\n':
            print("enter \t {:.6f} \t {}".format(prob, code))
        else:
            print("{} \t {:.6f} \t {}".format(symbol, prob, code))

    # Encode the text
    encoded_text = text
    for symbol in unique_char:
        encoded_text = encoded_text.replace(symbol, huff_code[symbol])

    # Expected average length of coding sample:
    n_tries = 10
    total_length = 0
    for i in range(n_tries):
        if i % 50 == 0:
            print("{}\{}".format(i, n_tries))

        #Compute huffman code     
        huff_code = huffman_code(symbol_probability)
        # print("huff_code['&']",huff_code['&'])
        # print("huff_code['6']",huff_code['6'])
        # print("huff_code['8']",huff_code['8'])
        # print("huff_code['4']",huff_code['4'])

        #Encode the text
        encoded_text = text
        for symbol in unique_char:
            encoded_text = encoded_text.replace(symbol, huff_code[symbol])
        print(len(encoded_text))
        total_length += len(encoded_text)
    expected_average_length = int(total_length/n_tries)
    
    print("Total length of text is {} chars, so {} bits assuming unicode encoding (32 bit per char)".format(len(text), len(text)*32))
    print("Expected average length of encoded text is {} bits".format(expected_average_length))
    print("Compression rate is ", len(text) * 32 /expected_average_length)



    