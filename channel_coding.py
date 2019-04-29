from scipy.io import wavfile

import matplotlib
matplotlib.use("TkAgg")  # Fixing a bug of matplotlib on MacOS
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def encode(samples, n_bits):
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




if __name__ == "__main__":

    # Q8: Plot of the sound signal
    sampling_rate, signal_samples = wavfile.read('sound.wav')
    plt.plot(signal_samples)
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('sound.eps')

    # Q9: Transform sound signal into binary code
    binary_signal = encode(signal_samples, 8)
    