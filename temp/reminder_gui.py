# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 11:35:36 2019

@author: slos1
"""

import tkinter
from configuration import config
import fnmatch
import os
import time

class Reminder_gui:
    def __init__(self): 
        win = tkinter.Tk()
        win.title("Reservation Record")
        win.resizable(0,0)
        
        datetime_label = tkinter.Label(win, font=('Arial bold',12),text="Record").grid(column=0,row=0)
        
        datetime_listbox = tkinter.Listbox(win,font=('Arial bold',12), width=60)
        datetime_listbox.grid(column=0,row=2)
        
        yscroll = tkinter.Scrollbar(win, command=datetime_listbox.yview, orient=tkinter.VERTICAL)
        yscroll.grid(column=3, row=2, sticky='ENS')
        datetime_listbox.configure(yscrollcommand=yscroll.set)
        
        i=-1 #for inserting elements
        datetime_list = []
        for file in sorted(os.listdir(config.path)):
            if fnmatch.fnmatch(file, '*record*'):
                datetime_list.insert(i+1,file) #list elements
        for t in datetime_list:
            datetime_listbox.insert(0,t)
             
        def onclick():
            file = config.path+datetime_listbox.get(datetime_listbox.curselection())
            f = open(file,"r")
            record_list = []
            record_lines = f.readlines()
            for line in record_lines:
                record_list.append(line)
            record = '\n'.join(record_list)
            x = win.winfo_x()
            y = win.winfo_y()
            top = tkinter.Toplevel(win)
            top.geometry("+%d+%d"%(x+200,y+100))
            top.wm_attributes("-topmost", 1)
            top_button = tkinter.Button(top,font=('Arial bold',12),text=record,command=top.destroy).grid()
        
        def onclick_delete():
            msg = tkinter.messagebox.askyesno("Warning","Delete the Reservation?")
            if msg == tkinter.YES:
                file = config.path+datetime_listbox.get(datetime_listbox.curselection())
                os.remove(file)
                time.sleep(0.2)
                datetime_listbox.delete(datetime_listbox.curselection())
                tkinter.messagebox.showinfo(title="Success",message="Record Deleted!")

        check_button = tkinter.Button(win, font=('Arial bold',12),text="Check Details", command=onclick).grid(row=3,column=0,padx=30)
        delete_button = tkinter.Button(win,font=('Arial bold',12), text="Delete", command=onclick_delete).grid(row=4,column=0,padx=30)
        
        explanation_label = tkinter.Label(win,font=('Arial bold',12), text="Please select a record and click ''Check/Delete'' to check/delete the booking record's information.",
                                          justify=tkinter.CENTER)
        explanation_label.grid(row=5)
        
        win.wm_attributes("-topmost", 1)
        
        win.mainloop()

if __name__=="__main__":
    Reminder_gui()