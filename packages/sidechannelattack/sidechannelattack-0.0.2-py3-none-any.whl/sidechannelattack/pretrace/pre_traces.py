import numpy as np
from scipy import signal
import numpy as np
from tqdm import tqdm, trange
from numba import cuda
import numba as nb
import time
from pretrace.filter import fast_lowpass,LowPass
from pretrace.moving_average import moving_average
from  matplotlib import pyplot as plt
from pretrace.new_math import mean_func,var_func
from attackmeasure.to_one import to_one2
np.seterr(divide='ignore',invalid='ignore')
# import random
def moving_average(traces, window):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'data' should be a numpy ndarray.")
    new_traces = []
    for t in range(traces.shape[0]):
        list = []
        new_traces.append(list)
        for i in range(traces.shape[1] - window):
            sum = 0
            for j in range(i, i + window):
                sum = traces[t][j] + sum
            a = sum / window
            list.append(a)
    return np.array(new_traces)
@nb.jit
def to_one2(traces):
    if not isinstance(traces, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0],traces.shape[1]), dtype=np.float32)
    a = np.mean(traces, axis=0)
    for t in range(traces.shape[0]):

        # s = np.std(traces[t])
        new_traces[t] = (traces[t]-a)
    return new_traces
@nb.jit
def fast_lowpass(traces,a):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'trace' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0],traces.shape[1]), dtype=np.float32)
    # point_list = []
    for t in range(traces.shape[0]):
        for i in range(0,traces.shape[1]):
            if i == 0:
                new_traces[t][0] = traces[t][0]
            else:
                new_traces[t][i] = (a*traces[t][i-1]+traces[t][i])/(1+a)
    return new_traces
# @cuda.jit
def LowPass(trace, frequency, cutoff,  axis=-1, precision='float32'):
    if not isinstance(trace, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if not isinstance(frequency, int) and not isinstance(frequency, float):
        raise TypeError("'frequency' should be an of int or float type.")
    if frequency <= 0:
        raise ValueError("'frequency' should be positive.")
    b, a = signal.butter(3, 2 * cutoff / frequency, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, trace)
    return filtedData
@cuda.jit
def fast_lowpass_wanggeyibu(traces, a, new_traces):
    t = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x
    gridStride = cuda.gridDim.x * cuda.blockDim.x
    for j in range(t, traces.shape[0], gridStride):
        for i in range(0, traces.shape[1]):
            if i == 0:
                new_traces[t][0] = traces[t][0]
            else:
                new_traces[t][i] = (a * traces[t][i - 1] + traces[t][i]) / (1 + a)
@nb.jit
def moving_resamples(traces, k):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0], traces.shape[1] // k), dtype=np.float32)
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
def moving_resamples2(traces, k):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'data' should be a numpy ndarray.")
    new_traces = np.zeros((traces.shape[0], traces.shape[1] // k), dtype=np.float32)
    if k >= traces.shape[1]:
        raise ValueError('window is too bigooo!')
    n = traces.shape[1]
    for t in range(traces.shape[0]):
        list = []
        # //地板除
        for i in range(n // k):
            # sum = 0
            # for j in range(i * k, i * k + k):
            #     sum = traces[t][j] + sum
            # print(traces[t][i*k:i*(k+1)-1])
            a = np.mean(traces[t][i*k:i*(k+1)-1])
            list.append(a)
        new_traces[t] = np.array(list)
    return new_traces
def cut_func(traces,min = None,max = None):
    if traces.ndim == 1:
        new_traces  = traces[min:max]
        return new_traces
    if traces.ndim == 2:
        new_traces = np.zeros((traces.shape[0],max-min))
        for i in range(traces.shape[0]):
            new_traces[i] = traces[i][min:max]
        return new_traces
if __name__ == '__main__':
    # 对曲线进行处理  大量多组曲线
    for j in trange(300):
        # arr = np.load(r"D:/sidechannel/attackmeasure/1229afternoon/1229afternoonTrace1Trace2arrPart{0}.npy".format(j))
        # arr = np.load(r"G:/0103nightfixtrace3trace4/0103nightfixtrace3trace4arrPart{0}.npy".format(j+118))
        # arr = np.load(r"G:/code1222order1trace1trace2alpha_sboxandmixalphaareuniqueandgoodhamming/code1222order1trace1trace2alpha_sboxandmixalphaareuniqueandgoodhammingarrPart{0}.npy".format(j))
        arr = np.load(r"G:/io_redo_share5_edit_synchronized/io_redo_share5_edit_synchronizedarrPart{0}.npy".format(j))
        # # arr = np.load(r"D:/sidechannel/attackmeasure/1227traces3traces4/passarrPart{0}.npy".format(j))
        # # arr = np.load(r"D:/sidechannel/attackmeasure/1228trace1trace2/1228trace1trace2arrPart{0}.npy".format(j))
        # # arr = np.load(r"C:/1228trace1trace2/1229trace1trace2arrPart{0}.npy".format(j))
        tracetoone = moving_resamples(arr,10)
        tracepass1 = to_one2(tracetoone)
        tracepass =LowPass(tracepass1, 12e6,2e6)

        np.save(r'G:/io_redo_share5_edit_synchronized/process_arrPart{0}.npy'.format(j),tracepass1)
        # arr = np.load(r"D:/sidechannel/attackmeasure/1228trace1trace2/passarrPart{0}.npy".format(j))
        #
        # tracepass = fast_lowpass(arr,50)
        #
        # np.save('D:/1222order1EditAlphaSboxMixAlphais1trace1trace2/yiwanarrPart{0}.npy'.format(j), tracepass)
    # # 单独一组曲线
    # arr = np.load(r"G:/0103trace1trace2_5000tiao/0103trace1trace2.npy")
    # tracetoone = moving_resamples(arr, 50)
    # tracepass = to_one2(tracetoone)
    # np.save(r'G:/0103trace1trace2/passarrPart50.npy',tracepass)

    # print(cut_func(arr,0,10))

    # arr = np.load(r'G:/0103trace1trace2/passarrPart50.npy')
    # plt.plot(np.mean(arr,axis = 0))
    # plt.show()
    # arr = np.load(r"G:/trace/arrPart{0}.npy".format(j))
    #     # # arr = np.load(r"D:/sidechannel/attackmeasure/1227traces3traces4/passarrPart{0}.npy".format(j))
    #     # # arr = np.load(r"D:/sidechannel/attackmeasure/1228trace1trace2/1228trace1trace2arrPart{0}.npy".format(j))
    #     # # arr = np.load(r"C:/1228trace1trace2/1229trace1trace2arrPart{0}.npy".format(j))
    #     tracetoone = moving_resamples(arr,10)
    #     tracepass1 = to_one2(tracetoone)
    #     tracepass =LowPass(tracepass1, 120e6,24e6)
    #
    #     np.save(r'G:/trace/process_arrPart{0}.npy'.format(j),tracepass1)
    # arr = np.load(r"d:/arr.npy")
    # tracetoone = moving_resamples(arr, 10)
    # tracepass1 = to_one2(tracetoone)
    # tracepass =LowPass(tracepass1, 120e6,24e6)
    #
    # np.save(r'd:/process_arrPart0.npy',tracepass1)
    # # np.save(r'G:/trace/process_arrPart{0}.npy', tracepass1)
    # print(arr.shape)


