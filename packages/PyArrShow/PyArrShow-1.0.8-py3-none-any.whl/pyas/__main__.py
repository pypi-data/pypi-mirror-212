#!usr/bin/python
import numpy as np

from pyas.model import pyArrShowModel
from pyas.view import pyArrShowWindow
from pyas.controller import pyArrShowController
from PySide6.QtWidgets import QApplication
from pyas.qrc_resources import *
from PySide6.QtWidgets import QApplication

class PyArrShow:
    def __init__(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        # self.show(np_array)
    
    def show(self,np_array = np.random.randn(256,256)):
        view = pyArrShowWindow()
        view.resize(500,900)
        view.show()
        pyArrShowController(model = pyArrShowModel(np_array), view = view)
        self.app.exec()

def main():
    pas = PyArrShow()
    pas.show()

if __name__ == '__main__':
    main()
    # im_c = np.random.rand(256,256,3,3).astype(float) + np.random.rand(256,256,3,3).astype(float) * 1j
    # pas = PyArrShow()
    # pas.show(im_c)
    # pas.show(im_c)
    # print('dirty trick')