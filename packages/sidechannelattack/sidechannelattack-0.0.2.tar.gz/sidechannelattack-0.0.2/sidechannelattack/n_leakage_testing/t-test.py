#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sca 
@File    ：suiqian.py.py
@Author  ：suyang
@Date    ：2022/5/6 16:06 
'''
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm, trange
np.seterr(divide='ignore', invalid='ignore')
def t_test(n, url_trace, trace_name):
    '''
    :instrctions:even  and  odd 间或采集
    :param n: blocks of traces
    :param N: sample numbers
    :return: result
    '''
    # arr = np.load(url_trace + r"2process_arrPart0.npy")
    arr = np.load(url_trace + trace_name + r".npy")
    count = 0
    N = arr.shape[1]
    old_var_even = np.zeros(N)
    old_mean_even = np.zeros(N)
    old_var_odd = np.zeros(N)
    old_mean_odd = np.zeros(N)
    oddcount = 0
    evencount = 0
    for j in trange(n):
        # arr = np.load(url_trace + r"2process_arrPart{0}.npy".format(j))
        arr = np.load(url_trace + trace_name + r".npy")
        for i in range(arr.shape[0]):
            if count % 2 == 0:
                new_mean = old_mean_even + (arr[i] - old_mean_even) / (evencount + 1)
                new_var = old_var_even + ((arr[i] - old_mean_even) * (arr[i] - new_mean) - old_var_even) / (
                        evencount + 1)
                old_mean_even = new_mean
                old_var_even = new_var
                evencount += 1
                # print(evencount)
                count = count + 1
            else:
                new_mean = old_mean_odd + (arr[i] - old_mean_odd) / (oddcount + 1)
                new_var = old_var_odd + ((arr[i] - old_mean_odd) * (arr[i] - new_mean) - old_var_odd) / (oddcount + 1)
                old_mean_odd = new_mean
                old_var_odd = new_var
                oddcount += 1
                count = count + 1
    temp1 = old_mean_even - old_mean_odd
    temp2 = (old_var_even / evencount) + (old_var_odd / oddcount)
    test_result = temp1 / np.sqrt(temp2)
    return test_result

def ttest_function(num_file_blocks, url_trace, trace_name):
    '''

    :param num_file_blocks: data is too big for our computer so we design n blocks to reduce size
    :param url_trace: data stored
    :param trace_name: As the name suggests
    :return: result
    '''
    plt.rcParams['figure.figsize'] = (12.0, 4.0)
    f, ax = plt.subplots(1, 1)
    ax.set_title('ttest_traces')
    ax.axhline(y=4.5, ls='--', c='red', linewidth=2)
    ax.axhline(y=-4.5, ls='--', c='red', linewidth=2)
    result = t_test(num_file_blocks, url_trace, trace_name)
    ax.plot(result)
    plt.show()

if __name__ == '__main__':

    # 文件路径
    url_trace = r"C:/Users/DELL/Desktop/"
    # 文件块数
    num_file_blocks = 1
    # 文件名字
    trace_name = "AES_DPA_ATTACK_trace"
    # 运行函数
    ttest_function(num_file_blocks, url_trace, trace_name)




