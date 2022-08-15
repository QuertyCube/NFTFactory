from PyQt5 import QtQuickWidgets, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication,QTextEdit,QLabel,QPushButton,QInputDialog
from PyQt5.QtWidgets import QDialog,QLineEdit,QDateTimeEdit, QTimeEdit,QFileDialog,QMessageBox
from PyQt5.QtCore import QFileInfo, QThread
from PyQt5.QtCore import QMutex, QObject, QThread, pyqtSignal
import requests
from PyQt5 import uic
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import pytz
import re

import os.path
from datetime import datetime
import create_collectible

import webbrowser
import datetime
import time
import brownie.project as project
from brownie import *

from urllib import response
from web3 import Web3, HTTPProvider
import urllib.request, json 
import requests



#ganti jadi Nama folder, exp nama folder NFTFactory:      p = project.load(r'D:\Collage\ScriptSweat\Proj\NFTFactory', name="NftfactoryProject")
p = project.load(r'D:\Collage\ScriptSweat\Proj\NFTFactory', name="NftfactoryProject")
p.load_config()
network.connect('rinkeby')

contract_addr='0xab38F479fFbDC478D6083D5FE09078a46dfb8C93'
adrees ="mg8"
kunci="74u"
maxsizefile ="The allowed file size is 20MB.\nPlease reselect the file."
size_file_max = 20971520

rege = re.compile(
        r'^(?:http|ftp)s?://'+ # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'+ #domain...
        r'localhost|'+ #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'+ # ...or ip
        r'(?::\d+)?'+ # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

########### Main Menu (menu pilihan) #################
class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu,self).__init__()
        uic.loadUi(r'.\ui\mainMenu.ui',self)
        
        

        #Define Widget
        self.pushButtonImage.clicked.connect(self.toformImage)
        self.pushButtonVideo.clicked.connect(self.toformVideo)
        self.pushButtonDocument.clicked.connect(self.toformDocument)
        self.pushButtonAudio.clicked.connect(self.toformAudio)
        self.pushButtonDomain.clicked.connect(self.toformDomain)
        self.pushButtonOther.clicked.connect(self.toformOther)
        self.pushButtonAsset.clicked.connect(self.toformAsset)
        
        iconImage = QPixmap(r'.\ui\image-icon.png')
        iconVideo = QPixmap(r'.\ui\video-icon.png')
        iconDocument= QPixmap(r'.\ui\document-icon.png')
        iconDomain= QPixmap(r'.\ui\domain-icon.png')
        iconSound= QPixmap(r'.\ui\audio-icon.png')
        iconOther= QPixmap(r'.\ui\other-icon.png')
        
        self.label_icon_image.setPixmap(iconImage.scaled(350, 100, QtCore.Qt.KeepAspectRatio))
        self.label_icon_video.setPixmap(iconVideo.scaled(350, 100, QtCore.Qt.KeepAspectRatio))
        self.label_icon_document.setPixmap(iconDocument.scaled(350, 110, QtCore.Qt.KeepAspectRatio))
        self.label_icon_domain.setPixmap(iconDomain.scaled(350, 110, QtCore.Qt.KeepAspectRatio))
        self.label_icon_audio.setPixmap(iconSound.scaled(350, 110, QtCore.Qt.KeepAspectRatio))
        self.label_icon_other.setPixmap(iconOther.scaled(250, 100, QtCore.Qt.KeepAspectRatio))

    def toformImage(self):
        formImage= FormImage()
        widget.addWidget(formImage)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def toformVideo(self):
        formVideo= FormVideo()
        widget.addWidget(formVideo)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def toformDocument(self):
        formDocument= FormDocument()
        widget.addWidget(formDocument)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def toformAudio(self):
        formAudio= FormSound()
        widget.addWidget(formAudio)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def toformDomain(self):
        formDomain= FormDomain()
        widget.addWidget(formDomain)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def toformOther(self):
        formOther= FormOther()
        widget.addWidget(formOther)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def toformAsset(self):
        formAset= AsetMenu()
        widget.addWidget(formAset)
        widget.setCurrentIndex(widget.currentIndex() + 1)


############ FORMULIR ################

class FormImage(QDialog):
    def __init__(self):
        super(FormImage, self).__init__()
        uic.loadUi(r'.\ui\formImage.ui',self)

        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.pushButton_choose.clicked.connect(self.browsefiles)

    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        self.pushButton_choose.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.lineEdit_loc_file.setEnabled(tf)
        #label
        self.label_file.setEnabled(tf)
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)

    file_extension="fille"    
    #Tombol Choose File
    def browsefiles(self):
        print(kunci)
        fname = QFileDialog.getOpenFileName(self,'Open File', "D:\\", "Picture files(*.bmp *.dib *.cur *.gif *.icns *.ico *.jpg *.jpeg *.jpe *.jfif *.pbm *.tif *.tiff *.pgm *.png *.ppm *.svg *.svgz *.tga *.wbm, *.webp *.xbm *.xpm);;RAW Image Files (*.raw *.cr2 *.nef *.orf *.sr2);;All Files (*)") #nama tab nya, location pilihan
        if fname != "":
            info = QFileInfo(fname[0])
            sizenya=info.size()
            if sizenya < size_file_max:  #jika file < 20 MB
                self.lineEdit_loc_file.setText(fname[0])
                self.file_extension = os.path.splitext(fname[0])[1][1:]  #dapetin png (bukan .png)
            else:
                self.show_popup("Warning",maxsizefile,"")
    hasi="www.google.com"
    #Klik MINT
    def minting(self):
        cek=""
        text_file_location = self.lineEdit_loc_file.text()
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()

        if(text_file_location == ""):
            cek=cek+"You haven't select the file.\n"
        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n\n"
        if (text_website == ""):
            pass
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\nor you can leave the column blank\n"

        mulai =self.loading_mulai()
        self.all_when_loading(False) 

        if(cek!=""):
            print("gk oke")
            self.show_popup("Information",cek,"")
            self.all_when_loading(True)
            self.loading_stop()
            
        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="image"
            self.mantin.fileloc_text=text_file_location
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=self.file_extension
            self.mantin.reg_text="reg_date"
            self.mantin.exp_text="exp_date"
            self.mantin.creator_text="creator_name"
            self.mantin.artis_text="artist_name"
            self.mantin.fcreated_text="fcreated_date"

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()



    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()


    def reset_text(self):
        self.lineEdit_loc_file.setText("")
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
        
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")


class FormVideo(QDialog):
    def __init__(self):
        super(FormVideo, self).__init__()
        uic.loadUi(r'.\ui\formVideo.ui',self)

        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.pushButton_choose.clicked.connect(self.browsefiles)

    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        self.pushButton_choose.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.lineEdit_loc_file.setEnabled(tf)
        self.lineEdit_Creator.setEnabled(tf)
        #label
        self.label_file.setEnabled(tf)
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)
        self.label_creator.setEnabled(tf)

    file_extension="fille"    
    #Tombol Choose File
    def browsefiles(self):
        print(kunci)
        fname = QFileDialog.getOpenFileName(self,'Open File', "D:\\", "Video files(*.webm *.mkv *.flv *.vob *.ogv *.ogg *.drc *.gif *.gifv *.mng *.avi *.MTS *.M2TS *.TS *.mov *.qt *.wmv *.yuv *.rm *.rmvb *.viv *.asf *.amv *.mp4 *.m4p *.m4v *.mpg *.mp2 *.mpeg *.mpe *.mpv *.mpg *.mpeg *.m2v *.m4v *.svi *.3gp *.3g2 *.mxf *.roq *.nsv *.flv *.f4v *.f4p *.f4a *.f4b);;All Files (*)") #nama tab nya, location pilihan
        if fname != "":
            info = QFileInfo(fname[0])
            sizenya=info.size()
            # print(sizenya)
            if sizenya <size_file_max:  #jika file < 20 MB
                self.lineEdit_loc_file.setText(fname[0])
                self.file_extension = os.path.splitext(fname[0])[1][1:]  #dapetin png (bukan .png)
            else:
                self.show_popup("Warning",maxsizefile,"")
    hasi="www.google.com"
    #Klik MINT
    def minting(self):
        cek=""
        text_file_location = self.lineEdit_loc_file.text()
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()
        text_creator = self.lineEdit_Creator.text()

        if(text_file_location == ""):
            cek=cek+"You haven't select the file.\n"
        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n"
        if(text_creator == "") or (text_creator.isspace()):
            cek=cek+"You haven't wrote the creator name.\n"
        if (text_website == ""):
            pass
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\nor you can leave the column blank.\n"


        self.loading_mulai()
        self.all_when_loading(False) 

        if(cek!=""):
            print("gk oke")
            self.show_popup("Warning",cek,"")
            self.all_when_loading(True)
            self.loading_stop()
            
        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="video"
            self.mantin.fileloc_text=text_file_location
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=self.file_extension
            self.mantin.reg_text="reg_date"
            self.mantin.exp_text="exp_date"
            self.mantin.creator_text=text_creator
            self.mantin.artis_text="artist_name"
            self.mantin.fcreated_text="fcreated_date"

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()


    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()

    def reset_text(self):
        self.lineEdit_loc_file.setText("")
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")
        self.lineEdit_Creator.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
        
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")



class FormDocument(QDialog):
    def __init__(self):
        super(FormDocument, self).__init__()
        uic.loadUi(r'.\ui\formDocument.ui',self)

        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.pushButton_choose.clicked.connect(self.browsefiles)

# 
    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        self.pushButton_choose.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.lineEdit_loc_file.setEnabled(tf)
        self.lineEdit_datecreated.setEnabled(tf)
        #label
        self.label_file.setEnabled(tf)
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)
        self.label_datecreated.setEnabled(tf)

    file_extension="fille"
    unix_fcreated=123
    #Tombol Choose File
    def browsefiles(self):
        print(kunci)
        fname = QFileDialog.getOpenFileName(self,'Open File', "D:\\", "Document files(*.djvu *.djv *.dbk *.xml *.fb2 *.fbz *.doc *.docx *.docm *.pptx *.pptm *.xlsx *.xlsm *.odt *.fodt *.oxps *.xps *.pages *.pdf *.ps *.rtf *.uof *.uot *.uos *.wpd *.wp *.wp7 *.wp6 *.wp5 *.wp4);;All Files (*)") #nama tab nya, location pilihan
        if fname != "":
            info = QFileInfo(fname[0])
            sizenya=info.size()
            # print(sizenya)
            if sizenya <size_file_max:  #jika file < 20 MB
                self.lineEdit_loc_file.setText(fname[0])
                self.file_extension = os.path.splitext(fname[0])[1][1:]  #dapetin png (bukan .png)
                
                self.unix_fcreated= int(os.path.getctime(fname[0]))
                print("self unix : "+str(self.unix_fcreated))
                self.lineEdit_datecreated.setText(datetime.datetime.fromtimestamp(self.unix_fcreated, datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S'))  #time nya local
            else:
                self.show_popup("Warning",maxsizefile,"")
    hasi=""
    #Klik MINT
    def minting(self):
        cek=""
        text_file_location = self.lineEdit_loc_file.text()
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()


        if(text_file_location == ""):
            cek=cek+"You haven't select the file.\n"
        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n"
        if (text_website == ""):
            pass
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\nor you can leave the column blank\n"



        self.loading_mulai()
        self.all_when_loading(False) 

        if(cek!=""):
            print("gk oke")
            self.show_popup("Warning",cek,"")
            self.all_when_loading(True)
            self.loading_stop()

        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="document"
            self.mantin.fileloc_text=text_file_location
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=self.file_extension
            self.mantin.reg_text="reg_date"
            self.mantin.exp_text="exp_date"
            self.mantin.creator_text="creator_name"
            self.mantin.artis_text="artist_name"
            self.mantin.fcreated_text=self.unix_fcreated

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()


    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()

    def reset_text(self):
        self.lineEdit_loc_file.setText("")
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")
        self.lineEdit_datecreated.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
        
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")






class FormDomain(QDialog):
    def __init__(self):
        super(FormDomain, self).__init__()
        uic.loadUi(r'.\ui\formDomain.ui',self)

        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.nan = self.findChild(QLineEdit, "lineEdit_nama")

        self.namanya = self.findChild(QLineEdit, "lineEdit_nama")
        self.deskripsinya =self.findChild(QTextEdit, "textEdit_deskripsi")
        self.websitenya = self.findChild(QLineEdit, "lineEdit_website")
        self.regisnya = self.findChild(QDateTimeEdit, "dateTimeEdit_register")
        self.expirednya =self.findChild(QDateTimeEdit, "dateTimeEdit_expired")

        self.regisnya.setDisplayFormat("dd/MM/yyyy, hh:mm:ss")
        self.expirednya.setDisplayFormat("dd/MM/yyyy, hh:mm:ss")

    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.dateTimeEdit_register.setEnabled(tf)
        self.dateTimeEdit_expired.setEnabled(tf)
        #label
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)
        self.label_registerdate.setEnabled(tf)
        self.label_expireddate.setEnabled(tf)


    hasi=""

    # klik mint
    def minting(self):

        #to Unix
        date_format_regis = datetime.datetime.strptime(self.regisnya.text(), "%d/%m/%Y, %H:%M:%S")
        utc_date_format_regis= date_format_regis.astimezone(pytz.UTC)
        unix_time_regis = int(datetime.datetime.timestamp(utc_date_format_regis))

        date_format_exp = datetime.datetime.strptime(self.expirednya.text(), "%d/%m/%Y, %H:%M:%S")
        utc_date_format_exp= date_format_exp.astimezone(pytz.UTC)
        unix_time_exp = int(datetime.datetime.timestamp(utc_date_format_exp))

        cek=""
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()


        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n"
        if(text_website == ""):
            cek=cek+"You haven't wrote the external url.\n"
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\n"

        self.loading_mulai()
        self.all_when_loading(False) 
        global hasi
        if(cek!=""):
            print("gk oke")
            self.show_popup("Information",cek,"")
            self.all_when_loading(True)
            self.loading_stop()
            
        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="domain"
            self.mantin.fileloc_text="file loc"
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=""
            self.mantin.reg_text=unix_time_regis
            self.mantin.exp_text=unix_time_exp
            self.mantin.creator_text="creator_name"
            self.mantin.artis_text="artist_name"
            self.mantin.fcreated_text="fcreated_date"

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()

    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()

    def reset_text(self):
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
        
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")



class FormSound(QDialog):
    def __init__(self):
        super(FormSound, self).__init__()
        uic.loadUi(r'.\ui\formSound.ui',self)


        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.pushButton_choose.clicked.connect(self.browsefiles)

    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        self.pushButton_choose.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.lineEdit_loc_file.setEnabled(tf)
        self.lineEdit_Creator.setEnabled(tf)
        self.lineEdit_Artist.setEnabled(tf)
        #label
        self.label_file.setEnabled(tf)
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)
        self.label_creator.setEnabled(tf)
        self.label_artist.setEnabled(tf)

    file_extension="fille"    
    #Tombol Choose File
    def browsefiles(self):
        print(kunci)
        fname = QFileDialog.getOpenFileName(self,'Open File', "D:\\", "Audio files(*.aa *.aac *.aax *.act *.aiff *.alac *.amr *.ape *.au *.awb *.cda *.dss *.dvf *.flac *.gsm *.iklax *.ivs *.m4a *.m4b *.m4p *.mmf *.mogg *.mp3 *.mpc *.msv *.nmf *.oga *.ogg *.opus *.ra *.raw *.rf64 *.rm *.sln *.tta *.voc *.vox *.wav *.webm *.wma *.wv *.3gp *.8svx);;All Files (*)") #nama tab nya, location pilihan
        if fname != "":
            info = QFileInfo(fname[0])
            sizenya=info.size()
            # print(sizenya)
            if sizenya <size_file_max:  #jika file < 20 MB
                self.lineEdit_loc_file.setText(fname[0])
                self.file_extension = os.path.splitext(fname[0])[1][1:]  #dapetin png (bukan .png)
            else:
                self.show_popup("Warning",maxsizefile,"")
    hasi="www.google.com"
    #Klik MINT
    def minting(self):
        cek=""
        text_file_location = self.lineEdit_loc_file.text()
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()
        text_creator = self.lineEdit_Creator.text()
        text_artist = self.lineEdit_Artist.text()

        if(text_file_location == ""):
            cek=cek+"You haven't select the file.\n"
        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n"
        if(text_creator == "") or (text_creator.isspace()):
            cek=cek+"You haven't wrote the creator name.\n"
        if(text_artist == "") or (text_artist.isspace()):
            cek=cek+"You haven't wrote the artist name.\n"

        if (text_website == ""):
            pass
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\nor you can leave the column blank\n"



        self.loading_mulai()
        self.all_when_loading(False) 
        
        if(cek!=""):
            print("gk oke")
            self.show_popup("Warning",cek,"")
            self.all_when_loading(True)
            self.loading_stop()
            
        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="sound"
            self.mantin.fileloc_text=text_file_location
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=self.file_extension
            self.mantin.reg_text="reg_date"
            self.mantin.exp_text="exp_date"
            self.mantin.creator_text=text_creator
            self.mantin.artis_text=text_artist
            self.mantin.fcreated_text="fcreated_date"

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()



    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()

    def reset_text(self):
        self.lineEdit_loc_file.setText("")
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")
        self.lineEdit_Creator.setText("")
        self.lineEdit_Artist.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
        
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")





class FormOther(QDialog):
    def __init__(self):
        super(FormOther, self).__init__()
        uic.loadUi(r'.\ui\formOther.ui',self)

        #Define Widget
        self.pushButton_close.clicked.connect(self.home)
        self.pushButton_mint.clicked.connect(self.minting)
        self.pushButton_choose.clicked.connect(self.browsefiles)

    #tentang LOADING
    def loading_mulai(self):
        self.movie = QMovie("./ui/loading.gif")
        self.label_loading.setMovie(self.movie)
        self.movie.start()

    def loading_stop(self):
        self.movie.stop()
        self.label_loading.setMovie(None)

    def all_when_loading(self,tf):
        #button
        self.pushButton_mint.setEnabled(tf)
        self.pushButton_close.setEnabled(tf)
        self.pushButton_choose.setEnabled(tf)
        #line edit
        self.lineEdit_nama.setEnabled(tf)
        self.textEdit_deskripsi.setEnabled(tf)
        self.lineEdit_website.setEnabled(tf)
        self.lineEdit_loc_file.setEnabled(tf)
        #label
        self.label_file.setEnabled(tf)
        self.label_nama.setEnabled(tf)
        self.label_website.setEnabled(tf)
        self.label_deskripsi.setEnabled(tf)

    file_extension="fille"    
    #Tombol Choose File
    def browsefiles(self):
        print(kunci)
        fname = QFileDialog.getOpenFileName(self,'Open File', "D:\\", "All Files (*)") #nama tab nya, location pilihan
        if fname != "":
            info = QFileInfo(fname[0])
            sizenya=info.size()
            if sizenya <size_file_max:  #jika file < 20 MB
                self.lineEdit_loc_file.setText(fname[0])
                self.file_extension = os.path.splitext(fname[0])[1][1:]  #dapetin png (bukan .png)

            else:
                self.show_popup("Warning",maxsizefile,"")
    hasi="www.google.com"
    #Klik MINT
    def minting(self):
        cek=""
        text_file_location = self.lineEdit_loc_file.text()
        text_nama = self.lineEdit_nama.text()
        text_deskripsi = self.textEdit_deskripsi.toPlainText()
        text_website = self.lineEdit_website.text()

        if(text_file_location == ""):
            cek=cek+"You haven't select the file.\n"
        if(text_nama == "") or (text_nama.isspace()):
            cek=cek+"You haven't wrote the name.\n"
        if(text_deskripsi == "") or (text_deskripsi.isspace()):
            cek=cek+"You haven't wrote the description.\n"
        if (text_website == ""):
            pass
        elif (False == (re.match(rege, text_website) is not None)) or (" " in text_website):
            cek=cek+"Please enter valid url, example: https://example.com\nor you can leave the column blank\n"

        self.loading_mulai()
        self.all_when_loading(False) 
 
        if(cek!=""):
            print("gk oke")
            self.show_popup("Information",cek,"")
            self.all_when_loading(True)
            self.loading_stop()
            
        else:
            self.mantin = Permintingan()
            self.mantin.hasil_minting_sinyal.connect(self.loadhasilmin)
            self.mantin.akses_text ="other"
            self.mantin.fileloc_text=text_file_location
            self.mantin.name_text=text_nama
            self.mantin.des_text=text_deskripsi
            self.mantin.web_text=text_website
            self.mantin.filex_text=self.file_extension
            self.mantin.reg_text="reg_date"
            self.mantin.exp_text="exp_date"
            self.mantin.creator_text="creator_name"
            self.mantin.artis_text="artist_name"
            self.mantin.fcreated_text="fcreated_date"

            self.show_popup("Information","All right your NFT on prosess.\nPlease wait until we finish mint it.","")
            self.loading_mulai()         
            self.mantin.start()
            



    def loadhasilmin(self, keluaran):
        global hasi
        print("hasil print jalan :"+keluaran)
        if("failed" in keluaran):
            if ("metadata" in keluaran):
                self.show_popup("Warning","Failed to upload your file to ipfs.\nCheck your internet connection and try again\n\n"+keluaran,"")
                print("ok")
            else:    
                self.show_popup("Warning",""+keluaran,"")
                print("ok")
        else:
            hasi=keluaran
            self.reset_text()
            self.show_popup("Information","Horray!!!\nMint NFT completely success.\nYou can view your NFT on OpenSea\n\n"+keluaran+"\n\nKlik Open button to see it","link")

        self.all_when_loading(True)
        self.loading_stop()

    def reset_text(self):
        self.lineEdit_loc_file.setText("")
        self.lineEdit_nama.setText("")
        self.textEdit_deskripsi.setText("")
        self.lineEdit_website.setText("")

    #to home
    def home(self):
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def show_popup(self,judul,pesan,jenis): #(judul,pesan,jenis,link)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText(pesan)
      
        if judul == "Information":
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle(judul)
        elif judul == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(judul)

        if jenis == "link":
            msg.setStandardButtons(QMessageBox.Open|QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Open)
            msg.buttonClicked.connect(self.popup_button)
        x=msg.exec_()
    
    def popup_button(self,i):
        if i.text() == "Open":
            webbrowser.open(f"{hasi}")
    



class Permintingan(QThread):
    
    hasil_minting_sinyal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Permintingan, self).__init__(parent)
        # self.kunci_text = None
        self.akses_text =None
        self.fileloc_text=None
        self.name_text=None
        self.des_text=None
        self.web_text=None
        self.filex_text=None
        self.reg_text=None
        self.exp_text=None
        self.creator_text=None
        self.artis_text=None
        self.fcreated_text=None

    def run(self):
        returnnya=create_collectible.main(kunci,self.akses_text,self.fileloc_text,self.name_text,self.des_text,self.web_text,self.filex_text,self.reg_text,self.exp_text,self.creator_text,self.artis_text,self.fcreated_text)
        self.hasil_minting_sinyal.emit(returnnya)

class LoadForm(QThread):
    jumlah_sinyall =pyqtSignal(int)
    new_signal = pyqtSignal(int, int, str)
    hasilnya_sinyal = pyqtSignal(str)



    def run(self):
        wallet_addr = str(accounts.add(kunci))

        api_get_nft_from_wallet_spec_addr='https://api-rinkeby.etherscan.io/api?module=account&action=tokennfttx&contractaddress={}&address={}&page=1&offset=100&startblock=0&endblock=27025780&sort=desc&apikey=YK3FX65I3DCB1BS92WFPCZFKB67P6W43DG'.format(contract_addr,wallet_addr)
        abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"tokenURI","type":"string"}],"name":"createCollectible","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenCounter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

        w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/88704d0c3a364cf1b3e46d9e5173a57f"))
        hdr = {"User-Agent": "My Agent"}

        


        with urllib.request.urlopen(api_get_nft_from_wallet_spec_addr) as url:
            ebet = json.loads(url.read().decode())

        escrow = w3.eth.contract(address='0x411703674217d706D055a4740771dc62C0c27054', abi=abi)
        linkrul=""
        row=0


        if ebet['status'] == "1":

            self.jumlah_sinyall.emit(len(ebet['result']))
            print("sono")

            for i in ebet['result']:

                self.new_signal.emit(row, 0, i["tokenID"])
                self.new_signal.emit(row, 12, ("https://rinkeby.etherscan.io/tx/"+i["hash"]))
                tx = w3.eth.get_transaction(str(i["hash"]))
                func_obj, func_params = escrow.decode_function_input(tx["input"])
                try:
                    # ebet2=respons.json()

                    linkrul =str(func_params["tokenURI"])

                    req = requests.get(linkrul, headers=hdr)
                    text=req.text
                    ebet2=json.loads(text)

                    print(ebet2["name"])
                    self.new_signal.emit(row, 1, ebet2["name"])
                    self.new_signal.emit(row, 2, ebet2["description"])
                    print(ebet2["description"])


                    try:
                        if ebet2["jenis_nft"] =="image":
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 3, ebet2["image"])
                            self.new_signal.emit(row, 11, "Image")
                            print("")

                        elif ebet2["jenis_nft"] =="video":
                            self.new_signal.emit(row, 3, ebet2["animation_url"])
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 6, ebet2["creator_name"])
                            self.new_signal.emit(row, 10, ebet2["image"])
                            self.new_signal.emit(row, 11, "Video")

                        elif ebet2["jenis_nft"] =="audio":
                            self.new_signal.emit(row, 3, ebet2["animation_url"])
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 6, ebet2["creator_name"])
                            self.new_signal.emit(row, 7, ebet2["artist_name"])
                            self.new_signal.emit(row, 10, ebet2["image"])  
                            self.new_signal.emit(row, 11, "Audio")                    

                        elif ebet2["jenis_nft"] =="domain":
                            self.new_signal.emit(row, 4, ebet2["url"])
                            self.new_signal.emit(row, 10, ebet2["image"])
                            self.new_signal.emit(row, 11, "Domain")

                            for ja in ebet2['attributes']:
                                if ja["trait_type"]== "Registration Date":
                                    regdate= datetime.datetime.fromtimestamp(ja["value"], datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')  #time nya local
                                    self.new_signal.emit(row, 8, str(regdate))
                                if ja["trait_type"]== "Expiration Date":
                                    expdate= datetime.datetime.fromtimestamp(ja["value"], datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')  #time nya local
                                    self.new_signal.emit(row, 9, str(expdate))


                        elif ebet2["jenis_nft"] =="document":
                            self.new_signal.emit(row, 3, ebet2["url"])
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 10, ebet2["image"]) 
                            self.new_signal.emit(row, 11, "Document")
                            

                        elif ebet2["jenis_nft"] =="other":
                            self.new_signal.emit(row, 3, ebet2["url"])
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 10, ebet2["image"]) 
                            self.new_signal.emit(row, 11, "Other")

                    except Exception as e:
                        try:
                            self.new_signal.emit(row, 3, ebet2["image"])
                            self.new_signal.emit(row, 4, ebet2["external_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 10, ebet2["image"])
                        except Exception as e:
                            print("")

                        try:
                            self.new_signal.emit(row, 3, ebet2["animation_url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                            self.new_signal.emit(row, 6, ebet2["creator_name"])
                            self.new_signal.emit(row, 7, ebet2["artist_name"])
                            
                        except Exception as e:
                            print("")

                        try:
                            self.new_signal.emit(row, 3, ebet2["url"])
                            self.new_signal.emit(row, 5, ebet2["model_file_type"])
                        except Exception as e:
                            print("")

                        try:
                            for ja in ebet2['attributes']:
                                if ja["trait_type"]== "Registration Date":
                                    regdate= datetime.datetime.fromtimestamp(ja["value"], datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')  #time nya local
                                    self.new_signal.emit(row, 8, str(regdate))
                                if ja["trait_type"]== "Expiration Date":
                                    expdate= datetime.datetime.fromtimestamp(ja["value"], datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')  #time nya local
                                    self.new_signal.emit(row, 9, str(expdate))
                            self.new_signal.emit(row, 3, "")
                            self.new_signal.emit(row, 10, ebet2["image_url"])
                            self.new_signal.emit(row, 4, ebet2["url"])
                        except Exception as e:
                            print("")
                except Exception as e:
                    print("No File detected")


                row=row+1
            ##udah selesai
            self.hasilnya_sinyal.emit("sudh selea")

        elif ebet['status'] == "0":
            self.jumlah_sinyall.emit(len(ebet['result'])+1)
            print('hasil ebet nih'+str(len(ebet['result'])))
            print("sini")

            self.new_signal.emit(row, 1, ebet["message"])
            self.new_signal.emit(row, 2, str(ebet["result"]))
        
        else:
            self.jumlah_sinyall.emit(1)
            self.new_signal.emit(row, 1, 'nothing')
            pass

    def stop(self):
        self._isRunning = False


class AsetMenu(QMainWindow):
    def __init__(self):
        super(AsetMenu,self).__init__()
        uic.loadUi(r'.\ui\tabel.ui',self)
        

        self.button_back.clicked.connect(self.home)
        self.worker = LoadForm()
        self.worker.jumlah_sinyall.connect(self.loadjumlah)
        self.worker.new_signal.connect(self.some_function)
        self.worker.hasilnya_sinyal.connect(self.loadhasil)
        self.worker.start()


    def stop_thread(self):
        self.worker.terminate()
        self.worker.stop()



    #to home
    def home(self):
        self.stop_thread()
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)



    def loadhasil(self, hasilnya):
        print(hasilnya)

    def loadjumlah(self, jum):
        self.tableWidget.setRowCount(jum)


    def some_function(self, r, c, text):
        it = QtWidgets.QTableWidgetItem(text)
        self.tableWidget.setItem(r, c, it)


#############
#masukan private key
class Private(QDialog):
    def __init__(self):
        super(Private, self).__init__()
        
        uic.loadUi(r".\ui\masukPrivateKey.ui",self)

        self.pushButtonOk.clicked.connect(self.fungsin)
        self.pushButtonCancel.clicked.connect(self.tutup)


    def fungsin(self):
        getprivate = self.inputPrivateKey.text()
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        


        if len(getprivate) == 64:

            if (regex.search(getprivate) == None) and (" " not in getprivate):

                global kunci
                global adrees
                kunci = ""+getprivate
                adrees =""+str(accounts.add(kunci))
                print(kunci)
                print (adrees)
                self.home()
            else:
                self.show_popup("Private Key can only be letters and numbers")
        else:
            self.show_popup("Private Key length is not eligible.\nEnter your 64 character Private Key")


    def tutup(self):
        sys.exit()

    def home(self):
        self.close()
        home= MainMenu()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.show()

    def show_popup(self,pesan):
        msg = QMessageBox()
        msg.setWindowTitle("Enter Private Key")
        msg.setText(pesan)
        msg.exec() 


#Initialize the app
app = QApplication(sys.argv)
UIWindow = MainMenu()
widget = QtWidgets.QStackedWidget()
widget.addWidget(UIWindow)
widget.setFixedHeight(560)
widget.setFixedWidth(700)
widget.setWindowTitle("NFT Factory")

Private().exec_()
# widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")
    sys.exit()


