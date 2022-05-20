#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##############################################
# Tiinc STRABISMUS EYETRACKING PROGRAM  v0.69 #
# Data : Make output csv FILE & PYQT GRAPH   #
# COPYRIGHT BY Jeon                          #
##############################################
# -------------------------------------------------------------------------------
# Change LogUSB_msg_dq

#[v0.1] 2021.09.07 : Made and connected FirstWindow(Input ProjectID, PatientID) & SecondWindow(Dataplotting, video streaming)
#                    Connected Tobii glasses 2 with computer, Data(Azimuth, Elevation, X,Y,Z) Plotting & Video Streaming
#[v0.2] 2021.09.09 : Changed FirstWindow GUI, added rule that coudn't continue if user does not insert project/patient ID
#                    Resized Video width(To 1/2), Added Layer(Setting), Added Legend(graph)
#[v0.3] 2021.09.15 : Added Serial Protocol(communicate Computer with Alternating Occulusion Machine, AOM), Added AOM Graph(ing)
#[v0.32] 2021.09.27 : plot 수정 
#[v0.5] 2021.10.25 : Tobii connection / AOM connection / AOM Mode status 추가 
#[v0.51] 2021.11.01 : Plot 수정
#[v0.6] 2021.11.01 : Layout 수정
#[v0.65]2021.12.03 : 동영상 Frame 수정
#[v0.66]2021.12.06 : 동영상 Frame 수정
#[v0.662]2021.12.06 : USB_msg Video frame으로 수정
#[v0.664]2021.12.21 : Tobii 명칭 > ETM(Eye Tracking Machine) 으로 변경
#[v0.665]2021.12.27 : USB msg 수정 L0R0 - > 4, cycle time 수정, UART통신 유선으로 변경, USB Messeage 최적화(Append구문변경)
#                     iloc 범위수정
#[v0.666]2021.12.28 : 동공 Detection 실패 시 데이터 None으로 기록
#[v0.67]2022.01.07 : 시간컬럼 0.1초까지 표시, 동공사이즈 컬럼 추가, 코드 시작 시점부터 데이터 기록 Serial 데이터 수신부 Video_
#Thread로 옮김
#[v0.671]2022.01.07 : 교대가림기 데이터 수신 시 offset 범위로 인해 잘못된 데이터 수신, offset 조정 0 -> -0.2
#[v0.672]2022.01.12 : 시간,분,초.000 > 분초.000으로 수정
#[v0.68]2022.01.19 : 클래스별로 코드 분화
#[v0.69]2022.01.28 : Video_thread 제거, Qthread Class(name : worker, Serial 및 Video capture 내장) 생성
#[v0.7]2022.02.07 : Firstwindow, Secondwindow 창 크기 컴퓨터 모니터에 맞게 자동 조절기능 추가 
                   # 비디오 녹화 기능 추가
#[v0.8]2022.02.11 : Third Window 창 추가 - 데이터 분석
#[v0.9]2022.02.15 : Third Window > FourthWindow로 변경, 파일 찾기 창(ThirdWindow) 추가 데이터 분석
#[v0.91]2022.03.03 : 데이터 분석 - 알고리즘 추가(노이즈 제거)
#[v1.0]2022.03.04 : 3rd, 4th windows 제거 , 1st window에 데이터 분석 버튼 추가
#[v1.1]2022.03.04 : 데이터 분석 구간 2개로 변경
#[v1.2]2022.03.23 : 그래프시작위치차이, 전체 그래프 x축 연동(x = data.index), 구간선택시 오른쪽/왼쪽 분석결과 동시 출력
#[v1.3]2022.03.25 : 수정요청사항 반영, Export 양식에 따라 데이터 Export 버튼 추가
#[v1.4]2022.03.30 : 안구 시뮬레이터 추가
#[v1.5]2022.03.30 : Time 수정 기존 분초.xxx  >  Running Time
#[v1.6]2022.04.20 : 데이터 획득시간 150ms 로 변경(기존 50ms)
#[v1.7]2022.05.18 : 이상치 제거 함수 수정

import sys
from PyQt5.QtWidgets import *
from First_0518 import FirstWindow
import os



if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = FirstWindow()
    sys.exit(app.exec_())


# In[ ]:




