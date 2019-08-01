
#! python3
# _*_ coding:utf-8 _*_
 
"""IBM notes send email
"""
 
# notes 9.0
from win32com.client import DispatchEx
from win32com.client import makepy
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from gui import *
from configuration import *
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
        
 

def main():
    mail = NotesMail(config().server, config().nsf) #(Mail Server, "mail\\User.nsf")
    win = mail_user_gui()
    #receivers = ['User1/szABCtech', 'User2/szABCtech']   
    receivers = config().receivers
    win.subject = win.subject + '[Booking Date:' + win.time_str + ']'
    win.body = 'Date: ' + win.time_str + '\n' + win.body
    mail.send_mail(receivers, win.subject, win.body) #send mail function  
    

if __name__ == '__main__':
    main()

