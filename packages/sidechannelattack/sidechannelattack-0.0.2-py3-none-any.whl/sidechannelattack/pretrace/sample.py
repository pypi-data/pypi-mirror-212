import numpy as np
from scipy.fftpack import fft
# import matplotlib.pyplot as plt
# Fs =10e3      # 采样频率
# f1 =390       # 信号频率1
# f2 = 2e3      # 信号频率2
# t=np.linspace(0,1,Fs)   # 生成 1s 的实践序列
# noise1 = np.random.random(10e3)      # 0-1 之间的随机噪声
# noise2 = np.random.normal(1,10,10e3)
# #产生的是一个10e3的高斯噪声点数组集合（均值为：1，标准差：10）
# y=2*np.sin(2*np.pi*f1*t)+5*np.sin(2*np.pi*f2*t)+noise2
#
# def FFT (Fs,data):
#     L = len (data)                        # 信号长度
#     N =np.power(2,np.ceil(np.log2(L)))    # 下一个最近二次幂
#     FFT_y1 = np.abs(fft(data,N))/L*2      # N点FFT 变化,但处于信号长度
#     Fre = np.arange(int(N/2))*Fs/N        # 频率坐标
#     FFT_y1 = FFT_y1[range(int(N/2))]      # 取一半
#     return Fre, FFT_y1
#
# Fre, FFT_y1 = FFT(Fs,y)
# plt.figure
# plt.plot(Fre,FFT_y1)
# plt.grid()
# plt.show()




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
    for i in range(0,t-r):
        tr_correct = correlation_func(initialtrace[i:i+r-1],ref)
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
        newref_trace[len(reftrace)+n+1:len(reftrace)] = mean_trace[-n+1:len(reftrace)]
        newref_trace[0:len(reftrace)+n] = reftrace[-n:len(reftrace)]
    return newref_trace
if __name__ == '__main__':
    pass