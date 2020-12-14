from tkinter import *
import os
import time
import ctypes 
import sys
from ctypes import *
from time import sleep



def loopFor(value):
    for i in range(value):
        print("---")


def actionAfter(waitTime,actionName):

    totalTime = waitTime-1
    sys.stdout.flush()
    some_list = [0] * waitTime
    loopFor(5)
    for i in enumerate(some_list):
        msg = "%s in %i Sec....." % (actionName,totalTime)
        totalTime-=1
        sys.stdout.write(msg + chr(8) * len(msg))
        sys.stdout.flush()
        sleep(1)
    print()

    

def actionName():
    options = input("Chose your option: 1> ShutDown ::: 2> Restart ::: 3> Logout ::: 4> Sleep :-> ")
    if options == '1':
        return '1'
    elif options == '2':
        return '2'
    elif options == '3':
        return '3'
    elif options == '4':
        return '4' 
    else:
        loopFor(2)
        print("Wrong Input!!!!!")
        print("Try again....")
        actionName()


def actionTimeType():
    options = input("Enter the Time Type: 1>Hour ::: 2>Minutes ::: 3>Secound :-> ")
    if options == '1':
        return actonTimeDuration('1') 
    elif options == '2':
        return actonTimeDuration('2') 
    elif options == '3':
        return actonTimeDuration('3') 
    else:
        loopFor(2)
        print("Wrong Input!!!!!")
        print("Try again....")
        actionTimeType()


def actonTimeDuration(options2):
    loopFor(3)
    waitTime=0
    if options2 == '1':
        waitTime= input("Hours :-> ")
        waitTime=int(waitTime)*60*60
    elif options2 == '2':
        waitTime= input("Minutes :-> ")
        waitTime=int(waitTime)*60
    elif options2 == '3':
        waitTime= input("Secound :-> ")
        waitTime=int(waitTime)

    return waitTime



def finalAction(options,waitTime):
    if options == '1':
        print("Running..........")
        actionAfter(waitTime,'PC Shutdown')
        os.system("shutdown /s /t 1")

    elif options == '2':
        print("Running..........")
        actionAfter(waitTime,'PC Restart')
        os.system("shutdown /r /t 1")
    elif options == '3':
        print("Running..........")
        actionAfter(waitTime,'Sceen Lock')
        #print("done")
        ctypes.windll.user32.LockWorkStation()
    elif options == '4':
        print("Running..........")
        actionAfter(waitTime,'Sceen Lock')
        #print("done")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")







#main

options = actionName()
loopFor(3)
waitTime = actionTimeType()
loopFor(3)

options3 = input("Are you sure about the action? : 1> Yes ::: AnyButton> No  :-> ")

loopFor(3)
if options3 == '1':
    finalAction(options,waitTime)
else:
    exit()



