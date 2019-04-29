import numpy
import string
import random
import math

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
    expected_average_length = 0

    file = open("text.txt","r") 
    text = file.read().lower()
    text_length = len(text)
    unique_char = list(set(text))
    normal_chars = list(string.digits + string.ascii_lowercase)
    special_char = [c for c in unique_char if c not in normal_chars]
    nb_chars = len(unique_char)


    # Computing probability of each unique character
    symbol_probability = {}
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
        expected_average_length += prob * len(huff_code[symbol])

    # Encode the text
    # Don't mix up symbols '0' and '1' with encoded symbols
    encoded_text = text
    encoded_text = encoded_text.replace('1', '!!!one!!!')
    encoded_text = encoded_text.replace('0', huff_code['0'])
    encoded_text = encoded_text.replace('!!!one!!!', huff_code['1'])
    for symbol in unique_char:
        if symbol != '0' and symbol != '1':
            encoded_text = encoded_text.replace(symbol, huff_code[symbol])


    print("Special characters : ", special_char)
    print("Number of unique characters in the text: ",nb_chars)
    print("Total length of text is {} chars, so {} bits assuming unicode encoding (32 bit per char)".format(len(text), len(text)*32))
    print("Expected average length of encoded text is ceil({:.3f}) = {} bits".format(expected_average_length, math.ceil(expected_average_length)))
    print("Empirical average length of encoded text is ceil({:.3f}) = {} bits".format(len(encoded_text)/len(text), math.ceil(len(encoded_text)/len(text))))
    print("Compression rate is ", len(text) * 32 /len(encoded_text))



    