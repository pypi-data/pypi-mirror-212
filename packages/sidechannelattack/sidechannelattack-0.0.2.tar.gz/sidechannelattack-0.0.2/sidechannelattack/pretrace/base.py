import numpy as np
import estraces as traces

import filetype


from numpy import test


def is_bytes_array(traces):
    if not isinstance(traces, np.ndarray):
        raise TypeError(f'array should be a Numpy ndarray instance, not {type(traces)}.')
    if not traces.dtype == 'uint8':
        raise ValueError(f'array should be a byte array with uint8 dtype, not {traces.dtype}.')
    return True


def get_traces_num(traces):
    # with open('parallel.npy', "rb") as f:
    #     kind = filetype.guess(f)
    #     if kind is None:
    #         print('Cannot identyfy the file type')
    #         return
    # print(kind.extension)
    # print(kind.mime)
    # print('the correct extension')
    # trace_name = project.ensure_cwp_extension(filename)
    return np.shape(traces)[0]


def get_trace_sample(trace):
    return np.size(trace)


def get_traces_sample(traces):
    return np.shape(traces)[1]


def get_traces_mean(traces):
    return np.mean(traces, axis=0)


def get_traces_abs(traces):
    return np.abs(traces)


def get_traces_square(traces):
    return np.square()

def cut_func(traces,min = None,max = None):
    if traces.ndim == 1:
        new_traces  = traces[min:max]
        return new_traces
    if traces.ndim == 2:
        new_traces = np.zeros((traces.shape[0],max-min))
        for i in range(traces.shape[0]):
            new_traces[i] = traces[i][min:max]
        return new_traces
if __name__ == '__main__':
    pass