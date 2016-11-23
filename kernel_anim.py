import numpy as np
import matplotlib
import math
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from animation import Animator

def gaussian_kernel(u):
    return 1.0/math.sqrt(2*math.pi)*math.exp(-(u*u)/2)

def kernel_estimator(x, data, h, kernel):
    N = len(data)
    return 1/(N*h) * sum(kernel((x-d)/h) for d in data)

h = 0.5
xs = np.arange(0, 8, 0.01)
data = [0.5, 0.7, 0.8, 1.9, 2.4, 6.1, 6.2, 7.3]
estimate = [kernel_estimator(x, data, h, gaussian_kernel) for x in xs]

def setup():
    plt.gcf().set_size_inches(8,6)
    plt.suptitle("Gaussian Kernel Estimator for h = {}".format(h))

def frame(i):
    plt.cla()

    # plot original data
    plt.plot(xs, estimate)
    plt.plot(data, [0]*len(data), 'xk')
    plt.axhline(0, color='k', linewidth=0.5)

    x = i/10

    kernel = [gaussian_kernel((x-x_val)/h) for x_val in xs]
    kernel = [-k / max(kernel) * max(estimate) * 0.3 for k in kernel]
    kernel_patch = [(x_val, k) for x_val, k in zip(xs, kernel) if k < -max(estimate)*0.001]
    kernel_patch_xs, kernel_patch_ys = zip(*kernel_patch)
    plt.plot(kernel_patch_xs, kernel_patch_ys, 'C3')

    max_response = gaussian_kernel(0)
    for d in data:
        if kernel_patch_xs[0] <= d <= kernel_patch_xs[-1]:
            response = gaussian_kernel((x-d)/h)
            t = response / max_response
            plt.plot(d, 0, 'x', color=(t, 0.0, 0.0), markersize = 10*t + 6)

    plt.plot([x, x], [-max(estimate) * 0.3, estimate[i * 10]], '--C3')
    plt.plot(x, estimate[i * 10], '.C3')

    plt.yticks(*zip(*[(tick, str(tick)) for tick in plt.yticks()[0] if tick >= 0]))


    plt.xlim(-0.5, 8.5)




a = Animator(name='GaussianEstimator', setup_handle=setup)
a.setFrameCallback(frame_handle=frame, max_frame=80)
a.run(clear=True, precompile=True)
