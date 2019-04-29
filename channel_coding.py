from scipy.io import wavfile

import matplotlib
matplotlib.use("TkAgg")  # Fixing a bug of matplotlib on MacOS
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
plt.style.use('ggplot')








if __name__ == "__main__":

    # Plot of the sound signal
    sampling_rate, data = wavfile.read('sound.wav')
    plt.plot(data)
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time', fontsize=13)
    plt.title('Sample wav')
    plt.savefig('sound.eps')

    
    