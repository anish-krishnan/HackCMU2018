import sys
import time 
sys.path.insert(0, 
"/Users/anishkrishnan/GitHub/HackCMU2018/LeapDeveloperKit_2.3.1+31549_mac 4/")

import pyttsx
import threading


engine = pyttsx.init()

def coolStuff():
    
    engine.say("a")
    # engine.runAndWait()
    
    t = threading.Thread(target=engine.runAndWait,name="hi")
    # t.daemon = True
    t.start()
    
    print("stop")

def this():
    coolStuff()
    time.sleep(1)
    coolStuff()


    
    
    
    
    