from scipy.io import wavfile
from random import random

import matplotlib
matplotlib.use("TkAgg")  # Fixing a bug of matplotlib on MacOS
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def binary_encode(samples, n_bits):
    """
    Transform the sound signal using a (naive) fixed-length binary code.
    """
    binary_signal = ''

    # Convert each sample into binary code and add it to signal
    for sample in samples:
        bin_sample = "{0:b}".format(sample)
        prefix = '0' * (n_bits - len(binary_signal))
        binary_signal += (prefix + bin_sample)

    return binary_signal


def hamming_encode(binary_signal):
    """
    Function that returns the Hamming (7,4) code for a given sequence of
    binary symbols. Each sequence of 4 bits is encoded in form :
    H2 H1 H0 D3 D2 D1 D0.
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
        p[0] = (d[1] + d[2] + d[3]) % 2
        p[1] = (d[0] + d[2] + d[3]) % 2
        p[2] = (d[0] + d[1] + d[3]) % 2
        parity = ''.join(map(str, p))  # Convert into string
        
        # Compute hamming code
        hamming_signal += (parity + data)

        # Go forward in the binary sequence
        binary_signal = binary_signal[K:]

    return hamming_signal


def simulate_noisy_channel(binary_signal):
    """
    Simulate a binary symmetric channel with a probability of error
    equal to 0.01
    """
    corrupted_signal = ''

    for bit in binary_signal:





if __name__ == "__main__":

    # Q8: Plot of the sound signal
    sampling_rate, signal_samples = wavfile.read('sound.wav')
    plt.plot(signal_samples)
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('sound.eps')

    # Q9: Transform sound signal into binary code
    binary_signal = binary_encode(signal_samples, 8)
    
    # Q10: Hamming (7,4) code for binary signal
    hamming_signal = hamming_encode(binary_signal)
    
    # Q11: Generate corrupted version of binary sound signal

    