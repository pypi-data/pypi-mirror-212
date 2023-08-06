import numpy as np

from  matplotlib import pyplot as plt
from attackmeasure.new_math import mean_func,var_func
np.seterr(divide='ignore',invalid='ignore')


def ttest(t1,t2):
    Na = t1.shape[0]
    Nb = t2.shape[0]
    temp1 = mean_func(t1)-mean_func(t2)
    temp2 = (var_func(t1) / Na) + (var_func(t2) / Nb)
    test_result = temp1/np.sqrt(temp2)
    return test_result
# def T_test(traces,)

def split_func(traces):
    if traces.ndim == 2:
        n = int(traces.shape[0] / 2)
        print(n)
        traceodd = np.zeros((n, traces.shape[1]))
        traceven = np.zeros((n, traces.shape[1]))
        odd = 0
        even = 0
        for i in range(traces.shape[0]):
            if i % 2 == 0:
                traceven[even] = traces[i]
                even = even + 1
            if (i + 1) % 2 == 0:
                traceodd[odd] = traces[i]
                odd = odd + 1
        return traceodd, traceven
    else:
        print("please check data's ndim")

if __name__ == '__main__':



    trace12 = np.load('D:/sidechannel/attackmeasure/traces/m1228trace3trace4.npy')


    plt.plot(ttest(split_func(trace12)[0],split_func(trace12)[1]))

    plt.show()
