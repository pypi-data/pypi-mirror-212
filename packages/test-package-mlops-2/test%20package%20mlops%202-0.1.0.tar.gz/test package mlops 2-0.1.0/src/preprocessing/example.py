import matplotlib.pyplot as plt
import numpy as np


def random_seq():
    return np.random.rand(12)

def plot_seq():
    plt.plot(random_seq)


if __name__ == '__main__':
    print(np.abs(12))