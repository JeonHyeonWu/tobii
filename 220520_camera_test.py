import os
import cv2

if not os.path.exists('result') :
    os.makedirs('result')

cap = cv2.VideoCapture(0)

width = int(cap.get(3)) # 가로 길이 가져오기 
height = int(cap.get(4)) # 세로 길이 가져오기
fps = 30
cnt = 1

fcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('result/webcam.avi', fcc, fps, (width, height))

while (True) :
    k = cv2.waitKey(1) & 0xFF
    ret, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if ret :
        out.write(frame)
        cv2.imshow('frame', frame)
        
        if k == ord('s') :
            print("Screenshot saved...")
            cv2.imwrite('result/screenshot{}.png'.format(cnt), frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
            cnt += 1
        elif k == ord('q') : break
    else :
        print("Fail to read frame!")
        break

cap.release()
out.release()
cv2.destroyAllWindows()
