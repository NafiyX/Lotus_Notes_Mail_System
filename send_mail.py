
#! python3
# _*_ coding:utf-8 _*_
 
"""IBM notes send email
"""
 
# notes 9.0
import time
from win32com.client import DispatchEx
from win32com.client import makepy
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
#makepy.GenerateFromTypeLibSpec('Lotus Notes Automation Classes') 
# from win32com.client import DispatchEx   # notes 8.5
 
class NotesMail(object):
    def __init__(self, server, file):
        print('init mail client')
        self.session = DispatchEx('Notes.NotesSession')
        # self.server = self.session.GetEnvironmentString("MailServer", True)
        #self.server = 'MACEDD25N/SERVERS/CEDD/HKSARG'
        #self.file = 'C:\\Users\\Desktop\\ppcslo.nsf'
        self.db = self.session.GetDatabase(server, file)
        if not self.db.IsOpen:
            print('open mail db')
            try:
                self.db.OPENMAIL
            except Exception as e:
                print(str(e))
                print( 'could not open database: {}'.format(self.db) )
                
    def send_mail(self, receiver_list, subject, body=None):
        doc = self.db.CREATEDOCUMENT
        doc.sendto = receiver_list
        doc.Subject = subject
        if body:
            doc.Body = body
        doc.SEND(0, receiver_list)
        print('send success')
        
    def mail_input(self):
        receivers = list(map(str, input("Enter receivers'' addresses:\n"
                        "For multiple mail addresses, Please use ',' to seperate the addresses\n").split(",")))
    
        subject= input('Please input the mail subject:\n')
    
        buffer = []
        print("Please input the mail body:\n"
          "To quit, Enter . in a new line")
        while True:
            line = input()
            if line == ".":
                break
            buffer.append(line+'\n')
        body = "".join(buffer)
    
        print("Send to:", receivers)
        print("Subject:", subject)
        print("Mail Body:", body)
        
        #write mail details in text file
        t = str(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
        the_file = 'C:\\Users\\slos1\\Desktop\\mail system(9 jul)\\record_'+t+'.txt'
        f = open(the_file, 'w+')
        f.write(t)
        f.write('\n')
        f.write("Receivers: ") 
        f.write(str(receivers))
        f.write('\n')
        f.write("Subject: %s" %subject)
        f.write('\n')
        f.write("Mail Body: %s" %body)
        f.close()
        print('new record created.')
        
        return receivers, subject, body
    


def mail_input_gui():
    win = tkinter.Tk()
    win.geometry("1200x600")
    win.title("Booking Mail System")
        
    #booking time  #row0
    bk_time_label = Label(win, text="Booking Date and Time")
    bk_time_label.grid(column=0,row=1)
        
    bk_title = ['Year','Month','Day','Hour','Minutes']
    for x in bk_title:
        bk_label = Label(win, text=x)
        bk_label.grid(column=bk_title.index(x)+1,row=0)
        
    bk_year_list = []
    year = tkinter.StringVar()
    for x in range(100):
        bk_year_list.append(x+2019)
    bk_year = ttk.Combobox(win, values=bk_year_list, textvariable=year)
    bk_year.grid(column=1,row=1)
    bk_year.current(0)
        
    bk_month_list = []
    for x in range(12):
        bk_month_list.append(x+1)
    bk_month = ttk.Combobox(win, values=bk_month_list)
    bk_month.grid(column=2,row=1)
    bk_month.current(0)
    bk_month.bind("<<ComboboxSelected>>",callbackFunc)

    bk_day_list = []
    for x in range(31):
        bk_day_list.append(x+1)
    bk_day = ttk.Combobox(win, values=bk_day_list)
    bk_day.grid(column=3,row=1)   
    bk_day.current(0)
    bk_day.bind("<<ComboboxSelected>>",callbackFunc)
    
    bk_hour_list = []
    for x in range(24):
        bk_hour_list.append(x+1)
    bk_hour = ttk.Combobox(win, values=bk_hour_list)
    bk_hour.grid(column=4,row=1)
    bk_hour.current(0)
        
        
    bk_min_list = []
    for x in range(60):
        bk_min_list.append(x+1)
    bk_min = ttk.Combobox(win, values=bk_min_list)
    bk_min.grid(column=5,row=1)
    bk_min.current(0)
    
    bk_confirm = Button(win, text="Confirm", command=onclick)
    bk_confirm.grid(column=6,row=1)

    show_time = Entry(win, text="Booking Time: ")
    show_time.grid(column=7, row=1)
        
    win.mainloop()    

def onclick():
    show_time.configure(text="Booking Time:" + year.get())
            
def callbackFunc(event):
    print("New Element Selected")

def main():
    # receivers = ['User1/szABCtech', 'User2/szABCtech']
    #receivers = ['ppc_slo@cedd.gov.hk']
    
    #mail = NotesMail('MACEDD25N/SERVERS/CEDD/HKSARG', 'mail\\ppcslo.nsf') 
    #(Mail Server, "mail\\User.nsf")
    mail_input_gui()
    #receivers, subject, body = mail.mail_input()
    
    #mail.send_mail(receivers, subject , body) #send mail function 

if __name__ == '__main__':
    main()

