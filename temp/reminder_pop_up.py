# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:42:49 2019

@author: slos1
"""

import fnmatch
import os
import tkinter
import time
from datetime import datetime
from configuration import config
import shutil



def read_file():
    body_list = []
    for file in sorted(os.listdir(config.path)):
        if fnmatch.fnmatch(config.path+file,config.path+'*record*'):
            if check_time(file) == 2:
                f = open(config.path+file,"r")
                record_body = []
                record_lines = f.readlines()
                subject = ''
                for line in record_lines:
                    record_body.append(line)
                record = '\n'.join(record_body)
                subject = record_body[2]
                body = record + "\n++++++++++++++++++++++++++++++++\n"
                f.close()
                shutil.move(config.path+file,config.expired_path+file)
                
                body_list.append(body)
    
            elif check_time(file) == 3:
                shutil.move(config.path+file,config.expired_path+file)
    print(body_list)
    return body_list        

def check_time(file):
    f = open(config.path+file,"r")
    temp = f.readline()
    temp = temp.rstrip('\n')
    f.close()
    
    if not os.path.isdir(config.expired_path):
        os.mkdir(config.expired_path)
 
    booking_time = time.strptime(temp, "%Y-%m-%d %H%M")
    booking_time = time.mktime(booking_time)
    
    local = time.localtime()
    local_time = time.mktime(local)
    
    counter =  booking_time - local_time
    print(counter)
    
    #tdy report
    if counter > 0 and counter < int(config.timer): #less than reservation time = tdy record , 
        return 2
    elif counter > 0 and counter < (86400 - (local.tm_hour-1)*60*60): # tdy record only , tdy report
        return 1 
    elif counter < 0: # expired record 
        return 3

    #tmr report         
    if local.tm_wday == 4 and counter > 86400*3-10*60*60 and counter < 3*86400: # fri to mon report 
         return 4
    elif counter > 86400-10*60*60 and counter < 86400:  # normal day
         return 4   

if __name__=="__main__": 
    win = tkinter.Tk()
    win.iconify() # change it to win.withdraw() so main window hides
    
    def generate_report_tdy():
        pass
    
    def generate_report_tmr():
        pass
    
    def reminder():
        record = []
        record = read_file()
        if len(record) == 0:
            record.append("No Record!")
            
        #new window default setting
        top = tkinter.Toplevel(win)
        top_button = tkinter.Button(top,text=record,font=("Arial",12), command=top.destroy).grid()
        
        #repeat
        win.after(10000,reminder)
    
    #(timer,function)
    win.after(0,generate_report_tdy)
    win.after(int(config.timer)*1000,generate_report_tmr)
    win.after(1000,reminder)       
    
    
    win.mainloop()


    