#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from guppy.heapy import RM
import tkinter as tk
import pyqtgraph
import sys
from pyqtgraph.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pandas import DataFrame
from collections import deque
import serial
import serial.tools.list_ports
from datetime import datetime
import binascii
import numpy as np
import math
from PyQt5 import *
import cv2
import threading
import json
from tobiiglassesctrl import TobiiGlassesController
import matplotlib.style as mplstyle
import pyqtgraph.opengl as gl
import tracemalloc
#tracemalloc.start()

USB_msg = "0"
Right_status = 0
AOM_status = 0
Left_status = 0
mode_status = 0
res = 0
USB_msg_dq = deque([])
Cycle_Time = 100
DF_Result = DataFrame({"Azimuth_Right":[0],"Azimuth_Left":[0],"AOM_Right":[0],"AOM_Left":[0],
                       "Elevation_Right":[0],"Elevation_Left":[0], "Xaxis_Right":[0],"Xaxis_Left":[0],
                       "Yaxis_Right":[0], "Yaxis_Left":[0],"Zaxis_Right":[0],"Zaxis_Left":[0],
                       'Pupil_Diameter_Right': [0],'Pupil_Diameter_Left': [0],"mode_status":[0]})

class SecondWindow(QWidget):
    def __init__(self,root_data,project_ID,patient_ID,patient_birth):
        super().__init__()
        self.root_data = root_data
        self.project_ID = project_ID
        self.patient_ID = patient_ID
        self.patient_birth = patient_birth
        self.graph_and_video()


        
    def ImageUpdateSlot(self,Image):
        self.video_viewer_label.setPixmap(QPixmap.fromImage(Image))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def graph_and_video(self):
        global tobiiglasses
        global ipv4_address
        global Font_4
        root = tk.Tk()
        # 레이아웃 생성
        hbox0 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        vbox0 = QVBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        Gbox0 = QVBoxLayout()
        Gbox1 = QVBoxLayout()
        Gbox2 = QVBoxLayout()
        Gbox4 = QVBoxLayout()
        Gbox5 = QVBoxLayout()
        Gbox6 = QVBoxLayout()
        gzbox0 = QHBoxLayout()
        gzgrbox = QVBoxLayout()
        self.video_viewer_label = QtWidgets.QLabel()
        self.setting_label = QLabel(self)
        width_px = root.winfo_screenwidth()
        height_px = root.winfo_screenheight()
        width_pm = int(width_px/2)
        height_pm = int(height_px/2.4)
        pm = QPixmap('igaze.png')
        self.setting_label.setPixmap(pm.scaled(width_pm, height_pm/2, QtCore.Qt.IgnoreAspectRatio))
        # 기본 글꼴 설정
        Font_3 = QFont('Bahnschrift SemiLight', 8)
        Font_4 = QFont('Bahnschrift SemiLight', 12, QFont.Bold)
        self.setFont(Font_4) 
        bk_color = 50,50,50
        self.gz_r = gl.GLViewWidget()
        self.gz_r.setBackgroundColor(bk_color)
        self.gz_l = gl.GLViewWidget()
        self.gz_l.setBackgroundColor(bk_color)
        point1 = np.array([0, 0, 0])
        point2 = np.array([0, 5, 0])
        radius = np.linalg.norm(point2 - point1) / 2
        md = gl.MeshData.sphere(rows=100, cols=200, radius=radius)
        m1 = gl.GLMeshItem(
            meshdata=md,
            background = (1,0,0),
            smooth=True,
            color=(1, 1, 1, 0.4),
            shader="balloon",
            glOptions="translucent",
        )
        m1.translate(0,0,0)
        point1_2 = np.array([0, 0, 0])
        point2_2 = np.array([2.5, 0, 0])
        radius_2 = np.linalg.norm(point2_2 - point1_2) / 2
        md_2 = gl.MeshData.sphere(rows=10, cols=20, radius=radius_2)
        m2 = gl.GLMeshItem(
            meshdata=md_2,
            smooth=True,
            color=(0.1,0.1,0.1,1),
            shader="balloon",
            glOptions="translucent",
        )
        m2.translate(1.5,0,0)
        self.gz_r.addItem(m1)
        self.gz_r.addItem(m2)
        self.gz_l.addItem(m1)
        self.gz_l.addItem(m2)
        # 그래프 객체 5개 생성 및 X축을 STRING축으로 설정
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

        # Y축 이름 스타일 설정
        labelStyle = {'color': '#828282', 'font-size': '9pt', 'font-weight' : 'bold' }

        # Y축 이름 생성
        self.Zaxis.setLabel('bottom', 'Time(s)', **labelStyle)
        # x,y 눈금 글꼴 설정

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


        # 그래프 그리드 설정
        self.Azi.showGrid(x=True, y=True)
        self.AOM.showGrid(x=True, y=True)
        self.Elevation.showGrid(x=True, y=True)
        self.Xaxis.showGrid(x=True, y=True)
        self.Yaxis.showGrid(x=True, y=True)
        self.Zaxis.showGrid(x=False, y=True)

        # 그래프 배경색 지정
        self.Azi.setBackground((240,240,240))
        self.AOM.setBackground((240,240,240))
        self.Elevation.setBackground((240,240,240))
        self.Xaxis.setBackground((240,240,240))
        self.Yaxis.setBackground((240,240,240))
        self.Zaxis.setBackground((240,240,240))

        # Data Indicator 그룹 박스 생성
        self.groupbox_ES = QGroupBox('AOM Connection')
        self.groupbox_EB = QGroupBox('AOM Mode Status')
        self.groupbox_TC = QGroupBox('ETM Connection')
        self.groupbox_TB = QGroupBox('ETM Battery Status')
        self.groupbox_CB = QGroupBox('Do Calibrate')
        self.groupbox_TS = QGroupBox('Calibration Status')

        # Data Indicator 라벨 생성
        self.label_ES = QLabel('Not Connected', self)
        self.label_EB = QLabel('0', self)
        self.label_TC = QLabel('Connected', self)
        #self.label_TB = QProgressBar(self, minimum=0, maximum=100, textVisible=True,
#                        objectName="BlueProgressBar")
        self.label_TB = QProgressBar(self)
        self.label_TB.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored,
                                                 QtWidgets.QSizePolicy.Ignored))
#        self.label_TB.setGeometry(10,10,300,20)
        self.button_CB = QPushButton('Do Calibrate')
        self.button_CB.clicked.connect(self.cali)
        self.label_TS = QLabel('Not Calibrated', self)

        # Data Indicator 가운데 정렬
        self.label_ES.setAlignment(Qt.AlignCenter)
        self.label_EB.setAlignment(Qt.AlignCenter)
        self.label_TC.setAlignment(Qt.AlignCenter)
        self.label_TB.setAlignment(Qt.AlignCenter)
        self.label_TS.setAlignment(Qt.AlignCenter)
        self.setting_label.setAlignment(Qt.AlignCenter)

        # Data Indicator 배경색 및 테두리 설정
        self.label_ES.setStyleSheet("color:rgb(255, 0, 0);" "background-color:rgb(82,131,190);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                   "border-radius: 5px")
        self.label_EB.setStyleSheet("color:rgb(244, 121, 40);" "background-color:rgb(255,255,255);"
                                   "border-style: solid;" "border-width: 2px;" "border-color: rgb(81,131,190);"
                                   "border-radius: 5px")
        self.label_TC.setStyleSheet("color:rgb(255, 255, 255);" "background-color:rgb(82,131,190);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                   "border-radius: 5px")
        self.label_TB.setStyleSheet('''
        QProgressBar::chunk {
            text-align: center;
            border: 2px solid #5183BE;
            background-color: #5183BE;
            width : 2px;
            margin : 2px;
        }
        ''')

        self.button_CB.setStyleSheet("color:rgb(255, 255, 255);" "background-color:rgb(82,131,190);"
                                   "border-style: solsid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                   "border-radius: 5px")
        self.label_TS.setStyleSheet("color:rgb(255, 0, 0);" "background-color:rgb(82,131,190);"
                                   "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                   "border-radius: 5px")

        # Data Indicator 글꼴 설정
        Font_5 = QFont("Bahnschrift SemiLight", 15, QFont.Bold)
        self.label_ES.setFont(Font_5)
        self.label_EB.setFont(Font_5)
        self.label_TC.setFont(Font_5)
        self.label_TB.setFont(Font_4)
        self.button_CB.setFont(Font_5)
        self.label_TS.setFont(Font_5)

        # 그룹박스와 Data Indicator 라벨 그룹화

        Gbox0.addWidget(self.label_ES)
        Gbox1.addWidget(self.label_EB)
        Gbox2.addWidget(self.label_TC)
        Gbox4.addWidget(self.label_TB)
        Gbox5.addWidget(self.button_CB)
        Gbox6.addWidget(self.label_TS)
        self.groupbox_ES.setLayout(Gbox0)
        self.groupbox_EB.setLayout(Gbox1)
        self.groupbox_TC.setLayout(Gbox2)
        self.groupbox_TB.setLayout(Gbox4)
        self.groupbox_CB.setLayout(Gbox5)
        self.groupbox_TS.setLayout(Gbox6)

        # 수평방향으로 창 그룹화 (1행 1열 그래프 5개), (1행 2열 스트리밍영상+Setting), (2행 라벨 6개)
        gzbox0.addWidget(self.gz_l)
        gzbox0.addWidget(self.gz_r)
        vbox1.addWidget(self.Azi_label)
        vbox1.addWidget(self.Azi)
        vbox1.addWidget(self.AOM_label)
        vbox1.addWidget(self.AOM)
        vbox1.addWidget(self.Elevation_label)
        vbox1.addWidget(self.Elevation)
        vbox1.addWidget(self.Xaxis_label)
        vbox1.addWidget(self.Xaxis)
        vbox1.addWidget(self.Yaxis_label)
        vbox1.addWidget(self.Yaxis)
        vbox1.addWidget(self.Zaxis_label)
        vbox1.addWidget(self.Zaxis)
        #vbox2.addWidget(self.setting_label)
#gazebox 연결!
        gzgrbox.addLayout(gzbox0)
        gzgrbox.addWidget(self.setting_label)

        vbox2.addWidget(self.video_viewer_label)
        vbox2.addLayout(gzgrbox)
        hbox0.addLayout(vbox1)
        hbox0.addLayout(vbox2)
        hbox1.addWidget(self.groupbox_ES)
        hbox1.addWidget(self.groupbox_EB)
        hbox1.addWidget(self.groupbox_TC)
        hbox1.addWidget(self.groupbox_TB)
        hbox1.addWidget(self.groupbox_CB)
        hbox1.addWidget(self.groupbox_TS)
        # 그룹화된 창 수직방향으로 그룹화
        vbox0.addLayout(hbox0)
        vbox0.addLayout(hbox1)

        # 윈도우창생성 및 레이아웃 배치
        self.setLayout(vbox0)
        self.setGeometry(0, 30, width_px, int(height_px*0.935))  # 창 위치(x, y), width, height
        self.center()
        #self.setWindowTitle("TI inc. STRABISMUS EYETRACKING PROGRAM v0.66 by Jeon ")
        self.setWindowTitle("TI inc. igazy v1.0 ")

        # 그래프 펜 설정   ??
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
        self.Azi.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Azi.setYRange(-50, 50, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.AOM.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.AOM.setYRange(-1, 1, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Elevation.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Elevation.setYRange(-50, 50, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Xaxis.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Xaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Yaxis.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Yaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        self.Zaxis.setXRange(0, 150, padding=0) # 항상 x축 시간을 최근 범위만 보여줌
        self.Zaxis.setYRange(-2, 2, padding=0) # 항상 x축 시간을 최근 범위만 보여줌.
        # 범례 추가 및 글꼴 설정 /////수정필요함

        # Tobii 연결
        ipv4_address = "192.168.71.50"
        tobiiglasses = TobiiGlassesController(ipv4_address, video_scene=True)
        tobiiglasses.start_streaming()
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        #ipv4_address = "192.168.137.1"
        # 일정 시간 마다 그래프 및 라벨값 갱신
        self.start_clock = round(time.time(),3)
        self.SetTimer()
        self.showMaximized()

##data 몇개?
    def SetTimer(self):
        self.Data_Get_Timer = QTimer()
        self.Data_Get_Timer.setInterval(Cycle_Time)
        self.Data_Get_Timer.timeout.connect(self.update)
        self.Data_Get_Timer.start()

    def cali(self):
        global project_id
        global participant_id
        global calibration_id
        global res

        if tobiiglasses.is_recording():
            rec_id = tobiiglasses.get_current_recording_id()
            tobiiglasses.stop_recording(rec_id)
        project_id = tobiiglasses.create_project(self.project_ID)
        participant_id = tobiiglasses.create_participant(project_id, self.patient_ID)
        calibration_id = tobiiglasses.create_calibration(project_id, participant_id)
        tobiiglasses.start_calibration(calibration_id)
        res = tobiiglasses.wait_until_calibration_is_done(calibration_id)
        if res is False:
            Tobii_Cali_Status = "Not Calibrated"
            self.label_TS.setText(Tobii_Cali_Status)
        if res == 1:
            self.label_TS.setStyleSheet("color:rgb(255, 255, 255);" "background-color:rgb(82,131,190);"
                                        "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                        "border-radius: 5px")
            self.label_TS.setText("Calibrated")
            recording_id = tobiiglasses.create_recording(participant_id)
            tobiiglasses.start_recording(recording_id)
    # pyqtslot ()  ~ 이벤트핸들러, timeout 시 update 수행

    @pyqtSlot()
    def update(self):
        # INDEX용 시간 계산
        global Right_status
        global Left_status
        global mode_status
        global AOM_status
        global res
        global Font_4
        global offset
        global data_gp
        global data_pts
        global DF_Result
        global root_data
        data_gp  = tobiiglasses.get_data()['gp']
        data_pts = tobiiglasses.get_data()['pts']
        offset = (data_gp['ts'] - data_pts['ts'])/1000000.0
        #self.DF_Time = time.strftime('%H:%M:%S', time.localtime(time.time_ns()))
        self.current_clock = round(time.time(),3)
        mi_time = round(self.current_clock - self.start_clock,3)
        self.DF_Time = '%.3f'%mi_time
        #self.DF_Time = (datetime.now().strftime('%M%S.%f')[:-3])

        if offset > 0 and offset <= float(40):
            RS485 = self.Tobii_RX()
            Result_Temp = DataFrame(RS485, index = [self.DF_Time])  ## AOM Append 시키기 (Index
            if (len(DF_Result.index) <= 150):
                DF_Result = DF_Result.append(Result_Temp)
                if (DF_Result.iloc[-2,0] == Result_Temp.iloc[-1,0]):
                    Result_Temp.iloc[0,0] = None
                if (DF_Result.iloc[-2,1] == Result_Temp.iloc[-1,1]):
                    Result_Temp.iloc[0,1] = None
            else :
                DF_Result = DF_Result.iloc[-2:-1,:]
            Result_Temp.to_csv(self.root_data, mode='a', header=False)
            # X축 최대 개수 눈금 제한 (Tick간 겹치지않게 숫자 설정)
            xMAXTickN = 10
            xdict = dict(enumerate(DF_Result.index))
            xlist = list(xdict.items())
            xticklist = []
            xtick_ap = xticklist.append
            if len(xlist) > xMAXTickN:
                tick_interval = 15
                tick_key = 0
                for i in range(xMAXTickN+1):
                    xtick_ap(xlist[tick_key])
                    tick_key += tick_interval
                # Tick키가 리스트 범위를 넘지 않도록 조건문 추가
                    if tick_key >= len(xlist):
                        tick_key = len(xlist)-1
                self.stringaxisZ.setTicks([xticklist])

            else:
                self.stringaxisZ.setTicks([xdict.items()])
        # 그래프 갱신   ,,,  AOM  추가

            self.Azi_r.setData(DF_Result.Azimuth_Right, name="Azimuth_Right")
            self.Azi_l.setData(DF_Result.Azimuth_Left, name="Azimuth_Left")
            self.AOM_r.setData(DF_Result.AOM_Right, name="AOM_Right")
            self.AOM_l.setData(DF_Result.AOM_Left, name="AOM_Left")                
            self.Ele_r.setData(DF_Result.Elevation_Right, name="Elevation_Right")
            self.Ele_l.setData(DF_Result.Elevation_Left, name="Elevation_Left")
            self.Xaxis_r.setData(DF_Result.Xaxis_Right, name="Xaxis_Right")
            self.Xaxis_l.setData(DF_Result.Xaxis_Left, name="Xaxis_Left")
            self.Yaxis_r.setData(DF_Result.Yaxis_Right, name="Yaxis_Right")
            self.Yaxis_l.setData(DF_Result.Yaxis_Left, name="Yaxis_Left")
            self.Zaxis_r.setData(DF_Result.Zaxis_Right, name="Zaxis_Right")
            self.Zaxis_l.setData(DF_Result.Zaxis_Left, name="Zaxis_Left")

            # orbit 아이트래커 신호에 따라 움직임
            self.gz_r.eyeRotation(DF_Result.Azimuth_Right.iloc[-1],DF_Result.Elevation_Right.iloc[-1])
            self.gz_l.eyeRotation(DF_Result.Azimuth_Left.iloc[-1],DF_Result.Elevation_Left.iloc[-1])
              
            # Data Indicator 갱신
            self.label_TB.setValue(tobiiglasses.get_battery_status()['level'])
            self.label_EB.setText("%d" %mode_status)
                # Tobii 연결 확인     #tobiiglasses.__connect__
            if AOM_status == 1:
                self.label_ES.setText("Connected")
                self.label_ES.setStyleSheet("color:rgb(255, 255, 255);" "background-color:rgb(82,131,190);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                            "border-radius: 5px")
                AOM_status = 2

        elif offset < -0.2 :
            empty_data = {'Azimuth_Right': 0,'Azimuth_Left': 0,'AOM_Right' : Right_status, 'AOM_Left' : Left_status,
                    'Elevation_Right': 0,'Elevation_Left': 0,'Xaxis_Right': 0,
                    'Xaxis_Left': 0,'Yaxis_Right': 0,'Yaxis_Left': 0,'Zaxis_Right': 0,
                    'Zaxis_Left': 0,'Pupil_Diameter_Right': 0,'Pupil_Diameter_Left': 0,'mode' : mode_status}
            Result_Temp = DataFrame(empty_data, index = [self.DF_Time])  ## AOM Append 시키기 (Index

            if (len(DF_Result.index) <= 200):
                DF_Result = DF_Result.append(Result_Temp)
                if (DF_Result.iloc[-2,0] == 0):
                    Result_Temp.iloc[0,0] = 0
                    Result_Temp.iloc[0,1] = 0
                else :
                    if (DF_Result.iloc[-2,0] == Result_Temp.iloc[0,0]):
                        Result_Temp.iloc[0,0] = None
                    if (DF_Result.iloc[-2,1] == Result_Temp.iloc[0,1]):
                        Result_Temp.iloc[0,1] = None
            else :
                DF_Result = DF_Result.iloc[-2:-1,:]
            Result_Temp.to_csv(self.root_data, mode='a', header=False)
            xMAXTickN = 10
            xdict = dict(enumerate(DF_Result.index))
            xlist = list(xdict.items())
            xticklist = []
            xtick_ap = xticklist.append
            if len(xlist) > xMAXTickN:
                tick_interval = 20
                tick_key = 0
                for i in range(xMAXTickN+1):
                    xtick_ap(xlist[tick_key])
                    tick_key += tick_interval
                    if tick_key >= len(xlist):
                        tick_key = len(xlist)-1
                self.stringaxisZ.setTicks([xticklist])
            else:
                self.stringaxisZ.setTicks([xdict.items()])

            self.Azi_r.setData(DF_Result.Azimuth_Right, name="Azimuth_Right")
            self.Azi_l.setData(DF_Result.Azimuth_Left, name="Azimuth_Left")
            self.AOM_r.setData(DF_Result.AOM_Right, name="AOM_Right")
            self.AOM_l.setData(DF_Result.AOM_Left, name="AOM_Left")                
            self.Ele_r.setData(DF_Result.Elevation_Right, name="Elevation_Right")
            self.Ele_l.setData(DF_Result.Elevation_Left, name="Elevation_Left")
            self.Xaxis_r.setData(DF_Result.Xaxis_Right, name="Xaxis_Right")
            self.Xaxis_l.setData(DF_Result.Xaxis_Left, name="Xaxis_Left")
            self.Yaxis_r.setData(DF_Result.Yaxis_Right, name="Yaxis_Right")
            self.Yaxis_l.setData(DF_Result.Yaxis_Left, name="Yaxis_Left")
            self.Zaxis_r.setData(DF_Result.Zaxis_Right, name="Zaxis_Right")
            self.Zaxis_l.setData(DF_Result.Zaxis_Left, name="Zaxis_Left")
            self.gz_r.eyeRotation(0,0)
            self.gz_l.eyeRotation(0,0)
            self.label_TB.setValue(tobiiglasses.get_battery_status()['level'])
            self.label_EB.setText("%d" %mode_status)
            if AOM_status == 1:
                self.label_ES.setText("Connected")
                self.label_ES.setStyleSheet("color:rgb(255, 255, 255);" "background-color:rgb(82,131,190);"
                                            "border-style: solid;" "border-width: 1px;" "border-color: rgb(81,131,190);"
                                            "border-radius: 5px")
                AOM_status = 2
            #snapshot1 = tracemalloc.take_snapshot()
# ... call the function leaking memory ...
            #snapshot2 = tracemalloc.take_snapshot()
            #top_stats = snapshot2.compare_to(snapshot1, 'lineno')
            #print("[ Top 10 differences ]")
            #for stat in top_stats[:10]:
#                print(stat)
    def Tobii_RX(self):
        RX_X_r = tobiiglasses.get_data()['right_eye']['gd']['gd'][0]
        RX_X_l = tobiiglasses.get_data()['left_eye']['gd']['gd'][0]
        RX_Y_r = tobiiglasses.get_data()['right_eye']['gd']['gd'][2]
        RX_Y_l= tobiiglasses.get_data()['left_eye']['gd']['gd'][2]
        RX_Z_r = tobiiglasses.get_data()['right_eye']['gd']['gd'][1]
        RX_Z_l = tobiiglasses.get_data()['left_eye']['gd']['gd'][1]
        CX_Azi_r = float(math.atan2(RX_Y_r,RX_X_r)*180/np.pi-90)
        CX_Azi_l = float(math.atan2(RX_Y_l,RX_X_l)*180/np.pi-90)
        CX_Elevation_r = float(math.atan2(RX_Z_r,(RX_X_r**2 + RX_Y_r**2)**(1/2))*180/np.pi*(-1))
        CX_Elevation_l = float(math.atan2(RX_Z_l,(RX_X_l**2 + RX_Y_l**2)**(1/2))*180/np.pi*(-1))
        pupil_r = tobiiglasses.get_data()['left_eye']['pd']['pd']
        pupil_l = tobiiglasses.get_data()['right_eye']['pd']['pd']
        CX_Result = {'Azimuth_Right': CX_Azi_r,'Azimuth_Left': CX_Azi_l,'AOM_Right' : Right_status, 'AOM_Left' : Left_status,
                    'Elevation_Right': CX_Elevation_r,'Elevation_Left': CX_Elevation_l,'Xaxis_Right': RX_X_r,
                    'Xaxis_Left': RX_X_l,'Yaxis_Right': RX_Y_r,'Yaxis_Left': RX_Y_l,'Zaxis_Right': RX_Z_r,
                    'Zaxis_Left': RX_Z_l,'Pupil_Diameter_Right': pupil_r,'Pupil_Diameter_Left': pupil_l,'mode' : mode_status}
        return CX_Result

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("교대가림기를 PC와 연결해 주십시오")
        msgBox.setWindowTitle("시리얼 통신 연결 상태 불량")
        returnValue = msgBox.exec()

    def run(self):
        global Right_status
        global Left_status
        global mode_status
        global AOM_status
        global USB_msg
        global offset
        global label_ES
        root = tk.Tk()
        width_px = root.winfo_screenwidth()
        height_px = root.winfo_screenheight()
        width_pm = int(width_px/2)
        height_pm = int(height_px/2.4)
        ports = list(serial.tools.list_ports.comports())
        ser_check = 0
        for p in ports:
            if 'USB Serial Port' in p.description:
                self.ser = serial.Serial(p.device, baudrate=9600, timeout = 0.01)
                ser_check = 1
        if ser_check == 0:
            self.showDialog()
        append_dq = USB_msg_dq.append
        self.ThreadActive = True
        Capture = cv2.VideoCapture("rtsp://%s:8554/live/scene" % ipv4_address)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret :
                if offset > 0.0 and offset <= float(40):
                    cv2.circle(frame,(int(data_gp['gp'][0]*1920),int(data_gp['gp'][1]*1080)), 30, (0,0,255), 2)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image,1)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(width_pm, height_pm, QtCore.Qt.IgnoreAspectRatio)
                self.ImageUpdate.emit(Pic)
                USB_msg = self.ser.readline() #데이터를 한 줄 끝까지 읽는다
                USB_msg = USB_msg.decode('utf-8')
                USB_msg = USB_msg.replace('\n','')
                append_dq(USB_msg)
                if len(USB_msg) > 0 :
                    USB_msg = USB_msg_dq.pop()
                    if USB_msg == "c":
                        Right_status = float(0)
                        Left_status = float(0)
                        AOM_status = 1
                    elif USB_msg == "4":
                        Right_status = float(0)
                        Left_status = float(0)
                    elif USB_msg == "5":
                        Right_status = float(1)
                        Left_status = float(0)
                    elif USB_msg == "6":
                        Right_status = float(0)
                        Left_status = float(1)
                    elif USB_msg == "7":
                        Right_status = float(1)
                        Left_status = float(1)
                    elif USB_msg == "0":
                        mode_status = float(0)
                    elif USB_msg == "1":
                        mode_status = float(1)
                    elif USB_msg == "2":
                        mode_status = float(2)
                    elif USB_msg == "3":
                        mode_status = float(3)