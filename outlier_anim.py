import numpy as np
import matplotlib
import math
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from animation import Animator

points = []

def dist(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt((ax - bx)**2 + (ay - by)**2)

def setup():
    plt.subplot(111, aspect='equal')
    plt.ylim(0,10)
    plt.xlim(0,10)
    plt.draw()

xs = np.arange(0, 10, 0.1)
ys = np.arange(0, 10, 0.1)
k = 3

def frame(i):
    global points
    plt.cla()
    if not points:
        return
    if len(points) >= k+1:


        img = np.zeros((len(xs), len(ys)))
        for y_i, y in enumerate(ys):
            for x_i, x in enumerate(xs):

                neighbors_dists = [(p_t, dist(p_t, (x, y))) for p_t in points]
                neighbors_dists.sort(key=lambda item: item[1])
                _, d_k = neighbors_dists[k-1]
                k_nns = [neighbor for neighbor, _ in neighbors_dists[:k]]


                avg_dist = sum(
                    sorted(dist(p_t, s) for p_t in points)[k]
                    for s in k_nns
                ) / k
                img[x_i, y_i] = d_k / avg_dist

        plt.imshow(img, extent=(0,10,0,10), cmap=plt.cm.Reds, origin='lower')

        from matplotlib.colors import LinearSegmentedColormap
        colormap = LinearSegmentedColormap.from_list('', [
            matplotlib.colors.to_rgba('r', alpha=0),
            matplotlib.colors.to_rgba('k', alpha=1)])
        plt.imshow(np.isclose(img, 1.0, atol=0.01), extent=(0,10,0,10), cmap=colormap, origin='lower')






    plt.plot(*zip(*points), 'xb')
    plt.ylim(0,10)
    plt.xlim(0,10)
    plt.draw()

def click(xdata, ydata, dblclick, button, **kwargs):
    global points
    if dblclick:
        points.append((xdata, ydata))
    elif button == 3:
        if not points:
            return
        point_dists = [(p, dist(p, (xdata, ydata))) for p in points]
        point_dists.sort(key=lambda item: item[1])
        points.remove(point_dists[0][0])



a = Animator(name='LOFAnimation', setup_handle=setup)
a.setFrameCallback(frame_handle=frame, max_frame=80)
a.setClickCallback(click)
a.run(clear=True, precompile=False)
