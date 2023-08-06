#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sca 
@File    ：zhoujiayun.py
@Author  ：suyang
@Date    ：2022/5/21 12:57 
'''
import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import tqdm, trange

# np.nanmax:排除nan值求最大
np.seterr(divide='ignore', invalid='ignore')
from numba import njit, jit

def getHW(byte):
    '''

    :param byte: input intermediate value
    :return: hw
    '''
    HW_table = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3,
                4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4,
                4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2,
                3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5,
                4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4,
                5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3,
                3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2,
                3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6,
                4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5,
                6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5,
                5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6,
                7, 7, 8]
    return HW_table[byte]
# all the attack need data matrix
def big_correlation_func(n, url_trace, trace_name,url_data,data_name):
    '''

    :param n: 变量的块数
    :param url_trace: 曲线集的路径
    :param url_data: 数据的路径
    :return:
    '''
    for i in trange(n):
        dataaaa = np.loadtxt(url_data + data_name + r"{0}.npy".format(i))
        for j in range(len(dataaaa)):
            dataaaa[j] = getHW(dataaaa[j])
        np.save(url_data + r"data_hw{0}.npy".format(i), dataaaa)
    arr = np.load(url_trace + trace_name+r"0.npy")
    # data = np.load(url_data + r"new_arrdata0.npy")
    Na = arr.shape[1]
    old_cov = np.zeros(Na)
    old_mean_data = 0
    old_mean_traces = np.zeros(Na)
    old_var_data = 0
    old_var_traces = np.zeros(Na)
    temp = 0
    for j in trange(n):
        data = np.load(url_data + r"data_hw{0}.npy".format(j))
        arr = np.load(url_trace + trace_name + r"{0}.npy".format(j))
        for i in range(arr.shape[0]):
            new_mean_data = old_mean_data + (data[i] - old_mean_data) / (temp + 1)
            new_mean_traces = old_mean_traces + (arr[i] - old_mean_traces) / (temp + 1)

            new_var_data = old_var_data + ((data[i] - old_mean_data) * (data[i] - new_mean_data) - old_var_data) / (
                    temp + 1)
            new_var_traces = old_var_traces + (
                    (arr[i] - old_mean_traces) * (arr[i] - new_mean_traces) - old_var_traces) / (temp + 1)
            new_cov = (old_cov * temp + (data[i] - old_mean_data) * (arr[i] - new_mean_traces)) / (temp + 1)
            old_mean_data = new_mean_data
            old_mean_traces = new_mean_traces
            old_cov = new_cov
            old_var_traces = new_var_traces
            old_var_data = new_var_data
            temp = temp + 1
    correlation_result = old_cov / np.sqrt(old_var_traces * old_var_data)
    return correlation_result

if __name__ == '__main__':
    # 文件块数
    n = 100
    # 所需数据所在文件夹的路径
    url_trace = r"H:/zhoujiayun1/"
    url_data = r"H:/zhoujiayun1/"
    # 所需数据的名字
    data_name = "data"
    trace_name = "data"


    #运行函数且绘图
    f, ax = plt.subplots(1, 1)
    ax.set_title('hw_cpa_traces')
    result = big_correlation_func(n, url_trace, trace_name,url_data,data_name)
    ax.plot(result)
    plt.show()

