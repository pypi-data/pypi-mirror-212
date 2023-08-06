# 基本示例
def online_mean(old_mean, new_x, N):
    new_mean = old_mean + (new_x - old_mean) / (N + 1)
    return new_mean
def welford(old_var, old_mean, new_x, new_mean):
    new_var = old_var + ((new_x - old_mean) * (new_x - new_mean) - old_var) / (N + 1)
    return new_var
# def tt_mean(traces):
#     # 都是按列的
#     t_sum = np.zeros(traces.shape[1])
#     t_num = traces.shape[0]
#     aver_mean = np.zeros(traces.shape[1])
#     n = 0
#     for t in range(t_num):
#         n = n+1
#         t_sum = aver_mean*(n-1)+traces[t,:]
#         aver_mean = t_sum/n
#     return aver_mean
# def tt_var(traces):
#     return tt_mean(traces**2)-(tt_mean(traces))**2
# def calc_corr(a, b):
#     a_avg = sum(a) / len(a)
#     b_avg = sum(b) / len(b)
#     # 计算分子，协方差————按照协方差公式，本来要除以n的，由于在相关系数中上下同时约去了n，于是可以不除以n
#     cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
#     # 计算分母，方差乘积————方差本来也要除以n，在相关系数中上下同时约去了n，于是可以不除以n
#     sq = math.sqrt(sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b]))
#     corr_factor = cov_ab / sq
#     return corr_factor
# def cor(data,trace1):
#     list = []
#     for t in range(trace1.shape[1]):
#         a = calc_corr(data,trace1[:,t])
#         list.append(a)
#     return np.array(list)
import numpy as np
from numpy import loadtxt
# 读入曲线

# 求矩阵均值按列
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

# 求矩阵方差，按行
def var_func(traces):
    if traces.ndim == 1:
        old_var = np.zeros(len(traces))
        new_var = np.zeros(len(traces))
        old_mean = np.zeros(len(traces))
        new_mean = np.zeros(len(traces))
        for i in range(len(traces) - 1):
            # 初始化
            old_var[0] = 0
            old_mean[0] = traces[0]

            # 需要的均值
            new_mean[i + 1] = old_mean[i] + (traces[i] - old_mean[i]) / (i + 1)

            # 均值的更新
            old_mean[i + 1] = new_mean[i + 1]


            new_var[i + 1] = old_var[i] + ((traces[i + 1] - old_mean[i]) * (traces[i + 1] - new_mean[i + 1]) - old_var[i]) / (i + 1)
            old_var[i + 1] = new_var[i + 1]
        return new_var[i + 1]
    if traces.ndim == 2:
        old_var = np.zeros((traces.shape[0], traces.shape[1]))
        new_var = np.zeros((traces.shape[0], traces.shape[1]))
        old_mean = np.zeros((traces.shape[0], traces.shape[1]))
        new_mean = np.zeros((traces.shape[0], traces.shape[1]))
        for i in range(traces.shape[0]-1):
            old_var[0] = np.zeros(traces.shape[1])
            old_mean[0] = traces[0]
            new_mean[i + 1] = old_mean[i] + (traces[i] - old_mean[i]) / (i + 1)
            old_mean[i + 1] = new_mean[i + 1]
            new_var[i+1] = old_var[i] + ((traces[i+1] - old_mean[i]) * (traces[i+1] - new_mean[i+1]) - old_var[i]) / (i + 1)
            old_var[i+1] = new_var[i+1]
        return new_var[i+1]


# 求一条data和trace每列的协方差
def cov_func(data,traces):

    if data.ndim == 1 and traces.ndim ==2:
        old_cov = np.zeros((traces.shape[0], traces.shape[1]))
        new_cov = np.zeros((traces.shape[0], traces.shape[1]))
        old_mean_data = np.zeros(len(data))
        new_mean_data = np.zeros(len(data))
        old_mean_traces = np.zeros((traces.shape[0], traces.shape[1]))
        new_mean_traces = np.zeros((traces.shape[0], traces.shape[1]))

        for i in range(traces.shape[0]-1):
            # 初始化
            old_cov[0] = np.zeros(traces.shape[1])
            old_mean_data[0] = data[0]
            old_mean_traces[0] = traces[0]

            # 需要的均值
            new_mean_data[i + 1] = old_mean_data[i] + (data[i] - old_mean_data[i]) / (i + 1)
            new_mean_traces[i + 1] = old_mean_traces[i] + (traces[i] - old_mean_traces[i]) / (i + 1)

            # 均值的更新
            old_mean_data[i + 1] = new_mean_data[i + 1]
            old_mean_traces[i + 1] = new_mean_traces[i + 1]
            # 注意这里的i值
            # 协方差的计算
            new_cov[i+1] = (old_cov[i]*i + (data[i+1]-old_mean_data[i])*(traces[i+1]-new_mean_traces[i+1]))/(i+1)

            print(old_cov[i])
            # 协方差更新
            old_cov[i+1] = new_cov[i+1]
            # print(old_cov[i+1],data[i+1]-old_mean_data[i])
        return new_cov[i+1]
    if data.ndim == 1 and traces.ndim ==1:
        old_cov = np.zeros(len(traces))
        new_cov = np.zeros(len(traces))
        old_mean_data = np.zeros(len(data))
        new_mean_data = np.zeros(len(data))
        old_mean_traces = np.zeros(len(traces))
        new_mean_traces = np.zeros(len(traces))

        for i in range(traces.shape[0]-1):
            # 初始化
            old_cov[0] = 0
            old_mean_data[0] = data[0]
            old_mean_traces[0] = traces[0]

            # 需要的均值
            new_mean_data[i + 1] = old_mean_data[i] + (data[i] - old_mean_data[i]) / (i + 1)
            new_mean_traces[i + 1] = old_mean_traces[i] + (traces[i] - old_mean_traces[i]) / (i + 1)

            # 均值的更新
            old_mean_data[i + 1] = new_mean_data[i + 1]
            old_mean_traces[i + 1] = new_mean_traces[i + 1]
            # 注意这里的i值
            # 协方差的计算
            new_cov[i+1] = (old_cov[i]*i + (data[i+1]-old_mean_data[i])*(traces[i+1]-new_mean_traces[i+1]))/(i+1)

            # print(old_cov[i])
            # 协方差更新
            old_cov[i+1] = new_cov[i+1]
            # print(old_cov[i+1],data[i+1]-old_mean_data[i])
        return new_cov[i+1]



# 求一条data和trace每列的相关系数
def correlation_func(data,traces):


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


    if data.ndim == 1 and traces.ndim == 1:
        old_cov = np.zeros(len(traces))
        new_cov = np.zeros(len(traces))
        old_mean_data = np.zeros(len(data))
        new_mean_data = np.zeros(len(data))
        old_mean_traces = np.zeros(len(traces))
        new_mean_traces = np.zeros(len(traces))
        old_var_data = np.zeros(len(data))
        new_var_data = np.zeros(len(data))
        old_var_traces = np.zeros(len(traces))
        new_var_traces = np.zeros(len(traces))
        for i in range(traces.shape[0]-1):
            old_cov[0] = 0
            old_mean_data[0] = data[0]
            old_var_data[0] = 0
            old_var_traces[0] = 0
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

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    data = np.load(r"G:/py+idea/python/sidechannel/attackmeasure/traces/SendData.npy")
    trace = np.load(r"G:/py+idea/python/sidechannel/attackmeasure/traces/0x01.npy")
    # print(data.shape, trace.shape)
    # print(cov_func(data, trace[0]))
    plt.plot(abs(correlation_func(data, trace[0])))
    plt.show()


