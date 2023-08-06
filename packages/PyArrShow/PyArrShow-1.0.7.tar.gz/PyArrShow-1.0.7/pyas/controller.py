import os
from functools import partial
import numpy as np

from PySide6.QtWidgets import (QFileDialog,QInputDialog,QLineEdit,QMessageBox)
from PySide6.QtCore import Slot,Qt,QSize,QRect,QDir,QTimer

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
