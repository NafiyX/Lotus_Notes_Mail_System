# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:29:20 2019

@author: slos1
"""

import fnmatch
import os
import time
from datetime import  date, timedelta
from configuration import config
import shutil
import threading
from multiprocessing import Queue
from send_mail import NotesMail

class Reminder:
    def read_file():
        for file in sorted(os.listdir(config.path)):
            if fnmatch.fnmatch(config.path+file,config.path+'*record*'):
                if Reminder.check_time(file) == 2:
                    f = open(config.path+file,"r")
                    record_body = []
                    record_lines = f.readlines()
                    subject = ''
                    for line in record_lines:
                        record_body.append(line)
                    record = '\n'.join(record_body)
                    subject = record_body[2]
                    body = record
                    f.close()
                    Reminder.send(subject,body)
                    shutil.move(config.path+file,config.expired_path+file)
                    
                elif Reminder.check_time(file) == 3:
                    shutil.move(config.path+file,config.expired_path+file)
                    

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
        
            
            
    def generate_report_today():
        counter = 0
        subject = 'No of Reservation Today: %s' %str(counter)
        body="No Records."
        record_list=[]
        for file in sorted(os.listdir(config.path)):
            if fnmatch.fnmatch(config.path+file,config.path+'*record*'):
                if Reminder.check_time(file) in (1,2):
                    f = open(config.path+file,"r")
                    record_body = []
                    record_lines = f.readlines()
                    for line in record_lines:
                        record_body.append(line)
                    record = '\n'.join(record_body)
                    record_list.append(record+'\n+++++++++++++++++++++++++++++\n')
                    counter = counter +1
                    subject = 'No of Reservation Today: %s' %str(counter)
        body = '\n'.join(record_list)  
        Reminder.send(subject,body)
    
    def generate_report_tmr():
        counter = 0
        subject = 'No of Reservation Tomorrow: %s' %str(counter)
        body="No Records."
        record_list=[]
        for file in sorted(os.listdir(config.path)):
            if fnmatch.fnmatch(config.path+file,config.path+'*record*'):
                if Reminder.check_time(file) == 4:
                    f = open(config.path+file,"r")
                    record_body = []
                    record_lines = f.readlines()
                    for line in record_lines:
                        record_body.append(line)
                    record = '\n'.join(record_body)
                    record_list.append(record+'\n+++++++++++++++++++++++++++++\n')
                    counter = counter +1
                    subject = 'No of Reservation Tomorrow: %s' %str(counter)
                    f.close()
        if time.localtime().tm_wday == 4:
           subject = 'No of Reservation on Monday: %s' %str(counter) 
        body = '\n'.join(record_list)  
        Reminder.send(subject,body)
    
    def send(subject,body):
        mail = NotesMail(config.server,'mail\\.nsf')
        receivers = config.receivers.split(",")
        mail.send_mail(receivers, subject, body)
        
        
             
def report_timer(q):
    temp_time = time.localtime()
    report_hour=int(config.hour) #config
    report_min=int(config.minute) #config
    if report_hour == temp_time.tm_hour:
        report_hour = report_hour+1
    report_time=abs(report_hour-temp_time.tm_hour)*60*60+(report_min-temp_time.tm_min)*60
    print("report timer")
    time.sleep(report_time)      
    q.put(Reminder.generate_report_tmr)
    
def reminder_timer(q):
    print("reminder timer")
    time.sleep(int(config.interval))
    q.put(Reminder.read_file)

def main():
    q = Queue(maxsize=0)
    
    t = config.date   
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    if  d1 >= t:
        print("tdy")
        print(today.weekday())
        if today.weekday() != 4:
            tmr = today + timedelta(days=1)
        else:
            tmr = today + timedelta(days=3)
        config.date_change(tmr)
        Reminder.generate_report_today()
    
    report_thread = threading.Thread(target=report_timer,args=(q,))
    report_thread.start()

    while True:
        report_thread.join(timeout=1)
        reminder_thread = threading.Thread(target=reminder_timer,args=(q,))  
        if reminder_thread.is_alive(): 
            reminder_thread.join(timeout=0.5)
        else:
            reminder_thread.start()
        f = q.get()
        f() 
        time.sleep(0.2)
        
        
        
if __name__ == '__main__':
    main()
