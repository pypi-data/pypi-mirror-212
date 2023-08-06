import numpy as np
from PySide6.QtGui import QAction, QImage, QIcon,qRgb, QPixmap,QMouseEvent,QResizeEvent
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