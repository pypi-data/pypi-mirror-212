import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm, trange

def prepare_data(url_trace, trace_name, url_data, data_name, n,loadData):
    m = {}
    v = {}
    trace = np.load(url_trace + data_name+ r"0.npy")
    count_temp = np.zeros(300, dtype=np.int32)
    for i in loadData:
        m[i] = np.zeros(trace.shape[1])
        v[i] = np.zeros(trace.shape[1])
    for j in trange(n):
        data = np.loadtxt(url_data + data_name + r"{0}.txt".format(j), delimiter=',', dtype="int")
        # print(data)
        trace = np.load(url_trace +trace_name+ r"{0}.npy".format(j))
        for count, label in enumerate(data):
            # d[label].append(trace[count])
            old_mean = m[label]

            m[label] = m[label] + (trace[count] - m[label]) / (count_temp[label] + 1)
            v[label] = v[label] + ((trace[count] - old_mean) * (trace[count] - m[label]) - v[label]) / (
                    count_temp[label] + 1)
            count_temp[label] += 1
    signal = []
    noise = []
    for i_ in loadData:
        signal.append(m[i_])
    for j_ in loadData:
        noise.append(v[j_])
    signal_var = np.var(signal, axis=0)
    noise_mean = np.mean(noise, axis=0)
    return signal_var / noise_mean

def snr_function(n,url_trace,trace_name,url_data,data_name):
    plt.rcParams['figure.figsize'] = (12.0, 4.0)
    f, ax = plt.subplots(1, 1)
    ax.set_title('snr_traces')
    list = (np.unique(np.loadtxt(url_data + data_name+r"0.txt", delimiter=',', dtype="int"))).tolist()
    for i in range(n - 1):
        dataaaa = np.loadtxt(url_data + data_name + r"{0}.txt".format(i + 1), delimiter=',', dtype="int")
        num = (np.unique(dataaaa)).tolist()
        list = list + num
    loadData = (np.unique(list))
    result_data = prepare_data(url_trace, trace_name, url_data, data_name, n,loadData)
    ax.plot(result_data)
    plt.show()


if __name__ == '__main__':
    '''
    确定文件路径，名字，块数    
    '''
    url_trace = r"H:/zhoujiayun4/"
    url_data = r"H:/zhoujiayun4/"
    data_name = "aaadata"
    trace_name = "arrPart"
    n = 100




    # 运行此函数
    snr_function(n,url_trace,trace_name,url_data,data_name)

