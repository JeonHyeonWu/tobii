#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas import DataFrame
import logging
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from datetime import datetime
from PyQt5 import *
from Second_0420 import SecondWindow
from Third_0518 import ThirdWindow
import tkinter as tk

global Style_1
global Style_2
global Style_3
global Style_4
global Style_5
logging.basicConfig(level=logging.WARNING)
Style_1 = "color: gray;""background-color: white;""border-style: solid;""border-width: 2px;""border-color: gray;""border-radius: 3px"
Style_2 = "color: gray;""border-style: solid;""border-width: 2px;""border-color: red;""border-radius: 3px"
Style_3 = "color: black;""background-color: white;""border-style: solid;""border-width: 2px;""border-color: black;""border-radius: 3px"
Style_4 = "color: black;""background-color: white;""border-style: solid;""border-width: 2px;""border-color: green;""border-radius: 3px"
Style_5 = "color: black;""border-style: solid;""border-width: 2px;""border-color: green;""border-radius: 3px"

class FirstWindow(QWidget):
    
    ############### 전역변수 설정 및 기존 데이터 취득 #####################################
    # 초기 입력값 설정

    Cycle_Time = 20
    DF_Result = DataFrame({"Azimuth_Right":[0],"Azimuth_Left":[0],"AOM_Right":[0],"AOM_Left":[0],
                           "Elevation_Right":[0],"Elevation_Left":[0], "Xaxis_Right":[0],"Xaxis_Left":[0],
                           "Yaxis_Right":[0], "Yaxis_Left":[0],"Zaxis_Right":[0],"Zaxis_Left":[0],
                           'Pupil_Diameter_Right': [0],'Pupil_Diameter_Left': [0],"mode_status":[0]})
    
    #######################################################################################

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        global project_ID
        global patient_ID
        global patient_birth
        global Style_1
        global Style_2
        Font_1 = QFont("Times New Roman",12,QFont.Bold)
        Font_2 = QFont("Bahnschrift SemiLight",10) 
        Font_n = QFont("Bahnschrift SemiLight",9) 
        self.lbl_red = QLabel('프로젝트명 : ')
        self.lbl_red.setText('<font color="gray">프로젝트명</font><font color="red">*</font><font color="gray">   :   </font>')
        self.lbl_green = QLabel('환자명 : ')
        self.lbl_green.setText('<font color="gray">환자명</font><font color="red">*</font><font color="gray">   :   </font>')
        self.lbl_birth = QLabel('ID : ')
        self.lbl_notion = QLabel()
        self.lbl_notion.setText('<font color="red">*</font><font color="black">은 필수 입력사항입니다.</font>')
        self.lbl_red.setStyleSheet(Style_1)
        self.lbl_green.setStyleSheet(Style_1)
        self.lbl_birth.setStyleSheet(Style_1)
        self.lbl_notion.setAlignment(Qt.AlignRight)
        self.lbl_red.setFont(Font_1)
        self.lbl_green.setFont(Font_1)
        self.lbl_birth.setFont(Font_1)
        self.lbl_notion.setFont(Font_n)
        self.pb_project_ID = QPushButton('프로젝트명 입력')
        self.pb_project_ID.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_project_ID.setStyleSheet(Style_2)
        self.pb_project_ID.setFont(Font_2)
        self.pb_project_ID.clicked.connect(self.project_ID_dialog)
        project_ID = {}
        self.pb_patient_ID = QPushButton('환자명 입력')
        self.pb_patient_ID.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_patient_ID.setStyleSheet(Style_2)
        self.pb_patient_ID.setFont(Font_2)
        self.pb_patient_ID.clicked.connect(self.patient_ID_dialog)
        patient_ID = {}
        self.patient_birth = QPushButton('ID 입력')
        self.patient_birth.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.patient_birth.setStyleSheet(Style_2)
        self.patient_birth.setFont(Font_2)
        self.patient_birth.clicked.connect(self.patient_birth_dialog)
        patient_birth = {}   
        self.pb_Done_ID = QPushButton('입력 완료')
        self.pb_Done_ID.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_Done_ID.setStyleSheet(Style_2)
        self.pb_Done_ID.setFont(Font_2)
        self.pb_Done_ID.clicked.connect(self.toggle_window1)

        self.analy = QPushButton('데이터 분석')
        self.analy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.analy.setStyleSheet(Style_2)
        self.analy.setFont(Font_2)
        self.analy.clicked.connect(self.analy_window)
        
        vbox0 = QVBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()
        vbox4 = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox1.addWidget(self.lbl_red)
        vbox1.addWidget(self.lbl_green)
        vbox1.addWidget(self.lbl_birth)
        vbox1.addWidget(self.lbl_notion)
        vbox2.addWidget(self.pb_project_ID)
        vbox2.addWidget(self.pb_patient_ID)
        vbox3.addWidget(self.patient_birth)
        vbox3.addWidget(self.pb_Done_ID)
        vbox4.addWidget(self.analy)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)
        vbox0.addLayout(vbox1)
        vbox0.addLayout(hbox)
        vbox0.addLayout(vbox4)
        self.setLayout(vbox0)
        self.setWindowTitle('TI inc. Igaze Ver 1.0')
        root = tk.Tk()
        width_mm = int((508*350)/root.winfo_screenmmwidth())
        height_mm = int((286*300)/root.winfo_screenmmheight())
        self.setGeometry(0, 0, width_mm, height_mm)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def project_ID_dialog(self):
        global project_ID
        global Style_1
        global Style_2
        global Style_3
        global Style_4
        global Style_5
        
        project_ID, ok = QInputDialog.getText(self, '프로젝트명 : ', '프로젝트명 입력')
        if ok:
            self.lbl_red.setText('<font color="black">프로젝트명</font><font color="red">*</font><font color="black">:</font> %s' %project_ID)
            self.lbl_red.setStyleSheet(Style_3)
            self.pb_project_ID.setText('프로젝트명 수정')
            self.pb_project_ID.setStyleSheet(Style_4)
            if (len(project_ID) != 0) and (len(patient_ID) != 0):
                self.pb_Done_ID.setStyleSheet(Style_5)
            elif (len(project_ID) == 0) :
                self.pb_project_ID.setText('프로젝트명 입력')
                self.pb_project_ID.setStyleSheet(Style_2)
                self.lbl_red.setText('<font color="gray">프로젝트명</font><font color="red">*</font><font color="gray">:</font> %s' %project_ID)
                self.lbl_red.setStyleSheet(Style_1)
                self.pb_Done_ID.setStyleSheet(Style_2)
            else :
                self.pb_Done_ID.setStyleSheet(Style_2)
            
    def patient_ID_dialog(self):
        global patient_ID
        global Style_1
        global Style_2
        global Style_3
        global Style_4
        global Style_5

        patient_ID, ok = QInputDialog.getText(self, '환자명 : ', '환자명 입력')
        if ok:
            self.lbl_green.setText('<font color="black">환자명</font><font color="red">*</font><font color="black">:</font> %s' % patient_ID)
            self.lbl_green.setStyleSheet(Style_3)
            self.pb_patient_ID.setText('환자명 수정')
            self.pb_patient_ID.setStyleSheet(Style_4)

            if (len(project_ID) != 0) and (len(patient_ID) != 0):
                self.pb_Done_ID.setStyleSheet(Style_5)
            elif (len(patient_ID) == 0) :
                self.pb_patient_ID.setStyleSheet(Style_2)
                self.lbl_green.setText('<font color="gray">환자명</font><font color="red">*</font><font color="gray">:</font> %s' % patient_ID)
                self.lbl_green.setStyleSheet(Style_1)
                self.pb_Done_ID.setStyleSheet(Style_2)
            else :
                self.pb_Done_ID.setStyleSheet(Style_2)

    def patient_birth_dialog(self):
        global patient_birth
        global Style_1
        global Style_2
        global Style_3
        global Style_4
        global Style_5

        patient_birth, ok = QInputDialog.getText(self, 'ID : ', 'ID 입력')
        if ok:
            self.lbl_birth.setText('ID : %s' %patient_birth)
            self.lbl_birth.setStyleSheet(Style_3)
            self.patient_birth.setText('ID 수정')
            self.patient_birth.setStyleSheet(Style_4)

            if (len(patient_birth) != 0) and (len(patient_birth) != 0):
                self.patient_birth.setStyleSheet(Style_5)
            elif (len(patient_birth) == 0) :
                self.patient_birth.setText('ID 입력')
                self.patient_birth.setStyleSheet(Style_2)
                self.lbl_birth.setText('ID : %s'%patient_birth)
                self.lbl_birth.setStyleSheet(Style_1)
                self.patient_birth.setStyleSheet(Style_2)
            else :
                self.patient_birth.setStyleSheet(Style_2)
                

    def toggle_window1(self):
        global DF_Result
        global DF_Date
        global OutFileName
        global root_folder
        global root_data

        if (len(project_ID) == 0) and (len(patient_ID) !=0):
            QtWidgets.QMessageBox.warning(self, "QMessageBox", "\n프로젝트명을 입력해주십시오.")
        elif (len(project_ID) != 0) and (len(patient_ID) == 0):
            QtWidgets.QMessageBox.warning(self, "QMessageBox", "\n환자명을 입력해주십시오.")
        elif (len(project_ID) == 0) and (len(patient_ID) == 0):
            QtWidgets.QMessageBox.warning(self, "QMessageBox", "\n프로젝트, 환자명을 입력해주십시오.")
        else:
            DF_Date = datetime.now().strftime('%Y-%m-%d')
            
            OutFileName = "Strabismus_eyetracking_Data_%s" %DF_Date
            if len(patient_birth) > 0 :
                patient_all = '%s_%s' %(patient_ID,patient_birth)
            else :
                patient_all = '%s_%s' %(patient_ID,DF_Date)
            root_folder = './Data/%s/%s' % (project_ID,patient_all)
            root_data = '%s/%s.csv'% (root_folder,OutFileName)
            try:
                if not(os.path.isdir(root_folder)):
                    os.makedirs(os.path.join(root_folder))
                    self.DF_Result.to_csv(root_data, mode='w')

            except OSError as e:
                print("Failed to create directory!!!!!")
                raise

                
            self.window1 = SecondWindow(root_data,project_ID,patient_ID,patient_birth)
            self.window1.showMaximized()

    def analy_window(self):
        root = tk.Tk()
        width_px = root.winfo_screenwidth()
        height_px = root.winfo_screenheight()
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './', "csv files (*.csv)")
        all_name = FileOpen[0]
        self.window3 = ThirdWindow(all_name,width_px,height_px)
        self.window3.showMaximized() 

