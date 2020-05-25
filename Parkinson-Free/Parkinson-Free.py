import cv2
import numpy as np
from tkinter import *
from tkinter.ttk import Progressbar
from fpdf import FPDF

import time
import datetime
from firebase import firebase
rightTime, leftTime, traceScore, scoreForMotion = 0,0,0,0

firebase = firebase.FirebaseApplication('https://cs-ia-1271a.firebaseio.com/', None)

fistCascade = cv2.CascadeClassifier("Opencv-master-3/haarcascade/aGest.xml")
handCascade = cv2.CascadeClassifier("Opencv-master-3/haarcascade/palm.xml")
fistCascade1 = cv2.CascadeClassifier("Opencv-master-3/haarcascade/fist.xml")
handCascade1 = cv2.CascadeClassifier("Opencv-master-3/haarcascade/Palm-Fist-Gesture-Recognition-master/open_palm.xml")

cap = cv2.VideoCapture(0)

#Declaring all constant and setups
winner = [11,12,13,14,15,16,17,18,19]

Black_img = np.zeros((450, 450), np.uint8)

cv2.line(Black_img, (150, 0), (150, 450), (255, 255, 255), 4)
cv2.line(Black_img, (300, 0), (300, 450), (255, 255, 255), 4)
cv2.line(Black_img, (450, 0), (450, 450), (255, 255, 255), 4)
cv2.line(Black_img, (0, 150), (450, 150), (255, 255, 255), 4)
cv2.line(Black_img, (0, 300), (450, 300), (255, 255, 255), 4)
cv2.line(Black_img, (0, 450), (450, 450), (255, 255, 255), 4)
flag = True

Total_Training_Score = 0
#Declaring all funtions
def winnerDeclaration(chance):
    if winner[0] == winner[1] == winner[2]:
        return True
    elif winner[3] == winner[4] == winner[5]:
        return True
    elif winner[6] == winner[7] == winner[8]:
        return True
    elif winner[3] == winner[4] == winner[5]:
        return True
    elif winner[3] == winner[4] == winner[5]:
        return True
    elif winner[0] == winner[3] == winner[6]:
        return True
    elif winner[1] == winner[4] == winner[7]:
        return True
    elif winner[2] == winner[5] == winner[8]:
        return True
    elif winner[0] == winner[4] == winner[8]:
        return True
    elif winner[2] == winner[4] == winner[6]:
        return True
def drawOnPoint(num, shape):
    x = 1
    y = 1
    if num == 1:
        x = 70 + 150
        y = 60
    elif num == 2:
        x = 70 + 300
        y = 60

    elif num == 3:
        x = 70
        y = 60 + 150
    elif num == 4:
        x = 70 + 150
        y = 60 + 150
    elif num == 5:
        x = 70 + 300
        y = 60 + 150
    elif num == 6:
        x = 70
        y = 60 + 300
    elif num == 7:
        x = 70 + 150
        y = 60 + 300
    elif num == 8:
        x = 70 + 300
        y = 60 + 300
    else:
        x = 70
        y = 60
    if shape == 'x':
        drawCross(x, y)
    elif shape == 'o':
        drawCircle(x, y)
def findingEye2BoxLoc(p1, p2):

    c = 1
    r = 1
    # finding colomn
    if p1 < 150:
        c = 1
    elif p1 < 300:
        c = 2
    elif p1 < 450:
        c = 3
    # finding row:
    if p2 < 150:
        r = 1
    elif p2 < 300:
        r = 2
    elif p2 < 450:
        r = 3

    if r == 1:
        blockNum = -1 + c
    elif r == 2:
        blockNum = 2 + c
    elif r == 3:
        blockNum = 5 + c

    # blockNum = ((r*c)+1)
    # print("p1: " + str(p1))
    # print("p2: " + str(p2))
    # print("r: " + str(r))
    # print("c: " + str(c))

    return (blockNum)
def drawCircle(x, y):
    cv2.circle(Black_img, (x, y), 50, (255, 255, 255), 4)
    cv2.imshow("we", Black_img)
def drawCross(x, y):  # 50,50

    cv2.line(Black_img, (abs(x - 40), abs(y - 40)), (x + 40, y + 40), (255, 255, 255), 4)
    cv2.line(Black_img, (abs(x - 40), y + 40), (x + 40, abs(y - 40)), (255, 255, 255), 4)
    cv2.imshow("we", Black_img)
def usingGesturesToMark(gray,frame):
    fist_rects = fistCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in fist_rects:
        if (y+h)*(x+w) > 100:

            Xpoint = (x + w / 2)
            Ypoint = (y + h / 2)

            print(Xpoint, Ypoint)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True,findingEye2BoxLoc(Xpoint, Ypoint)


    else:
        return 0,0
def usingGesturesToMark1(gray,frame):

    fist_rects = handCascade.detectMultiScale(gray, 1.2, 5)
    for (x, y, w, h) in fist_rects:
        if (y+h)*(x+w) > 100:

            Xpoint = (x + w / 2)
            Ypoint = (y + h / 2)

            print(Xpoint, Ypoint)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True,findingEye2BoxLoc(Xpoint, Ypoint)
    else:
            return 0, 0
def Close(winner):
    window = Tk()
    window.title("WELCOME to Gesture Tic-Tac-Toe")
    window.geometry('350x200+500+300')

    window.grid_location(250, 250)
    lbl = Label(window, text="Gesture Tic-Tac-Toe").pack()

    lable = Label(window, text="Congratulations!!, the winner is " + winner).pack(side='bottom')

    window.mainloop()
def greenTurn(green,frame):
    (_, contours, _) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for picy, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        if (area> 300):
            cv2.rectangle(frame, (x, y),( w, h),(0,0,0),2)
            return True, findingEye2BoxLoc(x, y)
    return False, 0
def redTurn(red):
    (_, contours, _) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        if (area > 300):
            # cv2.rectangle(frame, (x, y),( w, h),(0,0,0),2)

            return True, findingEye2BoxLoc(x, y)
    return False, 0
def SignUp():
    window1 = Tk()
    window1.title("Login/Sign up")
    window1.geometry('670x400+500+300')

    window1.grid_location(250, 250)
    lable = Label(window1, text="Parkinsons-Free").pack()
    global lable2

    lable2 = Label(window1)
    lable2.pack()

    def login():
        global lable2,user

        user = userId.get()

        pword = password.get()
        if (firebase.get('/user', user)) == pword:
            print("loading")
            print('Logging in, Please wait :)')

            firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Right Hand Movement', 0)
            firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Left Hand Movement', 0)
            firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Hand in Motion Training', 0)
            firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Steady Hand Training', 0)

            bar(100)
            lable2.config(text="Logged in, Please close this window")

        else:
            lable2.config(text="Incorrect Password or User ID")


    def signup():
        user = userId.get()
        pword = password.get()
        firebase.put('/user', user, pword)
        firebase.put('/data', user, "session")

        lable2.config( text="Thank you for signing up, Please click the login button now")

    userId = Entry(window1)
    userId.insert(1, 'Username')
    userId.pack()
    password = Entry(window1)
    password.insert(1, 'Password')
    password.pack()
    logo8 = PhotoImage(
        file='Unknown.gif')
    show8 = Label(window1, image=logo8).pack(side='top')
    login = Button(window1, text="Login!", command=login).pack(side=LEFT)
    signup = Button(window1, text="Signup!", command=signup).pack(side=RIGHT)
    progress = Progressbar(window1, orient=HORIZONTAL, length=100, mode='determinate')

    def bar(x):
        progress['value'] = x
        window1.update_idletasks()

    progress.pack()

    window1.mainloop()
#function to play tic tac toe using your Hand
def playGame():
    count = 0
    countR = 0
    arealist = []
    arealistR = []

    while True:


        ret, frame = cap.read()

        frame = cv2.resize(frame, None, fx=450 / 1290, fy=450 / 720, interpolation=cv2.INTER_CUBIC)
        cv2.line(frame, (150, 0), (150, 450), (255, 255, 255), 4)
        cv2.line(frame, (300, 0), (300, 450), (255, 255, 255), 4)
        cv2.line(frame, (450, 0), (450, 450), (255, 255, 255), 4)
        cv2.line(frame, (0, 150), (450, 150), (255, 255, 255), 4)
        cv2.line(frame, (0, 300), (450, 300), (255, 255, 255), 4)
        cv2.line(frame, (0, 450), (450, 450), (255, 255, 255), 4)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flag, area = usingGesturesToMark(gray,frame)
        if flag:
            count = count + 1
            arealist.append(area)
            print(arealist)
        else:
            count = 0

        if count > 10:

            if len(set(arealist)) == 1:
                # and winner[list(set(arealistR))[0]] == 0:
                print("draw Cross")
                print(list(set(arealist))[0])
                loc = list(set(arealist))[0]
                drawOnPoint(list(set(arealist))[0], 'o')
                winner[list(set(arealist))[0]] = 4
                # arealist.clear()

                count = 0
                if winnerDeclaration(12):
                    print("WE HAVE A WINNER -- its the O")
                    Close('O')
                    print(winner)
                    exit()


            else:
                arealist = []

        flagR, areaR = usingGesturesToMark1(gray,frame)
        if flagR:
            countR = countR + 1
            arealistR.append(areaR)
        else:
            countR = 0

        if countR > 20:

            if len(set(arealistR)) == 1:
                # and winner[list(set(arealistR))[0]] == 0:
                print("draw Cricle")
                print(list(set(arealistR))[0])
                drawOnPoint(list(set(arealistR))[0], 'x')
                winner[list(set(arealistR))[0]] = 2
                countR = 0
                # print(winner)

                if winnerDeclaration(6):
                    print("WE HAVE A WINNER -- its the X ")
                    print(winner)
                    Close('X')
                    exit()

            else:
                arealistR = []

        cv2.imshow("Game Play", frame)
        cv2.moveWindow('Game Play',790,230)
        cv2.moveWindow('we',330,230)

        k = cv2.waitKey(1)
        if k == 113:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            break


        cv2.waitKey(1)
def playWColour():
    flag = True

    count = 0
    countR = 0

    arealist = []
    arealistR = []

    while (True):

        ret, frame = cap.read()

        frame = cv2.resize(frame, None, fx=450 / 1290, fy=450 / 720, interpolation=cv2.INTER_CUBIC)
        cv2.line(frame, (150, 0), (150, 450), (255, 255, 255), 4)
        cv2.line(frame, (300, 0), (300, 450), (255, 255, 255), 4)
        cv2.line(frame, (450, 0), (450, 450), (255, 255, 255), 4)
        cv2.line(frame, (0, 150), (450, 150), (255, 255, 255), 4)
        cv2.line(frame, (0, 300), (450, 300), (255, 255, 255), 4)
        cv2.line(frame, (0, 450), (450, 450), (255, 255, 255), 4)

        #######TRACKING REDDD
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)

        # defining the Range of Blue color
        blue_lower = np.array([22, 60, 200], np.uint8)
        blue_upper = np.array([60, 255, 255], np.uint8)

        red = cv2.inRange(hsv, red_lower, red_upper)
        green = cv2.inRange(hsv, blue_lower, blue_upper)

        kernal = np.ones((5, 5), "uint8")

        red = cv2.dilate(red, kernal)
        res = cv2.bitwise_and(frame, frame, mask=red)

        green = cv2.dilate(green, kernal)
        res1 = cv2.bitwise_and(frame, frame, mask=green)

        # GAME PLAY:


        ##MAKING SURE THAT A TURN IS MARKED ONLY WHEN THE PLAYER HOLDS THE COLOUR IN THAT SPOT FOR AN AMOUNT OF TIME
        # FOR GREEN

        flag, area = greenTurn(green,frame)
        if flag:
            count = count + 1
            arealist.append(area)
        else:
            count = 0

        if count > 80:

            if len(set(arealist)) == 1:
                # and winner[list(set(arealistR))[0]] == 0:
                print("draw Cross")
                print(list(set(arealist))[0])
                loc = list(set(arealist))[0]
                drawOnPoint(list(set(arealist))[0], 'x')
                winner[list(set(arealist))[0]] = 4

                count = 0
                if winnerDeclaration(12):
                    print("WE HAVE A WINNER -- its the CROSS")
                    print(winner)
                    exit()






            else:
                arealist = []

                # FOR RED

        # detecttime = endtime


        flagR, areaR = redTurn(red)
        if flagR:
            countR = countR + 1
            arealistR.append(areaR)
        else:
            countR = 0

        if countR > 90:

            if len(set(arealistR)) == 1:
                # and winner[list(set(arealistR))[0]] == 0:
                print("draw Cricle")
                print(list(set(arealistR))[0])
                drawOnPoint(list(set(arealistR))[0], 'o')
                winner[list(set(arealistR))[0]] = 2
                countR = 0
                # print(winner)

                if winnerDeclaration(6):
                    print("WE HAVE A WINNER -- its the knot ")
                    print(winner)
                    exit()

            else:
                arealistR = []

        cv2.imshow("Tick Tac Toe", frame)
        cv2.moveWindow("Tick Tac Toe", 50, 50)

        k = cv2.waitKey(1)
        if k == 113:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            exit()
            break


        cv2.waitKey(1)
def playTraining():
    fistCascade = cv2.CascadeClassifier("Opencv-master-3/haarcascade/aGest.xml")
    handCascade = cv2.CascadeClassifier("Opencv-master-3/haarcascade/palm.xml")


    Black_img = np.zeros((450, 450), np.uint8)


    global posX,posY,colourChange,score, countR,change,scoreForMotion

    posX, posY,scoreForMotion = 0, 0,0
    colourChange = False

    def functionRandPos(state):

        global RanDX, RanDY, posY, posX, change, colourChange

        RanDY = 350 * posY
        RanDX = 350 * posX

        if state:
            posX = posX + 1

        else:
            pass
        new1 = ((0 + RanDX), (0 + RanDY))
        new2 = ((350 + RanDX), (350 + RanDY))
        change = False
        if posX == 3:
            posX = 0
            posY = posY + 1
        if posY > 1:
            posY = 0
            colourChange = not colourChange

        return new1, new2

    score = 0

    def pointsAdd(correct):
        global score

        if correct:
            score = 10 + score

    def usingGesturesToMark():
        fist_rects = fistCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in fist_rects:
            if (y + h) * (x + w) > 100:

                Xpoint = (x + w / 2)
                Ypoint = (y + h / 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)

                if Xpoint >= (0 + RanDX) and Xpoint <= (350 + RanDX) and Ypoint >= (0 + RanDY) and Ypoint <= (
                            350 + RanDY):

                    return True, 1

                else:
                    return False, 0


        else:
            return False, 0

    count = 0
    countR = 0

    arealist = []
    arealistR = []

    # Start()
    a = 0
    change = False

    def drawRect(colourChangePass):
        p1, p2 = functionRandPos(change)

        if colourChangePass:
            cv2.rectangle(frame, (p1), (p2), (0, 250, 250), 4)
            cv2.putText(frame, " Right Hand!", (400, 710), cv2.FONT_ITALIC, 3, 255, thickness=2)

        else:
            cv2.rectangle(frame, (p1), (p2), (250, 250, 0), 4)
            cv2.putText(frame, " Left Hand", (400, 710), cv2.FONT_ITALIC, 3, 255, thickness=2)

    while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        drawRect(colourChange)
        flag, state = usingGesturesToMark()

        if flag:
            countR = countR + 1

            # arealistR.append(state)

            print(countR)

            # LR.config(text = str((len(arealistR)) ))
            # LR.pack()

            cv2.putText(frame, str(countR), (620, 470), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 255), 4,
                        cv2.LINE_AA)

        else:
            countR = 0

        if countR > 9:
            print(countR)
            if 1 == 1:

                print("VERY GOOD")
                change = True
                countR = 0
                scoreForMotion+=10

            else:
                countR = 0

        cv2.imshow("Exercise 1: Movement", frame)
        cv2.moveWindow("Exercise 1: Movement",87,91)

        k = cv2.waitKey(1)
        if k == 113:  # wait for ESC key to exit
            cv2.destroyAllWindows()
            startTraining = False
            break
def playTap():
    print("enrerinh")


    global rightHandInp, LR, addR,rightTime
    global leftHandInp, LL, addL,leftTime
    rightTime = time.time()
    leftTime = time.time()
    leftHandInp, rightHandInp = 0, 0
    addR = 1
    addL = 1
    def RightKey(event):
        global rightHandInp, LR, addR, rightTime

        rightHandInp = rightHandInp + addR
        lableRight.config(text=rightHandInp)
        if rightHandInp > 49:
            LR.config(text='Very well done')
            addR = 0
            rightTime = time.time() - rightTime
            print("rt")
            print(rightTime)




        elif rightHandInp > 30:
            LR.config(text='Only 20 more')

    def LeftKey(event):
        global leftHandInp, LL, addL,leftTime
        leftHandInp = leftHandInp + addL
        lableLeft.config(text=leftHandInp)
        if leftHandInp > 49:
            LL.config(text='Very well done')
            addL = 0
            leftTime = time.time() - leftTime
            print("lt")
            print(leftTime)



        elif leftHandInp > 30:
            LL.config(text='Only 20 more')

    def leave(e):

        global startTap
        startTap = False
        window.destroy()




    window = Tk()
    window.title('Rapid Clicker')
    window.geometry('850x200+500+300')
    reward = Label(window, fg='red', font=("Courier", 7)).pack()

    intructions = Label(window, fg='black', font=("Courier", 14),
                        text="Press the 'J' and 'L' key from your right hand fingers and 'A' and 'D' key from the left hand fingers ")
    intructions.pack()
    lableRight = Label(window, fg='green', font=("Courier", 74))
    LR = Label(window, fg='green', font=("Courier", 17), text='Right-hand-Fingers')
    lableRight.pack(side='right')
    LR.pack(side='right')

    lableLeft = Label(window, fg='red', font=("Courier", 74))
    lableLeft.pack(side='left')
    LL = Label(window, fg='red', font=("Courier", 17), text='Left-hand-Fingers')
    LL.pack(side='left')


    window.bind('<j>', RightKey)
    window.bind('<l>', RightKey)
    window.bind('<a>', LeftKey)
    window.bind('<d>', LeftKey)
    window.bind('<q>', leave)


    window.mainloop()
def playTrace():
        def usingGesturesToMarkNew():
            global traceScore
            fist_rects = fistCascade1.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in fist_rects:
                if (y + h) * (x + w) > 100:

                    Xpoint = (x + w / 2)
                    Ypoint = (y + h / 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
                    print(Xpoint, Ypoint)
                    if (Xpoint > 180 and Xpoint < 240 and Ypoint > 180 and Ypoint < 550):
                        cv2.circle(frame, (int(Xpoint), int(Ypoint)), 10, (0, 255, 0), 3)
                        traceScore+=1
                    elif (Xpoint > 180 and Xpoint < 1000 and Ypoint > 180 and Ypoint < 240):
                        traceScore+=1

                        cv2.circle(frame, (int(Xpoint), int(Ypoint)), 10, (0, 255, 0), 3)
                    elif (Xpoint > 940 and Xpoint < 1000 and Ypoint > 180 and Ypoint < 550):
                        traceScore+=1

                        cv2.circle(frame, (int(Xpoint), int(Ypoint)), 10, (0, 255, 0), 3)
                    elif (Xpoint > 180 and Xpoint < 1000 and Ypoint > 490 and Ypoint < 550):
                        traceScore+=1

                        cv2.circle(frame, (int(Xpoint), int(Ypoint)), 10, (0, 255, 0), 3)
                    else:
                        cv2.circle(frame, (int(Xpoint), int(Ypoint)), 10, (0, 0, 255), 3)

                    return True, 1

                else:
                    return False, 0
        global traceScore
        traceScore = 0
        while True:


            ret, frame = cap.read()
            # frame = cv2.flip(frame, flipCode=1)
            cv2.rectangle(frame, (180, 180), (1000, 550), (255, 0, 0), 5)
            cv2.rectangle(frame, (240, 240), (940, 490), (255, 0, 0), 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            usingGesturesToMarkNew()
            cv2.putText(frame, "Trace the path with your fist to gain points", (360, 360), cv2.FONT_ITALIC, 1, (255, 255, 255),
                        thickness=2)

            cv2.imshow("Exercise 2: Trace", frame)
            cv2.moveWindow("Exercise 2: Trace", 87, 91)

            print(traceScore)

            k = cv2.waitKey(1)
            if k == 113:  # wait for ESC key to exit
                cv2.destroyAllWindows()
                startInfinity = False
                break

def aboutPage():

        htp = Tk()
        htp.title("Learn to Play")
        htp.geometry('750x300+500+300')

        htp1 = Label(htp, text="This is an application for patients of Parkinson's Disease.").pack()
        hptt = Label(htp, text="There are multiple therapies that are designed to help cure this disease").pack()
        htp2 = Label(htp, text="As you do the the training therapies you earn points ").pack()
        htp3 = Label(htp, text="To play the Tic-Tac-Toe game, use your fist to mark an 'O' and the palm to mark an 'X' ").pack()
        htp4 = Label(htp, text="You can also play using different colours: Red and Green").pack()
def Start():
    global email
    window = Tk()
    window.title("Parkinsons-Free")
    window.geometry('670x420+520+320')
    logo8 = PhotoImage(
        file='Unknown.gif')
    show8 = Label(window, image=logo8).pack(side='top')
    def leave(e):

        global startTap
        startTap = False
        window.destroy()



    window.grid_location(250, 250)
    # email = Entry(window)
    # email.insert(0,"Doctor's email")
    # email.pack()

    lable = Label(window, text="Welcome - "+user).pack()



    # lbl = Label(window, text="Learn To Play").pack()
    lable = Label(window, text="Parkinsons-Free").pack()

    btn = Button(window, text="Learn To Play", command=aboutPage).pack(side= TOP)
    quit = Label(window, text=" 'Q' to exit screen").pack(side=BOTTOM)



    openGame = Button(window, text="Tic-Tac-Toe Game", command=playGame).pack(side = LEFT)
    # openGameWColour =  Button(window, text="Tic-Tac-Toe with colour", command=playWColour).pack(side = RIGHT)
    openTraining = Button(window, text=" Steady hand Training!", command=playTraining).pack(side = RIGHT)

    openTap = Button(window, text=" Finger Mobility Training!", command=playTap).pack(side = LEFT)
    openInfinity = Button(window, text=" Hand movement Training! ", command=playTrace).pack(side = LEFT)


    window.bind('<q>', leave)




    window.mainloop()
def ScoreTabulation():
    firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Right Hand Movement', rightTime)
    firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Left Hand Movement', leftTime)
    firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Hand in Motion Training', traceScore)
    firebase.put('/data/' + user + '/session on ' + str(datetime.date.today()), 'Steady Hand Training', scoreForMotion)
def pdfFile():

    pdf = FPDF()
    pdf.add_page()
    pdf.image('pk disease.jpeg', x=85, y=15)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 1, txt="Parkinson-Free report", ln=1, align="C")
    # pdf.cell(200, 50, txt="Parkinson-Free report", ln=1, align="L")
    pdf.cell(1, 20, txt="Name: "+ user, ln=1, align="L")
    pdf.cell(1, 4, txt="Date: " + str(datetime.date.today()), ln=1, align="L")

    pdf.cell(1, 4, txt="Right Hand Movement: " + str(rightTime)+ " seconds", ln=1, align="L")
    pdf.cell(1, 4, txt="Left Hand Movement: "+ str(leftTime)+ " seconds",ln=1, align="L")
    pdf.cell(1, 4, txt="Hand in Motion Training: "+ str(traceScore)+ " points", ln=1, align="L")
    pdf.cell(1, 4, txt="Steady Hand Training: "+str(scoreForMotion)+ " points" , ln=1, align="L")
    pdf.output(str(user)+"'s report"+" on "+ str(datetime.date.today())+"_.pdf")



SignUp()

# print(user)

Start()

pdfFile()

# print(scoreForMotion)

ScoreTabulation()







