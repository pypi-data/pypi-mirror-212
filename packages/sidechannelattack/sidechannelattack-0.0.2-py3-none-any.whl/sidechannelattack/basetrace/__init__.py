from base import *
import numpy as np
# from .base import load
# 读取曲线
# 两种方式，第一种scared   利用estraces包，import estraces as traces,然后调用函数，第二种，open project

def open_file(filename):
    filename = ensure_extension(filename)
    proj = load(filename)
    return proj


# filepath = 'G:/py+idea/python/sidechannel/basetrace/exsample.csv'
# t1 = np.genfromtxt(filepath,delimiter=',',encoding='utf-8',skip_header=2)
# npt1 = t1[:,2]
# print(npt1)
# # print(t1)