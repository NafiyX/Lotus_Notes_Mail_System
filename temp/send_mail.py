
#! python3
# _*_ coding:utf-8 _*_
 
"""IBM notes send email
"""
 
# notes 9.0
from reminder_gui import Reminder_gui
import win32com.client
import win32com.client.makepy
import tkinter
import tkinter.ttk
import tkinter.messagebox
from configuration import config
import os
import sys
import datetime
win32com.client.makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
#makepy.GenerateFromTypeLibSpec('Lotus Notes Automation Classes') 
# from win32com.client import DispatchEx   # notes 8.5

def f_day(x):
    temp_dict = {
        ('01','03','05','07','08','10','12'): 31,
        ('04','06','09','11'): 30,
        ('02'): 28,
        ('02N'): 29
        }
    for k, v in temp_dict.items():
        if x in k: 
            return (x, v) 


class NotesMail(object):
    def __init__(self, server, file):
        print('init mail client')
        self.session = win32com.client.DispatchEx('Notes.NotesSession') 
        # self.server = self.session.GetEnvironmentString("MailServer", True)
        #self.server = 'MACEDD25N/SERVERS/CEDD/HKSARG'
        #self.file = 'C:\\Users\\Desktop\\ppcslo.nsf'
        self.db = self.session.GetDatabase(server, file)
        
        self.username = self.session.commonUserName

        if not self.db.IsOpen:
            print('open mail db')
            try:
                self.db.OPENMAIL
            except Exception:
                print( 'could not open database: {}'.format(self.db))
                pass
                
                
    def send_mail(self, receiver_list, subject, body=None):
        doc = self.db.CREATEDOCUMENT
        doc.sendto = receiver_list
        doc.Subject = subject
        if body:
            doc.Body = body
        doc.SEND(0, receiver_list)
        print('send success')

class mail_user_gui:
    
    def __init__(self):
        self.subject = ''
        
        win = tkinter.Tk()
        win.geometry("850x500") 
        win.title("Reservation System")
        def on_closing():
            if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
                win.destroy()
                sys.exit()
        win.protocol("WM_DELETE_WINDOW", on_closing)
        
            
        #booking time  #row0  
        bk_title = ['Year','Month','Day','Hour','Minutes']
        for x in bk_title:
            bk_label = tkinter.Label(win, text=x, font=('Arial bold',12))
            bk_label.grid(column=bk_title.index(x)+1,row=0)
        
        #row1
        bk_time_label = tkinter.Label(win, text="Setup Time:",font=('Arial bold',12))
        bk_time_label.grid(column=0,row=1,ipadx=20)
            
        bk_year_list = []
        for x in range(2):
            bk_year_list.append(x+datetime.date.today().year)
        bk_year = tkinter.ttk.Combobox(win, values=bk_year_list, font=('Arial bold',12), width=5, state="readonly")
        bk_year.grid(column=1,row=1)
        bk_year.current(0)
               
        bk_month_list = []
        for x in range(12):
            if x < 9:
                bk_month_list.append('0'+str(x+1))
            else:
                bk_month_list.append(x+1)
        bk_month = tkinter.ttk.Combobox(win, values=bk_month_list,font=('Arial bold',12), width=5, state="readonly")
        bk_month.grid(column=2,row=1)

        bk_day_list = []
        for x in range(31):
            if x < 9:
                bk_day_list.append('0'+str(x+1))
            else:
                bk_day_list.append(x+1)
        bk_day = tkinter.ttk.Combobox(win,font=('Arial bold',12), width=5,state="readonly")
        bk_day['values'] = bk_day_list
        bk_day.grid(column=3,row=1) 
        
        def callback(eventObject):
            bk_day.current(0)
            bk_day_list.clear()
            days = f_day(bk_month.get())   #print(days)  e.g.('01',31)
            if(int(bk_year.get())%4 == 0 and bk_month.get()=='02'):
                days = f_day(bk_month.get()+'N')
            if(days):
                for day in range(days[1]):
                    if day < 9:
                        bk_day_list.append('0'+str(day+1))
                    else:
                        bk_day_list.append(day+1)

            bk_day['values'] = bk_day_list
            self.time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+bk_min.get()
            subject_var.set(config.subject + self.time_str)
        bk_month.bind("<<ComboboxSelected>>",callback)        
        
        import time
        t = time.localtime()
        bk_month.current(t.tm_mon-1)
        bk_day.current(t.tm_mday-1)
        
        bk_hour_list = []
        for x in range(15):
            if x < 2:
                bk_hour_list.append('0'+str(x+8))
            else:
                bk_hour_list.append(x+8)
        bk_hour = tkinter.ttk.Combobox(win, values=bk_hour_list,font=('Arial bold',12), width=5, state="readonly")
        bk_hour.grid(column=4,row=1)
        bk_hour.current(0)
                       
        bk_min_list = []
        for x in range(4):
            if x < 1:
                bk_min_list.append('0'+str(x*15))
            else:    
                bk_min_list.append(x*15)
        bk_min = tkinter.ttk.Combobox(win, values=bk_min_list,font=('Arial bold',12), width=5, state="readonly")
        bk_min.grid(column=5,row=1)
        bk_min.current(0)
        
        def callback_date_in_subject(eventObject):
            self.time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+bk_min.get()
            subject_var.set(config.subject + self.time_str)
        bk_year.bind("<<ComboboxSelected>>",callback)
        bk_day.bind("<<ComboboxSelected>>",callback_date_in_subject)
        bk_hour.bind("<<ComboboxSelected>>",callback_date_in_subject)
        bk_min.bind("<<ComboboxSelected>>",callback_date_in_subject)

        
        #requester       #row2
        '''requester_label = tkinter.Label(win, text="Requested By :")
        requester_label.grid(column=0, row=2)
        requester_entry = tkinter.Entry(win, text="Please Enter Lotus Note Username", width=90)
        requester_entry.grid(column=1, row=2, columnspan=5, sticky="W", pady=10)'''
        
        #subject        #row3
        subject_label = tkinter.Label(win,font=('Arial bold',12), text="Subject: ").grid(column=0, row=3)
        subject_var = tkinter.StringVar()
        subject_entry = tkinter.Entry(win, width=70, font=('Arial bold',12),textvariable=subject_var)
        time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+bk_min.get()
        subject_var.set(config.subject + time_str)
        subject_entry.grid(column=1, row=3, columnspan=5, sticky="W", pady=10)
        
        
        #Location     #row4
        location_label = tkinter.Label(win, font=('Arial bold',12),text="Location: ").grid(column=0, row=4)
        location_list = config.location.split(",")
        location = tkinter.ttk.Combobox(win, values=location_list,font=('Arial bold',12), state="readonly")
        location.grid(column=1,row=4,columnspan=2, sticky="W", ipadx=30)
        location.current(0)
        
        #notebook     #row5
        notebook_label = tkinter.Label(win,font=('Arial bold',12), text="Notebook: ").grid(column=0, row=5)
        notebook = tkinter.Scale(win, font=('Arial bold',12),foreground="red",from_=0, to=config.notebook, orient=tkinter.HORIZONTAL)
        notebook.set(config.notebook_set)
        notebook.grid(column=1,row=5,columnspan=2, sticky="WN")


        #laser Pointer        #row6
        laser_label = tkinter.Label(win,font=('Arial bold',12), text="Laser Pointer: ").grid(column=0, row=6)
        laser = tkinter.Scale(win, font=('Arial bold',12),foreground="red", from_=0, to=config.laser, orient=tkinter.HORIZONTAL)
        laser.set(config.laser_set)
        laser.grid(column=1,row=6,columnspan=2, sticky="WN")       
        
        #projector     #row7
        '''projector_label = tkinter.Label(win, text="Projector: ").grid(column=0, row=7)
        projector = tkinter.Scale(win, from_=0, to=config.projector, orient=tkinter.HORIZONTAL)
        projector.grid(column=1,row=7,columnspan=2, sticky="WN")'''
        
        #Mail Body #row8
        body_label = tkinter.Label(win,font=('Arial bold',12), text="Remark: ").grid(column=0, row=7, sticky="N")
        body_entry = tkinter.Text(win, width=50, height=10, font=('Arial bold',12))
        body_entry.grid(column=1, row=7,columnspan=5,rowspan=2, sticky="NW")

        review_booking_button = tkinter.Button(win, text="Reservation\nReview",justify=tkinter.CENTER, font=('Arial bold',12),command=Reminder_gui).grid(column=5,row=7,sticky="NWE",ipady=5,pady=25)
        
        
        def onclick():
            #store the data
            self.time_str = bk_year.get()+'-'+bk_month.get()+'-'+bk_day.get()+'  '+bk_hour.get()+bk_min.get()
            #self.requester = requester_entry.get()
            self.subject = subject_entry.get()
            self.location = location.get()
            self.notebook = notebook.get()
            self.laser = laser.get()
            #self.projector = projector.get()
            self.body = body_entry.get('1.0',tkinter.END)
            if self.body == '\n':
                self.body = 'N/A'
            

            #save as text file for reminder function
            #t = str(time.strftime("%Y-%m-%d %H-%M", time_str)
            if not os.path.isdir(config.path):
                os.mkdir(config.path)
                
            mail = NotesMail(config.server,'mail\\.nsf')
            
            the_file = (config.path+self.time_str+'_%s_record') %self.location
            f = open(the_file, "w+")
            f.write(str(self.time_str))
            f.write('\n')
            f.write("Reserved By: ")
            f.write(mail.username)
            f.write('\n')
            f.write("%s" %self.subject)
            f.write('\n')
            f.write("Location: %s" %self.location)
            f.write('\n')
            f.write("Notebook: %s" %self.notebook)
            f.write('\n')
            f.write("Laser Pointer: %s" %self.laser)
            f.write('\n')
            #f.write("Projector: %s" %self.projector)
            #f.write('\n')
            f.write("Remark: \n%s" %self.body)
            f.close()
            print('new record created.')
            tkinter.messagebox.showinfo("Message", "Reservation Completed.")
            self.body = "Location: {}\nReserved By: {}\nNotebook: {}\nLaser Pointer: {}\nRemark: {}".format(self.location, mail.username, self.notebook , self.laser, self.body)
            
            
            #send mail function 
            receivers = config.receivers.split(",")
            mail.send_mail(receivers, self.subject, self.body)
            
                
        #confirm all info  #row7    
        confirm_button = tkinter.Button(win, text="Confirm", font=('Arial bold',12), command=onclick).grid(column=5,row=8,sticky="NWE",ipady=5,pady=25)
        
        win.wm_attributes("-topmost", 1)
        
        win.mainloop()

def main():   
    #receivers = ['User1/szABCtech', 'User2/szABCtech'] 
    win = mail_user_gui()

    
    
    

if __name__ == '__main__':
    main()

