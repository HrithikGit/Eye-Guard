#Imports
import cv2
import time 
from win10toast import ToastNotifier
import os

#Function to get the differnce between two time periods
def getTimeDiffernce(lasttime):
    currtime = time.time()
    return int(currtime-lasttime)

#Function to Shut Down the PC
def shutdown():
    os.system("shutdown /s /t 1")

#Initializatoins
cap = cv2.VideoCapture(0)
cap.set(10,60)
print("Click 'q' to abort ")
lasttime =time.time()
notification = ToastNotifier()

#Customize Messages
message = "You have been staring at Screen for a while now, take a break for a minute"
alert_title = "Danger !"
count =0

while(True):
    success,img = cap.read()
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(img,1.0485258, 6)
    for (ex,ey,ew,eh) in eyes:
        currtime = time.time()
        time_gap= getTimeDiffernce(lasttime)
        print(time_gap)

        #If the time gap is 2 hours i.e., User's eye has been getting detected from past 2 hours continuously
        if(time_gap==7200):  
            notification.show_toast(alert_title,"It's high time you need to take your eyes off screen, shutting down your computer in 10 seconds",icon_path="eyeicon.ico",duration=10)
            time.sleep(20)
            shutdown()      #Shutting down the System   
         
        #If time gap is 30 minute, asking user to take a strict break by multiple notifications      
        elif(time_gap==1800): 
            notification.show_toast('Break Needed',message,icon_path="eyeicon.ico",duration=10) 
            time.sleep(10)
            notification.show_toast("Break Needed(2)","You might not need a break, but your eyes do",icon_path="eyeicon.ico",duration=10)
        
        #If the time gap is 10 min, Gently reminding the User to look away from screen
        elif(time_gap==600):
            notification.show_toast('Reminder',"Hey! remember to look away from screen once a while",icon_path="eyeicon.ico",duration=10)
        
        #Displaying the image
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow("Video",img)
        #Resetting count if eye was detected
        count=0
    else:
        cv2.imshow("Video",img)
        count+=1
        #Considering only a break of 2 min or more
        if(count>=180):
            lasttime = time.time()
    #Terminating Condition 
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break


