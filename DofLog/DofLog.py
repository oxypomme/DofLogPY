# -*- coding: utf-8 -*-

from threading import Thread, Event
from time import sleep
from os import environ, remove, getcwd
from os.path import exists, join
from PIL import Image, ImageGrab
from subprocess import Popen, DEVNULL
from win10toast import ToastNotifier

from configparser import *
from pyautogui import *

import win32gui

PAUSE = 0.25
FAILSAFE = True

df_windowTitle = "DofLog"
df_version = "0.1.1" # Version.SousVersion.Build | Version = 0 : Beta/Alpha | SousVersion = 0 : Alpha

config = ConfigParser()

class AccountNotFoundError(Exception):
    pass

class logDof(Thread):
    accNames = []

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        nbAcc = len(self.accNames)
        usernames = []
        passwords = []
        dofIDs = []
        toastMessage = ""

        try:
            for i in range(nbAcc):
                usernames.append(self.__getUsername(self.accNames[i]))
                passwords.append(self.__getPassword(self.accNames[i]))
        except AccountNotFoundError:
            toastMessage = "Pas de comptes enregistrés !"
        else:
            self.__startAL()
            if not (__isLogable == (134,182,68) or __isLogable == (133,181,68)):
                self.__logAL(usernames[0],passwords[0])
            dofIDs.append(self.__startDof())
            while not self.__isLogable(1200,835) == (214,246,0):
                if self.__isLogable(955,585) == (214,246,0):
                    self.__logDof(dofIDs[0],usernames[0],passwords[0])
                else:
                    sleep(1)
            if nbAcc>1:
                for i in range(1,nbAcc):
                    dofIDs.append(self.__startDof())
                for i in range(1,nbAcc):
                    self.__logDof(dofIDs[i],usernames[i],passwords[i])
            if config["General"]["stay_logged"] == "False":
                self.__unlogAL(dofIDs[0])

            toastMessage = "Connexion du compte {0} réussie !".format(upper_str(self.accNames[0]))
            if nbAcc>1:
                accountsNames = upper_str(self.accNames[0])
                for i in range(1, nbAcc):
                    accountsNames+=", "+upper_str(self.accNames[i])
                toastMessage = "Connexion des comptes {0} réussie !".format(accountsNames)
            toaster_thread.message = toastMessage
            toaster_thread.isShowing = True
            self.__resetVars()

    def __getUsername(self, name):
        if "Accounts" in config:
                user = config["Accounts"][name.lower()]
                user_logs = user.split('/')
                return bytearray.fromhex(user_logs[0]).decode()
        raise AccountNotFoundError
    def __getPassword(self, name):
        if "Accounts" in config:
            try:
                user = config["Accounts"][name.lower()]
                user_logs = user.split('/')
                return bytearray.fromhex(user_logs[1]).decode()
            except:
                pass
        raise AccountNotFoundError

    def __isLogable(self, startX, startY):
        color = ImageGrab.grab((startX, startY, startX+1, startY+1)).load()[0,0]
        return color

    def __special_char(self, passwd, key):
        typewrite(passwd)
        press('capslock')
        press(key)
        press('capslock')
        return ""
    def __typepassword(self, password):
        passwd = ""
        for c in password:
            if c == 'é':
                passwd = self.__special_char(passwd,'2')
            elif c == 'è':
                passwd = self.__special_char(passwd,'7')
            elif c == '_':
                passwd = self.__special_char(passwd,'8')
            elif c == 'ç':
                passwd = self.__special_char(passwd,'9')
            elif c == 'à':
                passwd = self.__special_char(passwd,'0')
            elif c == 'ù':
                passwd = self.__special_char(passwd,'%')
            elif c == ':':
                passwd = self.__special_char(passwd,'/')
            elif c == '!':
                passwd = self.__special_char(passwd,'!')
            elif c == '§':
                typewrite(passwd)
                press('!')
                passwd = ""
            else:
                passwd+=c
        typewrite(passwd)

    def __windowEnumerationHandler(self, hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    def __focusOnWindow(self, title=None, id=None):
        if title!=None:
            results = []
            top_windows = []
            win32gui.EnumWindows(self.__windowEnumerationHandler, top_windows)
            for i in top_windows:
                if title in i[1]:
                    win32gui.ShowWindow(i[0],5)
                    win32gui.SetForegroundWindow(i[0])
                    return True
            return False
        elif id!=None:
            win32gui.ShowWindow(id,5)
            win32gui.SetForegroundWindow(id)

    def __startAL(self):
        if self.__focusOnWindow(title="Ankama Launcher"):
                return
        Popen(config["General"]["al_path"], stdout=DEVNULL)
        #TODO 01 - PRIORITE ABSOLUE : Si AL est pas au bon endroit ?
    def __logAL(self, username, password):
        while not self.__isLogable(560,515)==(130,141,148):
            sleep(1)
        moveTo(620, 340)
        click()
        hotkey('ctrl', 'a')
        press('backspace')
        typewrite(username)

        press('tab')
        hotkey('ctrl', 'a')
        press('backspace')
        self.__typepassword(password)

        while not self.__isLogable(560,515)==(254,252,250):
            sleep(1)
        moveTo(560, 515)
        click()

    def __startDof(self):
        self.__focusOnWindow(title="Ankama Launcher")
        moveTo(395, 270)
        click()
        while True:
            isLog = self.__isLogable(585,505)
            if isLog == (134,182,68) or isLog == (133,181,68):
                break
            sleep(1)
        moveTo(585, 505)
        click()
        while not win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Dofus":
            sleep(1)
        return win32gui.GetForegroundWindow()
    def __logDof(self, windowID, username, password):
        self.__focusOnWindow(id=windowID)
        while not self.__isLogable(955,585)==(214,246,0):
            sleep(1)
        moveTo(945, 350)
        click()
        hotkey('ctrl', 'a')
        press('backspace')
        typewrite(username)

        press('tab')
        hotkey('ctrl', 'a')
        press('backspace')
        self.__typepassword(password)

        press('enter')
    def __unlogAL(self, dofWinID):
        self.__focusOnWindow(title="Ankama Launcher")
        moveTo(1535, 205)
        click()
        moveTo(1535, 325)
        click()
        self.__focusOnWindow(id=dofWinID)

    def __resetVars(self):
        for i in range(len(self.accNames)):
            del self.accNames[0]

class saveLogs(Thread):
    name = ""
    raw_username = ""
    raw_password = ""

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        h_username = self.raw_username.encode('utf-8').hex()
        h_password = self.raw_password.encode('utf-8').hex()
        try:
            config.set("Accounts",self.name,"{0}/{1}".format(h_username,h_password))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except NoSectionError:
            config.add_section("Accounts")
            self.run()
        except FileNotFoundError:
            setup_config()
        toaster_thread.message = upper_str(self.name)+" enregistré !"
        toaster_thread.isShowing = True

class deleteLogs(Thread):
    name=""
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            config.remove_option("Accounts", self.name)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except NoSectionError:
            config.add_section("Accounts")
            self.run()
        except NoOptionError:
            pass
        except FileNotFoundError:
            setup_config()
        toaster_thread.message = upper_str(self.name)+" supprimé !"
        toaster_thread.isShowing = True

class toasterWin10(Thread):
    message = ""
    isShowing = False
    isRunning = True

    def __init__(self):
        Thread.__init__(self)
        self.__toaster = ToastNotifier()
   
    def run(self):
        while self.isRunning:
            if self.isShowing:
                old_msg = self.message
                self.__toaster.show_toast(df_windowTitle, self.message, "icon.ico", 3)
                if old_msg == self.message:
                    self.message = ""
                    self.isShowing = False
            else:
                sleep(0.5)

def setup_config():
    if exists('config.ini'):
        config.read("config.ini")
    else:
        config.add_section("General")
        config.set("General","al_path","C:\\Users\\"+environ['USERNAME']+"\\AppData\\Local\\Programs\\zaap\\Ankama Launcher.exe")
        config.set("General","stay_logged",str(False))
        config.set("General","upper_accounts",str(True))

        config.add_section("Accounts")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def upper_str(str):
    string = list(str)
    if config["General"]["upper_accounts"] == "True":
        string[0] = string[0].upper()
    return "".join(string)

setup_config()

toaster_thread = toasterWin10()
toaster_thread.start()