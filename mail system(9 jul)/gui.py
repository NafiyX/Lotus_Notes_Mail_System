# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:36:24 2019

@author: slos1
"""
from configuration import *
from tkinter import ttk
from reminder import *
import fnmatch
import os
import datetime
import tkinter.messagebox

class mail_user_gui:
    def __init__(self):
        
        win = tkinter.Tk()
        win.geometry("1400x600")
        win.title("Booking Mail System")
            
        #booking time  #row0  
        bk_title = ['Year','Month','Day','Hour','Minutes']
        for x in bk_title:
            bk_label = Label(win, text=x)
            bk_label.grid(column=bk_title.index(x)+1,row=0)
        
        #row1
        bk_time_label = Label(win, text="Booking Date and Time")
        bk_time_label.grid(column=0,row=1)
            
        bk_year_list = []
        for x in range(100):
            bk_year_list.append(x+datetime.date.today().year)
        bk_year = ttk.Combobox(win, values=bk_year_list)
        bk_year.grid(column=1,row=1)
        bk_year.current(0)
               
        bk_month_list = []
        for x in range(12):
            if x < 9:
                bk_month_list.append('0'+str(x+1))
            else:
                bk_month_list.append(x+1)
        bk_month = ttk.Combobox(win, values=bk_month_list)
        bk_month.grid(column=2,row=1)
        bk_month.current(0)
    
        bk_day_list = []
        for x in range(31):
            if x < 9:
                bk_day_list.append('0'+str(x+1))
            else:
                bk_day_list.append(x+1)
        bk_day = ttk.Combobox(win, values=bk_day_list)
        bk_day.grid(column=3,row=1)   
        bk_day.current(0)
        #bk_day.bind("<<ComboboxSelected>>",callbackFunc)
        
        bk_hour_list = []
        for x in range(24):
            if x < 10:
                bk_hour_list.append('0'+str(x))
            else:
                bk_hour_list.append(x)
        bk_hour = ttk.Combobox(win, values=bk_hour_list)
        bk_hour.grid(column=4,row=1)
        bk_hour.current(0)
                       
        bk_min_list = []
        for x in range(60):
            if x < 10:
                bk_min_list.append('0'+str(x))
            else:    
                bk_min_list.append(x)
        bk_min = ttk.Combobox(win, values=bk_min_list)
        bk_min.grid(column=5,row=1)
        bk_min.current(0)
        
        #receivers       #row2
        #requester_label = Label(win, text="Requested By:")
        #requester_label.grid(column=0, row=2)
        #requester_entry = Entry(win, width=120)
        #requester_entry.grid(column=1, row=2, columnspan=5)
        
        #subject        #row3
        subject_label = Label(win, text="Subject: ").grid(column=0, row=3)
        subject_entry = Entry(win, width=120)
        subject_entry.grid(column=1, row=3, columnspan=5)
        
        #Location     #row4
        location_label = Label(win, text="Location: ").grid(column=0, row=4)
        location_list = config().location.split(",")
        location = ttk.Combobox(win, values=location_list)
        location.grid(column=1,row=4)
        location.current(0)
        
        #Mail Body #row5
        body_label = Label(win, text="Body: ").grid(column=0, row=5)
        body_entry = Text(win, width=120, height=30)
        body_entry.grid(column=1, row=5, columnspan=5, rowspan=3)
        
        self.time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+'-'+bk_min.get()
        
        def onclick():
            #store the data
            time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+'-'+bk_min.get()
            mail_user_gui.time_str = time_str
            #mail_user_gui.requester = requester_entry.get()
            mail_user_gui.subject = subject_entry.get()
            mail_user_gui.location = location.get()
            mail_user_gui.body = body_entry.get('1.0',END)
            
            #save as text file for reminder function
            #t = str(time.strftime("%Y-%m-%d %H-%M", time_str)
            counter=1
            the_file = (config().path+time_str+'_record_%d_') %counter
            while os.path.isfile(the_file):
                the_file = (config().path+time_str+'_record_%d_') %counter
                counter=counter+1
            f = open(the_file, 'w')
            f.write(time_str)
            f.write('\n')
            f.write("Requested By: ") 
            f.write(config().sender)
            f.write('\n')
            f.write("Subject: %s" %mail_user_gui.subject)
            f.write('\n')
            f.write("Location: %s" %mail_user_gui.location)
            f.write('\n')
            f.write("Mail Body: \n%s" %mail_user_gui.body)
            f.close()
            print('new record created.')
            tkinter.messagebox.showinfo("Warning", "Mail Sent")
            win.destroy()


        #confirm all info  #row7    
        confirm_button = Button(win, text="Confirm", command=onclick).grid(column=7,row=7)
        
        win.mainloop()

#def callbackFunc(event):
    #print("New Element Selected")

class reminder_gui:
    def __init__(self):
        win = tkinter.Tk()
        win.geometry("560x300")
        win.title("Booking Record")

        datetime_label = Label(win, text="Record").grid(column=0,row=0)
        
        datetime_listbox = Listbox(win, width=40)
        datetime_listbox.grid(column=0,row=2)
        
        yscroll = tkinter.Scrollbar(command=datetime_listbox.yview, orient=tkinter.VERTICAL)
        yscroll.grid(column=1, row=2, sticky='ENS')
        datetime_listbox.configure(yscrollcommand=yscroll.set)
        
        i=-1 #for inserting elements
        datetime_list = []
        for file in os.listdir(config().path):
            if fnmatch.fnmatch(file, '*record*'):
                    datetime_list.insert(i+1,file) #list elements
        for time in datetime_list:
            datetime_listbox.insert(0,time)
            
        
                     
        def onclick():
            file = config().path+datetime_listbox.get(datetime_listbox.curselection())
            f = open(file,"r")
            record_list = []
            record_lines = f.readlines()
            for line in record_lines:
                record_list.append(line)
            record = '\n'.join(record_list)
            tkinter.messagebox.showinfo("Record",record)
        
        
        confirm_button = Button(win, text="Confirm", command=onclick).grid(column=0, row=3)
        
        explanation_label = Label(win, text="Please select a record and click ''Confirm'' to check the booking record's information.",
                                  font=20, justify=CENTER)
        explanation_label.grid(row=4)

        win.mainloop()
    
if __name__ == '__main__':
   reminder_gui()
