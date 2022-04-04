import sys
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
import time

banco = sqlite3.connect('login.db')
cursor = banco.cursor()

def register():
    user = window.usuarioIn.text()
    password = window.senhaIn.text()
    name = window.nomeIn.text()
    email = window.emailIn.text()
    
    if user == '':
        pass
    if password == '':
        pass
    if name == '':
        pass
    if email == '':
        pass
    else:
        try:
            cursor.execute(f"""INSERT INTO data VALUES(Null, '{user}', '{password}', '{email}', '{name}')""")
            banco.commit()
            cursor.execute(f"""SELECT * FROM data""")
            dados = cursor.fetchall()
            adm.dataTable.setRowCount(len(dados))
            adm.dataTable.setColumnCount(5)
            adm.dataTable.setHorizontalHeaderLabels(['Id', 'User', 'Password', 'Email', 'Name'])
            for i in range(0, len(dados)):
                for j in range(0, 5):
                    adm.dataTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
                    
        except sqlite3.IntegrityError:
            print('Ja existe')
            
    window.usuarioIn.clear()
    window.senhaIn.clear()
    window.nomeIn.clear()
    window.emailIn.clear()

def login():
    user = window.usuarioLo.text()
    password = window.senhaLo.text()
    
    cursor.execute("""SELECT User, Password FROM data""")
    for data in cursor.fetchall():
        if user in data:
            if password in data:
                cursor.execute(f"""SELECT * FROM data""")
                dados = cursor.fetchall()
                adm.dataTable.setRowCount(len(dados))
                adm.dataTable.setColumnCount(5)
                adm.dataTable.setHorizontalHeaderLabels(['Id', 'User', 'Password', 'Email', 'Name'])
                adm.dataTable.horizontalHeader().hide()
                for i in range(0, len(dados)):
                    for j in range(0, 5):
                        adm.dataTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
                adm.show()    
        else:
            pass
    
    window.usuarioLo.clear()
    window.senhaLo.clear()
        
def recover():
    email = window.emailEs.text()
    
    fromAdress = 'docafavarato@gmail.com'
    toAdress = email
    message = MIMEMultipart('Teste')
    message['Subject'] = 'Recuperação de dados'
    message['From'] = fromAdress
    message['To'] = toAdress
    cursor.execute(f"""SELECT Name FROM data WHERE Email = '{email}'""")
    for data in cursor.fetchall():
        for name in data:
            cursor.execute(f"""SELECT User, Password FROM data WHERE email = '{email}'""")
            for recover in cursor.fetchall():
                content = MIMEText(f'''Olá, {name}. Seus dados são:
Usuário: {recover[0]}
Senha: {recover[1]}''')
    message.attach(content) 
    
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(fromAdress, 'DocaPedro11!')
    mail.sendmail(fromAdress, toAdress, message.as_string())
    mail.close()
    
    window.emailEs.clear()
    
    
def regPage():
    window.login.setStyleSheet('QPushButton \
                                { \
                                font-size: 14px; \
                                border-style: none; \
                                color: white; \
                                } \
                                QPushButton::hover \
                                { \
                                border-style: solid; \
                                background-color: \
                                rgb(110, 110, 110); \
                                }')
    
    window.esqueci.setStyleSheet('QPushButton \
                                    { \
                                    font-size: 14px; \
                                    border-style: none; \
                                    color: white; \
                                    } \
                                    QPushButton::hover \
                                    { \
                                    border-style: solid; \
                                    background-color: \
                                    rgb(110, 110, 110); \
                                    }')
    
    window.Pages.setCurrentWidget(window.page)
    window.registrar.setStyleSheet('''background-color: rgb(110, 110, 110); border-style: none; color: white; font-size: 14px;''')
    
def loginPage():
    window.registrar.setStyleSheet('QPushButton \
                                    { \
                                    font-size: 14px; \
                                    border-style: none; \
                                    color: white; \
                                    } \
                                    QPushButton::hover \
                                    { \
                                    border-style: solid; \
                                    background-color: \
                                    rgb(110, 110, 110); \
                                    }')
    
    window.esqueci.setStyleSheet('QPushButton \
                                    { \
                                    font-size: 14px; \
                                    border-style: none; \
                                    color: white; \
                                    } \
                                    QPushButton::hover \
                                    { \
                                    border-style: solid; \
                                    background-color: \
                                    rgb(110, 110, 110); \
                                    }')
    window.Pages.setCurrentWidget(window.page_2)
    window.login.setStyleSheet('background-color: rgb(110, 110, 110); border-style: none; color: white; font-size: 14px;')
    
def esqueciPage():
    window.registrar.setStyleSheet('QPushButton \
                                    { \
                                    font-size: 14px; \
                                    border-style: none; \
                                    color: white; \
                                    } \
                                    QPushButton::hover \
                                    { \
                                    border-style: solid; \
                                    background-color: \
                                    rgb(110, 110, 110); \
                                    }')
    
    window.login.setStyleSheet('QPushButton \
                                { \
                                font-size: 14px; \
                                border-style: none; \
                                color: white; \
                                } \
                                QPushButton::hover \
                                { \
                                border-style: solid; \
                                background-color: \
                                rgb(110, 110, 110); \
                                }')
    
    window.Pages.setCurrentWidget(window.page_3)
    window.esqueci.setStyleSheet('background-color: rgb(110, 110, 110); border-style: none; color: white; font-size: 14px;')

# Window

app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('login.ui')
adm = uic.loadUi('admin.ui')

adm.dataTable.horizontalHeader().setStretchLastSection(True)


# Buttons

window.registrar.clicked.connect(regPage)
window.login.clicked.connect(loginPage)
window.esqueci.clicked.connect(esqueciPage)

window.enviar.clicked.connect(register)
window.logar.clicked.connect(login)
window.enviarEmail.clicked.connect(recover)

window.show()
app.exec()

banco.close()
