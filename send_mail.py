
#! python3
# _*_ coding:utf-8 _*_
 
"""IBM notes send email
"""
 
# notes 9.0
from win32com.client import DispatchEx
from win32com.client import makepy
makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
#makepy.GenerateFromTypeLibSpec('Lotus Notes Automation Classes') 
# from win32com.client import DispatchEx   # notes 8.5
 
class NotesMail(object):
    def __init__(self, server, file):
        print('init mail client')
        self.session = DispatchEx('Notes.NotesSession')
        # self.server = self.session.GetEnvironmentString("MailServer", True)
        self.server = 'MACEDD25N/SERVERS/CEDD/HKSARG'
        self.file = 'C:\\Users\\Desktop\\ppcslo.nsf'
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
    # receivers = ['User1/szABCtech', 'User2/szABCtech']
    receivers = ['ppc_slo@cedd.gov.hk']
    mail = NotesMail('MACEDD25N/SERVERS/CEDD/HKSARG', 'mail\\ppcslo.nsf')
    mail.send_mail(receivers, 'test sender', 'This is a test mail body ')
 
if __name__ == '__main__':
    main()

