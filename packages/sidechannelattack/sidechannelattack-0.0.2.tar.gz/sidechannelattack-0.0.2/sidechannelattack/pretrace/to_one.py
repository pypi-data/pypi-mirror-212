import numpy as np


def to_one(traces):
    if not isinstance(traces, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0],traces.shape[1]), dtype=float)
    for t in range(traces.shape[0]):
        a = np.mean(traces[t])
        s = np.std(traces[t])
        new_traces[t] = (traces[t]-a)/s
    return new_traces
def to_one2(traces):
    if not isinstance(traces, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0],traces.shape[1]), dtype=float)
    for t in range(traces.shape[0]):
        a = np.mean(traces[t])
        # s = np.std(traces[t])
        new_traces[t] = (traces[t]-a)
    return new_traces
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from pretrace import filter
    import random
    from numpy import loadtxt
    plt.subplot(211)
    plt.plot(to_one(loadTrace).T)
    plt.subplot(212)
    plt.plot(loadTrace.T)

    plt.show()
    print(loadTrace[0,0:10])
    print(to_one(loadTrace)[0,0:10])