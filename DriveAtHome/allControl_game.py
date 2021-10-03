#for user to see the frame send by car
from ar_score import *
from ar_time import *
from free import *

#for user to use their body to control car
from bp import *
from main_change import *
from new import *
# from dp import *

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QApplication
from Dialog_connect import Ui_Dialog_connect

import threading



def allControl(player, CMchoose, PMchoose, square):
    if(PMchoose == "ar_score"):
        t = threading.Thread(target = ar_score, args=(player,))
        # ar_score(player)   
        # return 0 
    elif(PMchoose == "ar_time"):
        t = threading.Thread(target = ar_time, args=(player,))
        # return 0
    elif(PMchoose == "drive"): #equal to free mode
        t = threading.Thread(target = free, args=(player,))
        # return 0
    t.start()
    if(CMchoose == "body"):
        x = main(square)
        return x
    elif(CMchoose == "drive"):
        x = dp(square)
        print(x+111111111111111)
        return x
    # t.join()
    print("done")


