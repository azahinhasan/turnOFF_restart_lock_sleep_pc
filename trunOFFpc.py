from tkinter import *
import os
import time
import ctypes 
import sys
import msvcrt
from ctypes import *
from time import sleep
from colorama import init
from colorama import Fore, Back, Style
init(convert=True)


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
    message1()
    if options == '1':
        return '1'
    elif options == '2':
        return '2'
    elif options == '3':
        return '3'
    elif options == '4':
        return '4'
    elif options == 'e' or options == 'E':
        exit() 
    else:
        invalidMessage(1)
        return actionName()


def actionTimeType():
    options = input("Enter the Time Type: 1>Hour ::: 2>Minutes ::: 3>Secound :-> ")
    if options == '1':
        return actonTimeDuration('1') 
    elif options == '2':
        return actonTimeDuration('2') 
    elif options == '3':
        return actonTimeDuration('3')
    elif options == 'e' or options == 'E':
        exit() 
    else:
        invalidMessage(1)
        return actionTimeType()


def actonTimeDuration(options2):
    loopFor(3)
    waitTime=0
    if options2 == '1':
        waitTime= input("Hours :-> ")
        if waitTime.isnumeric()== True:
            waitTime=int(waitTime)*60*60
        elif waitTime == 'e' or waitTime == 'E':
            exit() 
        else:
            invalidMessage(2)
            return actonTimeDuration('1')
        
    elif options2 == '2':
        waitTime= input("Minutes :-> ")
        if waitTime.isnumeric()== True:
            waitTime=int(waitTime)*60
        elif waitTime == 'e' or waitTime == 'E':
            exit() 
        else:
            invalidMessage(2)
            return actonTimeDuration('2')
    elif options2 == '3':
        waitTime= input("Secound :-> ")
        if waitTime.isnumeric()== True:
            waitTime=int(waitTime)
        elif waitTime == 'e' or waitTime == 'E':
            exit() 
        else:
            invalidMessage(2)
            return actonTimeDuration('3')

    return waitTime



def finalAction(options,waitTime):
    if options == '1':
        print("Running..........")
        actionAfter(waitTime,'PC Shutdown')
        os.system("shutdown /s /t 1")

    elif options == '2':
        print("Running..........")
        actionAfter(waitTime,'PC gonna Restart')
        os.system("shutdown /r /t 1")
    elif options == '3':
        print("Running..........")
        actionAfter(waitTime,'Sceen gonna Lock')
        #print("done")
        ctypes.windll.user32.LockWorkStation()
    elif options == '4':
        print("Running..........")
        actionAfter(waitTime,'PC gonna Sleep')
        #print("done")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")




def  message1():
    loopFor(3)
    print(Fore.RED)
    print(Back.WHITE)
    print("[...For Exiting or Stop the loop press e/E and Enter]")
    print(Style.RESET_ALL)
    loopFor(3)

def message2():
    loopFor(3)
    print(Fore.RED)
    print(Back.WHITE)
    print("[...For Stoping the Countdown You have to Close the Terminal]")
    print("[...Wanna Pause the Countdown? Click on the Terminal..]")
    print("[...Wanna Resume the Countdown? Press Enter..]")
    print(Style.RESET_ALL)
    loopFor(3)

def invalidMessage(value):
    print(Fore.RED)
    if value == 1:
        loopFor(2)
        print("Wrong Input!!!")
        print("Try again....")
        loopFor(2)
    elif value == 2:
        loopFor(2)
        print("Invalid Input!!!")
        print("Please Input a Intiger..")
        loopFor(2)
    print(Style.RESET_ALL)
#main

options = actionName()
loopFor(3)
waitTime = actionTimeType()
loopFor(3)
options3 = input("Are you sure about the action? : 1> Yes ::: AnyButton> No  :-> ")
message2()

if options3 == '1':
    finalAction(options,waitTime)
else:
    exit()