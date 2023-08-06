# import numpy as np
#
#
# def pca(traces, k):
#     n_samples, n_features = traces.shape
#     print(n_samples)
#     mean = np.array([np.mean(traces[:, i]) for i in range(n_features)])
#     norm_traces = traces - mean
#     scatter_matrix = np.dot(np.transpose(norm_traces), norm_traces)
#     eig_val, eig_vec = np.linalg.eig(scatter_matrix)
#     eig_pairs = [(np.abs(eig_val[i]), eig_vec[:, i]) for i in range(n_features)]
#     eig_pairs.sort(reverse=True)
#     feature = np.array([ele[1] for ele in eig_pairs[:k]])
#     data = np.dot(norm_traces, np.transpose(feature))
#     return data
import time

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


def pr_co_an(traces, k: int):
    if not isinstance(traces, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if k <= 0:
        raise ValueError("k can't <0")
    if k >= traces.shape[1]:
        raise ValueError("k is toooo big!!!")
    pca = PCA(n_components=k)
    pca.fit(traces)
    traces_new = pca.transform(traces)

    return np.array(traces_new)


if __name__ == '__main__':
    n = np.load('G:/py+idea/python/sidechannel/pretrace/aes_traces.npy')

    plt.plot(n.T)
    plt.show()
    print(pr_co_an(n, 1))
    print(n.shape)
