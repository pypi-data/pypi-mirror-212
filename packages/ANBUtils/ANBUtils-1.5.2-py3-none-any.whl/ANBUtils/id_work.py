# -*- coding: utf-8 -*-

import math

import matplotlib.pyplot as plt
import numpy as np


def matplot_set():
    import matplotlib as mplt
    mplt.rcParams['figure.figsize'] = (20, 8)


def int_mark(statr: int, end: int, step: int, extract: int,
             isReplace: bool = False, isShuffle: bool = False) -> list:
    if not type(statr) == type(end) == type(step) == type(extract) == int:
        raise ValueError(' start | end | step | extract type must is int!')

    if statr + step > end:
        raise ValueError(' [ start + step ] must be greater than [ end ]!')

    if not isReplace and extract >= step:
        raise ValueError(' When the mode isReplace = False , [ step ] must be greater than [ extract ]!')

    S = math.floor(statr / step)
    E = math.ceil(end / step)

    a = list(range(step))

    ids = []

    for i in range(S, E):
        at = np.random.choice(a, size=extract, replace=isReplace)
        for t in at:
            ids.append(i * step + t)

    if isShuffle:
        np.random.shuffle(ids)

    return ids


def id_analyst(data, steps=10, plot='pyplot'):
    from math import log10, ceil
    d = sorted(data)
    nd_max = int(log10(d[-1]))
    nd_min = int(log10(d[0]))

    if nd_max != nd_min:
        start = 0
    else:
        start = int(d[0] / (10 ** (nd_min - 1))) * (10 ** (nd_min - 1))

    end = ceil(d[-1] / (10 ** (nd_max - 1))) * (10 ** (nd_max - 1))
    step = (end - start) / steps
    counter = [0] * (steps + 1)

    for i in d:
        counter[int((i - start) / step)] += 1

    rtn = {
        "counter": counter,
        "step": step,
        "start": start,
        "end": end
    }

    x = [i * step + start for i in range(steps + 1)]
    y = counter

    if plot == "pyplot":
        matplot_set()
        plt.plot(x, y)
        plt.show()

    elif plot == "matlab":
        import matlab
        import matlab.engine
        eng = matlab.engine.start_matlab()
        X = matlab.double(x)
        Y = matlab.double(y)
        eng.plot(X, Y)
        rtn['plot'] = eng

    return rtn
