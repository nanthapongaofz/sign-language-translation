from tkinter import *
from PIL import Image, ImageTk
import cv2
#from tkinter import filedialog
import mediapipe as mp
#import pyttsx3
import pygame

#engine = pyttsx3.init()
#TH_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_THAI"
#engine.setProperty('voice', TH_voice_id)
#engine.setProperty('rate', 120)  #ช้าลงหรือเพิ่มขึ้น 0-148

pygame.init()
pygame.mixer.init()
s01 = 'C:/Users/NW/Documents/Python/sign/sound/หยุดอย่าขยับ.wav'
s02 = 'C:/Users/NW/Documents/Python/sign/sound/ยอดเยี่ยมคุณทำได้ดีมาก.wav'
s03 = 'C:/Users/NW/Documents/Python/sign/sound/ยินดีที่ได้พบคุณ.wav'
s04 = 'C:/Users/NW/Documents/Python/sign/sound/ขยับมาใกล้ๆ.wav'
s05 = 'C:/Users/NW/Documents/Python/sign/sound/เย่!เราชนะแล้ว.wav'
s06 = 'C:/Users/NW/Documents/Python/sign/sound/ขยับมาทางซ้าย.wav'
s07 = 'C:/Users/NW/Documents/Python/sign/sound/ขยับมาทางขวา.wav'
s08 = 'C:/Users/NW/Documents/Python/sign/sound/ฉันเห็นด้วยนะ.wav'
s09 = 'C:/Users/NW/Documents/Python/sign/sound/ไม่เอาดีกว่า.wav'

win = Tk()
width=win.winfo_screenwidth()
height=win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))
win.iconbitmap(r'C:\Users\NW\Documents\Python\sign\info.ico') ##************ path ไอคอน
win.configure(bg="#FFFFFF")
win.title('Sign Language Translator : URRWNM CODING')

global img,finalImage,finger_tips,thumb_tip,cap, image, rgb, hand, results, _, w,h,status,mpDraw,mpHands,hands,label1

cap=None

Label(win,text='Sign Language Translator : URRWNM CODING (ภาษาไทย)',font=('Helvatica',18,'italic'),bd=5,bg='#f31932',fg='white',relief=SOLID,width=200 ).pack(pady=15,padx=300)

def wine():
    global finger_tips, thumb_tip, mpDraw, mpHands, cap, w, h, hands, label1, check, img
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    w = 1750
    h = 900

    if cap:
        cap.release()  # Release the previous video capture

    label1 = Label(win, width=w, height=h, bg="#FFFFF7")
    label1.place(x=80, y=70)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)


###########################################Detection##########################################
def live():
    global v
    global upCount
    global cshow,img
    cshow=""
    upCount = StringVar()
    _, img = cap.read()

    img = cv2.resize(img, (w, h))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand.landmark):
                lm_list.append(lm)
            finger_fold_status = []

            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                if lm_list[tip].x < lm_list[tip - 2].x:
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

            #print(finger_fold_status)
            x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
            #print(x, y)
            # stop
            if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'STOP ! Dont move.'
                #print('STOP ! Dont move.')
                #upCount.set('STOP ! Dont move.')
                #engine.say("หยุดอย่าขยับ")
                #engine.runAndWait()
                #s01.play()
                #pygame.mixer.init()
                pygame.mixer.music.load(s01)
                pygame.mixer.music.play()
                #pygame.event.wait()
                
                
                
            # okay
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Perfect , You did  a great job.'
                #print('Perfect , You did  a great job.')
                #upCount.set('Perfect , You did  a great job.')
                #engine.say("ยอดเยี่ยม คุณทำได้ดีมาก")
                #engine.runAndWait()
                #s02.play()
                #pygame.mixer.init()
                pygame.mixer.music.load(s02)
                pygame.mixer.music.play()
                #pygame.event.wait()
            # spidey
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Good to see you.'
                #print(' Good to see you. ')
                #upCount.set('Good to see you.')
                #engine.say("ยินดีที่ได้พบคุณ")
                #engine.runAndWait()
                pygame.mixer.music.load(s03)
                pygame.mixer.music.play()
                #s03.play()
                
            # Point
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                #upCount.set('You Come here.')
                #print("You Come here.")
                cshow = 'You Come here.'
                #engine.say("ขยับมาใกล้ๆ")
                #engine.runAndWait()
                #s04.play()
                pygame.mixer.music.load(s04)
                pygame.mixer.music.play()
                
            # Victory
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                #upCount.set('Yes , we won.')
                #print("Yes , we won.")
                cshow = 'Yes , we won.'
                #engine.say("เย้ เราชนะแล้ว")
                #engine.runAndWait()
                pygame.mixer.music.load(s05)
                pygame.mixer.music.play()
                #s05.play()
                
            # Left
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                #upCount.set('Move Left')
                #print(" MOVE LEFT")
                cshow = 'Move Left'
                #engine.say("ขยับมาทางซ้าย")
                #engine.runAndWait()
                #s06.play()
                pygame.mixer.music.load(s06)
                pygame.mixer.music.play()
                
            # Right
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                #upCount.set('Move Right')
                #print("Move RIGHT")
                cshow = 'Move Right'
                #engine.say("ขยับมาทางขวา")
                #engine.runAndWait()
                #s07.play()
                pygame.mixer.music.load(s07)
                pygame.mixer.music.play()
                
            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    #print("I like it")
                    #upCount.set('I Like it')
                    cshow = 'I Like it'
                    #engine.say("ฉันเห็นด้วยนะ")
                    #engine.runAndWait()
                    #s08.play()
                    pygame.mixer.music.load(s08)
                    pygame.mixer.music.play()
                    
                # Dislike
                elif lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    #upCount.set('I dont like it.')
                    #print(" I dont like it.")
                    cshow = 'I dont like it.'
                    #engine.say("ไม่เอาดีกว่า")
                    #engine.runAndWait()
                    #s09.play()
                    pygame.mixer.music.load(s09)
                    pygame.mixer.music.play()
            
        else:
            mpDraw.draw_landmarks(rgb, hand, mpHands.HAND_CONNECTIONS)
        cv2.putText(rgb, f'{cshow}', (10, 50),
                cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 255), 2)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    win.after(1, live)
    #crr=Label(win,text='Current Status :',font=('Helvetica',18,'bold'),bd=5,bg='gray',width=15,fg='#232224',relief=GROOVE )
    #status = Label(win,textvariable=upCount,font=('Helvetica',18,'bold'),bd=5,bg='gray',width=50,fg='#232224',relief=GROOVE )

    #status.place(x=400,y=600)
    #crr.place(x=120,y=600)


wine()
live()

win.mainloop()