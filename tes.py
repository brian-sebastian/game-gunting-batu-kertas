import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

waktu = 0
stateResult = False
startGame = False
score = [0, 0]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
    
    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[: , 80:480]
    
    # tampilkan tangan
    hands, img = detector.findHands(imgScaled)
    
    if startGame:
        
        if stateResult is False:
            waktu = time.time() - initialTime
            cv2.putText(imgBG, str(int(waktu)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            
            if waktu > 3:
                stateResult = True
                waktu = 0
                
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    
                    randomNumber = random.randint(1, 3)
                    imgAi = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAi, (149, 310))
                    
                    # Ketika plyer menang
                    if(playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        score[1] += 1
                            
                    # AI menang
                    if(playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        score[0] += 1
       
    
    imgBG[234:654, 795:1195] = imgScaled
    
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAi, (149, 310))
    
    
    cv2.putText(imgBG, str(score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    
    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("Scaled", imgScaled)
    
      
    key = cv2.waitKey(1) #menunggu input keyboard selama 1 milidetik
   
    if key == ord('s'): # memeriksa jika tombol 's' di tekan 
        startGame = True
        initialTime = time.time()
        stateResult = False
    
    
