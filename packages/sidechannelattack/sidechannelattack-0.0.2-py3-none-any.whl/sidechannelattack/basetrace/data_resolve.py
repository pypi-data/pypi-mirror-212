# 给我一个中间值，就是函数处理的中间值，我去找能量映射模型？
# 汉明重量
import numpy as np
# 有时间加一个类型限制   整数类型哦
def _hamming_weight(intermediate_value):
    '''

    :param intermediate_value: 一个中间值
    :return: 中间值的汉明重量
    '''
    m = 0
    while intermediate_value != 0:
        # print(type(intermediate_value))
        m=m+(intermediate_value & 1)
        intermediate_value >>= 1
    return m
def _LSB(intermediate_value):
    '''

    :param intermediate_value: 一个中间值
    :return: 返回最低有效位
    '''
    m = 0
    while intermediate_value != 0:
        m = intermediate_value & 1
    return m
def HW(data):
    '''

    :param data: 一组中间值
    :return: 一组中间值的汉明重量
    '''
    if not isinstance(data, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if data.ndim == 1:
        new_data = np.zeros(len(data), dtype=float)
        for i in range(len(data)):
            new_data[i] = _hamming_weight(int(data[i]))
        return new_data
    if data.ndim == 2:
        new_data = np.zeros((data.shape(0),data.shape[1]), dtype=float)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                new_data[i][j] = _hamming_weight(int(data[i][j]))
        return new_data
def LSB(data):
    """

    :param data:同上
    :return:
    """
    if not isinstance(data, np.ndarray):
        raise TypeError("'data' should be a numpy ndarray.")
    if data.ndim == 1:
        new_data = np.zeros(len(data), dtype=float)
        for i in range(len(data)):
            new_data[i] = _LSB(data[i])
        return new_data
    if data.ndim == 2:
        new_data = np.zeros((data.shape(0),data.shape[1]), dtype=float)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                new_data[i][j] = _LSB(data[i][j])
        return new_data
# print(HW(np.array(255)))
if __name__ == '__main__':
    pass