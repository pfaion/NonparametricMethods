import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import Qt
import tempfile
import os

class Animator:

    def __init__(self, name = None, setup_handle = None):
        self.qApp = QtWidgets.QApplication([])

        self.w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.w.setLayout(layout)

        self.stack = QtWidgets.QStackedLayout()
        layout.addLayout(self.stack)

        self.label = QtWidgets.QLabel()
        self.stack.addWidget(self.label)
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.stack.addWidget(self.canvas)

        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.visualize)
        layout.addWidget(self.slider)

        self.recompile_buttom = QtWidgets.QPushButton("Recompile")
        self.recompile_buttom.pressed.connect(self.recompile)
        # hide button for now...
        # layout.addWidget(self.recompile_buttom)


        self.precompiled_cb = QtWidgets.QCheckBox("Precompiled")
        layout.addWidget(self.precompiled_cb)

        self.precompiled = None

        if name == None:
            self.tmpdir = tempfile.TemporaryDirectory()
            self.dir = self.tmpdir.name
        else:
            self.dir = ".precompiled/" + name
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)

        if setup_handle != None:
            setup_handle()

    def setFrameCallback(self, frame_handle, max_frame):
        self.frame_handle = frame_handle
        self.max_frame = max_frame
        self.slider.setMaximum(max_frame - 1)

    def recompile(self):
        self.clear()
        self.precompile()

    def precompile(self):
        if len(os.listdir(self.dir)) == 0:
            print("precompiling images...")
            for i in range(self.max_frame):
                print("compiling frame {}/80".format(i))
                self.frame_handle(i)
                plt.savefig("{}/{}.png".format(self.dir, i))


    def visualize(self, i):
        if self.precompiled_cb.isChecked():
            if not self.precompiled:
                self.precompile()
            if self.stack.currentWidget() != self.label:
                self.stack.setCurrentWidget(self.label)
            pm = QtGui.QPixmap("{}/{}.png".format(self.dir, i))
            self.label.setPixmap(pm)
        else:
            if self.stack.currentWidget() != self.canvas:
                self.stack.setCurrentWidget(self.canvas)
            self.frame_handle(i)
            self.canvas.draw()

    def clear(self):
        for file in os.listdir(self.dir):
            os.remove(self.dir + "/" + file)

    def run(self, clear = False, precompile = True):
        if clear:
            self.clear()
        if precompile:
            self.precompile()

        self.precompiled = precompile
        self.precompiled_cb.setChecked(precompile)

        self.w.show()
        self.visualize(0)
        self.qApp.exec()






