# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:22:10 2019

@author: slos1
"""

import configparser
import os

class config:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
    
        sender = config.get('Mail_Sender','sender')
        path = config.get('Paths','record_dir')
        receivers = config.get('Mail_Receivers','receivers')
        nsf = config.get('Mail_Nsf','mail_nsf')
        timer = config.get('Reminder_Timer','timer')
        server = config.get('Mail_Server','server')
        location = config.get('Locations','location')
        
        self.path = path
        self.receivers = receivers
        self.nsf = nsf
        self.timer = int(timer)
        self.server = server
        self.location = location
        self.sender = sender

