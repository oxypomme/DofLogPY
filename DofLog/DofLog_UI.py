# -*- coding: utf-8 -*-

from DofLog import *

from wget import download
from zipfile import ZipFile

from sys import argv, exit
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class CheckList(QtWidgets.QListWidget):
    def __init__(self, strings, parent=None):
        super().__init__(parent)
        for text in strings:
            self.createItems(text)

    def createItems(self, text):
        item = QtWidgets.QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Qt.Unchecked)
        self.addItem(item)

class DofLogWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        toaster_thread.isRunning = False
        discord_thread.stop()
        event.accept()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.icon = QtGui.QIcon("res/icon.ico")
        MainWindow.setMaximumSize(QtCore.QSize(315, 185))

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(363, 182)
        MainWindow.setWindowIcon(self.icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.nameLE = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLE.setMinimumSize(QtCore.QSize(153, 0))
        self.nameLE.setMaximumSize(QtCore.QSize(153, 16777215))
        self.nameLE.setObjectName("nameLE")
        self.gridLayout.addWidget(self.nameLE, 0, 1, 1, 1)
        self.passwordLbl = QtWidgets.QLabel(self.centralwidget)
        self.passwordLbl.setMaximumSize(QtCore.QSize(97, 16777215))
        self.passwordLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.passwordLbl.setObjectName("passwordLbl")
        self.gridLayout.addWidget(self.passwordLbl, 2, 0, 1, 1)
        self.connectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.connectBtn.setObjectName("connectBtn")
        self.gridLayout.addWidget(self.connectBtn, 4, 2, 1, 1, QtCore.Qt.AlignTop)
        self.organiserBtn = QtWidgets.QPushButton(self.centralwidget)
        self.organiserBtn.setObjectName("organiserBtn")
        self.gridLayout.addWidget(self.organiserBtn, 2, 2, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignLeft)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.upBtn = QtWidgets.QPushButton(self.centralwidget)
        self.upBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.upBtn.setObjectName("upBtn")
        self.gridLayout_3.addWidget(self.upBtn, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.stayLogCB = QtWidgets.QCheckBox(self.centralwidget)
        self.stayLogCB.setObjectName("stayLogCB")
        self.gridLayout_3.addWidget(self.stayLogCB, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.downBtn = QtWidgets.QPushButton(self.centralwidget)
        self.downBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        self.downBtn.setObjectName("downBtn")
        self.gridLayout_3.addWidget(self.downBtn, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout.addLayout(self.gridLayout_3, 4, 0, 1, 1)
        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.addBtn.setObjectName("addBtn")
        self.gridLayout.addWidget(self.addBtn, 0, 2, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignLeft)
        self.passwordLE = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordLE.setMinimumSize(QtCore.QSize(153, 0))
        self.passwordLE.setMaximumSize(QtCore.QSize(153, 16777215))
        self.passwordLE.setFrame(True)
        self.passwordLE.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLE.setObjectName("passwordLE")
        self.gridLayout.addWidget(self.passwordLE, 2, 1, 1, 1)
        self.listWidget = CheckList([])
        self.listWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(153, 75))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 4, 1, 1, 1)
        self.usernameLbl = QtWidgets.QLabel(self.centralwidget)
        self.usernameLbl.setMaximumSize(QtCore.QSize(97, 16777215))
        self.usernameLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.usernameLbl.setObjectName("usernameLbl")
        self.gridLayout.addWidget(self.usernameLbl, 1, 0, 1, 1)
        self.nameLbl = QtWidgets.QLabel(self.centralwidget)
        self.nameLbl.setMaximumSize(QtCore.QSize(97, 16777215))
        self.nameLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLbl.setObjectName("nameLbl")
        self.gridLayout.addWidget(self.nameLbl, 0, 0, 1, 1)
        self.usernameLE = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameLE.setMinimumSize(QtCore.QSize(153, 0))
        self.usernameLE.setMaximumSize(QtCore.QSize(153, 16777215))
        self.usernameLE.setObjectName("usernameLE")
        self.gridLayout.addWidget(self.usernameLE, 1, 1, 1, 1)
        self.deleteBtn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.deleteBtn.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.deleteBtn.setObjectName("deleteBtn")
        self.gridLayout.addWidget(self.deleteBtn, 1, 2, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignLeft)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.reloadList()

        self.retranslateUi(MainWindow)
        self.addBtn.clicked.connect(self.addAction)
        self.deleteBtn.clicked.connect(self.remAction)
        self.connectBtn.clicked.connect(self.connectAction)
        self.stayLogCB.clicked.connect(self.staylogAction)
        self.upBtn.clicked.connect(self.upList)
        self.downBtn.clicked.connect(self.downList)
        self.organiserBtn.clicked.connect(self.organizerLink)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.nameLE, self.usernameLE)
        MainWindow.setTabOrder(self.usernameLE, self.passwordLE)
        MainWindow.setTabOrder(self.passwordLE, self.listWidget)
        MainWindow.setTabOrder(self.listWidget, self.addBtn)
        MainWindow.setTabOrder(self.addBtn, self.connectBtn)
        MainWindow.setTabOrder(self.connectBtn, self.organiserBtn)

        self.error_msg = QtWidgets.QMessageBox()
        self.error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_msg.setWindowTitle(df_windowTitle)
        self.error_msg.setWindowIcon(self.icon)

        self.setImages()

        retro_mode = False
        if config["General"]["stay_logged"] == "True":
            retro_mode = True

        MainWindow.setStyleSheet("""
                QPushButton{
                        background-color:transparent;
                    }

                QCheckBox::indicator:unchecked{
                        image: url('res/checkbox_uc.jpg')
                    }
                QCheckBox::indicator:checked{
                        image: url('res/checkbox_c.jpg')
                    }
                
                QListWidget::indicator:unchecked{
                        image: url('res/checkbox_uc.jpg')
                    }
                QListWidget::indicator:checked{
                        image: url('res/checkbox_c.jpg');
                    }

                QListWidget{
                        background-color: transparent;
                        border-style: outset;
                        border-color: transparent;
                    }

                QLineEdit{
                        background-color:transparent;
                        border-style: outset;
                        border-color:transparent;
                    }

                QLabel,QCheckBox,QLineEdit,QListWidget::item{
                        color:white;
                    }

                #MainWindow{
                        background-image:url('res/bg_2.jpg');
                    }
                """)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", df_windowTitle + " - v" + df_version))
        self.passwordLbl.setText(_translate("MainWindow", "Mot de passe :"))
        #self.organiserBtn.setText(_translate("MainWindow", "Organiser (nAiO)"))
        self.organiserBtn.setToolTip(_translate("MainWindow", "Lance l'Organiser (nAiO)"))
        #self.addBtn.setText(_translate("MainWindow", "Ajouter"))
        self.addBtn.setToolTip(_translate("MainWindow", "Ajoute le compte dans le fichier sauvegarde"))
        self.usernameLbl.setText(_translate("MainWindow", "Nom de compte :"))
        self.nameLbl.setText(_translate("MainWindow", "Nom du raccourci :"))
        self.connectBtn.setToolTip(_translate("MainWindow", "Connecte le/les compte(s) sélectionné(s)"))
        #self.connectBtn.setText(_translate("MainWindow", "Connecter !"))
        self.deleteBtn.setToolTip(_translate("MainWindow", "Supprime le compte sélectionné"))
        #self.deleteBtn.setText(_translate("MainWindow", "Supprimer"))
        self.stayLogCB.setToolTip(_translate("MainWindow", "Reste connecté à Ankama Launcher après la connexion à Dofus"))
        self.stayLogCB.setText(_translate("MainWindow", "Rester co"))
        #self.upBtn.setText(_translate("MainWindow", "▲"))
        self.upBtn.setToolTip(_translate("MainWindow", "Monte le compte sélectionné dans la liste"))
        #self.downBtn.setText(_translate("MainWindow", "▼"))
        self.downBtn.setToolTip(_translate("MainWindow", "Descend le compte sélectionné dans la liste"))

    def setImages(self):
        self.organiserBtn.setIcon(QtGui.QIcon('res/organiser.ico'))
        self.organiserBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.addBtn.setIcon(QtGui.QIcon('res/add.png'))
        self.addBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.deleteBtn.setIcon(QtGui.QIcon('res/rem.png'))
        self.deleteBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.connectBtn.setIcon(QtGui.QIcon('res/login.png'))
        self.connectBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.connectBtn.setIconSize(Qt.QSize(32,32))
        self.upBtn.setIcon(QtGui.QIcon('res/up.png'))
        self.upBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.downBtn.setIcon(QtGui.QIcon('res/down.png'))
        self.downBtn.setCursor(QtCore.Qt.PointingHandCursor)
        self.stayLogCB.setCursor(QtCore.Qt.PointingHandCursor)

    def addAction(self):
        savelogsThread = saveLogs()

        nameLE_txt = self.nameLE.text()
        usernameLE_txt = self.usernameLE.text()
        passwordLE_txt = self.passwordLE.text()

        if nameLE_txt == "" or (' ' in nameLE_txt) or \
           usernameLE_txt == "" or (' ' in usernameLE_txt) or \
           passwordLE_txt == ""or (' ' in passwordLE_txt):
            self.error_msg.setText("L'un des champs requis est vide ou contient un espace !")
            self.error_msg.exec_()
        else:
            savelogsThread.name = nameLE_txt
            savelogsThread.raw_username = usernameLE_txt
            savelogsThread.raw_password = passwordLE_txt

            savelogsThread.start()

            self.nameLE.clear()
            self.usernameLE.clear()
            self.passwordLE.clear()

        self.reloadList()
    def remAction(self):
        try:
            deletelogsThread = deleteLogs()
            deletelogsThread.name = self.listWidget.currentItem().text().lower()
            deletelogsThread.start()
            self.reloadList()
        except AttributeError:
            self.error_msg.setText("Aucun compte sélectionné !")
            self.error_msg.exec_()

    def organizerLink(self):
        if not exists(r'Modules/Organizer.exe'):
            toaster_thread.message = "Téléchargement d'Organizer en cours..."
            toaster_thread.isShowing = True
            download(r"http://update.naio.fr/v2/Organizer/1.4/Organizer.zip", getcwd())
            with ZipFile('Organizer.zip', 'r') as zipObj:
               zipObj.extractall()
            remove(join(getcwd(), 'Organizer.zip'))
            toaster_thread.message = "Téléchargement d'Organizer terminé !"
            toaster_thread.isShowing = True
        Popen(join(getcwd(), r'Modules/Organizer.exe'), stdout=DEVNULL)

    def connectAction(self):
        connexionThread = logDof()

        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).checkState():
                connexionThread.accNames.append(self.listWidget.item(i).text().lower())

        if len(connexionThread.accNames) > 0:
            if not exists(config["General"]["al_path"]):
                self.error_msg.setText("Le chemin vers Ankama Launcher est invalide !\nUne fenêtre vous demandant d'ouvrir le .exe d'Ankama Launcher va s'ouvrir...")
                self.error_msg.exec_()
                fileName = QtWidgets.QFileDialog.getOpenFileName(caption="Sélectionnez Ankama Launcher", directory="C:\\",filter="Exe Files (*.exe)")
                config.set("General","al_path",fileName[0].replace('/','\\'))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            connexionThread.start()
        else:
            self.error_msg.setText("Aucun compte sélectionné !")
            self.error_msg.exec_()

    def reloadList(self):
        self.listWidget.clear()
        for acc in config['Accounts']:
            self.listWidget.createItems(upper_str(acc))

        self.stayLogCB.setChecked(False)
        if config["General"]["stay_logged"] == "True":
            self.stayLogCB.setChecked(True)

    def staylogAction(self):
        config.set("General","stay_logged", str(self.stayLogCB.isChecked()))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def upList(self):
        try:
            name = self.listWidget.currentItem().text().lower()
            accounts = list(config.items('Accounts'))
            for i in range(len(accounts)):
                if accounts[i][0] == name:
                    id = i
                    break
            if id > 0:
                accounts[id], accounts[id-1] = accounts[id-1], accounts[id]
                config.remove_section('Accounts')
                config.add_section("Accounts")
                for i in range(len(accounts)):
                    config.set("Accounts", accounts[i][0], accounts[i][1])
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            self.reloadList()
        except AttributeError:
            self.error_msg.setText("Aucun compte sélectionné !")
            self.error_msg.exec_()
    def downList(self):
        try:
            name = self.listWidget.currentItem().text().lower()
            accounts = list(config.items('Accounts'))
            for i in range(len(accounts)):
                if accounts[i][0] == name:
                    id = i
                    break
            if id < len(accounts)-1:
                accounts[id], accounts[id+1] = accounts[id+1], accounts[id]
                config.remove_section('Accounts')
                config.add_section("Accounts")
                for i in range(len(accounts)):
                    config.set("Accounts", accounts[i][0], accounts[i][1])
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            self.reloadList()
        except AttributeError:
            self.error_msg.setText("Aucun compte sélectionné !")
            self.error_msg.exec_()
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    MainWindow = DofLogWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    exit(app.exec_())
