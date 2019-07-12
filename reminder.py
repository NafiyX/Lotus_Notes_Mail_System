# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:29:20 2019

@author: slos1
"""
import fnmatch
import os
import time
from tkinter import *

class Reminder(object):
    def _init_(self):
        print('.')

    def read_file():
        for file in os.listdir('C:\\Users\\slos1\\Desktop\\mail system(9 jul)'):
            if fnmatch.fnmatch(file, 'record_*'):
                print (file)
                file_name = 'C:\\Users\\slos1\\Desktop\\mail system(9 jul)\%s' %file
                if Reminder.check_time(file_name) == True:
                    Reminder.reminder_message(file_name)
                    
                
    def check_time(file):
        f = open(file,"r")
        temp = f.readline()
        temp = temp.rstrip('\n')
        print(temp)
        try:
            booking_time = time.strptime(temp, "%Y-%m-%d %H-%M-%S")
            booking_time = time.mktime(booking_time)
            print(booking_time)
            
            local_time = time.localtime()
            local_time = time.mktime(local_time)
            print(local_time)

            counter =  booking_time - local_time
            
            if counter < (86400): #less than a day
                print ("Reminder")
                return True
                #Reminder.reminder_message()
            else:               
                print(counter)
                return False
                
        except Exception as e:
            print("Error ocurred: %s" %str(e))
            
    def reminder_message(file_name):
        win = tkinter.Tk()
        win.title("Reminder Message")
        f = open(file_name,"r")
        mail = f.readlines()
        #mail = [x.strip() for x in mail]
        mail_label = Label(win, text = mail,  font=('Arial', 20))
        mail_label.pack()
        
        #ok_button = Button(win, text="OK", command=on_click)
        #ok_button.pack()
        
        win.mainloop()
        



def main():
    Reminder()
    Reminder.read_file()
   
if __name__ == '__main__':
    main()