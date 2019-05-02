from scipy.io import wavfile
from random import random
import numpy as np

import matplotlib
matplotlib.use("TkAgg")  # Fixing a bug of matplotlib on MacOS
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def binary_encode(samples, n_bits):
    """
    Transform the sound signal using a (naive) fixed-length binary code.
    """
    binary_signal = ''

    for sample in samples:
        # Convert sample to binary code
        bin_sample = "{0:b}".format(sample)
        # Add some 0 to have n bits
        prefix = '0' * (n_bits - len(bin_sample))
        # Append sample to the binary sequence
        binary_signal += (prefix + bin_sample)

    return binary_signal


def binary_decode(binary_signal, n_bits):
    """
    Transform a fixed-length binary code into a sound signal.
    """
    samples = []

    while len(binary_signal) >= n_bits:
        # Get sample of n bits
        sample = binary_signal[0:n_bits]
        # Convert it to int and append to the list
        samples.append(int(sample, 2))
        # Move forward to the binary sequnce
        binary_signal = binary_signal[n_bits:]

    return samples


def simulate_noisy_channel(binary_signal):
    """
    Simulate a binary symmetric channel with a probability of error
    equal to 0.01
    """
    corrupted_signal = ''

    # For each bit, with a probability of 1%, change bit
    for bit in binary_signal:
        if random() <= 0.01:
            corrupted_bit = '1' if bit == '0' else '0'
            corrupted_signal += corrupted_bit
        else:
            corrupted_signal += bit

    return corrupted_signal


def hamming_encode(binary_signal):
    """
    Function that returns the Hamming (7,4) code for a given sequence of
    binary symbols. Each sequence of 4 bits (D0 D1 D2 D3) is encoded
    in form : (P0 P1 D0 P2 D1 D2 D3)
    """
    K = 4
    hamming_signal = ''

    # Read in K=4 bits at a time and write out those plus parity bits
    while len(binary_signal) >= K:

        # Get data bits
        data = binary_signal[0:K]
        d = list(map(int, list(data)))  # Convert into list of int
        
        # Calculate parity bits
        p = [0, 0, 0]
        p[0] = (d[0] + d[1] + d[3]) % 2
        p[1] = (d[0] + d[2] + d[3]) % 2
        p[2] = (d[1] + d[2] + d[3]) % 2

        # Create the hamming code
        h_code = [p[0], p[1], d[0], p[2], d[1], d[2], d[3]]
        h_code = ''.join(map(str, h_code))  # Convert list into string
        
        # Add hamming code to signal
        hamming_signal += h_code

        # Go forward in the binary sequence
        binary_signal = binary_signal[K:]

    return hamming_signal


def hamming_decode(hamming_signal):
    """
    Function that decode a binary sequence of Hamming (7,4) codes.
    Each code of 7 bits is in form : (P0 P1 D0 P2 D1 D2 D3)
    """
    K = 7
    decoded_signal = ''

    # Read in K=4 bits at a time and decode them
    while len(hamming_signal) >= K:

        # Get data and parity bits
        data = hamming_signal[0:K]
        d = list(map(int, list(data)))  # Convert into list of int

        # Calculate syndrome
        s = [0, 0, 0]
        s[0] = (d[0] + d[2] + d[4] + d[6]) % 2  # P0 + D0 + D1 + D3
        s[1] = (d[1] + d[2] + d[5] + d[6]) % 2  # P1 + D0 + D2 + D3
        s[2] = (d[3] + d[4] + d[5] + d[6]) % 2  # P2 + D1 + D2 + D3
        syndrome = 4*s[2] + 2*s[1] + s[0]

        # If error elsewhere than in parity bits, correct bit
        if syndrome!=0 and syndrome!=1 and syndrome!=2 and syndrome!=4:
            d[syndrome-1] = (d[syndrome-1] + 1) % 2 

        # Get the decoded code
        code = [d[2], d[4], d[5], d[6]]
        code = ''.join(map(str, code))  # Convert list into string

        # Add decoded code to signal
        decoded_signal += code

        # Move forward in the hamming sequence
        hamming_signal = hamming_signal[K:]

    return decoded_signal


if __name__ == "__main__":
    # Fix number of bits
    n_bits = 8

    # Q8: Plot of the sound signal
    sampling_rate, signal_samples = wavfile.read('sound.wav')
    plt.plot(signal_samples)
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('sound.eps')
    plt.close()

    # Q9: Transform sound signal into binary code
    binary_signal = binary_encode(signal_samples, n_bits)
    
    # Q10: Hamming (7,4) code for binary signal
    hamming_signal = hamming_encode(binary_signal)
    
    # Q11: Generate corrupted version of binary sound signal
    corrupted_signal = simulate_noisy_channel(binary_signal)
    corrupted_samples = binary_decode(corrupted_signal, n_bits)  # Decode the binary corrupted signal
    wavfile.write('corrupted_sound.wav', sampling_rate, np.array(corrupted_samples, dtype='uint8'))  # Write corrupted sound
    plt.plot(corrupted_samples)  # Plot corrupted signal
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('corrupted_sound.eps')
    plt.close()

    # Q12: Using properties of Hamming, recover the corrupted signal
    corrupted_hamming_signal = simulate_noisy_channel(hamming_signal)
    decoded_hamming_signal = hamming_decode(corrupted_hamming_signal)
    decoded_hamming_samples = binary_decode(decoded_hamming_signal, n_bits)
    wavfile.write('corrected_hamming_sound.wav', sampling_rate, np.array(decoded_hamming_samples, dtype='uint8'))  # Write corrected sound
    plt.plot(decoded_hamming_samples)  # Plot corrupted signal
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('corrected_hamming_sound.eps')
    plt.close()
