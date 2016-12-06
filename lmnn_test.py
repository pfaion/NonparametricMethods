import numpy as np
from metric_learn import LMNN
from sklearn.datasets import load_iris

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

iris_data = load_iris()
X = iris_data['data'][:,0:2]
Y = iris_data['target']

lmnn = LMNN(k=5, learn_rate=1e-6)
lmnn.fit(X, Y)
m = lmnn.metric()



px = 5
py = 2.5
xs = np.arange(4, 6.5, 0.1)
ys = np.arange(2, 3.5, 0.1)

img = np.zeros((ys.shape[0], xs.shape[0]))

for x_i, x in enumerate(xs):
    for y_i, y in enumerate(ys):
        g = np.array([px - x, py - y])
        result = g @ m @ g.T
        img[y_i, x_i] = result

plt.figure()

plt.imshow(img, origin='lower')

plt.plot(px*10-40, py*10-20, 'oC0', markersize=8)

colors = ['r', 'g', 'b']
for c in range(3):
    # xs, ys, zs = zip(*[(X[i,0], X[i,1], X[i,2]) for i in range(150) if Y[i] == c])
    # ax.plot(xs, ys, zs, '.', color = colors[c])
    xs, ys = zip(*[(X[i, 0]*10-40, X[i, 1]*10-20) for i in range(150) if Y[i] == c])
    plt.plot(xs, ys, '.', color = colors[c])


plt.show()





