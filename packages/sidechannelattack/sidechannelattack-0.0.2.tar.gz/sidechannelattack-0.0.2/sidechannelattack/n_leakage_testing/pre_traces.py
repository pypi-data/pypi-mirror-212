from scipy import signal
import numpy as np
from tqdm import tqdm, trange
import numba as nb

np.seterr(divide='ignore', invalid='ignore')


@nb.jit
def to_one2(traces):
    if not isinstance(traces, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0], traces.shape[1]), dtype=float)
    a = np.mean(traces, axis=0)
    for t in range(traces.shape[0]):

        # s = np.std(traces[t])
        new_traces[t] = (traces[t] - a)
    return new_traces

# @cuda.jit
def LowPass(trace, frequency, cutoff, axis=-1, precision='float32'):
    if not isinstance(trace, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if not isinstance(frequency, int) and not isinstance(frequency, float):
        raise TypeError("'frequency' should be an of int or float type.")
    if frequency <= 0:
        raise ValueError("'frequency' should be positive.")
    b, a = signal.butter(3, 2 * cutoff / frequency, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, trace)
    return filtedData



@nb.jit
def moving_resamples(traces, k):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0], traces.shape[1] // k), dtype=float)
    if k >= traces.shape[1]:
        raise ValueError('window is too bigooo!')
    n = traces.shape[1]
    for t in range(traces.shape[0]):
        list = []
        # //地板除
        for i in range(n // k):
            sum = 0
            for j in range(i * k, i * k + k):
                sum = traces[t][j] + sum
            a = sum / k
            list.append(a)
        new_traces[t] = np.array(list)
    return new_traces



if __name__ == '__main__':

    # 文件路径
    url_trace = r"H:/zhoujiayun3/"
    # 原始文件名
    trace_name = ""
    # 要保存的文件名
    pre_trace_name = ""
    # 板子采样率
    sample_rate = 12e6
    # 低通滤波值
    filter_value = 2e6
    # 文件块数
    num_file_blocks = 100


    for j in trange(num_file_blocks):
        arr = np.load(url_trace+trace_name+r"{0}.npy".format(j))
        tracetoone = moving_resamples(arr, 10)
        tracepass1 = to_one2(tracetoone)
        # 此为低通滤波
        tracepass = LowPass(tracepass1, sample_rate, filter_value)
        np.save(url_trace+pre_trace_name+r'{0}.npy'.format(j), tracepass)
