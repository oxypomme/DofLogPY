# -*- coding: utf-8 -*-
from threading import Thread, Event
from time import sleep, time
from os import environ, remove, getcwd, rename, mkdir
from os.path import exists, join
from PIL import Image, ImageGrab
from subprocess import Popen, DEVNULL
from win10toast import ToastNotifier
from pypresence import Presence, InvalidID, InvalidPipe

from configparser import *
from pyautogui import *

import win32gui

PAUSE = 0.25 # Pause entre chaque action
FAILSAFE = True # Si la souris est bougé vers le coin en haut à gauche de l'écran le programme
                # s'arrête
df_windowTitle = "DofLog"
df_version = "1.0.0"

config = ConfigParser() # Fichier config
class AccountNotFoundError(Exception):
    """
        Si un compte demandé n'est pas trouvé
    """
    pass

class logDof(Thread):
    accNames = [] # Variable modifiée pour savoir quels comptes connecter

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        nbAcc = len(self.accNames)
        usernames = []
        passwords = []
        dofIDs = [] # Liste des processid des fenêtres Dofus
        toastMessage = "" # Message envoyé par la notification Win10

        self.__retro_mode = False
        if config["General"]["retro_mode"] == "True":
            self.__retro_mode = True

        try:
            for i in range(nbAcc):
                usernames.append(self.__getUsername(self.accNames[i]))
                passwords.append(self.__getPassword(self.accNames[i]))
        except AccountNotFoundError:
            toastMessage = "Pas de comptes enregistrés !"
        else:
            self.__startAL()
            isLog = self.__isLogable(650,525) # Vérifie si le programme peut se connecter à AL
            if not (isLog == (134,182,68) or isLog == (133,181,68)):
                self.__logAL(usernames[0],passwords[0])
            dofIDs.append(self.__startDof())
            if not self.__retro_mode:
                while not self.__isLogable(1200,835) == (214,246,0):
                    # Vérifie si le compte est bien connecté
                    if self.__isLogable(955,585) == (214,246,0):
                        # Vérifie si le programme peut lancer Dofus
                        self.__logDof(dofIDs[0],usernames[0],passwords[0])
                    else:
                        sleep(1)
            else:
                # Lance Dofus Retro
                self.__logDof(dofIDs[0],usernames[0],passwords[0])
            if nbAcc > 1:
                for i in range(1,nbAcc):
                    dofIDs.append(self.__startDof())
                for i in range(1,nbAcc):
                    self.__logDof(dofIDs[i],usernames[i],passwords[i])
            if config["General"]["stay_logged"] == "False":
                self.__unlogAL(dofIDs[0])

            toastMessage = "Connexion du compte {0} réussie !".format(upper_str(self.accNames[0]))
            if nbAcc > 1:
                accountsNames = upper_str(self.accNames[0])
                for i in range(1, nbAcc):
                    accountsNames+=", " + upper_str(self.accNames[i])
                toastMessage = "Connexion des comptes {0} réussie !".format(accountsNames)
            toaster_thread.message = toastMessage
            toaster_thread.isShowing = True
            self.__resetVars()

    ### RECUPERATION DU COMPTE ###
    def __getUsername(self, name):
        """
           Récupère le nom d'utilisateur pour le compte demandé
        """
        if "Accounts" in config:
                user = config["Accounts"][name.lower()]
                user_logs = user.split('/')
                return bytearray.fromhex(user_logs[0]).decode()
        raise AccountNotFoundError
    def __getPassword(self, name):
        """
            Récupère le mot de passe pour le compte demandé
        """
        if "Accounts" in config:
            try:
                user = config["Accounts"][name.lower()]
                user_logs = user.split('/')
                return bytearray.fromhex(user_logs[1]).decode()
            except:
                pass
        raise AccountNotFoundError

    ### VERFICATION DE L'ETAT DE LA FENETERE ###
    def __isLogable(self, startX, startY):
        """
            Retourne la couleur du pixel indiqué
        """
        color = ImageGrab.grab((startX, startY, startX + 1, startY + 1)).load()[0,0]
        #print("{0}:{1} | {2}".format(startX, startY, color)) # debug purpose
        return color

    ### ECRITURE DU MOT DE PASSE ###
    def __special_char(self, passwd, key):
        """
            Écrit les précédentes lettres du mot de passe avant d'écrire le caractère spécial
            NON SUPPORTÉ : #
        """
        typewrite(passwd)
        press('capslock')
        press(key)
        press('capslock')
        return "" # Sert à reset la suite de lettres alphanumériques du mot de passe
    def __typepassword(self, password):
        """
            Écrit le mot de passe en prenant en compte les caractères spéciaux
        """
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

    ### GESTION DES FENÊTRES ###
    def __focusOnWindow(self, title=None, id=None):
        """
            Met au premier plan la fenêtre avec le nom/processid correspondant
        """
        if title != None:
            results = []
            top_windows = []
            win32gui.EnumWindows(windowEnumerationHandler, top_windows)
            for i in top_windows:
                if title in i[1]:
                    win32gui.ShowWindow(i[0],5)
                    win32gui.SetForegroundWindow(i[0])
                    return True
            return False
        elif id != None:
            win32gui.ShowWindow(id,5)
            win32gui.SetForegroundWindow(id)

    ### DEMARRAGE DE L'ANKAMA LAUNCHER ###
    def __startAL(self):
        """
            Met l'Ankama Launcher si ce dernier est lancé, sinon le lance
        """
        if self.__focusOnWindow(title="Ankama Launcher"):
                return
        Popen(config["General"]["al_path"], stdout=DEVNULL)
    def __logAL(self, username, password):
        """
            Se connecte à L'Ankama Launcher avec le premier compte
        """
        while not self.__isLogable(650,525) == (24,44,58):
            sleep(1)
        moveTo(620, 340) # Position du champ "Nom de compte" de l'AL
        click()
        hotkey('ctrl', 'a')
        press('backspace')
        typewrite(username)

        press('tab')
        hotkey('ctrl', 'a')
        press('backspace')
        self.__typepassword(password)

        while not self.__isLogable(650,525) == (255,168,44):
            # Tant que le programme ne peut se connecter
            sleep(1)
        moveTo(650,525) # Se connecte
        click()

    ### DEMARRAGE DE DOFUS ###
    def __startDof(self):
        """
            Lance Dofus et retourne son processid
        """
        self.__focusOnWindow(title="Ankama Launcher")
        while True:
            if not self.__retro_mode:
                moveTo(395, 65) # Clique sur l'onglet Dofus
            else:
                moveTo(395,325) # Clique sur l'onglet Dofus Retro
            sleep(0.5)
            click()
            # Vérifie si le programme peut lancer Dofus
            if self.__isLogable(1380,742) == (255,255,255):
                break
            sleep(1)
        moveTo(1380,742) # Lance Dofus
        click()
        while not "Dofus" in win32gui.GetWindowText(win32gui.GetForegroundWindow()):
            # Tant que dofus n'est pas au premier plan
            sleep(1)
        return win32gui.GetForegroundWindow()
    def __logDof(self, windowID, username, password):
        """
            Se connecte à Dofus (nécessite l'entrée d'un processid)
        """
        self.__focusOnWindow(id=windowID)
        if not self.__retro_mode:
            while not self.__isLogable(955,585) == (214,246,0):
                # Tant que le programme ne peut se connecter à Dofus
                sleep(1)
            moveTo(945, 350) # Position du champ "Nom de compte" de Dofus
        else:
             while not self.__isLogable(750,580) == (255,153,0):
                # Tant que le programme ne peut se connecter à Dofus Retro
                sleep(1)
             moveTo(790,465) # Position du champ "Nom de compte" de Dofus Retro
        click()
        hotkey('ctrl', 'a')
        press('backspace')
        typewrite(username)

        press('tab')
        hotkey('ctrl', 'a')
        press('backspace')
        self.__typepassword(password)

        press('enter') # Se connecte
    def __unlogAL(self, dofWinID):
        """
            Se déconnecte de AL
        """
        self.__focusOnWindow(title="Ankama Launcher")
        moveTo(1535, 205) # Postition de la gestion de compte sur AL
        click()
        while self.__isLogable(1380,530) == (255,255,255):
            sleep(1)
        moveTo(1380, 530) # Postition du bouton deconnexion sur AL
        click()
        self.__focusOnWindow(id=dofWinID)

    def __resetVars(self):
        for i in range(len(self.accNames)):
            del self.accNames[0]

class saveLogs(Thread):
    """
        Thread s'occupant de la sauvegarde des comptes
    """
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
        toaster_thread.message = upper_str(self.name) + " enregistré !"
        toaster_thread.isShowing = True

class deleteLogs(Thread):
    """
        Thread s'occupant de la suppression des comptes
    """
    name = ""
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
        toaster_thread.message = upper_str(self.name) + " supprimé !"
        toaster_thread.isShowing = True

class toasterWin10(Thread):
    """
        Thread s'occupant des notifications Windows 10
    """
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
                self.__toaster.show_toast(df_windowTitle, self.message, "res/icon.ico", 3)
                if old_msg == self.message:
                    self.message = ""
                    self.isShowing = False
            else:
                sleep(0.5)

class DiscordRPC(Thread):
    """
        Thread dédié au Discord Rich Presence
    """

    RPC = ""
    DRPCisEnabled = False
    isStopped = False
    startTime = int(time.time())
    timeBuffer = 5
    
    def run(self):
        try:
            self.RPC = Presence(int(bytearray.fromhex('363233383936373835363035333631363634').decode()))
            self.RPC.connect()
        except (InvalidPipe):
            self.DRPCisEnabled = False
        else:
            self.DRPCisEnabled = True
            while(not self.isStopped): 
                if True:
                    nameList = "Se connecte..."
                    if(self.timeBuffer == 5):
                        nbDof = 0
                        namePerso = self.__countWindows()
                        sizePerso = len(namePerso)
                        if sizePerso >= 1:
                            for i in range(sizePerso):
                                if not "Dofus" in namePerso[i][0]:
                                    nameList+=namePerso[i][0]
                                    nbDof+=1
                                    if not i == sizePerso - 1:
                                        nameList+=", "
                                else:
                                    nameList = "Se connecte..."
                        self.timeBuffer = 0
                    else:
                        self.timeBuffer+=1

                    modifier = ""
                    if config["General"]["retro_mode"] == "True":
                        modifier = "retro"

                    message = "Joue avec 0 comptes :"
                    if nbDof > 1 or nbDof == 0:
                        message = "Joue avec {0} comptes {1} :".format(nbDof, modifier)
                    else:
                        message = "Joue avec 1 compte {0} :".format(modifier)

                    self.RPC.update(details=message, \
                                    large_image="header", \
                                    small_image="dofuslogo", \
                                    small_text="Dofus", \
                                    state=nameList, \
                                    start=self.startTime)
                else:
                    # En cas de déconnexion
                    self.run()
                    self.DRPCisEnabled = False
                sleep(1)

    def __countWindows(self):
        namePerso = []
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if "Dofus" in i[1]:
                namePerso.append(i[1].split(' - '))
        return namePerso

    def stop(self):
        "Arrête le thread"
        if(self.DRPCisEnabled):
            self.RPC.close()
        self.isStopped = True

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def setup_config():
    """
        Créer un fichier config si inexistant
    """
    if exists('config.ini'):
        config.read("config.ini")
    else:
        config.add_section("General")
        config.set("General","al_path","C:\\Users\\" + environ['USERNAME'] + "\\AppData\\Local\\Programs\\zaap\\Ankama Launcher.exe")
        config.set("General","stay_logged",str(False))
        config.set("General","upper_accounts",str(True))
        config.set("General","retro_mode",str(False))

        config.add_section("Accounts")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    #Bouge les fichiers au bon endroit
    if not exists("res"):
        mkdir("res")
        
    if not exists("res/d2"):
        mkdir("res/d2")
    if not exists("res/dr"):
        mkdir("res/dr")

    ## DOFUS 2 ##
    if not exists("res/d2/bg.jpg"):
        rename("bg2.jpg", "res/d2/bg.jpg")
    elif exists("bg2.jpg"):
        remove("bg2.jpg")
        
    if not exists("res/d2/checkbox_c.jpg"):
        rename("checkbox_c2.jpg", "res/d2/checkbox_c.jpg")
    elif exists("checkbox_c2.jpg"):
        remove("checkbox_c2.jpg")
        
    if not exists("res/d2/checkbox_uc.jpg"):
        rename("checkbox_uc2.jpg", "res/d2/checkbox_uc.jpg")
    elif exists("checkbox_uc2.jpg"):
        remove("checkbox_uc2.jpg")

    ## DOFUS RETRO ##
    if not exists("res/dr/bg.jpg"):
        rename("bgr.jpg", "res/dr/bg.jpg")
    elif exists("bgr.jpg"):
        remove("bgr.jpg")
        
    if not exists("res/dr/checkbox_c.jpg"):
        rename("checkbox_cr.jpg", "res/dr/checkbox_c.jpg")
    elif exists("checkbox_cr.jpg"):
        remove("checkbox_cr.jpg")
        
    if not exists("res/dr/checkbox_uc.jpg"):
        rename("checkbox_ucr.jpg", "res/dr/checkbox_uc.jpg")
    elif exists("checkbox_ucr.jpg"):
        remove("checkbox_ucr.jpg")

    ## COMMON ##
    if not exists("res/add.png"):
        rename("add.png", "res/add.png")
    elif exists("add.png"):
        remove("add.png")

    if not exists("res/down.png"):
        rename("down.png", "res/down.png")
    elif exists("down.png"):
        remove("down.png")

    if not exists("res/login.png"):
        rename("login.png", "res/login.png")
    elif exists("login.png"):
        remove("login.png")

    if not exists("res/rem.png"):
        rename("rem.png", "res/rem.png")
    elif exists("rem.png"):
        remove("rem.png")

    if not exists("res/up.png"):
        rename("up.png", "res/up.png")
    elif exists("up.png"):
        remove("up.png")
        
    if not exists("res/settings.png"):
        rename("settings.png", "res/settings.png")
    elif exists("settings.png"):
        remove("settings.png")

    if not exists("res/icon.ico"):
        rename("icon.ico", "res/icon.ico")
    elif exists("icon.ico"):
        remove("icon.ico")

    if not exists("res/organiser.ico"):
        rename("organiser.ico", "res/organiser.ico")
    elif exists("organiser.ico"):
        remove("organiser.ico")


def upper_str(str):
    """
        Renvoie le nom de compte avec une majuscule au début
    """
    string = list(str)
    if config["General"]["upper_accounts"] == "True":
        string[0] = string[0].upper()
    return "".join(string)

setup_config()

toaster_thread = toasterWin10()
toaster_thread.start()

discord_thread = DiscordRPC()
discord_thread.start()

