import os
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QDialog,QLabel,QInputDialog,
                               QLineEdit,QMessageBox)
from PySide6.QtGui import QAction, QIcon,QPixmap,QResizeEvent
from PySide6.QtCore import Qt
from pyas.DataCursorFrame import DataCursorFrame
from pyas.ImgDisplayFrame import ImgDisplayFrame
from pyas.PilotFrame import PilotFrame
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