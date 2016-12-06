from animation import Animator
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

def k_nearest_estimator(x, data, k):
    dists = [abs(x - d) for d in data]
    sorted_dists = sorted(dists)
    dist_k = sorted_dists[k-1]
    N = len(data)
    return k/(2*N*dist_k)

k = 3
xs = np.arange(0, 8, 0.01)
data = [0.5, 0.7, 0.8, 1.9, 2.4, 6.1, 6.2, 7.3]
estimate = [k_nearest_estimator(x, data, k) for x in xs]


def setup():
    plt.gcf().set_size_inches(8,6)
    plt.suptitle("K-Nearest-Neighbor Density Estimator for k = {}".format(k))

def frame(i):
    plt.cla()

    # plot original data
    plt.plot(xs, estimate)
    plt.plot(data, [0]*len(data), 'xk')
    plt.axhline(0, color='k', linewidth=0.5)

    x = i/20

    dists = [(idx, abs(x - d)) for idx, d in enumerate(data)]

    sorted_dists = sorted(dists, key=lambda t: t[1])
    idx_k, dist_k = sorted_dists[k-1]

    data_k = data[idx_k]

    plt.plot(data_k, 0, 'oC3')

    plt.plot([x, x], [0, estimate[i*5]], '--C3')
    plt.plot(x, estimate[i*5], '.C3')

    hyperbole_xs = [x_val for x_val in xs if (x <= data_k and x_val <= data_k) or (x > data_k and x_val > data_k)]
    hyperbole_ys = [k/(2*len(data)*abs(x_val-data_k)) for x_val in hyperbole_xs]
    plt.plot(hyperbole_xs, hyperbole_ys, '--C3', alpha=0.5)



    yrange = max(estimate) - min(estimate)
    off = yrange * 0.1
    plt.plot([data_k, data_k], [0, max(estimate)+off], '--C3', alpha=0.5)
    plt.ylim(0-off, max(estimate)+off)

    plt.xlim(-0.5, 8.5)



a = Animator(name='KNNEstimator', setup_handle=setup)
a.setFrameCallback(frame_handle=frame, max_frame=160)
a.run(clear=False, precompile=False)
