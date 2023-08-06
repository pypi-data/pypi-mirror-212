import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt


def t_test(n, url_trace):
    '''
    :instrctions:even  and  odd 间或采集
    :param n: blocks of traces
    :param N: sample numbers
    :return: result
    '''
    arr = np.load(url_trace + r"arrPart0.npy")
    count = 0
    N = arr.shape[1]
    old_var_even = np.zeros(N)
    old_mean_even = np.zeros(N)
    old_var_odd = np.zeros(N)
    old_mean_odd = np.zeros(N)
    oddcount = 0
    evencount = 0
    for j in trange(n):
        arr = np.load(url_trace + r"arrPart{0}.npy".format(j))
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

#
# def plt_t_test(all_kinds_of_results):
#     plt.rcParams['figure.figsize'] = (12.0, 7.0)
#     f, ax = plt.subplots(1, 1)
#     plt.plot(t_test(200, url_trace))
#     ax.axhline(y=4.5, ls='--', c='red', linewidth=2)
#     ax.axhline(y=-4.5, ls='--', c='red', linewidth=2)
#     plt.show()


import numba as nb
import time


# @nb.jit
# def initial_tranform():
#     new_arr = np.zeros((45000, 7500), dtype=np.float32)
#     # for i in trange(int(1800000 / 45000)):
#     # 一共有多少块
#     m = 8
#     for i in trange(int(18000000 / 45000)):
#         for j in trange(300):
#             arr1 = np.load(r"G:/io_redo_share5_edit_synchronized/process_arrPart{0}.npy".format(j)).T
#             new_arr[:, 25 * j:25 * j + 25] = arr1[0:45000]
#         np.save(r'E:/D/new_arr{0}.npy'.format(i), new_arr)
# def transform():
#     new_arr = np.zeros((1800000, 50), dtype=np.float32)
#     # for i in trange(int(1800000 / 45000)):
#     # 一共有多少块
#     # m = 8
#     for i in trange(int(300/2)):
#         # 第一轮几块拼接
#         for j in range(2):
#             # start = time.time()
#             arr1 = np.load(r"G:/io_redo_share5_edit_synchronized/process_arrPart{0}.npy".format(j+i*2)).T
#             # arr = np.concatenate((arr1, arr2), axis=1)
#             new_arr[:, 25 * j:25 * j + 25] = arr1
#         # print(i)
#         for k in range(int(1800000 / 90000)):
#             np.save(r'D:/1/transform{0}_pre_arrPart{1}.npy'.format(i, k), new_arr[90000*k:90000*k+90000])
# def pinjie_function():
#     new_arr = np.zeros((90000, 7500), dtype=np.float32)
#     for i in trange(int(1800000/90000)):
#         for j in range(int(300/2)):
#             arr1 = np.load(r"D:/1/transform{0}_pre_arrPart{1}.npy".format(j, i))
#             # arr1 = np.load(r"E:/D/transform{0}_arrPart{1}.npy".format(j,i))
#             # arr = np.concatenate((arr1, arr2), axis=1)
#             new_arr[:, 50 * j:50 * j + 50] = arr1
#         np.save(r'D:/1/new_arr{0}.npy'.format(i), new_arr)

if __name__ == '__main__':
    # url_trace = r"H:/traceaes2/"
    # plt.rcParams['figure.figsize'] = (12.0, 7.0)
    # f, ax = plt.subplots(1, 1)
    # ax.axhline(y=4.5, ls='--', c='red', linewidth=2)
    # ax.axhline(y=-4.5, ls='--', c='red', linewidth=2)
    # result = t_test(100, url_trace)
    # # np.save(r'G:/side_channel_attack/side_channel_attack/pre_result3.npy', result )
    # # result = np.load(r'G:/side_channel_attack/result_io_redo_share5_edit_synchronized.npy')
    # # print(t_test(1,url_trace))
    # # print(np.argmax(result))
    # plt.plot(result)
    # # arr = np.load(r"H:/traceaes2/arrPart0.npy")
    # # print(arr.shape)
    # plt.show()
    # import time
    # initial_tranform()
    # transform()
    # pinjie_function()
    import gc
    import time
    start= time.time()
    arr = np.load(r"G:/io_redo_share5_edit_synchronized/process_arrPart299.npy")
    arr2 = np.load(r'D:/1/new_arr0.npy')
    # arr1 = np.load(r"G:/io_redo_share5_edit_synchronized/process_arrPart299.npy")
    print(time.time()-start)
    # print(arr[0])
    print(arr)
    print(arr.shape)
    print(arr2.shape)
    print(arr2)
    # #
    # arr = np.load(
    #     r"H:/io_redo_share5_edit_synchronized/io_redo_share5_edit_synchronizedarrPart0.npy")
    # start = time.time()
    # arr2 = arr.T
    # print(time.time() - start)
    # print(arr2.shape)
    # print(arr2[0:25, 0])
    #
    # arr1 = np.load(
    #     r"H:/io_redo_share5_edit_synchronized/transform_arrPart0.npy")
    # print(arr1.shape)
    # print(arr1[0, 2400:2501])
