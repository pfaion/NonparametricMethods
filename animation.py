import matplotlib
import matplotlib.backend_bases
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt
import tempfile
import os


class Animator:


    def mouseFun(self, event: matplotlib.backend_bases.MouseEvent):
        self.click_cb(**(event.__dict__))
        self.visualize()



    def setScaledPixmap(self):
        if not self.pixmap:
            return
        if not self.pixw or not self.pixh:
            self.label.setPixmap(self.pixmap)
        else:
            self.label.setPixmap(self.pixmap.scaled(self.pixw, self.pixh, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def __init__(self, name = None, setup_handle = None):
        self.qApp = QtWidgets.QApplication([])

        self.w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self.w.setLayout(layout)



        self.stack = QtWidgets.QStackedLayout()
        layout.addLayout(self.stack)


        self.label = QtWidgets.QLabel()
        self.stack.addWidget(self.label)
        self.pixmap = None # type: QtGui.QPixmap
        self.pixw = None
        self.pixh = None

        def widgetResizeEvent(event: QtGui.QResizeEvent):
            nonlocal self
            new_size = event.size()  # type: QtCore.QSize
            self.pixw = new_size.width() - 100
            self.pixh = new_size.height() - 100
            self.setScaledPixmap()

        self.w.resizeEvent = widgetResizeEvent


        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.stack.addWidget(self.canvas)


        self.canvas.mpl_connect('button_press_event', self.mouseFun)

        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.visualize)
        layout.addWidget(self.slider)

        self.precompiled_cb = QtWidgets.QCheckBox("Precompiled")
        layout.addWidget(self.precompiled_cb)

        self.precompiled = None

        self.name = name
        if name == None:
            self.tmpdir = tempfile.TemporaryDirectory()
            self.dir = self.tmpdir.name
            self.name = 'animator_'+self.dir
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

    def setClickCallback(self, click_cb):
        self.click_cb = click_cb

    def recompile(self):
        self.clear()
        self.precompile()

    def precompile(self):
        if len(os.listdir(self.dir)) == 0:
            print("precompiling images...")
            for i in range(self.max_frame):
                print("compiling frame {}/{}".format(i, self.max_frame))
                self.frame_handle(i)
                plt.savefig("{}/{}.png".format(self.dir, i))


    def visualize(self, i = None):
        if i == None:
            i = self.slider.value()
        if self.precompiled_cb.isChecked():
            if not self.precompiled:
                self.precompile()
            if self.stack.currentWidget() != self.label:
                self.stack.setCurrentWidget(self.label)
            self.pixmap = QtGui.QPixmap("{}/{}.png".format(self.dir, i))
            self.setScaledPixmap()
        else:
            self.pixmap = None
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




