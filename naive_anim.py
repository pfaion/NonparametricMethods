import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from animation import Animator

def naive_estimator(x, data, h):
    n = sum(1 for d in data if x-h/2 < d <= x+h/2)
    N = len(data)
    return n/(N*h)

data = [0.5, 0.7, 0.8, 1.9, 2.4, 6.1, 6.2, 7.3]
xs = np.arange(0, 8, 0.01)
h = 2
hist = [naive_estimator(x, data, h) for x in xs]

def setup():
    plt.gcf().set_size_inches(8,6)
    plt.suptitle("Naive Estimator for h = {}".format(h))

def frame(i):
    plt.cla()

    # plot original data
    plt.plot(xs, hist)
    plt.plot(data, [0]*len(data), 'xk')
    plt.axhline(0, color='k', linewidth=0.5)

    # calculate current interval
    x = i / 10
    x1, x2 = x-h/2, x+h/2

    # calculate relative width for visualization
    axis_to_data = plt.gca().transAxes + plt.gca().transData.inverted()
    bottom = axis_to_data.transform((0, 0))[1]
    top = -bottom

    # plot visualization lines
    plt.plot([x, x], [0, hist[i * 10]], '--C3')
    plt.plot([x1, x1], [bottom, top], 'C3', linewidth=0.5)
    plt.plot([x2, x2], [bottom, top], 'C3', linewidth=0.5)
    plt.plot([x1, x2], [0, 0], 'C3', linewidth=0.5)
    plt.fill_between([x1, x2], bottom, top, color='C3', alpha=0.3)
    plt.plot(x, hist[i * 10], '.C3')

    # highlight data in interval
    highlight_data = [d for d in data if x1 < d <= x2]
    plt.plot(highlight_data, [0]*len(highlight_data), 'oC3')

    plt.xlim(-0.5, 8.5)




a = Animator(name='NaiveEstimator', setup_handle=setup)
a.setFrameCallback(frame_handle=frame, max_frame=80)
a.run(clear=False, precompile=True)
