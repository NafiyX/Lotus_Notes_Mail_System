# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:29:20 2019

@author: slos1
"""
import fnmatch
import os
import time
import tkinter
from tkinter import messagebox
from configuration import config
import shutil

class Reminder:
    def read_file():
        record_list = []
        for file in os.listdir(config.path):
            if fnmatch.fnmatch(config.path+file,config.path+'*record*'):
                if Reminder.check_time(file) == 1:
                    f = open(config.path+file,"r")
                    record_body = []
                    record_lines = f.readlines()
                    for line in record_lines:
                        record_body.append(line)
                    record = '\n'.join(record_body)
                    record_list.append(record + "\n++++++++++++++++++++++++++++++++++++++++++")
                    
                elif Reminder.check_time(file) == 2:
                    if not os.path.isdir(config.expired_path):
                        os.mkdir(config.expired_path)
                    shutil.move(config.path+file,config.expired_path+file)
                    #os.rename(config.path,'C:\\Users\\slos1\\Desktop\\mailsys\\expired\\'+file)
        Reminder.reminder_message(record_list)

    def check_time(file):
        f = open(config.path+file,"r")
        temp = f.readline()
        temp = temp.rstrip('\n')
        try:
            booking_time = time.strptime(temp, "%Y-%m-%d %H-%M")
            booking_time = time.mktime(booking_time)
            
            local_time = time.localtime()
            local_time = time.mktime(local_time)
            
            counter =  booking_time - local_time
            
            if counter > 0 and counter < 86400*int(config.day): #less than a day
                return 1
            elif counter < 0:
                return 2
                
        except Exception as e:
            print("Error ocurred: %s" %str(e))
            
            
    def reminder_message(record_list):
        win = tkinter.Tk()
        win.withdraw()
        win.wm_attributes("-topmost", 1) #always on top 
        win.after(int(config.timer)*1000,win.destroy)
        record = '\n'.join(record_list)
        if record == "":
            record = "No Record"
        tkinter.messagebox.showinfo("Record",record,parent=win)
        
        

if __name__ == '__main__':
    Reminder.read_file()
    #Reminder.reminder_message("asd")