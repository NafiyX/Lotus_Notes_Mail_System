# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:22:10 2019

@author: slos1
"""

import configparser
import os

class config:
    cwd = os.getcwd()
    config = configparser.ConfigParser()
    
    config.read(cwd+'\config.ini') #require full path
    
    
    timer = config.get('Reminder_Timer','time')
    interval = config.get('Reminder_Timer','interval')
    
    path = config.get('Paths','record_dir')
    receivers = config.get('Mail','receivers')
    server = config.get('Mail_Nsf','server')
    location = config.get('Locations','location')
    subject = config.get('Mail','subject')
    notebook = config.get('Equipment_Quantity','notebook')
    laser = config.get('Equipment_Quantity','laser')
    #projector = config.get('Equipment_Quantity','projector')
    expired_path = config.get('Paths','expired_path')
       
    laser_set = config.get('Equipment_Quantity','laser_set')
    notebook_set = config.get('Equipment_Quantity','notebook_set')
    
    date = config.get('Report_Timer','date')
    hour = config.get('Report_Timer','hour')
    minute =  config.get('Report_Timer','minute')
    
    

    def date_change(time):
        config.config.set('Report_Timer','date',str(time))
        with open(config.cwd+'\config.ini','w') as configfile:
            config.config.write(configfile)



if __name__=="__main__":
    print(config.date)
