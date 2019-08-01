# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:29:20 2019

@author: slos1
"""
import fnmatch
import os
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from configuration import *

class Reminder():
    def read_file():
        record_list = []
        for file in os.listdir(config().path):
            if fnmatch.fnmatch(file, '*record*'):
                if Reminder.check_time(file):
                    f = open(file,"r")
                    record_body = []
                    record_lines = f.readlines()
                    for line in record_lines:
                        record_body.append(line)
                    record = '\n'.join(record_body)
                    record_list.append(record + "\n++++++++++++++++++++++++++++++++++++++++++")
        Reminder.reminder_message(record_list)
                                      
                    
                
    def check_time(file):
        f = open(file,"r")
        temp = f.readline()
        temp = temp.rstrip('\n')
        try:
            booking_time = time.strptime(temp, "%Y-%m-%d %H-%M")
            booking_time = time.mktime(booking_time)
            
            local_time = time.localtime()
            local_time = time.mktime(local_time)
            
            counter =  booking_time - local_time
            
            if counter > 0 and counter <86400: #less than a day
                return True
            else:
                return False
                
        except Exception as e:
            print("Error ocurred: %s" %str(e))
            
    def reminder_message(record_list):
        win = tkinter.Tk()
        win.wm_attributes("-topmost", 1) #always on top 
        win.withdraw()
        record = '\n'.join(record_list)
        if record == "":
            record = "No Record"
        messagebox.showinfo("Record",record)
        win.destroy()

if __name__ == '__main__':
    Reminder.read_file()
    #Reminder.reminder_message("asd")