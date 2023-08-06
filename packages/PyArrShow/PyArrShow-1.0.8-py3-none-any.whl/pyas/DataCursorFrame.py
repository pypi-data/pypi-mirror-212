import numpy as np
import sys
from PySide6.QtWidgets import (QApplication,QHBoxLayout,QLabel,QFrame,QLayout)
from PySide6.QtGui import QAction, QImage, qRgb, QPixmap,QMouseEvent
from PySide6.QtCore import Qt


class DataCursorFrame(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setupUI()
        self.cfgUIStyle()
        # self.point_val = 0. + 0. * 1j
        # self.point_pos = [0,0]
    
    def setupUI(self):
        self.setLayout(QHBoxLayout())
        #point pos frame
        self.PosFrame = QFrame()
        self.PosFrame.setLayout(QHBoxLayout())
        self.PosWidgetKey = QLabel()
        self.PosWidgetKey.setText('X / Y')
        self.PosWidgetVal = QLabel()
        self.PosWidgetVal.setText('{0} / {1}'.format('-','-'))
        self.PosWidgetKey.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.PosWidgetVal.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.PosFrame.layout().addWidget(self.PosWidgetKey)
        self.PosFrame.layout().addWidget(self.PosWidgetVal)
        #point Re frame
        self.ReFrame = QFrame()
        self.ReFrame.setLayout(QHBoxLayout())
        self.ReWidgetKey = QLabel()
        self.ReWidgetKey.setText('Re:')
        self.ReWidgetVal = QLabel()
        self.ReWidgetVal.setText('{0}'.format('-'))
        self.ReWidgetKey.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ReWidgetVal.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ReFrame.layout().addWidget(self.ReWidgetKey)
        self.ReFrame.layout().addWidget(self.ReWidgetVal)
        #point Im frame
        self.ImFrame  = QFrame()
        self.ImFrame.setLayout(QHBoxLayout())
        self.ImWidgetKey = QLabel()
        self.ImWidgetKey.setText('Im:')
        self.ImWidgetVal = QLabel()
        self.ImWidgetVal.setText('{0}'.format('-'))
        self.ImWidgetKey.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ImWidgetVal.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ImFrame.layout().addWidget(self.ImWidgetKey)
        self.ImFrame.layout().addWidget(self.ImWidgetVal)
        #point Abs frame
        self.AbsFrame = QFrame()
        self.AbsFrame.setLayout(QHBoxLayout())
        self.AbsWidgetKey = QLabel()
        self.AbsWidgetKey.setText('Abs:')
        self.AbsWidgetVal = QLabel()
        self.AbsWidgetVal.setText('{0}'.format('-'))
        self.AbsWidgetKey.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.AbsWidgetVal.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.AbsFrame.layout().addWidget(self.AbsWidgetKey)
        self.AbsFrame.layout().addWidget(self.AbsWidgetVal)
        #point Pha frame
        self.PhaFrame = QFrame()
        self.PhaFrame.setLayout(QHBoxLayout())
        self.PhaWidgetKey = QLabel()
        self.PhaWidgetKey.setText('Phase:')
        self.PhaWidgetVal = QLabel()
        self.PhaWidgetVal.setText('{0}{1}'.format('-',chr(176)))
        self.PhaWidgetKey.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.PhaWidgetVal.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.PhaFrame.layout().addWidget(self.PhaWidgetKey)
        self.PhaFrame.layout().addWidget(self.PhaWidgetVal)

        self.layout().addWidget(self.PosFrame)
        self.layout().addWidget(self.ReFrame)
        self.layout().addWidget(self.ImFrame)
        self.layout().addWidget(self.AbsFrame)
        self.layout().addWidget(self.PhaFrame)

        self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.setFixedHeight(self.layout().totalMinimumSize().height())

    def cfgUIStyle(self):
        # DataCursorFrame UI
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        # PosFrame UI
        self.PosFrame.setFrameShape(QFrame.Shape.Box)
        self.PosFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # ReFrame UI
        self.ReFrame.setFrameShape(QFrame.Shape.Box)
        self.ReFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # ImFrame UI
        self.ImFrame.setFrameShape(QFrame.Shape.Box)
        self.ImFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # AbsFrame UI
        self.AbsFrame.setFrameShape(QFrame.Shape.Box)
        self.AbsFrame.setFrameShadow(QFrame.Shadow.Sunken)
        # PhaFrame UI
        self.PhaFrame.setFrameShape(QFrame.Shape.Box)
        self.PhaFrame.setFrameShadow(QFrame.Shadow.Sunken)
    
    def updateText(self,point_val,point_pos):
        self.PosWidgetVal.setText('{:>4d} / {:>4d}'.format(point_pos[0],point_pos[1]))
        self.ReWidgetVal.setText('{:.4g}'.format(np.real(point_val)))
        self.ImWidgetVal.setText('{:.4g}'.format(np.imag(point_val)))
        self.AbsWidgetVal.setText('{:.4g}'.format(np.abs(point_val)))
        self.PhaWidgetVal.setText('{:.2f}{}'.format(np.angle(point_val,True),chr(176)))
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = DataCursorFrame()
    test.show()
    sys.exit(app.exec_())