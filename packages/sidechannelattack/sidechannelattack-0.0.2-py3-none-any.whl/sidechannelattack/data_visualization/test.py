

import numpy as np
import matplotlib.pyplot as plt
import math
def set_view_size():
    plt.rcParams['figure.figsize'] = (8.0, 5.0)
if __name__ == '__main__':
    # arr1 = np.load(r'G:/1222nightfixtrace1trace2/2passarrPart0.npy')
    # arr2 = np.load(r'G:/1222nightfixtrace1trace2/2passarrPart1.npy')
    #
    # c = np.r_[arr1, arr2]
    #
    # final = np.mean(c,axis=0)
    # plt.plot(final)
    # plt.plot
    # plt.show()
    # coding: utf-8
    # -*- coding: utf-8 -*-
    import matplotlib.pyplot as plt

    font = {'family': 'serif',
            'serif': 'Times New Roman',
            'weight': 'normal',
            'size': 10}
    plt.rc('font', **font)
    plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    import numpy as np
    import matplotlib

    matplotlib.use('Agg')
    # pre-datas
    # cpu-gpu data
    # x = [6,7,8,9,10,11,12,13,14]  # x坐标
    # y1 = [21.59,48.56,86.14,187,348,749,1503,2933,6158]
    # y2 = [0.038,0.0390,0.047,0.047,0.044693395495414734,0.049913520950675011,0.051549483,0.05133368819952011,0.097315166]
    # y3 = [0.037413,0.0379158,0.0388481,0.041645900000000236,0.0519861,0.06957389999999997,0.1303835,0.25849550000000043,0.5195418]
    # y1 = [math.log(i) for i in y1]
    # y2 = [math.log(i) for i in y2]
    # y3 = [math.log(i) for i in y3]
    # 3090数据
    # x2 = [8,10,12,14,16,18,20,22,24,26,28,30,32]
    # y3 = [0.084,0.335,0.334,0.335,0.349,1.345,4.586,17.01847,67.98268089,271.00827,1081.70429,4665.39687,19335.698]
    # plt.plot(x, y1, lw=1, c='red', marker='s', ms=4, label='Y1')  # 绘制y1
    # plt.plot(x, y2, lw=1, c='g', marker='o', label='Y2')  # 绘制y2
    # # plt-style
    plt.rcParams['figure.figsize'] = (8.0, 5.0)
    # plt.plot(x2, y3, lw=1, c='g', marker='o', label='3090')
    # # 3090vsa5000
    # x = np.arange(20,29)
    # print(x)
    # y1 = [4.586,9.034388803,17.01847,34.61620531,67.98268089,136.4040879,271.00827,538.931011,1081.70429]
    # y2 = [5.905,10.59633394,22.4578,43.52783444,88.9740035,170.8229839,354.2441238,684.173861,1411.98]
    # y3 = [29.7561074,61.9852,121.96354,249.3684,495.6821,997.6532,1929.071761,4000.5689,7985.6213]

    # 数据量对比
    # x = [ 2500,  5000,  7500, 10000 ,12500, 15000, 17500, 20000, 22500, 25000]
    # print(x)
    # y1 = [0.417184748,
    #       0.833898731,
    #       1.254282456,
    #       1.673678096,
    #       2.092893183,
    #       2.530636728,
    #       2.949789375,
    #       3.374336913,
    #       3.795304704,
    #       4.216747954,
    #       ]
    # y2 = [0.94917937526479363, 1.0802326649427414, 1.6194070130586624, 2.1585998740047216, 2.6978394212201238,
    #       3.237421770580113, 3.776169336400926, 4.315651622600853, 4.855445458553731, 5.394205478951335]
    # y3 = [3.3328059999999997, 5.9462735, 8.919919700000001, 11.890184700000002, 14.841762200000002, 17.8053917,
    #       20.770165600000006, 23.7380445, 26.705500400000005, 29.7185647]

    # 并行计算二维同一维计算对比


    # # y1 = [22.4,35.12,58.08,111.84,211.52,447.12,829.89,203*8]
    # # # y2 = [88.78,
    # # #       184.32,
    # # #       358.4,
    # # #       738.127412,
    # # #       1476.2548,
    # # #       2916.352,
    # # #       7408
    # # #       ]
    # # y2 = [62.5,61.25,90,110,162.5,321.25,605,1162.5,2325.6]
    # # y3 = [20.5,24.5,35.95,70.3,139.5,278,555.5,1110.5,2298.6]
    # # y4 = [42,52,71,107,167,328,649,1307.9,2563.1]
    # # 25 350.2532  26  699  27
    # # y2 = [0.086, 0.087, 0.0884, 0.0892, 0.1019, 0.1024, 0.170, 0.334, 0.675, 1.35, 2.69, 5.37, 10.78, 21.60,43.71,88.56,175.64]
    x2 = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    y2 = [0.009,0.0118,0.01149,0.011605,0.0114738,0.01687,0.017798,0.034875,0.0780571,0.136032,0.271097,0.54133698,1.0318,2.0627,
          4.13567,8.2090,16.4688,33.1292,62.56,128.456,256,512,1024,2012.56,4036.98]
    y2 = [math.log(i * 1250) for i in y2]
    # print(y2_)
    # # 12 46  16 390.66746520996094
    # y4 = [4.86, 7.42, 15.22, 23.68, 46.70, 92.36, 180.52, 362.54, 717.1, 1919.36, 5044.96, 10177.85, 21577.69, 51107.98,104700.2]
    x3 = np.arange(8,28)
    y3 = [1.339,1.507,2.65,4.75,9.73,17.83,35.7,70.62,141.92,282.8,565.9,1364.526,3009.14,5828.73,14327.58,27044.15,51207.89,205096.693,808750,4378125]
    y3 = [math.log(i) for i in y3]
    x4 = np.arange(8,21)
    y4 = [1903,2431,3296,5054,8355,15556,30561,63963.85,131398.4,275936.64,607060.608,1821181.8,4078125]
    y4 = [math.log(i) for i in y4]
    x1 = np.arange(8,15)
    y1 = [4.339,5.365,11.235,17.15,41.85,91.56,201.56]
    y1 = [math.log(i/16) for i in y1]
    x5 = np.arange(8,24)
    y5 = [42.83121,82.6722,169.9863,455.11,707.711,1582.62,3781.68,8098.798,14981.42,32320.423,67535.438,131133.6985,309920.9169,798836.059,1396565.68,3080196.65]
    y5 = [math.log(i) for i in y5]
    # y4_ = [i * 64 for i in y4]
    # plt.figure()
    # plt.style.use('ggplot')
    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.plot(x2, y2, lw=0.5, c='red', marker='s', ms=4, label='Our algorithm')  # 绘制y1
    plt.plot(x3, y3, lw=0.5, c='b', marker='o', label='Wang\'s algorithm[17]')  # 绘制y2
    plt.plot(x1, y1, lw=0.5, c='g', marker='*', label='Gamaarachchi\'s algorithm[15]')  # 绘制y2
    plt.plot(x4, y4, lw=0.5, c='c', marker='X', label='Classical algorithm[5]')  # 绘制y2
    plt.plot(x5, y5, lw=0.5, c='y', marker='X', label='Lee\'s algorithm[14][16]')  # 绘制y2
    # plt.legend(loc=6, bbox_to_anchor=(1, 1))
    plt.axvline(x=23, ymin=0, ymax=0.88, c='y', linestyle='--')
    plt.axvline(x=27,ymin = 0,ymax = 0.9,c='b',linestyle='--')
    plt.axvline(x=32, ymin = 0,ymax = 0.9,c='r', linestyle='--')
    plt.axvline(x=14, ymin = 0,ymax = 0.23,c='g', linestyle='--')
    plt.axvline(x=20, ymin = 0,ymax = 0.9,c='c', linestyle='--')
    plt.text(13.5, -3.1, s="14", fontsize=12, c='g')
    # plt.text(20, -4.1, s="20", fontsize=12, c='y')
    plt.text(26.7, -3.1, s="27",fontsize=12,c='b')
    plt.text(31.7, -3.1, s="32", fontsize=12, c='red')
    plt.text(22.5, -3.1, s="23", fontsize=12, c='y')
    plt.legend(loc='upper left')

    # plt.plot(x, y4_, lw=0.5, c='g', marker='p', label='N = 100')  # 绘制y3
    plt.xlim(5, 34)  # y轴坐标范围
    plt.ylim(-2, 17.5)  # y轴坐标范围
    # plt.xlabel('X-Name')  # x轴标注
    # plt.ylabel('Y-Name')  # y轴标注
    # plt.legend()  # 图例
    # plt.grid(True)
    # plt.savefig('e:/parallel.png')  # 保存图片
    # plt.show()
    # plt.figure()
    # # plt.style.use('ggplot')
    # plt.plot(x, y1, lw=1, c='red', marker='s', ms=4, label='CPU')  # 绘制y1
    # plt.plot(x, y2, lw=1, c='b', marker='o', label='A5000')  # 绘制y2
    # plt.plot(x, y3, lw=1, c='g', marker='p', label='1050 Ti')  # 绘制y3
    # plt.plot(x2, y3, lw=2, c='g', marker='o', label='GPU_time')  # 绘制y3
    # plt.xticks(x)  # x轴的刻度
    # def formatnum(x, pos):
    #     return '$%.1f$x$10^{4}$' % (x / 10000)

    # plt.xticks(x, ('$0.25$x$10^{4}$','$0.5$x$10^{4}$', '$0.75$x$10^{4}$', '$1.0$x$10^{4}$','$1.25$x$10^{4}$','$1.5$x$10^{4}$','$1.75$x$10^{4}$','$2.0$x$10^{4}$','$2.25$x$10^{4}$','$2.5$x$10^{4}$'))
    # plt.xlim(4, 30, 2)  # x轴坐标范围
    # plt.title('loss & communication round')
    plt.ylabel('Log(time/s)', fontsize=16)
    plt.xlabel('Number of bits of the key' , fontsize=16)

    # plt.xticks(x)
    # plt.xticks(rotation=45)
    # plt.legend()
    plt.grid(True)
    plt.savefig('e:/new.png')  # 保存图片
    plt.show()
