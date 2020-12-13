from tkinter import *
import os
import time
import ctypes 
from ctypes import *


def lockActin():
    windll.user32.BlockInput(False)

def loopFor():
    for i in range(3):
        print("---")


def actionAfter(waitTime):

    totalTime = waitTime
    print("Time Left: ")
    for i in range(waitTime):      
        time.sleep(1)
        print(totalTime)
        totalTime-=1

    

waitTime=0

options = input("Chose your option: 1> ShutDown ::: 2> Restart ::: 3> Logout:-> ")
loopFor()
options2 = input("Enter the Time Type: 1>Hour ::: 2>Minutes ::: 3>Secound :-> ")
loopFor()
if options2 == '1':
    waitTime= input("Hours :-> ")
    waitTime=int(waitTime)*60*60
elif options2 == '2':
    waitTime= input("Minutes :-> ")
    waitTime=int(waitTime)*60
elif options2 == '3':
    waitTime= input("Secound :-> ")
    waitTime=int(waitTime)
else:
    print("Try Again....")
    exit()


loopFor()
options3 = input("Are you sure about the action: 1> Yes ::: 2> No  :-> ")

loopFor()


if options == '1' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime)
    #os.system("shutdown /s /t 1")

elif options == '2' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime)
    #os.system("shutdown /r /t 1")
elif options == '3' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime)
    print("done")
    #ctypes.windll.user32.LockWorkStation()

else:
    exit()




