from scipy import signal
import numpy as np
from fastdtw import fastdtw
# from base import get_trace_sample
from find_peaks import *
import scipy.stats as stats
import matplotlib.pyplot as plt
# from attackmeasure.new_math import var_func,mean_func,correlation_func

# # 在噪声加入的情况下表现不好，但可以同步曲线  目前是两个曲线要等长
# def align_traces(ref, trace):
#     N = trace.shape[1]
#     r = 1
#     aref = np.array(list(ref))
#     atrace = np.array(list(trace))
#     dist, path = fastdtw(aref, atrace, radius=r, dist=None)
#     px = [x for x, y in path]
#     py = [y for x, y in path]
#     n = [0] * N
#     s = [0.0] * N
#     for x, y in path:
#         s[x] += trace[y]
#         n[x] += 1
#
#     ret = [s[i] / n[i] for i in range(N)]
#     return ret
def correlation_func(data,traces):
    if data.ndim == 1:
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
        for i in range(traces.shape[0]-1):
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
                    (data[i + 1] - old_mean_data[i]) * (data[i + 1] - new_mean_data[i + 1]) - old_var_data[i]) / (i + 1)
            new_var_traces[i + 1] = old_var_traces[i] + (
                        (traces[i + 1] - old_mean_traces[i]) * (traces[i + 1] - new_mean_traces[i + 1]) - old_var_traces[i]) / (i + 1)
            new_cov[i+1] = (old_cov[i]*i + (data[i+1]-old_mean_data[i])*(traces[i+1]-new_mean_traces[i+1]))/(i+1)

            old_cov[i + 1] = new_cov[ i + 1]
            old_var_traces[i + 1] = new_var_traces[i + 1]
            old_var_data[i + 1] = new_var_data[i + 1]
        # print(new_cov[i+1],new_var_traces[i + 1],new_var_data[i + 1])
        return new_cov[i+1]/np.sqrt(new_var_traces[i + 1]*new_var_data[i + 1])
def mean_func(traces):
    # n = 0
    if traces.ndim == 1:
        old_mean = np.zeros(len(traces))
        new_mean = np.zeros(len(traces))
        for i in range(len(traces)-1):
            old_mean[0] = traces[0]
            new_mean[i + 1] = old_mean[i] + (traces[i] - old_mean[i]) / (i + 1)
            old_mean[i + 1] = new_mean[i + 1]
        return new_mean[i + 1]
    if traces.ndim ==2:
        old_mean = np.zeros((traces.shape[0],traces.shape[1]))
        new_mean = np.zeros((traces.shape[0], traces.shape[1]))
        for i in range(traces.shape[0]-1):
            # n = n+1
            old_mean[0] = traces[0]
            new_mean[i+1] = old_mean[i] + (traces[i] - old_mean[i]) / (i + 1)
            old_mean[i+1] = new_mean[i+1]
        return new_mean[i+1]

def corelation_align(traces,initialtrace,reftrace,leftmin, rightmax):
    # initialtrace为参照曲线   othertraces为其他曲线
    if not isinstance(initialtrace, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if not isinstance(reftrace, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    # ref因该为另一曲线的一部分
    ref = reftrace[leftmin:rightmax]
    t = len(initialtrace)
    r = len(ref)
    correct_list = []
    # for i in range(0,t-r+1):
    #     tr_correct = correlation_func(traces[i:i+r],reftrace)
    for i in range(0,t-r+1):
        tr_correct = correlation_func(initialtrace[i:i+r],ref)
        correct_list.append(tr_correct)
    # 从左到右遇到的第一个极大相关性值   因为其中一条曲线为所有采样点，故np.argmax即可代表两条曲线偏差
    m = np.argmax(correct_list)
    n = m-leftmin
    # 初始化对其之后的曲线
    newref_trace = np.zeros(len(reftrace))
    # 因为用到均值填充
    mean_trace = mean_func(traces)
    if n==0:
        newref_trace = reftrace
    if n>0:
        newref_trace[0:n-1] = mean_trace[0:n-1]
        newref_trace[n:len(reftrace)] = reftrace[0:len(reftrace)-n]
    if n<0:
        newref_trace[len(reftrace)+n+1:len(reftrace)] = mean_trace[len(reftrace)+n+1:len(reftrace)]
        newref_trace[0:len(reftrace)+n] = reftrace[-n:len(reftrace)]
    return newref_trace
# def aligner(traces):/
    # new_traces =
if __name__ == '__main__':

    trace1 = np.load(r"G:/py+idea/python/sidechannel/attackmeasure/antrace.npy")
    t1 = trace1[0]
    t2 = trace1[1][250:500]
    print(corelation_align(trace1,trace1[0],trace1[1],250,500))
    plt.plot(corelation_align(trace1,trace1[0],trace1[1],250,500))
    plt.show()




