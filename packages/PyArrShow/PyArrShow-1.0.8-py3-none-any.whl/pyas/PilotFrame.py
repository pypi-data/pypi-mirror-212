import numpy as np
import sys
import os
from PySide6.QtWidgets import (QApplication,QHBoxLayout,QVBoxLayout,QGridLayout,QLineEdit,QLabel,QLayout,
                               QSlider,QFrame,QPushButton,QComboBox,QWidget)
from PySide6.QtGui import QAction, QImage, qRgb, QPixmap,QMouseEvent
from PySide6.QtCore import Qt

class PilotFrame(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setupUI()
        self.cfgUIStyle()

    def setupUI(self):
        self.BtnHeight = 25         #fixed btn height
        self.BtnWidth = 35          #fixed btn width
        self.setLayout(QHBoxLayout())
        self.setupDataRangeFrame()
        self.setupCWSliderFrame()
        self.setupImgDescFrame()
        self.setupImgModalityFrame()
        
    def setupDataRangeFrame(self):
        self.DataRangeFrame = QFrame()
        self.DataRangeFrame.setLayout(QHBoxLayout())
        self.DataRangeFrame.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Array stores widgets
        self.DataRangeWidgets = []
        self.DataRangePlusBtns = []
        self.DataRangeEditLines = []
        self.DataRangeMinusBtns = []
        self.DataRangeMaxIdxs = []
        
        for iter_dim in range(1):   #disp one btn
            self.DataRangeWidgets.append(QVBoxLayout())
            self.DataRangePlusBtns.append(QPushButton('+'))
            self.DataRangeEditLines.append(QLineEdit('',alignment = Qt.AlignmentFlag.AlignCenter))
            self.DataRangeMinusBtns.append(QPushButton('-'))
            self.DataRangeMaxIdxs.append(QPushButton('Idx'))

            #configure size of Pilot widgets
            self.DataRangePlusBtns[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangePlusBtns[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeEditLines[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeEditLines[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMinusBtns[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMinusBtns[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMaxIdxs[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMaxIdxs[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)

            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangePlusBtns[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeEditLines[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeMinusBtns[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeMaxIdxs[iter_dim])
            self.DataRangeFrame.layout().addLayout(self.DataRangeWidgets[iter_dim])

        self.DataRangeFrame.layout().setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.DataRangeFrameHeight = self.DataRangeFrame.layout().totalMinimumSize().height()
        self.DataRangeFrame.setFixedHeight(self.DataRangeFrameHeight)
        self.DataRangeBtnWidthMin = 8
        self.DataRangeFrame.setFixedWidth(self.BtnWidth * (self.DataRangeBtnWidthMin + 1))  #init with 8 btn width

        self.layout().addWidget(self.DataRangeFrame)
    
    def setupCWSliderFrame(self):
        self.CWSliderFrame = QFrame()
        self.CWSliderFrame.setLayout(QVBoxLayout())
        self.CWSliderFrame.setFixedHeight(self.DataRangeFrameHeight)

        self.CSliderWidget = QSlider(Qt.Orientation.Horizontal)
        self.CSliderWidget.setMinimum(0)
        self.CSliderWidget.setMaximum(100)
        self.CSliderWidget.setSingleStep(1) #set 100 steps
        self.CSliderWidget.setValue(0)
        self.CSliderWidget.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.CSliderWidget.setTickInterval(10)

        self.WSliderWidget = QSlider(Qt.Orientation.Horizontal)
        self.WSliderWidget.setMinimum(1)
        self.WSliderWidget.setMaximum(100)
        self.WSliderWidget.setSingleStep(1) #set 100 steps
        self.WSliderWidget.setValue(1)
        self.WSliderWidget.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.WSliderWidget.setTickInterval(10)
        
        self.CWLabelFrame = QFrame()
        self.CWLabelFrame.setLayout(QHBoxLayout())
        self.CWLabelFrame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.CLabelWidget = QLabel()
        self.SlashLabelWidget = QLabel()
        self.WLabelWidget = QLabel()
        self.CLabelWidget.setText('-')
        self.SlashLabelWidget.setText('/')
        self.WLabelWidget.setText('-')
        self.CWLabelFrame.layout().addWidget(self.CLabelWidget)
        self.CWLabelFrame.layout().addWidget(self.SlashLabelWidget)
        self.CWLabelFrame.layout().addWidget(self.WLabelWidget)

        self.CWSliderFrame.layout().addWidget(self.CSliderWidget)
        self.CWSliderFrame.layout().addWidget(self.WSliderWidget)
        self.CWSliderFrame.layout().addWidget(self.CWLabelFrame)
        self.CWSliderFrame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout().addWidget(self.CWSliderFrame)

    def setupImgDescFrame(self):
        self.ImgDescFrame = QFrame()
        self.ImgDescFrame.setLayout(QGridLayout())
        self.ImgDescFrame.setFixedHeight(self.DataRangeFrameHeight)

        self.DataDimKeyWidget = QLabel()
        self.DataDimKeyWidget.setText('Dim:')
        self.DataDimValWidget = QLabel()
        self.DataDimValWidget.setText('-,-')

        self.DataMinKeyWidget = QPushButton('Min:')
        self.DataMinKeyWidget.setMinimumSize(self.BtnWidth,self.BtnHeight)
        self.DataMinKeyWidget.setMaximumSize(self.BtnWidth,self.BtnHeight)
        self.DataMinValWidget = QLabel()
        self.DataMinValWidget.setText('-')

        self.DataMeanKeyWidget = QLabel()
        self.DataMeanKeyWidget.setText('Mean:')
        self.DataMeanValWidget = QLabel()
        self.DataMeanValWidget.setText('')

        self.DataMaxKeyWidget = QPushButton('Max:')
        self.DataMaxKeyWidget.setMinimumSize(self.BtnWidth,self.BtnHeight)
        self.DataMaxKeyWidget.setMaximumSize(self.BtnWidth,self.BtnHeight)
        self.DataMaxValWidget = QLabel()
        self.DataMaxValWidget.setText('-')

        self.DataL2KeyWidget = QLabel()
        self.DataL2KeyWidget.setText('L2:')
        self.DataL2ValWidget = QLabel()
        self.DataL2ValWidget.setText('-')

        self.DataDimKeyWidget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.DataDimValWidget.setAlignment(Qt.AlignmentFlag.AlignRight)
        #self.DataMaxKeyWidget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.DataMinValWidget.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.DataMeanKeyWidget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.DataMeanValWidget.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.DataMaxWidgets.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.DataMaxValWidget.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.DataL2KeyWidget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.DataL2ValWidget.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ImgDescFrame.layout().addWidget(self.DataDimKeyWidget,0,0)
        self.ImgDescFrame.layout().addWidget(self.DataDimValWidget,0,1)
        self.ImgDescFrame.layout().addWidget(self.DataMinKeyWidget,1,0)
        self.ImgDescFrame.layout().addWidget(self.DataMinValWidget,1,1)
        self.ImgDescFrame.layout().addWidget(self.DataMeanKeyWidget,2,0)
        self.ImgDescFrame.layout().addWidget(self.DataMeanValWidget,2,1)
        self.ImgDescFrame.layout().addWidget(self.DataMaxKeyWidget,3,0)
        self.ImgDescFrame.layout().addWidget(self.DataMaxValWidget,3,1)
        self.ImgDescFrame.layout().addWidget(self.DataL2KeyWidget,4,0)
        self.ImgDescFrame.layout().addWidget(self.DataL2ValWidget,4,1)

        self.ImgDescFrame.setFixedWidth(self.BtnWidth * 4)
        self.layout().addWidget(self.ImgDescFrame)

    def setupImgModalityFrame(self):
        self.ImgModalityFrame = QFrame()
        self.ImgModalityFrame.setLayout(QVBoxLayout())
        self.ImgModalityFrame.setFixedHeight(self.DataRangeFrameHeight)
        
        self.ImgModalityComboBox = QComboBox()
        self.ImgModalityComboBox.setPlaceholderText('-Select disp Modality-')
        self.ImgModalityFrame.layout().addWidget(self.ImgModalityComboBox)

        self.layout().addWidget(self.ImgModalityFrame)
        
    def initUI(self,data_dim,slicing_str,ImgModalityOptions,disp_img_modality):
        self.initDataRangeFrame(data_dim,slicing_str)
        self.initImgModalityFrame(ImgModalityOptions,disp_img_modality)

    def initDataRangeFrame(self,data_dim,slicing_str):
        #remove original item
        # for i in reversed(range(self.DataRangeFrame.layout().count())):
            #remove widget
        while self.DataRangeFrame.layout().count():
            while self.DataRangeFrame.layout().itemAt(0).count():
                layout_item = self.DataRangeFrame.layout().itemAt(0).itemAt(0)
                widget = layout_item.widget()
                if widget is not None:
                    # widget.destroy()
                    widget.setParent(None)
                    self.DataRangeFrame.layout().itemAt(0).removeWidget(widget)
            self.DataRangeFrame.layout().removeItem(self.DataRangeFrame.layout().itemAt(0))

        # Array stores widgets
        self.DataRangeWidgets = []
        self.DataRangePlusBtns = []
        self.DataRangeEditLines = []
        self.DataRangeMinusBtns = []
        self.DataRangeMaxIdxs = []

        self.DataRangeFrame.setFixedWidth(self.BtnWidth * (np.max([len(data_dim),self.DataRangeBtnWidthMin]) + 1))

        for iter_dim in range(len(data_dim)):
            self.DataRangeWidgets.append(QVBoxLayout())
            self.DataRangePlusBtns.append(QPushButton('+'))
            self.DataRangeEditLines.append(QLineEdit("{0}".format(slicing_str[iter_dim]),alignment=Qt.AlignmentFlag.AlignCenter))
            self.DataRangeMinusBtns.append(QPushButton('-'))
            self.DataRangeMaxIdxs.append(QPushButton('{0}'.format(data_dim[iter_dim])))

            #configure size of Pilot widgets
            self.DataRangePlusBtns[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangePlusBtns[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeEditLines[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeEditLines[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMinusBtns[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMinusBtns[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMaxIdxs[iter_dim].setMinimumSize(self.BtnWidth,self.BtnHeight)
            self.DataRangeMaxIdxs[iter_dim].setMaximumSize(self.BtnWidth,self.BtnHeight)

            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangePlusBtns[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeEditLines[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeMinusBtns[iter_dim])
            self.DataRangeWidgets[iter_dim].addWidget(self.DataRangeMaxIdxs[iter_dim])
            self.DataRangeFrame.layout().addLayout(self.DataRangeWidgets[iter_dim])

    def initImgModalityFrame(self,ImgModalityOptions,disp_img_modality):
        self.ImgModalityComboBox.clear()
        for item in ImgModalityOptions:
            self.ImgModalityComboBox.addItem(item)
        self.ImgModalityComboBox.setCurrentIndex(np.where(np.array(ImgModalityOptions)==disp_img_modality)[0][0])

    def cfgUIStyle(self):
        # DataRange UI
        self.DataRangeFrame.setFrameShape(QFrame.Shape.Box)
        self.DataRangeFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # CWSlider UI
        self.CWSliderFrame.setFrameShape(QFrame.Shape.Box)
        self.CWSliderFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # ImgDesc UI
        self.ImgDescFrame.setFrameShape(QFrame.Shape.Box)
        self.ImgDescFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # ImgModality UI
        self.ImgModalityFrame.setFrameShape(QFrame.Shape.Box)
        self.ImgModalityFrame.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.setFixedHeight(self.layout().totalMinimumSize().height())

    def setDataRangeLineEdit(self,idx,val):
        self.DataRangeEditLines[idx].setText("{0}".format(str(val)))

    def updateImgDesc(self,disp_img):
        self.DataDimValWidget.setText('{:>4d},{:>4d}'.format(disp_img.shape[0],disp_img.shape[1]))
        self.DataMinValWidget.setText('{:.2g}'.format(np.min(disp_img)))
        self.DataMeanValWidget.setText('{:.2g}'.format(np.mean(disp_img)))
        self.DataMaxValWidget.setText('{:.2g}'.format(np.max(disp_img)))
        self.DataL2ValWidget.setText('{:.4g}'.format(np.linalg.norm(disp_img,ord = 2)))

    def setBtnActived(self,btn_id):
        for iter in range(self.DataRangeFrame.layout().count()):
            if iter != btn_id:
                self.DataRangeMaxIdxs[iter].setStyleSheet('color:black')
            else:
                self.DataRangeMaxIdxs[iter].setStyleSheet('color:red')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    nd_array = np.random.rand(256,256,3,4)
    disp_img = nd_array[:,:,1,1]
    window_center = (np.max(disp_img) - np.min(disp_img)) * 0.5        
    window_width = (np.max(disp_img) - np.min(disp_img))
    test = PilotFrame()#
    test.show()
    test.initUI(data_dims=nd_array.shape,slicing_str=[':',':','1','1'],data_type='float64')
    sys.exit(app.exec_())