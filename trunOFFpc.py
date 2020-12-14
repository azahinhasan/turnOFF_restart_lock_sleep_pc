from tkinter import *
import os
import time
import ctypes 
import sys
from ctypes import *
from time import sleep

def lockActin():
    windll.user32.BlockInput(False)

def loopFor(value):
    for i in range(value):
        print("---")


def actionAfter(waitTime,actionName):

    totalTime = waitTime-1
    print("Time Left: ")
    #for i in range(waitTime):      
    #    time.sleep(1)
     #   print(totalTime)
     #   totalTime-=1

    sys.stdout.flush()
    some_list = [0] * waitTime
    loopFor(5)
    for i in enumerate(some_list):
        msg = "%s in %i Sec....." % (actionName,totalTime)
        totalTime-=1
        sys.stdout.write(msg + chr(8) * len(msg))
        sys.stdout.flush()
        sleep(1)

    

    

waitTime=0

options = input("Chose your option: 1> ShutDown ::: 2> Restart ::: 3> Logout:-> ")
loopFor(3)
options2 = input("Enter the Time Type: 1>Hour ::: 2>Minutes ::: 3>Secound :-> ")
loopFor(3)
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


loopFor(3)
options3 = input("Are you sure about the action: 1> Yes ::: 2> No  :-> ")

loopFor(3)


if options == '1' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime,'Shutdown')
    os.system("shutdown /s /t 1")

elif options == '2' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime,'Restart')
    os.system("shutdown /r /t 1")
elif options == '3' and options3 == '1':
    print("Running..........")
    actionAfter(waitTime,'Sceen Lock')
    #print("done")
    ctypes.windll.user32.LockWorkStation()

else:
    exit()




