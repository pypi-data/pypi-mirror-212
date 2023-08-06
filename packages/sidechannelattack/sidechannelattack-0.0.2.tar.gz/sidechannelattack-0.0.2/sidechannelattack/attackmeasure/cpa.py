import numpy as np
import time

# np.nanmax:排除nan值求最大
np.seterr(divide='ignore', invalid='ignore')
from numba import njit, jit


# @jit
def correlation_func(data, traces):
    """

    :param data: 用于参与计算的中间值
    :param traces: 用于参与计算的曲线集
    :return: data和traces每一列的相关性
    """
    if data.ndim == 1 and traces.ndim == 2:
        old_cov = np.zeros((traces.shape[0], traces.shape[1]))
        new_cov = np.zeros((traces.shape[0], traces.shape[1]))
        old_mean_data = np.zeros(len(data))
        new_mean_data = np.zeros(len(data))
        old_mean_traces = np.zeros((traces.shape[0], traces.shape[1]))
        new_mean_traces = np.zeros((traces.shape[0], traces.shape[1]))
        old_var_data = np.zeros(len(data))
        new_var_data = np.zeros(len(data))
        old_var_traces = np.zeros((traces.shape[0], traces.shape[1]))
        new_var_traces = np.zeros((traces.shape[0], traces.shape[1]))
        for i in range(traces.shape[0] - 1):
            old_cov[0] = np.zeros(traces.shape[1])
            old_mean_data[0] = data[0]
            old_var_data[0] = 0
            old_var_traces[0] = np.zeros(traces.shape[1])
            old_mean_traces[0] = traces[0]
            new_mean_data[i + 1] = old_mean_data[i] + (data[i] - old_mean_data[i]) / (i + 1)
            new_mean_traces[i + 1] = old_mean_traces[i] + (traces[i] - old_mean_traces[i]) / (i + 1)
            old_mean_data[i + 1] = new_mean_data[i + 1]
            old_mean_traces[i + 1] = new_mean_traces[i + 1]
            new_var_data[i + 1] = old_var_data[i] + (
                    (data[i + 1] - old_mean_data[i]) * (data[i + 1] - new_mean_data[i + 1]) - old_var_data[i]) / (
                                          i + 1)
            new_var_traces[i + 1] = old_var_traces[i] + (
                    (traces[i + 1] - old_mean_traces[i]) * (traces[i + 1] - new_mean_traces[i + 1]) -
                    old_var_traces[i]) / (i + 1)
            new_cov[i + 1] = (old_cov[i] * i + (data[i + 1] - old_mean_data[i]) * (
                    traces[i + 1] - new_mean_traces[i + 1])) / (i + 1)

            old_cov[i + 1] = new_cov[i + 1]
            old_var_traces[i + 1] = new_var_traces[i + 1]
            old_var_data[i + 1] = new_var_data[i + 1]
        return np.absolute(new_cov[i + 1] / np.sqrt(new_var_traces[i + 1] * new_var_data[i + 1]))


# def correction(self, data, traces):
#     if traces.shape[0] != data.shape[0]:
#         raise ValueError("they should have same imediate value.")
#     if not isinstance(traces, np.ndarray):
#         raise TypeError("'data' should be a numpy ndarray.")
#     if not isinstance(data, np.ndarray):
#         raise TypeError("'data' should be a numpy ndarray.")
#     d_sum = 0.0
#     d2_sum = 0.0
#     t_sum = np.zeros(traces.shape[1])
#     t2_sum = np.zeros(traces.shape[1])
#     dt_sum = np.zeros(traces.shape[1])
#     tempt_sum = np.zeros(traces.shape[1])
#     tempdt_sum = np.zeros(traces.shape[1])
#     tempt2_sum = np.zeros(traces.shape[1])
#     correct_array = []
#     D = len(data)
#     n = 0
#
#     for i in range(traces.shape[0]):
#         n += 1
#
#         t_sum = tempt_sum * (n - 1) + traces[i, :]
#         tempt_sum = t_sum/n
#         t2_sum = tempt2_sum * (n-1)+(traces ** 2)[i, :]
#         tempt2_sum = t2_sum/n
#         dt_sum = tempdt_sum * (n-1)+(data[i] * traces[i])
#         tempdt_sum = dt_sum/n
#     # temp1 = 0
#     temp2 = 0
#     temp3 = 0
#     d_sum = np.sum(data)
#     d2_sum = np.sum(data**2)
#     temp1 = np.sqrt(D * d2_sum - d_sum ** 2)
#     temp2 = np.sqrt(D * t2_sum - t_sum ** 2)
#     temp3 = D * dt_sum - d_sum * t_sum
#     # temp1 = np.sqrt(var_func(data))
#     # temp2 = np.sqrt(var_func(traces))
#     # temp1 = np.sqrt(np.var(data))
#     # temp2 = np.sqrt(np.var(traces,axis=0))
#     correct_array = temp3/(temp1*temp2)
#     # print(temp1*temp2)
#     return correct_array
def one_key_guess(data, traces):
    one_key_guess_matrix = []
    for i in range(data.shape[1]):
        n = correlation_func(data[:, i], traces)
        one_key_guess_matrix.append(n)
    m = np.max(one_key_guess_matrix)
    t = np.where(one_key_guess_matrix == m)
    return t[0]


# np.argmax   np.where  np.max
if __name__ == '__main__':
    from numpy import loadtxt
    import math
    import matplotlib.pyplot as plt

    data = np.load(r"G:/py+idea/python/sidechannel/attackmeasure/traces/SendData.npy")
    trace = np.load(r"G:/py+idea/python/sidechannel/pretrace/mtraces/m0x01evenodd.npy")
    # print(data,trace)
    s_time = time.time()
    print(correlation_func(data, trace))

    e_time = time.time()
    print(e_time - s_time)
    plt.plot(correlation_func(data, trace))
    plt.show()
