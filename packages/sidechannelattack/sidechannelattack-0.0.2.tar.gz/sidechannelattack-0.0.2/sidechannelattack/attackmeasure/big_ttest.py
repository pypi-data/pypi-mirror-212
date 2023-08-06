import numpy as np
from new_math import var_func, mean_func
from  matplotlib import pyplot as plt
from tqdm import tqdm, trange
import numba as nb
def block_ttest(n,url_trace):
    '''

    :param n: 因数据量大  分块数
    :param Na: 序号奇数的曲线数量
    :param Nb: 序号偶数的曲线数量
    :param N: 每条曲线的采样点
    :return:奇偶曲线的ttest结果
    '''
    # N= 2
    count = 0
    arr = np.load(url_trace + "process_arrPart0.npy")
    N = arr.shape[1]
    old_var_even = np.zeros(N)
    old_mean_even = np.zeros(N)
    old_var_odd = np.zeros(N)
    old_mean_odd = np.zeros(N)
    oddcount = 0
    evencount = 0
    for j in trange(n):
        # arr = np.load(r"D:/sidechannel/attackmeasure/1228trace1trace2/fast_lowpassarrPart{0}.npy".format(j))
        # arr = np.load('D:/sidechannel/attackmeasure/traces/temp.npy')


        # !!!!!!!!!
        # arr = np.load(r"D:/1222order1EditAlphaSboxMixAlphais1trace1trace2/yiwanarrPart{0}.npy".format(j))
        arr = np.load(r"G:/3.28/process_arrPart{0}.npy".format(j))
        # arr = np.load(r'G:/code1222order1trace1trace2alpha_sboxandmixalphaareuniqueandgoodhamming/passarrPart{0}.npy'.format(j))
        for i in range(arr.shape[0]):
            if count % 2 == 0:
                new_mean = old_mean_even + (arr[i] - old_mean_even) / (evencount + 1)
                new_var = old_var_even + ((arr[i] - old_mean_even) * (arr[i] - new_mean) - old_var_even) / (evencount + 1)
                old_mean_even = new_mean
                old_var_even = new_var
                evencount += 1
                count = count + 1
            else:
                new_mean = old_mean_odd + (arr[i] - old_mean_odd) / (oddcount + 1)
                new_var = old_var_odd + ((arr[i] - old_mean_odd) * (arr[i] - new_mean) - old_var_odd) / (oddcount + 1)
                old_mean_odd = new_mean
                old_var_odd = new_var
                oddcount += 1
                count = count + 1

    temp1 = old_mean_even-old_mean_odd
    # temp1 = old_mean_odd - old_mean_even
    temp2 = (old_var_even/evencount)+(old_var_odd/oddcount)
    test_result = temp1 / np.sqrt(temp2)
    return test_result



def block_average(n,N):
    count = 0
    old_mean_even = np.zeros(N)
    for j in trange(n):
        arr = np.load(r"G:/order1EditAll1/passarrPart{0}.npy".format(j))
        for i in range(arr.shape[0]):
            new_mean = old_mean_even + (arr[i] - old_mean_even) / (count + 1)
            old_mean_even = new_mean
            count = count + 1
    return old_mean_even/2




@nb.jit
def fast_lowpass(traces,a):
    # if not isinstance(traces, np.ndarray):
    #     raise TypeError("'trace' should be a numpy ndarray.")

    new_traces = np.zeros((traces.shape[0],traces.shape[1]), dtype=float)
    # point_list = []
    for t in range(traces.shape[0]):
        for i in range(0,traces.shape[1]):
            if i == 0:
                new_traces[t][0] = traces[t][0]
            else:
                new_traces[t][i] = (a*traces[t][i-1]+traces[t][i])/(1+a)
    return new_traces
# @nb.jit
# def fast_lowpass(traces,a):
#     new_traces = np.zeros(len(traces), dtype=float)
#     for i in range(0, len(traces)):
#         if i == 0:
#             new_traces[0] = traces[0]
#         else:
#             new_traces[i] = (a * traces[i - 1] + traces[i]) / (1 + a)
#     return new_traces
def ttest(t1,t2):
    Na = t1.shape[0]
    Nb = t2.shape[0]
    temp1 = mean_func(t1)-mean_func(t2)
    temp2 = (var_func(t1) / Na) + (var_func(t2) / Nb)
    test_result = temp1/np.sqrt(temp2)
    return test_result
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
@nb.jit
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

    #xiangliang1 = fast_lowpass(xiangliang, 50)
    plt.rcParams['figure.figsize'] = (12.0, 4.0)
    f, ax = plt.subplots(1, 1)
    #xiangliang是一条曲线，最终结果，是对所有曲线按照列做mean
    #注意block_average里的路径要和block_ttest里的路径是一样的
    # xiangliang= block_average(200, 21000)
    # arr1 = np.load(r'd:/process_arrPart0.npy')
    # arr2 = np.load(r'd:/process_arrPart1.npy')


    # np.save(r'G:/trace/process_arrPart{0}.npy'.format(j),tracepass1)
    #c = np.r_[arr1, arr2]

    #final = np.mean(c,axis=0)
    #plt.plot(final[0:-700])
    # xiangliangt = ttest(arr1,arr2)
    #ttest结果
    xiangliangt = block_ttest(100)
    # np.save(r'D:/sidechannel/result/order1EditAll1.npy', xiangliangt)
    # plt.plot(xiangliang)
    # xiangliang = np.load(r"D:/sidechannel/result/bestorder2trace12.npy")

    # plt.plot(xiangliang[0:-750]/120)
    plt.plot(xiangliangt)
    plt.grid()
    ax.axhline(y=4.5, ls='--', c='red')
    ax.axhline(y=-4.5, ls='--', c='red')
    # plt.plot(xiangliang[0:20200])
    # plt.axhline(y=4.5, ls='--', c='red', linewidth=4)
    # plt.axhline(y=-4.5, ls='--', c='red', linewidth=4)
    plt.show()