import pyqtgraph
import sys
import os
from pyqtgraph.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pandas import DataFrame
from pandas import read_csv
from collections import deque
import serial
import serial.tools.list_ports
from datetime import datetime
import binascii
import numpy as np
import math
import cv2
import threading
import json
import copy
from tobiiglassesctrl import TobiiGlassesController
import matplotlib.style as mplstyle

class ThirdWindow(QWidget):
    def __init__(self,all_name,width_px,height_px):
        super().__init__()
        self.root_data = all_name
        self.width_px = width_px
        self.height_px = height_px
        self.read_csv_all()
        self.A_1 = 0
        self.E_1 = 0
        self.X_1 = 0
        self.Y_1 = 0
        self.Z_1 = 0

        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def outlier_iqr(self,data,row_f,row_s): 
        q25, q75 = data.iloc[row_f:row_s].quantile(0.25), data.iloc[row_f:row_s].quantile(0.75)            
        IQR = q75 - q25    
        cut_off = IQR * 1.5          
        lower, upper = q25 - cut_off, q75 + cut_off
        for i in range(len(data.iloc[row_f:row_s])):
            if (data.iloc[row_f+i] < upper) & (data.iloc[row_f+i] > lower):
                data.iloc[row_f+i] = data.iloc[row_f+i]
            else :
                data.iloc[row_f+i] = None
        return data
        
    def read_csv_all(self):
        global DF_Result
        global OutFileName
        global j
        global ck_area
        j = 0
        self.ck_area = 0
        DF_Date = datetime.now().strftime('%Y-%m-%d-%H-%M')
        OutFileName = "Export_Data_%s" %DF_Date
        DF_Result_origin = read_csv(self.root_data, index_col =0)
        DF_Result = DF_Result_origin.copy()
        Font_3 = QFont('Bahnschrift SemiLight', 8)   
        Font_5 = QFont("Bahnschrift SemiLight", 8, QFont.Bold)
        Font_6 = QFont("Bahnschrift SemiLight", 10, QFont.Bold)
        
        vbox0 = QVBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        vbox4 = QVBoxLayout()
        vbox5 = QVBoxLayout()
        vbox6 = QVBoxLayout()
        hbox0 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()        
        hbox4 = QHBoxLayout()        
        hbox5 = QHBoxLayout()
        gbox0 = QVBoxLayout()
        gbox1 = QVBoxLayout()
        gbox2 = QVBoxLayout()
        gbox3 = QVBoxLayout()
        gbox4 = QVBoxLayout()
        gbox5 = QVBoxLayout()
        grpbox0 = QHBoxLayout()
        grpbox2 = QHBoxLayout()
        grpbox1 = QHBoxLayout()
        epbox = QHBoxLayout()
              
        graph_label_Style = "color: gray;""font-size: 9pt;""font-weight : bold"
        self.stringaxisA = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisAOM = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisE = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisX = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisY = pyqtgraph.AxisItem(orientation='bottom')
        self.stringaxisZ = pyqtgraph.AxisItem(orientation='bottom')
        self.Azi_label = QLabel("        Azimuth (Deg)",self)
        self.Azi_label.setStyleSheet(graph_label_Style)
        self.Azi = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisA})
        self.AOM_label = QLabel("        AOM Status",self)
        self.AOM_label.setStyleSheet(graph_label_Style)
        self.AOM = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisAOM})
        self.Elevation_label = QLabel("        Elevation (Deg)",self)
        self.Elevation_label.setStyleSheet(graph_label_Style)
        self.Elevation = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisE})
        self.Xaxis_label = QLabel("        Xaxis (mm)",self)
        self.Xaxis_label.setStyleSheet(graph_label_Style)
        self.Xaxis = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisX})
        self.Yaxis_label = QLabel("        Yaxis (mm)",self)
        self.Yaxis_label.setStyleSheet(graph_label_Style)
        self.Yaxis = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisY})
        self.Zaxis_label = QLabel("        Zaxis (mm)",self)
        self.Zaxis_label.setStyleSheet(graph_label_Style)
        self.Zaxis = pyqtgraph.PlotWidget(axisItems={'bottom': self.stringaxisZ})
        labelStyle = {'color': '#828282', 'font-size': '9pt', 'font-weight' : 'bold' }
        self.Zaxis.setLabel('bottom', 'Time(s)', **labelStyle)
        
        self.Azi.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.AOM.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.Elevation.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.Xaxis.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.Yaxis.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.Zaxis.getAxis('left').setStyle(tickFont = Font_3, tickTextOffset=6)
        self.Azi.getAxis('bottom').setStyle(showValues=False)
        self.AOM.getAxis('bottom').setStyle(showValues=False)
        self.Elevation.getAxis('bottom').setStyle(showValues=False)
        self.Xaxis.getAxis('bottom').setStyle(showValues=False)
        self.Yaxis.getAxis('bottom').setStyle(showValues=False)        
        self.Zaxis.getAxis('bottom').setStyle(tickFont = Font_3, tickTextOffset=6)
        
        self.Azi.showGrid(x=True, y=True)
        self.AOM.showGrid(x=True, y=True)
        self.Elevation.showGrid(x=True, y=True)
        self.Xaxis.showGrid(x=True, y=True)
        self.Yaxis.showGrid(x=True, y=True)
        self.Zaxis.showGrid(x=False, y=True)
        self.Azi.setBackground((240,240,240))
        self.AOM.setBackground((240,240,240))
        self.Elevation.setBackground((240,240,240))
        self.Xaxis.setBackground((240,240,240))
        self.Yaxis.setBackground((240,240,240))
        self.Zaxis.setBackground((240,240,240))
        pen_black = pyqtgraph.mkPen(color = (0,0,0))
        pen_Red = pyqtgraph.mkPen(color = (255,0,0))
        pen_Blue = pyqtgraph.mkPen(color = (0,0,255))
        pen_Green = pyqtgraph.mkPen(color = (0,255,0))
        pen_Yellow = pyqtgraph.mkPen(color = (0,0,0),style=QtCore.Qt.DashLine)
        self.ALine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.ALine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.ALine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.ALine_3 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.ALine_4 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.AOLine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.AOLine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.AOLine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.AOLine_3 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.AOLine_4 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.ELine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.ELine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.ELine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Red)
        self.ELine_3 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.ELine_4 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Blue)
        self.XLine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.XLine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        self.XLine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        self.YLine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.YLine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        self.YLine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        self.ZLine = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_Yellow)
        self.ZLine_1 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        self.ZLine_2 = pyqtgraph.InfiniteLine(angle=90, movable=False,pen = pen_black)
        #self.hLine = pyqtgraph.InfiniteLine(angle=0, movable=False)
        self.cursorlabel = pyqtgraph.TextItem(anchor=(-1,10))
        self.Azi.addItem(self.ALine, ignoreBounds=True)
        self.Azi.addItem(self.ALine_1, ignoreBounds=True)
        self.Azi.addItem(self.ALine_2, ignoreBounds=True)
        self.Azi.addItem(self.ALine_3, ignoreBounds=True)
        self.Azi.addItem(self.ALine_4, ignoreBounds=True)
        self.AOM.addItem(self.AOLine, ignoreBounds=True)
        self.AOM.addItem(self.AOLine_1, ignoreBounds=True)
        self.AOM.addItem(self.AOLine_2, ignoreBounds=True)
        self.AOM.addItem(self.AOLine_3, ignoreBounds=True)
        self.AOM.addItem(self.AOLine_4, ignoreBounds=True)
        self.Elevation.addItem(self.ELine, ignoreBounds=True)
        self.Elevation.addItem(self.ELine_1, ignoreBounds=True)
        self.Elevation.addItem(self.ELine_2, ignoreBounds=True)
        self.Elevation.addItem(self.ELine_3, ignoreBounds=True)
        self.Elevation.addItem(self.ELine_4, ignoreBounds=True)
        self.Xaxis.addItem(self.XLine, ignoreBounds=True)
        self.Xaxis.addItem(self.XLine_1, ignoreBounds=True)
        self.Xaxis.addItem(self.XLine_2, ignoreBounds=True)
        self.Yaxis.addItem(self.YLine, ignoreBounds=True)
        self.Yaxis.addItem(self.YLine_1, ignoreBounds=True)
        self.Yaxis.addItem(self.YLine_2, ignoreBounds=True)
        self.Zaxis.addItem(self.ZLine, ignoreBounds=True)
        self.Zaxis.addItem(self.ZLine_1, ignoreBounds=True)
        self.Zaxis.addItem(self.ZLine_2, ignoreBounds=True)
        
        self.Azi.scene().sigMouseMoved.connect(self.mouseMoved_A)
        self.Azi.scene().sigMouseClicked.connect(self.onClick_A)
        self.Azi.scene().sigMouseMoved.connect(self.mouseMoved_E)
        self.Azi.scene().sigMouseClicked.connect(self.onClick_E)
        self.Azi.scene().sigMouseMoved.connect(self.mouseMoved_X)
        self.Azi.scene().sigMouseMoved.connect(self.mouseMoved_Y)
        self.Azi.scene().sigMouseMoved.connect(self.mouseMoved_Z)
        self.Elevation.scene().sigMouseMoved.connect(self.mouseMoved_A)
        self.Elevation.scene().sigMouseClicked.connect(self.onClick_A)        
        self.Elevation.scene().sigMouseMoved.connect(self.mouseMoved_E)
        self.Elevation.scene().sigMouseClicked.connect(self.onClick_E)
        self.Elevation.scene().sigMouseMoved.connect(self.mouseMoved_X)
        self.Elevation.scene().sigMouseMoved.connect(self.mouseMoved_Y)
        self.Elevation.scene().sigMouseMoved.connect(self.mouseMoved_Z)
        self.AOM.scene().sigMouseMoved.connect(self.mouseMoved_A)
        self.AOM.scene().sigMouseClicked.connect(self.onClick_A)
        self.AOM.scene().sigMouseMoved.connect(self.mouseMoved_E)
        self.AOM.scene().sigMouseClicked.connect(self.onClick_E)
        self.AOM.scene().sigMouseMoved.connect(self.mouseMoved_X)
        self.AOM.scene().sigMouseMoved.connect(self.mouseMoved_Y)
        self.AOM.scene().sigMouseMoved.connect(self.mouseMoved_Z)      
        self.Xaxis.scene().sigMouseMoved.connect(self.mouseMoved_X)
        self.Yaxis.scene().sigMouseMoved.connect(self.mouseMoved_Y)
        self.Zaxis.scene().sigMouseMoved.connect(self.mouseMoved_Z)
        
        self.export_button = QPushButton('\nData Export\n',self)
        self.export_button.setCheckable(True)
        self.export_button.setStyleSheet("color:rgb(0, 0, 0);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 2px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 8px")
        self.export_button.setFont(Font_6)
        self.export_button.clicked.connect(self.f_export_button)
        #왼쪽        
        
        self.label_0f = QLabel('1st 평균값\nNone', self)
        self.label_0s = QLabel('2nd 평균값\nNone', self)
        self.label_0m = QLabel('평균값 차이\nNone', self)
        self.label_0f.setAlignment(Qt.AlignCenter)
        self.label_0s.setAlignment(Qt.AlignCenter)
        self.label_0m.setAlignment(Qt.AlignCenter)
        self.label_0f.setStyleSheet("color:rgb(44,106, 180);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0s.setStyleSheet("color:rgb(44,106, 180);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0m.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0f.setFont(Font_5)
        self.label_0s.setFont(Font_5)
        self.label_0m.setFont(Font_5)
        #왼쪽
        self.label_2f = QLabel('1st 평균값\nNone', self)
        self.label_2s = QLabel('2nd 평균값\nNone', self)
        self.label_2m = QLabel('평균값 차이\nNone', self)
        self.label_2f.setAlignment(Qt.AlignCenter)
        self.label_2s.setAlignment(Qt.AlignCenter)
        self.label_2m.setAlignment(Qt.AlignCenter)
        self.label_2f.setStyleSheet("color:rgb(44,106, 180);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2s.setStyleSheet("color:rgb(44,106, 180);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2m.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2f.setFont(Font_5)
        self.label_2s.setFont(Font_5)
        self.label_2m.setFont(Font_5)
        
#오른쪽
        self.label_0f_L = QLabel('1st 평균값\nNone', self)
        self.label_0s_L = QLabel('2nd 평균값\nNone', self)
        self.label_0m_L = QLabel('평균값 차이\nNone', self)
        self.label_0f_L.setAlignment(Qt.AlignCenter)
        self.label_0s_L.setAlignment(Qt.AlignCenter)
        self.label_0m_L.setAlignment(Qt.AlignCenter)
        self.label_0f_L.setStyleSheet("color:rgb(203,26,126);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0s_L.setStyleSheet("color:rgb(203,26,126);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0m_L.setStyleSheet("color:rgb(0, 0, 0);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_0f_L.setFont(Font_5)
        self.label_0s_L.setFont(Font_5)
        self.label_0m_L.setFont(Font_5)
        self.label_2f_L = QLabel('1st 평균값\nNone', self)
        self.label_2s_L = QLabel('2nd 평균값\nNone', self)
        self.label_2m_L = QLabel('평균값 차이\nNone', self)
        self.label_2f_L.setAlignment(Qt.AlignCenter)
        self.label_2s_L.setAlignment(Qt.AlignCenter)
        self.label_2m_L.setAlignment(Qt.AlignCenter)
#오른쪽
        self.label_2f_L.setStyleSheet("color:rgb(203,26,126);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2s_L.setStyleSheet("color:rgb(203,26,126);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2m_L.setStyleSheet("color:rgb(0, 0, 0);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
        self.label_2f_L.setFont(Font_5)
        self.label_2s_L.setFont(Font_5)
        self.label_2m_L.setFont(Font_5)        


        #self.label_1f = QLabel('평균값 차이\n<span style="color:#FFFFFF;">None', self)
        self.label_1f = QLabel('평균값 차이\nNone', self)
        self.label_1s = QLabel('평균값 차이\nNone', self)
        self.label_1f.setAlignment(Qt.AlignCenter)
        self.label_1s.setAlignment(Qt.AlignCenter)
        self.label_1f.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                      "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                      "border-radius: 3px")   
        self.label_1s.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                      "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                      "border-radius: 3px")   
        self.label_1f.setFont(Font_5)
        self.label_1s.setFont(Font_5)
#AOM 
        self.label_1f_2 = QLabel('평균값 차이\nNone', self)
        self.label_1s_2 = QLabel('평균값 차이\nNone', self)
        self.label_1f_2.setAlignment(Qt.AlignCenter)
        self.label_1s_2.setAlignment(Qt.AlignCenter)
        self.label_1f_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                      "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                      "border-radius: 3px")   
        self.label_1s_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                      "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                      "border-radius: 3px")   
        self.label_1f_2.setFont(Font_5)
        self.label_1s_2.setFont(Font_5)
        
        self.radio_A_L = QLabel('오른쪽',self)
        self.radio_A_L.setAlignment(Qt.AlignCenter)
        self.radio_A_R = QLabel('왼쪽',self)
        self.radio_A_R.setAlignment(Qt.AlignCenter)
        self.radio_AO_L = QLabel('\n오른쪽',self)
        self.radio_AO_L.setAlignment(Qt.AlignCenter)
        self.radio_AO_R = QLabel('\n왼쪽',self)
        self.radio_AO_R.setAlignment(Qt.AlignCenter)        
        self.radio_E_L = QLabel('오른쪽',self)
        self.radio_E_L.setAlignment(Qt.AlignCenter)
        self.radio_E_R = QLabel('왼쪽',self)
        self.radio_E_R.setAlignment(Qt.AlignCenter)
        
        self.radio_A_L.setStyleSheet("color:rgb(203,26,126);""font-weight:bold")
        self.radio_A_R.setStyleSheet("color:rgb(44,106, 180);""font-weight:bold")
        self.radio_E_L.setStyleSheet("color:rgb(203,26,126);""font-weight:bold")
        self.radio_E_R.setStyleSheet("color:rgb(44,106, 180);""font-weight:bold")
        self.radio_AO_L.setStyleSheet("color:rgb(203,26,126);""font-weight:bold")
        self.radio_AO_R.setStyleSheet("color:rgb(44,106, 180);""font-weight:bold")

        gbox0.addWidget(self.radio_A_R)
        gbox0.addWidget(self.label_0f)
        gbox0.addWidget(self.label_0s)
        gbox0.addWidget(self.label_0m)
        gbox1.addWidget(self.radio_A_L)
        gbox1.addWidget(self.label_0f_L)
        gbox1.addWidget(self.label_0s_L)
        gbox1.addWidget(self.label_0m_L)
        gbox2.addWidget(self.radio_E_R)
        gbox2.addWidget(self.label_2f)
        gbox2.addWidget(self.label_2s)
        gbox2.addWidget(self.label_2m)
        gbox3.addWidget(self.radio_E_L)
        gbox3.addWidget(self.label_2f_L)
        gbox3.addWidget(self.label_2s_L)
        gbox3.addWidget(self.label_2m_L)
        gbox4.addWidget(self.radio_AO_R)
        gbox4.addWidget(self.label_1f)
        gbox4.addWidget(self.label_1f_2)
        gbox5.addWidget(self.radio_AO_L)
        gbox5.addWidget(self.label_1s)
        gbox5.addWidget(self.label_1s_2)
        
        
        vbox0.addWidget(self.Azi_label)
        vbox0.addWidget(self.Azi)
        
        grpbox0.addLayout(gbox0)
        grpbox0.addLayout(gbox1)
        
        hbox0.addLayout(vbox0)
        hbox0.addLayout(grpbox0)

        vbox1.addWidget(self.AOM_label)
        vbox1.addWidget(self.AOM)
        
        grpbox1.addLayout(gbox4)
        grpbox1.addLayout(gbox5)
        grpbox1.setGeometry(QtCore.QRect(2000, 2000, 3000, 3000))
        
        hbox1.addLayout(vbox1)
        hbox1.addLayout(grpbox1)
        
        vbox2.addWidget(self.Elevation_label)
        vbox2.addWidget(self.Elevation)
        
        grpbox2.addLayout(gbox2)
        grpbox2.addLayout(gbox3)
        
        hbox2.addLayout(vbox2)
        hbox2.addLayout(grpbox2)

        vbox3.addWidget(self.Xaxis_label)
        vbox3.addWidget(self.Xaxis)
        hbox3.addLayout(vbox3)
        #hbox3.addLayout(gbox3)
        
        vbox4.addWidget(self.Yaxis_label)
        vbox4.addWidget(self.Yaxis)
        hbox4.addLayout(vbox4)
        #hbox4.addLayout(gbox4)
        
        vbox5.addWidget(self.Zaxis_label)
        vbox5.addWidget(self.Zaxis)
        hbox5.addLayout(vbox5)
        #hbox5.addLayout(gbox5)
        epbox.addStretch(1)
        epbox.addWidget(self.export_button)
        epbox.addStretch(1)
        
        vbox6.addLayout(hbox0)
        vbox6.addLayout(hbox1)
        vbox6.addLayout(hbox2)
        vbox6.addLayout(epbox)
        vbox6.addLayout(hbox3)        
        vbox6.addLayout(hbox4)    
        vbox6.addLayout(hbox5)
    
        self.setLayout(vbox6)
        self.setGeometry(0, 30, self.width_px, int(self.height_px*0.935))  # 창 위치(x, y), width, height
        self.center()
        #self.setWindowTitle("TI inc. STRABISMUS EYETRACKING PROGRAM v0.66 by Jeon ")
        self.setWindowTitle("TI inc. igazy v1.0 ")
        
        self.Azi_r = self.Azi.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.Azi_l = self.Azi.plot(pen=pyqtgraph.mkPen(color=(44,106, 180), width=2, style=QtCore.Qt.DotLine, name = 'Left Eye'))
        self.AOM_r = self.AOM.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.AOM_l = self.AOM.plot(pen=pyqtgraph.mkPen(color=(44,106, 180), width=2, style=QtCore.Qt.DotLine, name = 'Left Eye'))
        self.Ele_r = self.Elevation.plot(pen=pyqtgraph.mkPen(color=(203, 26, 126), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.Ele_l = self.Elevation.plot(pen=pyqtgraph.mkPen(color=(44,106, 180), width=2, style=QtCore.Qt.DotLine, name = 'Left Eye'))
        self.Xaxis_r = self.Xaxis.plot(pen=pyqtgraph.mkPen(color=(120, 120, 120), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.Xaxis_l = self.Xaxis.plot(pen=pyqtgraph.mkPen(color=(244, 121, 40), width=2, style=QtCore.Qt.SolidLine, name = 'Left Eye'))        
        self.Yaxis_r = self.Yaxis.plot(pen=pyqtgraph.mkPen(color=(120, 120, 120), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.Yaxis_l = self.Yaxis.plot(pen=pyqtgraph.mkPen(color=(244, 121, 40), width=2, style=QtCore.Qt.SolidLine, name = 'Left Eye'))        
        self.Zaxis_r = self.Zaxis.plot(pen=pyqtgraph.mkPen(color=(120, 120, 120), width=2, style=QtCore.Qt.SolidLine,name = 'Right Eye'))
        self.Zaxis_l = self.Zaxis.plot(pen=pyqtgraph.mkPen(color=(244, 121, 40), width=2, style=QtCore.Qt.SolidLine, name = 'Left Eye'))        
        self.AOM.setXLink(self.Azi)
        self.Elevation.setXLink(self.Azi)
        self.Xaxis.setXLink(self.Azi)
        self.Yaxis.setXLink(self.Azi)
        self.Zaxis.setXLink(self.Azi)

        #setdata
        self.Azi_r.setData(DF_Result.index,DF_Result.Azimuth_Right, name="Azimuth_Right")
        self.Azi_l.setData(DF_Result.index,DF_Result.Azimuth_Left, name="Azimuth_Left")
        self.AOM_r.setData(DF_Result.index,DF_Result.AOM_Right, name="AOM_Right")
        self.AOM_l.setData(DF_Result.index,DF_Result.AOM_Left, name="AOM_Left")                
        self.Ele_r.setData(DF_Result.index,DF_Result.Elevation_Right, name="Elevation_Right")
        self.Ele_l.setData(DF_Result.index,DF_Result.Elevation_Left, name="Elevation_Left")
        self.Xaxis_r.setData(DF_Result.index,DF_Result.Xaxis_Right, name="Xaxis_Right")
        self.Xaxis_l.setData(DF_Result.index,DF_Result.Xaxis_Left, name="Xaxis_Left")
        self.Yaxis_r.setData(DF_Result.index,DF_Result.Yaxis_Right, name="Yaxis_Right")
        self.Yaxis_l.setData(DF_Result.index,DF_Result.Yaxis_Left, name="Yaxis_Left")
        self.Zaxis_r.setData(DF_Result.index,DF_Result.Zaxis_Right, name="Zaxis_Right")
        self.Zaxis_l.setData(DF_Result.index,DF_Result.Zaxis_Left, name="Zaxis_Left")
        self.Azi.addItem(self.cursorlabel)
        self.AOM.addItem(self.cursorlabel)
        self.Elevation.addItem(self.cursorlabel)
        self.Xaxis.addItem(self.cursorlabel)
        self.Yaxis.addItem(self.cursorlabel)
        self.Zaxis.addItem(self.cursorlabel)
        self.Azi.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Azi.setYRange(-50, 50, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.AOM.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.AOM.setYRange(-1, 1, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Elevation.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Elevation.setYRange(-50, 50, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Xaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Xaxis.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Yaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Yaxis.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Zaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Zaxis.setXRange(DF_Result.index[1], DF_Result.index[-1], padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        
        
    def mouseMoved_A(self,evt):
        global DF_Result
        global mouse_index
        pos = evt
        Data = DF_Result.Azimuth_Right
        if self.Azi.sceneBoundingRect().contains(pos):
            mousePoint = self.Azi.plotItem.vb.mapSceneToView(pos)
            #mx = abs(np.ones(len(Data))*mousePoint.x() - Data)
            mouse_index = float(format(mousePoint.x(),".1f"))
            self.ALine.setPos(mouse_index)
            self.AOLine.setPos(mouse_index)


    def onClick_A(self,evt):
        global DF_Result
        global A_1
        global first_index
        global mean_data_A
        global mean_data_A_L
        global mean_data_AO
        global mean_data_AO_L
        global mean_data_2
        global mean_data_2_L
        global mean_data_2_AO
        global mean_data_2_AO_L
        global diff_data
        global diff_data_L
        
        pos = evt        
        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
        Data = copy.deepcopy(DF_Result.Elevation_Left)
        Data_AO_R = copy.deepcopy(DF_Result.AOM_Right)
        Data_AO_L = copy.deepcopy(DF_Result.AOM_Left)
        
        if True:
            if int(mouse_index) in DF_Result.index.values.astype(int) :
                if self.A_1 == 0:
                    first_index = mouse_index
                    self.ALine_1.setPos(mouse_index)
                    self.AOLine_1.setPos(mouse_index)
                    self.A_1 = 1
                elif self.A_1 == 1:
                    second_index = mouse_index
                    self.ALine_2.setPos(mouse_index)
                    self.AOLine_2.setPos(mouse_index)
                    if first_index <= second_index:
                        Data = self.outlier_iqr(Data,int(first_index),int(second_index))
                        Data_L = self.outlier_iqr(Data_L,int(first_index),int(second_index))
                        mean_data_A = np.mean(Data[first_index:second_index])
                        mean_data_A_L = np.mean(Data_L[first_index:second_index])
                        mean_data_AO = round(np.mean(Data_AO_R[first_index:first_index+1]))
                        mean_data_AO_L = round(np.mean(Data_AO_L[first_index:first_index+1]))
                        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
                        Data = copy.deepcopy(DF_Result.Elevation_Left)
                    elif first_index >= second_index:
                        Data = self.outlier_iqr(Data,int(first_index),int(second_index))
                        Data_L = self.outlier_iqr(Data_L,int(first_index),int(second_index))
                        mean_data_A = np.mean(Data[second_index:first_index])
                        mean_data_A_L = np.mean(Data_L[second_index:first_index])
                        mean_data_AO = round(np.mean(Data_AO_R[second_index:second_index+1]))
                        mean_data_AO_L = round(np.mean(Data_AO_L[second_index:second_index+1]))
                        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
                        Data = copy.deepcopy(DF_Result.Elevation_Left)
                    self.label_0f.setText('1st 평균값\n%f' %mean_data_A)
                    self.label_0f_L.setText('1st 평균값\n%f' %mean_data_A_L)
                    if mean_data_AO_L == 1:
                        self.label_1f.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
                        if mean_data_AO == 1:
                            self.label_1s.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                        elif mean_data_AO == 0:
                            self.label_1s.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                    elif mean_data_AO_L == 0:
                        self.label_1f.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
                        if mean_data_AO == 1:
                            self.label_1s.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                        elif mean_data_AO == 0:
                            self.label_1s.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")               
            
                    self.A_1 = 2


                elif self.A_1 == 2:
                    first_index = mouse_index
                    self.ALine_3.setPos(mouse_index)
                    self.AOLine_3.setPos(mouse_index)
                    self.A_1 = 3                    
                    
                elif self.A_1 == 3:
                    second_index = mouse_index
                    self.ALine_4.setPos(mouse_index)
                    self.AOLine_4.setPos(mouse_index)
                    if first_index <= second_index:
                        Data = self.outlier_iqr(Data,int(first_index),int(second_index))
                        Data_L = self.outlier_iqr(Data_L,int(first_index),int(second_index))
                        mean_data_2 = np.mean(Data[first_index:second_index])
                        mean_data_2_L = np.mean(Data_L[first_index:second_index])
                        mean_data_2_AO = round(np.mean(Data_AO_R[first_index:first_index+1]))
                        mean_data_2_AO_L = round(np.mean(Data_AO_L[first_index:first_index+1]))
                        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
                        Data = copy.deepcopy(DF_Result.Elevation_Left)
                    elif first_index >= second_index:
                        Data = self.outlier_iqr(Data,int(first_index),int(second_index))
                        Data_L = self.outlier_iqr(Data_L,int(first_index),int(second_index))
                        mean_data_2 = np.mean(Data[second_index:first_index])
                        mean_data_2_L = np.mean(Data_L[second_index:first_index])
                        mean_data_2_AO = round(np.mean(Data_AO_R[second_index:second_index+1]))
                        mean_data_2_AO_L = round(np.mean(Data_AO_L[second_index:second_index+1]))
                        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
                        Data = copy.deepcopy(DF_Result.Elevation_Left)
                    diff_data = mean_data_A- mean_data_2
                    diff_data_L = mean_data_A_L- mean_data_2_L
                    self.label_0s.setText('2nd 평균값\n%f' %mean_data_2)
                    self.label_0m.setText('평균값 차이\n%f' %diff_data)
                    self.label_0s_L.setText('2nd 평균값\n%f' %mean_data_2_L)
                    self.label_0m_L.setText('평균값 차이\n%f' %diff_data_L)
                    self.label_1f_2.setText('가림 상태\n%d' %mean_data_2_AO_L)
                    self.label_1s_2.setText('가림 상태\n%d' %mean_data_2_AO)      
                    if mean_data_2_AO_L == 1:
                        self.label_1f_2.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
                        if mean_data_2_AO == 1:
                            self.label_1s_2.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                        elif mean_data_2_AO == 0:
                            self.label_1s_2.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                    elif mean_data_2_AO_L == 0:
                        self.label_1f_2.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                   "border-radius: 3px")
                        if mean_data_2_AO == 1:
                            self.label_1s_2.setStyleSheet("color:rgb(255,255,255);" "background-color:rgb(255,255,255);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")
                        elif mean_data_2_AO == 0:
                            self.label_1s_2.setStyleSheet("color:rgb(0,0,0);" "background-color:rgb(0,0,0);"
                                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                        "border-radius: 3px")    
                    self.ck_area = 1
                    self.A_1 = 4
                    
                elif self.A_1 == 4:                                     
                    self.label_0f.setText('1st 평균값\nNone')
                    self.label_0s.setText('2nd 평균값\nNone')
                    self.label_0m.setText('평균값 차이\nNone')
                    self.label_0f_L.setText('1st 평균값\nNone')
                    self.label_0s_L.setText('2nd 평균값\nNone')
                    self.label_0m_L.setText('평균값 차이\nNone')
                    self.label_1f.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                                  "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                  "border-radius: 3px")
                    self.label_1s.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                                  "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                  "border-radius: 3px")         
                    self.label_1f_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                                  "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                  "border-radius: 3px")
                    self.label_1s_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                                  "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                                  "border-radius: 3px")                        
                    self.ALine_1.setPos(0)
                    self.ALine_2.setPos(0)
                    self.ALine_3.setPos(0)
                    self.ALine_4.setPos(0)
                    self.AOLine_1.setPos(0)
                    self.AOLine_2.setPos(0)
                    self.AOLine_3.setPos(0)
                    self.AOLine_4.setPos(0)
                    self.ck_area = 0
                    self.A_1 = 0
            else :
                self.ALine_1.setPos(0)
                self.ALine_2.setPos(0)
                self.ALine_3.setPos(0)
                self.ALine_4.setPos(0)
                self.AOLine_1.setPos(0)
                self.AOLine_2.setPos(0)
                self.AOLine_3.setPos(0)
                self.AOLine_4.setPos(0)
                self.label_1f.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                            "border-radius: 3px")
                self.label_1s.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                            "border-radius: 3px")         
                self.label_1f_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                              "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                              "border-radius: 3px")
                self.label_1s_2.setStyleSheet("color:rgb(192,192,192);" "background-color:rgb(192,192,192);"
                                              "border-style: solid;" "border-width: 1px;" "border-color: rgb(0,0,0);"
                                              "border-radius: 3px")
                self.ck_area = 0
                self.A_1 = 0
                    
    def mouseMoved_E(self,evt):
        global DF_Result
        global mouse_index_E
        pos = evt
        Data = DF_Result.Elevation_Right
        if self.Azi.sceneBoundingRect().contains(pos):
            mousePoint = self.Elevation.plotItem.vb.mapSceneToView(pos)
            mouse_index_E = float(format(mousePoint.x(),".1f"))
            self.ELine.setPos(mouse_index_E)
            self.AOLine.setPos(mouse_index_E)

            
    def onClick_E(self,evt):
        global DF_Result
        global E_1
        global first_index_E
        global mean_data_E
        global mean_data_E_L
        global mean_data_AO_E
        global mean_data_AO_E_L

        pos = evt        
        Data_L = copy.deepcopy(DF_Result.Elevation_Right)
        Data = copy.deepcopy(DF_Result.Elevation_Left)
        Data_AO_R = copy.deepcopy(DF_Result.AOM_Right)
        Data_AO_L = copy.deepcopy(DF_Result.AOM_Left)

        if True:
            if int(mouse_index_E) in DF_Result.index.values.astype(int) :
                if self.E_1 == 0:
                    first_index_E = mouse_index_E
                    self.ELine_1.setPos(mouse_index_E)
                    self.AOLine_1.setPos(mouse_index_E)
                    self.E_1 = 1
                    
                elif self.E_1 == 1:
                    second_index = mouse_index_E
                    self.ELine_2.setPos(mouse_index_E)
                    self.AOLine_2.setPos(mouse_index_E)
                    if first_index_E <= second_index :
                        mean_data_E = np.mean(Data[first_index_E:second_index])
                        mean_data_E_L = np.mean(Data_L[first_index_E:second_index])
                        mean_data_AO_E = round(np.mean(Data_AO_R[first_index_E:first_index_E+1]))
                        mean_data_AO_E_L = round(np.mean(Data_AO_L[first_index_E:first_index_E+1]))
                    elif first_index_E > second_index :
                        mean_data_E = np.mean(Data[second_index:first_index_E])
                        mean_data_E_L = np.mean(Data_L[second_index:first_index_E])
                        mean_data_AO_E = round(np.mean(Data_AO_R[second_index:second_index+1]))
                        mean_data_AO_E_L = round(np.mean(Data_AO_L[second_index:second_index+1]))
                    self.label_2f.setText('1st 평균값\n%f' %mean_data_E)
                    self.label_2f_L.setText('1st 평균값\n%f' %mean_data_E_L)
                    self.E_1 = 2
                    
                elif self.E_1 == 2:
                    first_index_E = mouse_index_E
                    self.ELine_3.setPos(mouse_index_E)
                    self.AOLine_3.setPos(mouse_index_E)

                    self.E_1 = 3                    
                    
                elif self.E_1 == 3:
                    second_index = mouse_index_E
                    self.ELine_4.setPos(mouse_index_E)
                    self.AOLine_4.setPos(mouse_index_E)
                    
                    if first_index_E <= second_index :
                        mean_data_2 = np.mean(Data[first_index_E:second_index])
                        mean_data_2_L = np.mean(Data_L[first_index_E:second_index])
                        mean_data_2_AO = round(np.mean(Data_AO_R[first_index_E:first_index_E+1]))
                        mean_data_2_AO_L = round(np.mean(Data_AO_L[first_index_E:first_index_E+1]))
                    elif first_index_E > second_index :
                        mean_data_2 = np.mean(Data[second_index:first_index_E])
                        mean_data_2_L = np.mean(Data_L[second_index:first_index_E])
                        mean_data_2_AO = round(np.mean(Data_AO_R[second_index:second_index+1]))
                        mean_data_2_AO_L = round(np.mean(Data_AO_L[second_index:second_index+1]))
                    diff_data = mean_data_E- mean_data_2
                    diff_data_L = mean_data_E_L- mean_data_2_L
                    self.label_2s.setText('2nd 평균값\n%f' %mean_data_2)
                    self.label_2m.setText('평균값 차이\n%f' %diff_data)
                    self.label_2s_L.setText('2nd 평균값\n%f' %mean_data_2_L)
                    self.label_2m_L.setText('평균값 차이\n%f' %diff_data_L)
                    self.E_1 = 4

                elif self.E_1 == 4:                                     
                    self.label_2f.setText('1st 평균값\nNone')
                    self.label_2s.setText('2nd 평균값\nNone')
                    self.label_2m.setText('평균값 차이\nNone')
                    self.label_2f_L.setText('1st 평균값\nNone')
                    self.label_2s_L.setText('2nd 평균값\nNone')
                    self.label_2m_L.setText('평균값 차이\nNone')       
                    self.ELine_1.setPos(0)
                    self.ELine_2.setPos(0)
                    self.ELine_3.setPos(0)
                    self.ELine_4.setPos(0)
                    self.E_1 = 0
            else :
                self.ELine_1.setPos(0)
                self.ELine_2.setPos(0)
                self.ELine_3.setPos(0)
                self.ELine_4.setPos(0)
                self.E_1 = 0  

    def mouseMoved_X(self,evt):
        global DF_Result
        global mouse_index_X
        pos = evt
        Data = DF_Result.Xaxis_Right
        if self.Azi.sceneBoundingRect().contains(pos):
            mousePoint = self.Xaxis.plotItem.vb.mapSceneToView(pos)
            mx = abs(np.ones(len(Data))*mousePoint.x() - Data)
            mouse_index_X = mousePoint.x()
            self.XLine.setPos(mouse_index_X)

    def mouseMoved_Y(self,evt):
        global DF_Result
        global mouse_index_Y
        pos = evt
        Data = DF_Result.Yaxis_Right
        if self.Azi.sceneBoundingRect().contains(pos):
            mousePoint = self.Yaxis.plotItem.vb.mapSceneToView(pos)
            mx = abs(np.ones(len(Data))*mousePoint.x() - Data)
            mouse_index_Y = mousePoint.x()
            self.YLine.setPos(mouse_index_Y)
            
    def mouseMoved_Z(self,evt):
        global DF_Result
        global mouse_index_Z
        pos = evt
        Data = DF_Result.Zaxis_Right
        if self.Azi.sceneBoundingRect().contains(pos):
            mousePoint = self.Yaxis.plotItem.vb.mapSceneToView(pos)
            mx = abs(np.ones(len(Data))*mousePoint.x() - Data)
            mouse_index_Z = mousePoint.x()
            self.ZLine.setPos(mouse_index_Z)
            
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("올바른 범위를 지정해주십시오")
        msgBox.setWindowTitle("Error")
        returnValue = msgBox.exec()

    def showDialog_2(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("데이터 Export 완료")
        msgBox.setWindowTitle("Information")
        returnValue = msgBox.exec()        
        
        
    def f_export_button(self):
        global j
        if self.ck_area == 0:
            self.showDialog()
        else:
            if j == 0:
                export_data = DataFrame({"right_1":mean_data_A_L,"right_2":mean_data_2_L,
                                         "RIGHT_diff":diff_data_L,"left_1":mean_data_A,"left_2":mean_data_2,
                                         "LEFT_diff":diff_data,"right_AOM_1":mean_data_AO,"right_AOM_2":mean_data_2_AO,
                                         "left_AOM_1":mean_data_AO_L,"left_AOM_2":mean_data_2_AO_L},index=[j])
                export_data.to_csv(OutFileName+'.csv', mode = 'a')
                self.showDialog_2()
                j = j+1
                
            else:
                export_data = DataFrame({"right_1":mean_data_A,"right_2":mean_data_2,
                                         "RIGHT_diff":diff_data,"left_1":mean_data_A_L,"left_2":mean_data_2_L,
                                         "LEFT_diff":diff_data_L,"right_AOM_1":mean_data_AO,"right_AOM_2":mean_data_2_AO,
                                         "left_AOM_1":mean_data_AO_L,"left_AOM_2":mean_data_2_AO_L},index=[j])
                export_data.to_csv(OutFileName+'.csv', mode = 'a', header = False)
                self.showDialog_2()
                j = j+1
        