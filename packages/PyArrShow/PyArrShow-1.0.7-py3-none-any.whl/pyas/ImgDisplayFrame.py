import numpy as np
import sys
from PySide6.QtWidgets import (QApplication,QHBoxLayout,QLabel,QFrame,QLayout,QSizePolicy,QWidget)
from PySide6.QtGui import QAction, QImage, qRgb, QPixmap,QResizeEvent
from PySide6.QtCore import Qt,QSize

class ImgDisplayFrame(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setupUI()
        self.cfgUIStyle()
        self.initImgDisplayByZeros()
        self.cfgImgDisplayResizeEvent()
        # self.posTextWithInImgDisplay()
    
    def parsSetup(self):
        self.disp_qimg = []         #Image display buffer
        self.disp_pixmap = []
        self.ImgDisplayHandleMaxSize = []

    def setupUI(self):
        self.setLayout(QHBoxLayout())

        #ImgDisplayFrame have only one Widget of QLabel
        self.ImgDisplayHandle= QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
        self.ImgDisplayHandle.setSizePolicy(sizePolicy)
        self.ImgDisplayHandle.setMinimumSize(1,1)
        self.ImgDisplayHandle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ImgDisplayHandle.setLineWidth(0)

        self.layout().addWidget(self.ImgDisplayHandle)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    def cfgUIStyle(self):
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)

    def initImgDisplayByZeros(self):
        disp_img = np.zeros((256,256),dtype=np.int16)
        disp_qimg = QImage(disp_img, disp_img.shape[1], disp_img.shape[0], QImage.Format.Format_Grayscale16)
        self.updateImgDisplay(disp_qimg)
        # self.updateImgDisplayAspectRatio(disp_pixmap)

    def updateImgDisplay(self,disp_qimg):
        self.updateDispQImage(disp_qimg)
        self.updateImgDisplayHandleMaxSize()
        scaled_disp_pixmap = self.disp_pixmap.scaled(self.ImgDisplayHandleMaxSize,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.FastTransformation)
        self.ImgDisplayHandle.setPixmap(scaled_disp_pixmap)
    
    def cfgImgDisplayResizeEvent(self):
        self.resizeEvent = self.imgDisplayFrameResizeEvent

    def imgDisplayFrameResizeEvent(self,event):
        self.updateImgDisplayHandleMaxSize()
        scaled_disp_pixmap = self.disp_pixmap.scaled(self.ImgDisplayHandleMaxSize,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.FastTransformation)
        self.ImgDisplayHandle.setPixmap(scaled_disp_pixmap)
    
    def updateImgDisplayHandleMaxSize(self):
        MaxWidth = self.size().width() - 2 * self.lineWidth() - self.contentsMargins().left() - self.contentsMargins().right()
        MaxHeight = self.size().height() - 2 * self.lineWidth() - self.contentsMargins().top() - self.contentsMargins().bottom()
        self.ImgDisplayHandleMaxSize = QSize(MaxWidth,MaxHeight)
        
    def setDispQImage(self,disp_qimg):
        self.disp_qimg = disp_qimg
    
    def updateDispPixmap(self):
        self.disp_pixmap = QPixmap.fromImage(self.disp_qimg)
    
    def updateDispQImage(self,disp_qimg):
        self.setDispQImage(disp_qimg)
        self.updateDispPixmap()
    
    def getDispPixmap(self):
        return self.disp_pixmap
    
    # def posTextWithInImgDisplay(self):
    #     self.ImgDisplayHandle.setText("text")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = ImgDisplayFrame()
    # test.setDispImg(np.random.rand(256,256))
    test.show()
    sys.exit(app.exec_())

