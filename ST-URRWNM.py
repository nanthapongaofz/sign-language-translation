from tkinter import *
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
import mediapipe as mp
import pyttsx3


win = Tk()
width=win.winfo_screenwidth()
height=win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))
win.configure(bg="#FFFFF7")
win.title('Sign Language : URRWNM CODING')

global img,finalImage,finger_tips,thumb_tip,cap, image, rgb, hand, results, _, w, \
       h,status,mpDraw,mpHands,hands,label1,btn,btn2

cap=None

Label(win,text='Sign Language : URRWNM CODING',font=('Helvatica',18,'italic'),bd=5,bg='#199ef3',fg='white',relief=SOLID,width=200 )\
     .pack(pady=15,padx=300)

def wine():
    global finger_tips, thumb_tip, mpDraw, mpHands, cap, w, h, hands, label1, check, img
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    w = 1000
    h = 500

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
    cshow=0
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

            print(finger_fold_status)
            x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
            print(x, y)
            # stop
            if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'STOP ! Dont move.'
                upCount.set('STOP ! Dont move.')
                print('STOP ! Dont move.')
            # okay
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Perfect , You did  a great job.'
                print('Perfect , You did  a great job.')
                upCount.set('Perfect , You did  a great job.')

            # spidey
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Good to see you.'
                print(' Good to see you. ')
                upCount.set('Good to see you.')

            # Point
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                upCount.set('You Come here.')
                print("You Come here.")
                cshow = 'You Come here.'

            # Victory
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                upCount.set('Yes , we won.')
                print("Yes , we won.")
                cshow = 'Yes , we won.'

            # Left
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                upCount.set('Move Left')
                print(" MOVE LEFT")
                cshow = 'Move Left'
            # Right
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                upCount.set('Move Right')
                print("Move RIGHT")
                cshow = 'Move Right'
            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    print("I like it")
                    upCount.set('I Like it')
                    cshow = 'I Like it'
                # Dislike
                elif lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    upCount.set('I dont like it.')
                    print(" I dont like it.")
                    cshow = 'I dont like it.'

            mpDraw.draw_landmarks(rgb, hand, mpHands.HAND_CONNECTIONS)
        cv2.putText(rgb, f'{cshow}', (10, 50),
                cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 255), 2)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    win.after(1, live)
    crr=Label(win,text='Current Status :',font=('Helvetica',18,'bold'),bd=5,bg='gray',width=15,fg='#232224',relief=GROOVE )
    status = Label(win,textvariable=upCount,font=('Helvetica',18,'bold'),bd=5,bg='gray',width=50,fg='#232224',relief=GROOVE )

    status.place(x=400,y=600)
    crr.place(x=120,y=600)

def voice():

    engine = pyttsx3.init()
    engine.say((upCount.get()))
    engine.runAndWait()



wine()
live()

Button(win,text='Sound',padx=95,bg='#199ef3',fg='white',relief=RAISED,width=1,bd=5,font=('Helvatica',12,'bold') ,command=voice)\
      .place(x=width-250,y=500)

win.mainloop()