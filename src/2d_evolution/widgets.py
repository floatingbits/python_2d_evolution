from PyQt5.QtWidgets import QLabel, QSizePolicy, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from models import TheGame
from timeit import default_timer as timer
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QImage, qRgb, QPixmap
from PyQt5.QtWidgets import (QLabel, QSizePolicy)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("2dEvolution")

        canvas = MatrixViewer()
        model = TheGame(300, 500, 500)
        self.model = model
        canvas.set_model(model)
        self.canvas = canvas

        play = QPushButton()
        play.setText("Play")

        pause = QPushButton()
        pause.setText("Pause")

        step = QPushButton()
        step.setText("Step >")
        step.clicked.connect(self.step_clicked)

        tournament = QPushButton()
        tournament.setText("Tournament")
        tournament.clicked.connect(self.tournament_clicked)

        top = QHBoxLayout()
        top.addWidget(play)
        top.addWidget(pause)
        top.addWidget(step)
        top.addWidget(tournament)

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget = QWidget()
        widget.setLayout(top)
        layout.addWidget(widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def step_clicked(self):
        self.model.step_forward()
        self.canvas.updateView()

    def tournament_clicked(self):
        self.model.play_tournaments()
        self.canvas.updateView()


class MatrixViewer(QLabel):
    """
    Custom Widget to show and edit (with mouse events) the state of GoL.

    Attributes:
        matrixProvider         reference to an object of class GameOfLife (the model)
        drawing     bool value to keep track of mouse button long press and movement
        V_margin    dimension of right and left margin in window (widget) coordinates for the image
        H_margin    dimension of top and bottom margin in window (widget) coordinates for the image
        h           board (gol state) height
        w           board (gol state) height
        lastUpdate  time of the last view update
        pixmap      image representing the state of the game (QPixmap object) (self.pixmap())
    """

    def __init__(self):
        super().__init__()
        self.matrixProvider = None
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.drawing = False
        self.V_margin = 0
        self.H_margin = 0
        self.h = 0
        self.w = 0
        self.lastUpdate = timer()

    def set_model(self, matrixProvider):
        """
        Set the reference to the matrixProvider model.

        Args:
            matrixProvider     object of class GameOfLife
        """
        self.matrixProvider = matrixProvider
        self.updateView()  # update the view to show the first frame

    def updateView(self):
        """Update the view converting the current state (np.ndarray) to an image (QPixmap) and showing it on screen"""
        # All this conversion are not beautiful but necessary...
        mat = self.matrixProvider.get_state()
        self.h = mat.shape[0]
        self.w = mat.shape[1]
        qim = self.toQImage(mat)  # first convert to QImage
        qpix = QPixmap.fromImage(qim)  # then convert to QPixmap
        # set the pixmap and resize to fit the widget dimension
        self.setPixmap(qpix.scaled(self.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        # calculate the margins
        self.V_margin = (self.size().height() - self.pixmap().size().height()) / 2
        self.H_margin = (self.size().width() - self.pixmap().size().width()) / 2
        self.lastUpdate = timer()  # update the lastUpdate time

    def toQImage(self, im):
        """
        Utility method to convert a numpy array to a QImage object.

        Args:
            im          numpy array to be converted. It can be a 2D (BW) image or a color image (3 channels + alpha)

        Returns:
            QImage      The image created converting the numpy array
        """
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        if im is None:
            return QImage()
        if len(im.shape) == 2:  # 1 channel image
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable(gray_color_table)
            return qim
        elif len(im.shape) == 3:  # maybe in the future accept color images (for heatmap)
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                return qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                return qim

