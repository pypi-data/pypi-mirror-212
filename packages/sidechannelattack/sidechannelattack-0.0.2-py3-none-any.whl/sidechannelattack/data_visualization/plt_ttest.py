#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：sidechannelattack 
@File    ：plt_ttest.py
@Author  ：suyang
@Date    ：2022/12/6 20:03 
'''
from  matplotlib import pyplot as plt
def plt_ttest(data,length,height):
    plt.rcParams['figure.figsize'] = (length,height)
    f, ax = plt.subplots(1, 1)

    # xiangliangt = block_ttest(100)

    plt.plot(data)
    plt.grid()
    ax.axhline(y=4.5, ls='--', c='red')
    ax.axhline(y=-4.5, ls='--', c='red')

    plt.show()