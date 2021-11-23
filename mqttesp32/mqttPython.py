#Install package / Library# https://pypi.org
#==================================================================#
#pip install cvzone==1.4.1pip 
#pip install mediapipe==0.8.7   //Untuk Data Virtualisasi
#pip install pyFirmata
#pip install paho-mqtt

import cv2  #Memanggil Library Open CV
from cvzone.HandTrackingModule import HandDetector
from cvzone.FPS import FPS
import paho.mqtt.client as mqtt

AmbilKamera = cv2.VideoCapture(0)
#Set size screen
x_max, y_max = 1280, 720  #Ukuran Pixel Hasil Vidio
#x_max, y_max = 2560, 1440  #Ukuran Pixel Hasil Vidio
AmbilKamera.set(3, x_max)
AmbilKamera.set(4, y_max)

if  AmbilKamera.isOpened()==False: #Jika Kamera tidak Terdeteksi/gagal diakses
    print("Kamera Tidak dapat diakases, Silahkan Check ID kamera Anda!!!")
    exit()



broker_address="broker.hivemq.com"  #Setting MQTT Broker, Disesuaikan
client = mqtt.Client("iwanCiliburOpenCvClient01") #Masukan MQTT Client Harus UNIX
client.connect(broker_address) #connect to broker

        
fpsReader = FPS()
fps = fpsReader.update()

detector  = HandDetector(detectionCon=0.7)

counter_R, counter_Y, counter_G = 0, 0, 0
R_on, Y_on, G_on = False, False, False

while True:
    
    success, img = AmbilKamera.read()
    flip_img = cv2.flip(img,1)   #Memutar Kamera supaya sesuai dengan pergerakan tangan
    img = detector.findHands(flip_img)
    fps, img = fpsReader.update(flip_img)
    lmList, bboxInfo = detector.findPosition(flip_img)

    if lmList :
        x, y = 80, 80
        w, h = 225, 225
        X, Y = 80, 180

        fx, fy = lmList[8][0], lmList[8][1] #index fingertip
        posFinger = [fx, fy]
        cv2.circle(img, (fx, fy), 15, (255, 0, 255), cv2.FILLED) #draw circle on index fingertip
        cv2.putText(img, str(posFinger), (fx+10, fy-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        cv2.line(img, (0, fy), (x_max, fy), (255,255,0), 2) # x line
        cv2.line(img, (fx, y_max), (fx, 0), (255, 255, 0), 2)# y line

    
       

        if x < fx < x + w - 95 and y < fy < y + h - 95:
            counter_R += 1
            cv2.rectangle(img, (x, y), (w, h), (255, 255, 0), cv2.FILLED)
            if counter_R == 1:
                R_on = not R_on
        else :
            counter_R = 0
            if R_on:
                R_val = "on"
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
            else:
                R_val = "off"
                cv2.rectangle(img, (x, y), (w, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 0, 255), 5)

        if x + 250 < fx < x + 155 + w and y < fy < y + h - 95: #155 = 250 - 95
            counter_Y += 1
            cv2.rectangle(img, (x + 250, y), (w + 250, h), (255, 255, 0), cv2.FILLED)
            if counter_Y == 1:
                Y_on = not Y_on
        else:
            counter_Y = 0
            if Y_on:
                Y_val = "on"
                cv2.rectangle(img, (x+250, y), (w+250, h), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, "ON", (X+250, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
            else:
                Y_val = "off"
                cv2.rectangle(img, (x + 250, y), (w + 250, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X + 250, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 255, 255), 5)

        if x + 500 < fx < x + 405 + w and y < fy < y + h - 95: #500 - 95 = 405
            counter_G += 1
            cv2.rectangle(img, (x + 500, y), (w + 500, h), (255, 255, 0), cv2.FILLED)
            if counter_G == 1:
                G_on = not G_on

        else:
            counter_G = 0
            if G_on:
                G_val = "on"
                cv2.rectangle(img, (x + 500, y), (w + 500, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "ON", (X + 500, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (255, 255, 255), 5)
            else:
                G_val = "off"
                cv2.rectangle(img, (x + 500, y), (w + 500, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "OFF", (X + 500, Y), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 255, 0), 5)


        #val = str(R_val) + str(Y_val) + str(G_val)
        #client = mqtt.Client("iwanCiliburOpenCvClient01") #Masukan MQTT Client Harus UNIX
        client.connect(broker_address) #connect to broker
        client.publish("iwancilibur/LED_R", R_val)  # publish Merah
        client.publish("iwancilibur/LED_G",Y_val)  # publish Kuning
        client.publish("iwancilibur/LED_B", G_val)  # publish Hijau

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

