#!usr/bin/python
from matplotlib import pyplot as plt
import numpy as np
import random
import sys
import os
from functools import partial
import time


from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QMenuBar,QMenu,QDialog,QLabel,QFileDialog,QInputDialog,
                               QPushButton,QLineEdit,QFrame,QLayout,QSlider,QComboBox,QGraphicsView,QMessageBox,QErrorMessage)
from PySide6.QtGui import QAction, QImage, QIcon,qRgb, QPixmap,QMouseEvent,QResizeEvent
from PySide6.QtCore import Slot,Qt,QSize,QRect,QDir,QTimer
from pyas.DataCursorFrame import DataCursorFrame
from pyas.ImgDisplayFrame import ImgDisplayFrame
from pyas.PilotFrame import PilotFrame
from typing import overload
import sigpy
from pyas.qrc_resources import *

class pyArrShowWindow(QMainWindow):
    #pyArrShowView class
    def __init__(self):
        QMainWindow.__init__(self)
        self.appTitle = 'PyArrShow'
        self.setWindowTitle(self.appTitle)
        self.appIcon = QIcon(":PyAs_main_window.svg")
        self.setWindowIcon(self.appIcon)
        #Create Actions
        self._createActions()
        #Init menuBar
        self._createMenuBar()
        #init toolbar
        self._createToolBar()

        self.CentralWidgets = CentralWidgets()
        self.setCentralWidget(self.CentralWidgets)
        #create context menu
        self._createContextMenu()
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        operationMenu = menuBar.addMenu('&Operations')
        operationMenu.addAction(self.flipHAction)
        operationMenu.addAction(self.flipVAction)
        operationMenu.addAction(self.clockRot90Action)
        operationMenu.addAction(self.anticlockRot90Action)
        operationMenu.addSeparator()
        operationMenu.addAction(self.FFT2DAction)
        operationMenu.addAction(self.iFFT2DAction)
        operationMenu.addAction(self.FFTShiftAction)
        operationMenu.addAction(self.iFFTShiftAction)
        operationMenu.addSeparator()
        operationMenu.addAction(self.conjAction)
        operationMenu.addSeparator()
        operationMenu.addAction(self.reshapeAction)
        operationMenu.addAction(self.squeezeAction)
        operationMenu.addAction(self.permuteAction)
        operationMenu.addSeparator()
        operationMenu.addAction(self.resetAction)
        # toolMenu = menuBar.addMenu('&Tools')
        # relativeMenu = menuBar.addMenu('&Relatives')
        viewMenu = menuBar.addMenu('View')
        viewMenu.addAction(self.playVideoAction)

        figureMenu = menuBar.addMenu('Figure')
        figureMenu.addAction(self.changeTitleAction)
        # figureMenu.addAction(self.posTitleInImgDisplayAction)
        helpMenu = menuBar.addMenu(QIcon(":help_content.svg"),'&Help')
        helpMenu.addAction(self.aboutAction)

    def _createActions(self):
        #file actions
        self.openAction = QAction(QIcon(":file_open.svg"),'&Open',self)
        self.saveAction = QAction(QIcon(":file_save.svg"),'&Save',self)
        self.exitAction = QAction(QIcon(":file_exit.svg"),'&Exit',self)
        #operation actions
        self.flipHAction = QAction(QIcon(":operation_flip_horizontal.svg"),'&Horizontal Flip',self)
        self.flipVAction = QAction(QIcon(":operation_flip_vertical.svg"),'&Vertical Flip',self)
        self.clockRot90Action = QAction(QIcon(":operation_clockwise_rotation_90.svg"),'&Clockwise Rot 90' + chr(176),self)
        self.anticlockRot90Action = QAction(QIcon(":operation_anticlockwise_rotation_90.svg"),'&anti-Clockwise Rot 90' + chr(176),self)
        self.FFT2DAction = QAction(QIcon(":operation_FFT.svg"),'&FFT 2D',self)
        self.iFFT2DAction = QAction(QIcon(":operation_iFFT.svg"),'&iFFT 2D',self)
        self.FFTShiftAction = QAction(QIcon(":operation_FFTShift.svg"),'&FFTshift 2D',self)
        self.iFFTShiftAction = QAction(QIcon(":operation_iFFTShift.svg"),'&iFFTshift 2D',self)
        self.resetAction = QAction(QIcon(":operation_reset.svg"),'&Reset',self)
        self.conjAction = QAction(QIcon(':operation_conjugate.svg'),'&Conjugate',self)
        self.reshapeAction = QAction(QIcon(':operation_reshape.svg'),'&Reshape',self)
        self.squeezeAction = QAction(QIcon(':operation_squeeze.svg'),'&Squeeze',self)
        self.permuteAction = QAction(QIcon(':operation_permute.svg'),'&Permute',self)
        #View actions
        self.playVideoAction = QAction(QIcon(':view_playVideo.svg'),'&Play Video',self)
        #figure actions
        self.changeTitleAction = QAction(QIcon(":figure_change_title.svg"),'&Change Title',self)
        self.posTitleInImgDisplayAction = QAction(QIcon(":figure_show_title_within_image.svg"),'&Show Title Within Image',self)

        #help actions
        self.aboutAction = QAction(QIcon(":help_about.svg"),'&About',self)
        
        #UI-file actions 
        self.exitAction.triggered.connect(self.exitApp)
        #UI-figure actions
        self.changeTitleAction.triggered.connect(self.changeTitle)
        self.aboutAction.triggered.connect(self.showAboutPage)

        #set shortcut for actions
        self.openAction.setShortcut('Ctrl+O')
        self.saveAction.setShortcut('Ctrl+S')
        self.exitAction.setShortcut('Ctrl+Q')

    def _createToolBar(self):
        fileToolBar = self.addToolBar('File')
        fileToolBar.setMovable(False)
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAction)
        operationToolBar = self.addToolBar('Operation')
        operationToolBar.setMovable(False)
        operationToolBar.addAction(self.flipHAction)
        operationToolBar.addAction(self.flipVAction)
        operationToolBar.addAction(self.clockRot90Action)
        operationToolBar.addAction(self.anticlockRot90Action)
        operationToolBar.addAction(self.FFT2DAction)
        operationToolBar.addAction(self.iFFT2DAction)
        operationToolBar.addAction(self.resetAction)
        ViewToolBar = self.addToolBar('View')
        ViewToolBar.addAction(self.playVideoAction)

    def _createContextMenu(self):
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.saveAction)
        separator = QAction(self)
        separator.setSeparator(True)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(separator)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.flipHAction)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.flipVAction)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.clockRot90Action)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.anticlockRot90Action)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.FFT2DAction)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.iFFT2DAction)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.FFTShiftAction)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.iFFTShiftAction)
        separator = QAction(self)
        separator.setSeparator(True)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(separator)
        self.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.addAction(self.resetAction)

    def exitApp(self):
        dlg = QMessageBox()
        dlg.setWindowTitle(self.appTitle)
        dlg.setWindowIcon(self.appIcon)
        dlg.setText('Your app will Exit, continue?')
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.Cancel)
        dlg.setIcon(QMessageBox.Icon().Question)
        response = dlg.exec()
        if response == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def showAboutPage(self):
        dlg = AboutDialog()
        dlg.exec()
    
    def changeTitle(self):
        text,ok_pressed = QInputDialog().getText(self,self.appTitle,'Please Enter expected title',QLineEdit.EchoMode.Normal,"")
        if ok_pressed:
            self.setWindowTitle(self.appTitle +'-'+ text)

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        self.setLayout(QVBoxLayout())
        self.logo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),os.path.join('resources','About_logo.jpg'))
        if os.path.isfile(self.logo_path):
            self.about_logo = QLabel(self)
            self.about_logo.setPixmap(QPixmap(self.logo_path).scaled(self.about_logo.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.FastTransformation))
        self.about_desc = QLabel(self)
        self.about_desc.setText(r'PyArrShow V1.0 by Kaixuan,Zhao et.al, in Guangdong Privincial Peoples Hospital.')
        self.about_desc.setWordWrap(True)
        self.about_logo.sizePolicy().setVerticalStretch(4)
        self.about_desc.sizePolicy().setVerticalStretch(1)
        self.layout().addWidget(self.about_logo)
        self.layout().addWidget(self.about_desc)
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.blockSignals(True)
        self.about_logo.setPixmap(QPixmap(self.logo_path).scaled(self.about_logo.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.FastTransformation))
        self.blockSignals(False)
        return super().resizeEvent(event)

class CentralWidgets(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUI()

    def setupUI(self):
        self.setLayout(QVBoxLayout())
        self.PilotFrame = PilotFrame()
        self.ImgDisplayFrame = ImgDisplayFrame()
        self.DataCursorFrame = DataCursorFrame()

        self.layout().addWidget(self.PilotFrame)
        self.layout().addWidget(self.ImgDisplayFrame)
        self.layout().addWidget(self.DataCursorFrame)

class pyArrShowModel:
    #pyArrShowModel Class, backend
    def __init__(self,nd_array):
        self.parsSetup()
        self.parsInit(nd_array)
    
    def loadData(self,nd_array):
        self.parsSetup()
        self.parsInit(nd_array)

    def parsSetup(self):
        self.nd_array = []
        self.data_dim = []
        self.data_type = []
        self.disp_img = []
        self.disp_qimg = []
        self.slicing_img = []
        self.operated_slicing_img = []
        self.slicing_str = []
        self.slicing_idx = []
        self.window_center = 0
        self.window_width = 0
        self.window_center_slider_value = 0
        self.window_width_slider_value = 0
        self.window_center_slider_value_MAX = 100   #todo 
        self.window_width_slider_value_MAX = 100
        self.window_center_slider_value_MIN = 0
        self.window_width_slider_value_MIN = 1
        self.window_center_anchor = 0           #denote where window center start
        self.window_center_MAX = 0
        self.window_width_MAX = 0
        self.data_cursor_pos = [0,0]
        self.data_cursor_val = 0
        self.mouse_roll_dim = []
        self.disp_img_modality = []
        self.operationFuncs = []
        self.eps = np.finfo(np.float64).eps
    
    def parsInit(self,nd_array):
        self.dtypeFilter(nd_array)
        self.initSlicingStr()       #string start from 1
        self.initSlicingIdx()       #idx start from 0
        self.resetOperations()
        self.initImgModalityOptions()
        self.updateDispQImgBySlicingStrWithResetCW()

    def dtypeFilter(self,nd_array):
        #nparray only
        assert(type(nd_array) == np.ndarray)

        data_type_options = ['int32','float64','complex128']
        data_type_guesses = ['int','float','complex']

        for index,data_type_guess in enumerate(data_type_guesses):
            if data_type_guess in nd_array.dtype.name:
                if index < 2: #not complex
                    self.data_type = 'float'
                    self.nd_array = nd_array.astype(data_type_options[1]) #to float64
                else:
                    self.data_type = 'complex'
                    self.nd_array = nd_array.astype(data_type_options[2]) #to complex128
        self.data_dim = self.nd_array.shape

    #******************************************************************
    #Initialization Step 1: Init Slicing string
    #******************************************************************
    def initSlicingStr(self):
        self.slicing_str = [str(i) for i in np.ones([len(self.data_dim)],dtype=np.int32).tolist()]
        self.active_im_dim = [0,1]
        self.slicing_str[self.active_im_dim[0]] = ':'
        self.slicing_str[self.active_im_dim[1]] = ':'
        self.slicing_lambda_func = lambda x : int(x) - 1 if x !=':' else x

    def getSlicingStr(self):
        return self.slicing_str
    
    def setSlicingStr(self,slicing_str):
        self.slicing_str = slicing_str
    #******************************************************************
    #Initialization Step 2: Init Slicing Idx
    #******************************************************************
    def initSlicingIdx(self):
        self.slicing_idx = [0] * len(self.data_dim)

    #******************************************************************
    #Initialization Step 3: Update slicing idx from slicing str
    #******************************************************************
    def updateSlicingIdx(self):
        self.slicing_idx = [str(self.slicing_lambda_func(item)) for item in self.slicing_str]

    #******************************************************************
    #Initialization Step 4: Reterive slicing image
    #******************************************************************
    def getSlicingImg(self):
        try:
            exec('self.slicing_img=self.nd_array[' + ','.join(self.slicing_idx) +']')
        except Exception as e:
            raise(repr(e) + 'When slicing data!')
        
    #******************************************************************
    #Initialization Step 5: Init ImgModalityOptions according to data type
    #******************************************************************
    def initImgModalityOptions(self):
        #init ImgModalityOptions
        self.ImgModalityOptionsDict = {0:'Magnitude',
                                 1:'Real',
                                 2:'Imaginary',
                                 3:'Complex',
                                 4:'Phase'}
        if self.data_type == 'complex':
            self.ImgModalityList = [i for i in range(len(self.ImgModalityOptionsDict))]
        elif self.data_type == 'float':
            self.ImgModalityList = [i for i in [0,1]]
        else:
            print('TypeError:Not supported data type!')
        
        self.ImgModalityOptions = [self.ImgModalityOptionsDict[i] for i in self.ImgModalityList]
        self.disp_img_modality = self.ImgModalityOptions[0]
        
    #******************************************************************
    #Initialization Step 6: excute operations on disp_img
    #******************************************************************
    def operationsExec(self):
        self.operated_slicing_img = self.slicing_img
        if self.operationFuncs is not None:
            for func in self.operationFuncs:
                self.operated_slicing_img = func(self.operated_slicing_img)
        self.operated_slicing_img = np.ascontiguousarray(self.operated_slicing_img)
    
    def resetOperations(self):
        self.operationFuncs = []

    def getOperationList(self):
        return self.operationFuncs
    #******************************************************************
    #Initialization Step 6: Reterive disp_img from data modality and slicing data
    #******************************************************************
    def updateDispImg(self):
        if self.disp_img_modality == 'Magnitude':
            self.disp_img = np.abs(self.operated_slicing_img)
        elif self.disp_img_modality == 'Real':
            self.disp_img = np.real(self.operated_slicing_img)
        elif self.disp_img_modality == 'Imaginary':
            self.disp_img = np.imag(self.operated_slicing_img)
        elif self.disp_img_modality == 'Complex':
            self.disp_img = self.operated_slicing_img
        elif self.disp_img_modality == 'Phase':
            self.disp_img = np.angle(self.operated_slicing_img,True)
        
    #******************************************************************
    #Initialization Step 7: Update window_center/_width(_Max)
    #******************************************************************
    def updateCWMax(self):
        if self.disp_img_modality in ['Magnitude','Real','Imaginary','Phase']:
            self.window_center_anchor = - 1 *(np.mean(self.disp_img) - np.min(self.disp_img))
            self.window_center_MAX = (np.max(self.disp_img) - np.min(self.disp_img)) * 2    #MAX tobe 2 times of mean value - min value, assume Gaussian distrib
            self.window_width_MAX = (np.max(self.disp_img) - np.min(self.disp_img)) * 4     #default 4 times of max diff
        elif self.disp_img_modality == 'Complex':
            self.window_center_anchor = 0
            self.window_center_MAX = (np.max(np.abs(self.disp_img)) - np.min(np.abs(self.disp_img))) * 2    #MAX tobe 2 times of mean value - min value, assume Gaussian distrib
            self.window_width_MAX = (np.max(np.abs(self.disp_img)) - np.min(np.abs(self.disp_img))) * 4     #default 4 times of max diff
    
    def initWCSliderValue(self):
        self.window_center_slider_value = 25
        self.window_width_slider_value = 25

    def updateCWValue(self):
        self.updateCValue()
        self.updateWValue()

    def updateCValue(self):
        self.window_center = self.window_center_MAX * self.window_center_slider_value/self.window_center_slider_value_MAX + self.window_center_anchor
    
    def updateWValue(self):
        self.window_width = self.window_width_MAX * self.window_width_slider_value/self.window_width_slider_value_MAX
    
    def fintTuneCW(self):
        window_center_ori = self.window_center - self.window_center_anchor
        window_width_ori = self.window_width
        self.updateCWMax()
        window_center_MAX_new = self.window_center_MAX + self.eps
        window_width_MAX_new = self.window_width_MAX + self.eps

        window_center_slider_value = window_center_ori / window_center_MAX_new * self.window_center_slider_value_MAX
        window_width_slider_value = window_width_ori / window_width_MAX_new * self.window_width_slider_value_MAX

        self.window_center_slider_value = np.max([np.min([np.round(window_center_slider_value),self.window_center_slider_value_MAX]),self.window_center_slider_value_MIN])
        self.window_width_slider_value = np.max([np.min([np.round(window_width_slider_value),self.window_width_slider_value_MAX]),self.window_width_slider_value_MIN])

        self.updateCWValue()

    #******************************************************************
    #Initialization Step 8: update disp_img to disp_qimage, RGB channel or Grayscale
    #******************************************************************
    def updateDispQImg(self):
        self.dispImg2dispQImage()

    def dispImg2dispQImage(self):
        if self.disp_img_modality in ['Magnitude','Real','Imaginary']:
            disp_img = self.ConvertTo16DigitsSCh(self.disp_img)
            self.disp_qimg = QImage(disp_img.data, self.disp_img.shape[1],self.disp_img.shape[0],QImage.Format.Format_Grayscale16)
        elif self.disp_img_modality == 'Complex':
            disp_img = self.ConvertTo8DigitsRGBCh(self.disp_img)
            self.disp_qimg = QImage(disp_img.data, disp_img.shape[1],disp_img.shape[0], disp_img.strides[0], QImage.Format.Format_RGB888)
        elif self.disp_img_modality == 'Phase':
            disp_img = self.ConvertTo8DigitsPhaseRGBCh(self.disp_img)
            self.disp_qimg = QImage(disp_img.data, disp_img.shape[1],disp_img.shape[0], disp_img.strides[0], QImage.Format.Format_RGB888)
        return self.disp_qimg

    def ConvertTo16DigitsSCh(self,disp_img):
        #convert disp_img to single-channel 16bit int array
        #convert to (0,1)
        disp_img = (disp_img - (self.window_center - self.window_width * 0.5)) / (self.window_width + self.eps)
        disp_img = np.where(disp_img <= 0, 0, disp_img)
        disp_img = np.where(disp_img >= 1, 1, disp_img)
        #to 16bit gray
        disp_img = np.floor(disp_img * (2**16))
        disp_img = np.where(disp_img == (2**16), 2**16 - 1, disp_img).astype(np.uint16) #overflow protection
        return disp_img
    
    def ConvertTo8DigitsRGBCh(self,disp_img):
        disp_img_magnitude = np.abs(disp_img)
        disp_img_phase = np.angle(self.disp_img,True)
        disp_img_magnitude = (disp_img_magnitude - (self.window_center - self.window_width*0.5)) / (self.window_width + self.eps)
        disp_img_magnitude = np.where(disp_img_magnitude <=0, 0, disp_img_magnitude)
        disp_img_magnitude = np.where(disp_img_magnitude >=1, 1, disp_img_magnitude)
        disp_img_magnitude = np.floor(disp_img_magnitude * (2**8))
        disp_img_phase_RGB = np.zeros((self.disp_img.shape[0],self.disp_img.shape[1],3))
        phase_spliter = np.array([np.min(disp_img_phase),np.mean([np.min(disp_img_phase),np.max(disp_img_phase)]), np.max(disp_img_phase)])
        phase_color = np.array([[1,0,0],[0,1,0],[0,0,1]]).reshape(3,1,1,3)
        disp_img_phase = np.repeat(np.expand_dims(disp_img_phase,len(disp_img_phase.shape)),3,axis=2)

        disp_img_phase_RGB = np.where(disp_img_phase<phase_spliter[1], phase_color[1] * (disp_img_phase-phase_spliter[0]) + phase_color[0]* (phase_spliter[1] - disp_img_phase),phase_color[2] * (disp_img_phase-phase_spliter[1]) + phase_color[1]* (phase_spliter[2] - disp_img_phase))
        disp_img_phase_RGB = np.floor(disp_img_phase_RGB/(phase_spliter[1] - phase_spliter[0] + self.eps)*disp_img_magnitude.reshape((self.disp_img.shape[0],self.disp_img.shape[1],1)))
        disp_img_phase_RGB = np.where(disp_img_phase_RGB == 256, 255, disp_img_phase_RGB).astype(np.uint8)
        return disp_img_phase_RGB
    
    def ConvertTo8DigitsPhaseRGBCh(self,disp_img):
        #for phase data only
        disp_img = (disp_img - (self.window_center - self.window_width*0.5)) / (self.window_width + self.eps)
        disp_img = np.where(disp_img <=0, 0, disp_img)
        disp_img = np.where(disp_img >=1, 1, disp_img)
        disp_img_phase_RGB = np.zeros((self.disp_img.shape[0],self.disp_img.shape[1],3))
        phase_color = np.array([[1,0,0],[0,1,0],[0,0,1]]).reshape(3,1,1,3)
        phase_spliter = np.array([0,0.5,1])
        disp_img = np.repeat(np.expand_dims(disp_img,len(disp_img.shape)),3,axis=2)

        disp_img_phase_RGB = np.where(np.array(disp_img<phase_spliter[2]) & np.array(disp_img>phase_spliter[1]), phase_color[2] * (disp_img-phase_spliter[1]) + phase_color[1]* (phase_spliter[2] - disp_img),phase_color[1] * (disp_img-phase_spliter[0]) + phase_color[0]* (phase_spliter[1] - disp_img))
        disp_img_phase_RGB = np.floor(disp_img_phase_RGB / (phase_spliter[1] - phase_spliter[0] + self.eps) * (2**8))
        disp_img_phase_RGB = np.where(disp_img_phase_RGB == 256, 255, disp_img_phase_RGB).astype(np.uint8)

        return disp_img_phase_RGB
    
    #func for new slicing str idx
    def updateDispQImgBySlicingStrWithResetCW(self):
        self.updateSlicingIdx()
        self.getSlicingImg()
        self.updateDispQImgByOpeationsWithResetCW()

    #func for operations btn clicked
    def updateDispQImgByOpeationsWithResetCW(self):
        self.operationsExec()
        self.updateDispQImgByImgModalityWithResetCW()

    #func for ImgModality ComboBox
    def updateDispQImgByImgModalityWithResetCW(self):
        self.updateDispImg()
        self.updateCWMax()
        self.initWCSliderValue()
        self.updateCValue()
        self.updateDispQImagByCW()

    #func for new slicing str idx
    def updateDispQImgBySlicingStr(self):
        self.updateSlicingIdx()
        self.getSlicingImg()
        self.updateDispQImgByOpeations()

    #func for operations btn clicked
    def updateDispQImgByOpeations(self):
        self.operationsExec()
        self.updateDispQImgByImgModality()
    
    #func for ImgModality ComboBox
    def updateDispQImgByImgModality(self):
        self.updateDispImg()
        self.fintTuneCW()
        self.updateDispQImagByCW()

    #func for Slider event
    def updateDispQImagByCW(self):
        self.updateDispQImg()
    
    #Slider related func
    def setCSliderValue(self,window_center_slider_value):
        self.window_center_slider_value = window_center_slider_value
    
    def getCSliderValue(self):
        return self.window_center_slider_value

    def setWSliderValue(self,window_width_slider_value):
        self.window_width_slider_value = window_width_slider_value

    def getWSliderValue(self):
        return self.window_width_slider_value

    def setDispImgModality(self,disp_img_modality):
        self.disp_img_modality = disp_img_modality

    def setWindowCenter(self,window_center):
        self.window_center = window_center
    
    def setWindowWidth(self,window_width):
        self.window_width = window_width
    
    def getWindowCenter(self):
        return self.window_center
    
    def getWindowWidth(self):
        return self.window_width

    def setSlicingStr(self,idx,val):
        self.slicing_str[idx] = val
        self.updateSlicingIdx()

    def getDispImg(self):
        return self.disp_img

    def getDispQImg(self):
        return self.disp_qimg
    
    def getData(self):
        return self.nd_array
    
    def getMouseRollDim(self):
        return self.mouse_roll_dim
    
    def setMouseRollDim(self,mouse_roll_dim):
        self.mouse_roll_dim = mouse_roll_dim
    
    def getWindowCenterMax(self):
        return self.window_center_MAX
    
    def getWindowWidthMax(self):
        return self.window_width_MAX
    
    def getWindowCenterAnchor(self):
        return self.window_center_anchor
    
        #operation slot on disp_pixmap
    def flipHorizontally(self,data_in):
        data_out = np.fliplr(data_in)
        return data_out

    def flipVertically(self,data_in):
        data_out = np.flipud(data_in)
        return data_out

    def clockwiseRot90(self,data_in):
        data_out = np.rot90(data_in, 1)
        return data_out

    def anticlockwiseRot90(self,data_in):
        data_out = np.rot90(data_in, -1)
        return data_out

    def FFT2D(self,data_in):
        data_out = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(data_in)))
        return data_out

    def iFFT2D(self,data_in):
        data_out = np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(data_in)))
        return data_out

    def FFTShift(self,data_in):
        data_out = np.fft.fftshift(data_in)
        return data_out

    def iFFTShift(self,data_in):
        data_out = np.fft.ifftshift(data_in)
        return data_out
    
    def conjugate(self,data_in):
        data_out = np.conj(data_in)
        return data_out


class pyArrShowController:
    #pyArrShowController class
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self.InitUI()
        self.cfgUIEvent()
        self.cfgMenuBtnActions()
    
    def InitUI(self):
        self._view.CentralWidgets.PilotFrame.initUI(self._model.data_dim,self._model.slicing_str,self._model.ImgModalityOptions,self._model.disp_img_modality)
        self.updateCWSliderFrame()
        self.updateImgDisplyFrame()
        self.updateImgDescFrame()
    
    def cfgUIEvent(self):
        self.cfgMouseOverImgDispEvent()
        self.cfgSliderEvent()
        self.cfgDataRangePlusBtnsEvent()
        self.cfgDataRangeEditLinesEvent()
        self.cfgDataRangeMinusBtnsEvent()
        self.cfgDataRangeMaxIdxBtnsEvent()
        self.cfgDataRangeImgModalityComboBoxEvent()
    
    def cfgRelseaseUIEvent(self):
        self.cfgReleaseSliderEvent()
        self.cfgReleaseDataRangePlusBtnsEvent()
        self.cfgReleaseDataRangeEditLinesEvent()
        self.cfgReleaseDataRangeMinusBtnsEvent()
        self.cfgReleaseDataRangeMaxIdxBtnsEvent()
        self.cfgReleaseDataRangeImgModalityComboBoxEvent()
        
    def cfgDataRangeImgModalityComboBoxEvent(self):
        self._view.CentralWidgets.PilotFrame.ImgModalityComboBox.activated.connect(self.DataRangeImgModalityComboBoxItemChoosen)
    
    def cfgReleaseDataRangeImgModalityComboBoxEvent(self):
        self._view.CentralWidgets.PilotFrame.ImgModalityComboBox.activated.disconnect()

    def DataRangeImgModalityComboBoxItemChoosen(self):
        self._model.setDispImgModality(self._view.CentralWidgets.PilotFrame.ImgModalityComboBox.currentText())
        self._model.updateDispQImgByImgModalityWithResetCW()
        self.updateCWSlider()
        self.updateImgDisplyFrame()
        self.updateImgDescFrame()

    def cfgDataRangeMaxIdxBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeMaxIdxs[btn_id].clicked.connect(partial(self.DataRangeMaxIdxBtnsClicked,btn_id))
    
    def cfgReleaseDataRangeMaxIdxBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeMaxIdxs[btn_id].clicked.disconnect()
    
    def DataRangeMaxIdxBtnsClicked(self,btn_id):
        self.setMouseRollActiveDim(btn_id)

    def cfgSliderEvent(self):
        self._view.CentralWidgets.PilotFrame.WSliderWidget.valueChanged.connect(self.WSliderPulled)
        self._view.CentralWidgets.PilotFrame.CSliderWidget.valueChanged.connect(self.CSliderPulled)
    
    def cfgReleaseSliderEvent(self):
        self._view.CentralWidgets.PilotFrame.WSliderWidget.valueChanged.disconnect()
        self._view.CentralWidgets.PilotFrame.CSliderWidget.valueChanged.disconnect()
    
    def updateCWSliderFrame(self):
        self.updateCWSlider()
        self.updateCWSliderLabel()

    def updateCWSlider(self):
        #update view window center
        self.updateCSlider()
        self.updateWSlider()
    
    def updateCWSliderLabel(self):
        self.updateCSliderLabel()
        self.updateWSliderLabel()

    def updateWSlider(self):
        self._view.CentralWidgets.PilotFrame.WSliderWidget.blockSignals(True)
        self._view.CentralWidgets.PilotFrame.WSliderWidget.setValue(self._model.getWSliderValue())
        self._view.CentralWidgets.PilotFrame.WSliderWidget.blockSignals(False)
        
    def updateWSliderLabel(self):
        self._view.CentralWidgets.PilotFrame.WLabelWidget.setText('{:.2g}'.format(self._model.getWindowWidth()))

    def updateCSlider(self):
        self._view.CentralWidgets.PilotFrame.CSliderWidget.blockSignals(True)
        self._view.CentralWidgets.PilotFrame.CSliderWidget.setValue(self._model.getCSliderValue())
        self._view.CentralWidgets.PilotFrame.CSliderWidget.blockSignals(False)
        
    def updateCSliderLabel(self):
        self._view.CentralWidgets.PilotFrame.CLabelWidget.setText('{:.2g}'.format(self._model.getWindowCenter()))
        
    def updateImgDisplyFrame(self):
        self._view.CentralWidgets.ImgDisplayFrame.updateImgDisplay(self._model.getDispQImg())

    def updateImgDescFrame(self):
        self._view.CentralWidgets.PilotFrame.updateImgDesc(self._model.getDispImg())

    def WSliderPulled(self):
        self._model.setWSliderValue(self._view.CentralWidgets.PilotFrame.WSliderWidget.value())
        self._model.updateWValue()
        self.updateWSliderLabel()
        self._model.updateDispQImg()
        self.updateImgDisplyFrame()
    
    def CSliderPulled(self):
        self._model.setCSliderValue(self._view.CentralWidgets.PilotFrame.CSliderWidget.value())
        self._model.updateCValue()
        self.updateCSliderLabel()
        self._model.updateDispQImg()
        self.updateImgDisplyFrame()

        #mouse over imgdisplay for data cursor
    def cfgMouseOverImgDispEvent(self):
        self._view.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.setMouseTracking(True)
        self._view.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.mouseMoveEvent = self.mouseMoveOverImgDisplay
        self._view.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.wheelEvent = self.mouseOverImgDisplayWheelEvent


    def mouseMoveOverImgDisplay(self,event):
        if not event.button():
            data_cursor_pos_x = np.floor(event.position().x() * self._model.operated_slicing_img.shape[1] / self._view.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.size().width()).astype(int)
            data_cursor_pos_y = np.floor(event.position().y() * self._model.operated_slicing_img.shape[0] / self._view.CentralWidgets.ImgDisplayFrame.ImgDisplayHandle.size().height()).astype(int)
            self._model.data_cursor_pos = [data_cursor_pos_x + 1,data_cursor_pos_y + 1] #idx start from 1
            self._model.data_cursor_val = self._model.operated_slicing_img[data_cursor_pos_y,data_cursor_pos_x]
            self._view.CentralWidgets.DataCursorFrame.updateText(self._model.data_cursor_val,self._model.data_cursor_pos)

    def mouseOverImgDisplayWheelEvent(self,event):
        if bool(self._model.mouse_roll_dim):
            if event.angleDelta().y() > 0:
                self.DataRangePlusBtnsClicked(self._model.mouse_roll_dim)
            else:
                self.DataRangeMinusBtnsClicked(self._model.mouse_roll_dim)

    def cfgDataRangePlusBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangePlusBtns[btn_id].clicked.connect(partial(self.DataRangePlusBtnsClicked,btn_id))
    
    def cfgReleaseDataRangePlusBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangePlusBtns[btn_id].clicked.disconnect()

    def DataRangePlusBtnsClicked(self,btn_id):
        self.setMouseRollActiveDim(btn_id)
        current_text = self._view.CentralWidgets.PilotFrame.DataRangeEditLines[btn_id].text()
        if  current_text != ':':
            current_value = int(current_text)
            if current_value < self._model.data_dim[btn_id]:
                current_value = current_value + 1
                self._model.slicing_str[btn_id] = str(current_value)
                self._model.updateDispQImgBySlicingStr()
                self._view.CentralWidgets.PilotFrame.DataRangeEditLines[btn_id].setText("{0}".format(self._model.slicing_str[btn_id]))
                self._view.CentralWidgets.PilotFrame.updateImgDesc(self._model.getDispImg())
                self.updateImgDisplyFrame()
                self.updateCWSliderFrame()
            elif self.playVideoFlag:
                self.timer.stop()
                

    def setMouseRollActiveDim(self,btn_id):
        self._model.setMouseRollDim(btn_id)
        self._view.CentralWidgets.PilotFrame.setBtnActived(self._model.getMouseRollDim())

    def cfgDataRangeMinusBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeMinusBtns[btn_id].clicked.connect(partial(self.DataRangeMinusBtnsClicked,btn_id))
    
    def cfgReleaseDataRangeMinusBtnsEvent(self):
        for btn_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeMinusBtns[btn_id].clicked.disconnect()

    def DataRangeMinusBtnsClicked(self,btn_id):
        self.setMouseRollActiveDim(btn_id)
        current_text = self._view.CentralWidgets.PilotFrame.DataRangeEditLines[btn_id].text()
        if  current_text != ':':
            current_value = int(current_text)
            if current_value > 1:
                current_value = current_value - 1
                self._model.slicing_str[btn_id] = str(current_value)
                self._model.updateDispQImgBySlicingStr()
                self._view.CentralWidgets.PilotFrame.DataRangeEditLines[btn_id].setText("{0}".format(self._model.slicing_str[btn_id]))
                self._view.CentralWidgets.PilotFrame.updateImgDesc(self._model.getDispImg())
                self.updateImgDisplyFrame()
                self.updateCWSliderFrame()
    
    def cfgDataRangeEditLinesEvent(self):
        for el_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeEditLines[el_id].textEdited.connect(partial(self.DataRangeEditLineTextEdited,el_id))

    def cfgReleaseDataRangeEditLinesEvent(self):
        for el_id in range(len(self._model.data_dim)):
            self._view.CentralWidgets.PilotFrame.DataRangeEditLines[el_id].textEdited.disconnect()
    
    def DataRangeEditLineTextEdited(self,el_id,idx_new):
        self.setMouseRollActiveDim(el_id)
        if idx_new != '':
            idx_ori = self._model.slicing_str[el_id]
            msgBox = QMessageBox(self._view.CentralWidgets.PilotFrame.DataRangeEditLines[el_id])
            msgBox.setWindowTitle('Error Message')
            if idx_new != ':':
                try:
                    idx_new_int = int(idx_new)
                except TypeError:
                    msgBox.setText('Value Error: Input is expected integer between {0} and {1}, or {2}'.format(1,self._model.data_dim[el_id],':'))
                    reply = msgBox.exec()

                    if reply == QMessageBox.StandardButton.Ok:
                        self._view.CentralWidgets.PilotFrame.DataRangeEditLines[el_id].setText(idx_ori)
                
                if (idx_new_int >= 1) & (idx_new_int <= self._model.data_dim[el_id]) & (idx_new != idx_ori):
                    self._model.slicing_str[el_id] = idx_new
                    self._model.updateDispQImgBySlicingStr()
                    self._view.CentralWidgets.PilotFrame.updateImgDesc(self._model.getDispImg())        #update data desc
                    self.updateImgDisplyFrame()
                    self.updateCWSliderFrame()
                else:
                    msgBox.setText('Value Error: Input is expected integer between {0} and {1}, or {2}'.format(1,self._model.data_dim[el_id],':'))
                    reply = msgBox.exec()

                    if reply == QMessageBox.StandardButton.Ok:
                        #roll-back
                        self._view.CentralWidgets.PilotFrame.DataRangeEditLines[el_id].setText(idx_ori)
            else:
                self._model.slicing_str[el_id] = idx_new
                self._model.updateDispQImgBySlicingStr()
                self._view.CentralWidgets.PilotFrame.updateImgDesc(self._model.getDispImg())        #update data desc
                self.updateImgDisplyFrame()
                self.updateCWSliderFrame()

    #link button action to slot
    def cfgMenuBtnActions(self):
        #File btns action
        self._view.openAction.triggered.connect(self.loadFileEvent)
        self._view.saveAction.triggered.connect(self.saveFileEvent)
        #operation btns action
        self._view.flipHAction.triggered.connect(self.flipHorizontally)
        self._view.flipVAction.triggered.connect(self.flipVertically)
        self._view.clockRot90Action.triggered.connect(self.clockwiseRot90)
        self._view.anticlockRot90Action.triggered.connect(self.anticlockwiseRot90)
        self._view.FFT2DAction.triggered.connect(self.FFT2D)
        self._view.iFFT2DAction.triggered.connect(self.iFFT2D)
        self._view.FFTShiftAction.triggered.connect(self.FFTShift)
        self._view.iFFTShiftAction.triggered.connect(self.iFFTShift)
        self._view.resetAction.triggered.connect(self.resetOperations)
        self._view.conjAction.triggered.connect(self.conjugate)
        self._view.reshapeAction.triggered.connect(self.reshape)
        self._view.squeezeAction.triggered.connect(self.squeeze)
        self._view.permuteAction.triggered.connect(self.permute)
        #View btns action
        self._view.playVideoAction.triggered.connect(self.playVideo)
        self.cfgPlayVideoAction()
        #figure btns action
        # self._view.posTitleInImgDisplayAction.triggered.connect(self.posTitleInImgDisplay)

    #File Slot
    def loadFileEvent(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setFilter(QDir.Filter.NoFilter)
        if dlg.exec():
            filenames = dlg.selectedFiles()
            self.cfgRelseaseUIEvent()
            self._model.loadData(np.load(filenames[0]))
            self.InitUI()
            self.cfgUIEvent()

    def saveFileEvent(self):
        dlg = QFileDialog()
        file_name = dlg.getSaveFileName(filter="Images (*.jpg)")
        if file_name:
            with open(file_name[0],'wb') as f:
                status = self._view.CentralWidgets.ImgDisplayFrame.getDispPixmap().save(file_name[0],format = os.path.splitext(file_name[0])[1], quality = 100)
                if not status:
                    dlg = QMessageBox()
                    dlg.setWindowTitle(self._view.appTitle)
                    dlg.setWindowIcon(self._view.appIcon)
                    dlg.setText('Error when saving Images!')
                    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dlg.setIcon(QMessageBox.Icon().Warning)
                    dlg.exec()


    def resetOperations(self):
        self._model.getOperationList().clear()
        self._model.updateDispQImgByOpeationsWithResetCW()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()
    
    #operation slot
    def flipHorizontally(self):
        self._model.getOperationList().append(self._model.flipHorizontally)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def flipVertically(self):
        self._model.getOperationList().append(self._model.flipVertically)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def clockwiseRot90(self):
        self._model.getOperationList().append(self._model.clockwiseRot90)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def anticlockwiseRot90(self):
        self._model.getOperationList().append(self._model.anticlockwiseRot90)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def FFT2D(self):
        self._model.getOperationList().append(self._model.FFT2D)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def iFFT2D(self):
        self._model.getOperationList().append(self._model.iFFT2D)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def FFTShift(self):
        self._model.getOperationList().append(self._model.FFTShift)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()

    def iFFTShift(self):
        self._model.getOperationList().append(self._model.iFFTShift)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()
    
    def conjugate(self):
        self._model.getOperationList().append(self._model.conjugate)
        self._model.updateDispQImgByOpeations()
        self.updateImgDisplyFrame()
        self.updateCWSliderFrame()
    
    def reshape(self):
        shape,ok_pressed = QInputDialog().getText(self._view,self._view.appTitle,'Please Enter expected shape',QLineEdit.EchoMode.Normal,str(self._model.getData().shape))
        if ok_pressed:
            shape = tuple(map(int,shape.replace('(','').replace(')','').replace('[','').replace(']','').split(',')))
            self.cfgRelseaseUIEvent()
            self._model.loadData(np.reshape(self._model.getData(),shape))
            self.InitUI()
            self.cfgUIEvent()

    def squeeze(self):
        self.cfgRelseaseUIEvent()
        self._model.loadData(np.squeeze(self._model.getData()))
        self.InitUI()
        self.cfgUIEvent()

    def permute(self):
        shape,ok_pressed = QInputDialog().getText(self._view,self._view.appTitle,'Please Enter expected permute order',QLineEdit.EchoMode.Normal,'(' + ','.join([str(i) for i in range(len(self._model.data_dim))]) + ')')
        if ok_pressed:
            shape = tuple(map(int,shape.replace('(','').replace(')','').replace('[','').replace(']','').split(',')))
            self.cfgRelseaseUIEvent()
            self._model.loadData(np.transpose(self._model.getData(),shape))
            self.InitUI()
            self.cfgUIEvent()

    def playVideo(self):
        if self._model.getMouseRollDim():
            btn_id = self._model.getMouseRollDim()
            current_text = self._view.CentralWidgets.PilotFrame.DataRangeEditLines[btn_id].text()
            if current_text != ':':
                #reset data range value to 1
                self.DataRangeEditLineTextEdited(self,btn_id,np.min(1,self._model.data_dim[btn_id]))
                self.playVideoFlag = True
                self.timer.timeout.connect(partial(self.DataRangePlusBtnsClicked,btn_id))
                self.timer.start()
        else:
            dlg = QMessageBox()
            dlg.setWindowTitle(self._view.appTitle)
            dlg.setWindowIcon(self._view.appIcon)
            dlg.setText('Error: Roll dim not choosen!')
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon().Warning)
            dlg.exec()
    
    def cfgPlayVideoAction(self):
        self.timer = QTimer()
        self.timer.setInterval(200) #in ms
        self.playVideoFlag = False

    # #Figure slot
    # def posTitleInImgDisplay(self):
    #     self.title_label = QLabel()

class PyArrShow:
    def __init__(self,np_array = np.random.randn(256,256)):
        self.app = QApplication([])
        self.show(np_array)
        # view = pyArrShowWindow()
        # view.resize(500,900)
        # view.show()
        # pyArrShowController(model = pyArrShowModel(np_array), view = view)
        # self.app.exec()
        # sys.exit()
    
    def show(self,np_array):
        view = pyArrShowWindow()
        view.resize(500,900)
        view.show()
        pyArrShowController(model = pyArrShowModel(np_array), view = view)
        self.app.exec()

        

if __name__ == '__main__':
    im_c = np.random.rand(256,256,3,3).astype(float) + np.random.rand(256,256,3,3).astype(float) * 1j
    pas = PyArrShow()
    pas.show(im_c)
    pas.show(im_c)
    print('dirty trick')