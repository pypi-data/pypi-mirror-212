import numpy as np
import matplotlib.pyplot as plt

class Dirac():
    def __init__(self, vector_length):
        self.vector_length = vector_length

    def generate(self, sample_size):
        dirac_x = np.zeros((sample_size, self.vector_length))
        for i in range(sample_size):
            dirac_x[i, np.random.randint(self.vector_length)] = 1
        return dirac_x
    
    def plot(self, dirac_x, save_path, n=10):
        fig, ax = plt.subplots(n, 1, figsize=(5, n))
        for i in range(n):
            ax[i].plot(dirac_x[i])
            ax[i].set_xticks([])
        plt.savefig(save_path)
        plt.close()