# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 14:22:15 2019

@author: slos1
"""

import tkinter
import tkinter.ttk
from configuration import *
import os

import datetime
def main():
    win = tkinter.Tk()
    win.geometry("1400x600")
    win.title("Booking Mail System")
        
    #booking time  #row0  
    bk_title = ['Year','Month','Day','Hour','Minutes']
    for x in bk_title:
        bk_label = tkinter.Label(win, text=x)
        bk_label.grid(column=bk_title.index(x)+1,row=0)
    
    #row1
    bk_time_label = tkinter.Label(win, text="Booking Date and Time")
    bk_time_label.grid(column=0,row=1)
        
    bk_year_list = []
    for x in range(100):
        bk_year_list.append(x+datetime.date.today().year)
    bk_year = tkinter.ttk.Combobox(win, values=bk_year_list)
    bk_year.grid(column=1,row=1)
    bk_year.current(0)
           
    bk_month_list = []
    for x in range(12):
        if x < 9:
            bk_month_list.append('0'+str(x+1))
        else:
            bk_month_list.append(x+1)
    bk_month = tkinter.ttk.Combobox(win, values=bk_month_list)
    bk_month.grid(column=2,row=1)
    bk_month.current(0)

    bk_day_list = []
    for x in range(31):
        if x < 9:
            bk_day_list.append('0'+str(x+1))
        else:
            bk_day_list.append(x+1)
    bk_day = tkinter.ttk.Combobox(win, values=bk_day_list)
    bk_day.grid(column=3,row=1)   
    bk_day.current(0)
    #bk_day.bind("<<ComboboxSelected>>",callbackFunc)
    
    bk_hour_list = []
    for x in range(24):
        if x < 10:
            bk_hour_list.append('0'+str(x))
        else:
            bk_hour_list.append(x)
    bk_hour = tkinter.ttk.Combobox(win, values=bk_hour_list)
    bk_hour.grid(column=4,row=1)
    bk_hour.current(0)
                   
    bk_min_list = []
    for x in range(60):
        if x < 10:
            bk_min_list.append('0'+str(x))
        else:    
            bk_min_list.append(x)
    bk_min = tkinter.ttk.Combobox(win, values=bk_min_list)
    bk_min.grid(column=5,row=1)
    bk_min.current(0)
    
    #receivers       #row2
    #requester_label = Label(win, text="Requested By:")
    #requester_label.grid(column=0, row=2)
    #requester_entry = Entry(win, width=120)
    #requester_entry.grid(column=1, row=2, columnspan=5)
    
    #subject        #row3
    subject_label = tkinter.Label(win, text="Subject: ").grid(column=0, row=3)
    subject_entry = tkinter.Entry(win, width=120)
    subject_entry.grid(column=1, row=3, columnspan=5)
    
    #Location     #row4
    location_label = tkinter.Label(win, text="Location: ").grid(column=0, row=4)
    location_list = config().location.split(",")
    location = tkinter.ttk.Combobox(win, values=location_list)
    location.grid(column=1,row=4)
    location.current(0)
    
    #Mail Body #row5
    body_label = tkinter.Label(win, text="Body: ").grid(column=0, row=5)
    body_entry = tkinter.Text(win, width=120, height=30)
    body_entry.grid(column=1, row=5, columnspan=5, rowspan=3)
    
    #self.time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+'-'+bk_min.get()
    
    def onclick():
        #store the data
        time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+'-'+bk_min.get()
        #mail_user_gui.requester = requester_entry.get()
        subject = subject_entry.get()
        locations = location.get()
        body = body_entry.get('1.0',tkinter.END)
        
        #save as text file for reminder function
        #t = str(time.strftime("%Y-%m-%d %H-%M", time_str)
        counter=1
        the_file = ('*'+time_str+'_record_%d_') %counter
        while os.path.isfile(the_file):
            the_file = ('*'+time_str+'_record_%d_') %counter
            counter=counter+1
        f = open(the_file, 'w')
        f.write(time_str)
        f.write('\n')
        f.write("Requested By: ") 
        f.write("sender")
        f.write('\n')
        f.write("Subject: %s" %subject)
        f.write('\n')
        f.write("Location: %s" %locations)
        f.write('\n')
        f.write("Mail Body: \n%s" %body)
        f.close()
        print('new record created.')
        tkinter.messagebox.showinfo("Warning", "Mail Sent")
        win.destroy()


    #confirm all info  #row7    
    confirm_button = tkinter.Button(win, text="Confirm", command=onclick).grid(column=7,row=7)
    
    win.mainloop()
    
if __name__=='__main__':
    main()