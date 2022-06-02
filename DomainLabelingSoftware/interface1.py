# -*- coding: utf-8 -*-
import pyqtgraph as pg
import sys
import csv
import numpy as np
import pandas as pd
import csv, sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QListWidgetItem, QTableView, QApplication, QAction, QMainWindow, qApp, QWidget, QLabel, QGridLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from pyqtgraph import PlotWidget, plot
from PyQt5.QtGui import QImage, QIcon, QPixmap, QPalette, QBrush, QColor, QFontDatabase, QFont
import re

SERVER_NAME = 'DESKTOP-0NHDTT5'
DATABASE_NAME = 'wsdm_raw'
##USERNAME = 'mstadi'

##Feature objects
global sentence
global sentence_sql
global sentence_post
global featurelist
global businessobject
global investigationobject 
global propertyobject 
global metricobject 
global temporalmetric
global temporalstockmetric
global temporalstockmetric_text

global businessobject_text
global investigationobject_text 
global propertyobject_text
global metricobject_text 
global temporalobject 
global temporalobject_text 
global featurelist_sql 
global featuresfile 
global databaseconfig 

global connString
global db

##plot
bo_plot = []
metr_plot = []


    
class Ui_Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Config Dialog")
        self.resize(1480, 1000)

        #Read Configuration
        #fbusiness = open("businessobject.cfg", "r")
        #business_list = fbusiness.read()
   
        with open(r'cfg\database.cfg') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    global databaseconfig
                    databaseconfig = row
        
        def save_dbconfig():        
            global databaseconfig
            databaseconfig = self.lineEditServer.text() + ","+  self.lineEditDBName.text() + "," + self.lineEditUser.text() + "," + self.lineEditPW.text()
            cfg = open(r'cfg\database.cfg', "w")
            cfg.write(databaseconfig)
            cfg.close()
            savecfgmsg = QMessageBox()
            savecfgmsg.setIcon(QMessageBox.Information)
            savecfgmsg.setWindowTitle("Database settings saved")
            savecfgmsg.setText("Database settings saved")
            cfgs = savecfgmsg.exec_()
            
        with open(r'cfg\features.cfg') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=' ')
                for row in csvReader:
                    global featuresfile
                    featuresfile = row

        
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 40, 551, 341))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        ## Server name
        self.lineEditServer = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditServer.setObjectName("lineEdit")
        if databaseconfig[0] is None:
            self.lineEditServer.setText(SERVER_NAME) 
        else: 
            self.lineEditServer.setText(databaseconfig[0])
        self.gridLayout.addWidget(self.lineEditServer, 0, 2, 1, 1)

        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        ## DB Name
        self.lineEditDBName = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditDBName.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEditDBName, 1, 2, 1, 1)       
        if databaseconfig[1] is None:
            self.lineEditDBName.setText(DATABASE_NAME) 
        else: 
            self.lineEditDBName.setText(databaseconfig[1])
        
        ## User Name
        self.lineEditUser = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditUser.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEditUser, 4, 2, 1, 1)
        if databaseconfig[2] is None:
            self.lineEditUser.setText(DATABASE_NAME) 
        else: 
            self.lineEditUser.setText(databaseconfig[2])

        ## Password
        self.lineEditPW = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditPW.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEditPW, 3, 2, 1, 1)
        self.lineEditPW.setText(databaseconfig[3])
        if databaseconfig[3] is None:
            self.lineEditPW.setText(DATABASE_NAME) 
        else: 
            self.lineEditPW.setText(databaseconfig[3])

        #self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        #self.label_4.setObjectName("label_4")
        #self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("train_raw")
        self.comboBox.addItem("transactions")
        self.comboBox.addItem("hs_trans")
        self.comboBox.addItem("soccerdata")
        self.gridLayout.addWidget(self.comboBox, 5, 2, 1, 1)
        
        ## Save Config Button
        self.pushButton_savecfg = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_savecfg.setMinimumSize(QtCore.QSize(0, 40))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ic_savecfg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_savecfg.setIcon(icon)
        self.pushButton_savecfg.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_savecfg.setObjectName("pushButton_savecfg")
        self.gridLayout.addWidget(self.pushButton_savecfg, 6, 2, 1, 1)
        self.pushButton_savecfg.clicked.connect(save_dbconfig)  
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("DB Config", "DB Config"))
        self.label.setText(_translate("DB Config", "Database Server Name"))
        self.label_2.setText(_translate("DB Config", "Database Name"))
        #self.label_4.setText(_translate("Dialog", "Password"))
        self.label_5.setText(_translate("DB Config", "Table Name"))
        self.label_3.setText(_translate("DB Config", "User Name"))
        self.pushButton_savecfg.setText(_translate("DB Config", "Save Config"))
        self.comboBox.setItemText(0, _translate("DB Config", "train_raw"))
        self.comboBox.setItemText(1, _translate("DB Config", "transactions"))
        self.comboBox.setItemText(2, _translate("DB Config", "hs_trans"))
        self.comboBox.setItemText(3, _translate("DB Config", "soccerdata"))

class Ui_Dialog(QWidget):
    def __init__(self):
        super().__init__()
        
        def load_configuration_featuregenerator():
            self.listWidget.clear()  
            #QListWidget.takeItem( index ) # delete specific items

            ##Build List Items
            for i in businessobject_text:
                rownum = 1
                l2 = QListWidgetItem(QIcon(r'assets\ic_business.png'), i)
                self.listWidget.insertItem(rownum, l2)
                rownum+1

            for i in investigationobject_text:
                rownum = 1
                l1 = QListWidgetItem(QIcon(r'assets\ic_investigation.png'), i)
                self.listWidget.insertItem(rownum, l1)
                rownum+1

            for i in propertyobject_text:
                rownum = 1
                l3 = QListWidgetItem(QIcon(r'assets\ic_property.png'), i)
                self.listWidget.insertItem(rownum, l3)
                rownum+1

            for i in metricobject_text:
                rownum = 1
                l4 = QListWidgetItem(QIcon(r'assets\ic_metric.png'), i)
                self.listWidget.insertItem(rownum, l4)
                rownum+1

                 ##Build List Items
            for i in temporalobject_text:
                rownum = 1
                l6 = QListWidgetItem(QIcon(r'assets\ic_clock.png'), i)
                self.listWidget.insertItem(rownum, l6)
                rownum+1
            
            for i in temporalstockmetric:
                rownum = 1
                l7 = QListWidgetItem(QIcon(r'assets\ic_clock.png'), i)
                self.listWidget.insertItem(rownum, l7)
                rownum+1

            for i in temporalstockmetric_text:
                rownum = 1
                l8 = QListWidgetItem(QIcon(r'assets\ic_clock.png'), i)
                self.listWidget.insertItem(rownum, l8)
                rownum+1
        
        # Feature Engineering - Abstractive Domain Labeling Algorithmus

        def generate_featureexpression():
            self.listWidget_2.clear()
            rownum = 0
            rownumsql = 0
            rownumtempo = 0
            metricnames = ""
            featurelist = ""
            tempstocksaetze = ""
            basicsql_post = ""
            rownumtempsql = 0
            metricnamestemp = ""
            basictempsql_post = ""
            basicstocksql_pre = ""
            basicstocksql_post = ""
            metricnameststock_fin = ""
            SQLStock = ""

            # Features in klartext
            # Basic Features
            for i in metricobject_text:
                metric = i
                for y in investigationobject_text:
                    investigation = y
                    for x in businessobject_text:
                        business = x
                        sentence = metric + " " + investigation + " pro " + business
                        self.listWidget_2.insertItem(rownum,featurelist+ " " + sentence)
                        rownum = rownum + 1  
            
            # Temporale Differenz Features
            for i in temporalmetric_text:
                metric = i
                for index, firstelem in enumerate(temporalobject_text):
                    if(index<(len(temporalobject_text)-1)):
                        for index, elem in enumerate(temporalobject_text): 
                            if(index<(len(temporalobject_text)-1)):
                                investigation = y
                            for x in businessobject_text:
                                business = x
                                sentence = "Differenz zwischen " + metric + " "  + firstelem + " und " + metric + " " + elem +  " pro " + business
                                self.listWidget_2.insertItem(rownum,featurelist+ " " + sentence)
                                rownum = rownum + 1  


            # Temporale Bestand Features
            for i in metricobject_text:
                metric = i
                for y in investigationobject_text:
                    investigation = y
                    for x in businessobject_text:
                        business = x
                        sentence = metric  + " " + investigation + " in der ersten hälfte des Abbonements" + " pro " + business
                        self.listWidget_2.insertItem(rownum,featurelist+ " " + sentence)
                        rownum = rownum + 1  
            # TODO Einfügen für gewähltes Zeitattribut: Abfrage des Wochentages und Wochenendes SELECT strftime('%w',date) as WEEKDAY, CASE WHEN strftime('%w',date) in ('0','6') THEN 1 ELSE 0 END as WEEKEND  from train_raw

            # 1. Basic Features
            for i in metricobject:
                metric_sql = i
                for y in investigationobject:
                    investigation_sql = y
                    for x in businessobject:
                        business_sql = x
                        if metric_sql == "COUNT(DISTINCT":
                            sentence_sql = "(SELECT " + metric_sql + " " + investigation_sql + ")"+" AS " + "DISTINCT"+investigation_sql+ ", " +business_sql +" FROM train_raw GROUP BY "+ business_sql +") " + "a"+ str(rownumsql) + "\n" 
                            metricnames = metricnames + "DISTINCT"+investigation_sql+", "
                        else:
                            sentence_sql = "(SELECT " + metric_sql + "(" + investigation_sql + ")"+" AS " + metric_sql+investigation_sql+ ", " +business_sql +" FROM train_raw GROUP BY "+ business_sql +") " + "a"+ str(rownumsql) + "\n" 
                            metricnames = metricnames + metric_sql+investigation_sql+","

                        rownumsql = rownumsql + 1
                        # Ergebnis zusammensetzen
                        if rownumsql == 1:
                            basicsql_post = "\n"+sentence_sql+" \n"+" LEFT JOIN \n"
                        else:
                            basicsql_post = basicsql_post + sentence_sql+" \n"+ "on " + "a"+str(rownumsql-2)+"."+business_sql+"="+"a"+str(rownumsql-1)+"."+business_sql +"\n"+" LEFT JOIN \n"
           
  
            ##2. Temporale Differenz Features   
            for i in temporalmetric:
                tempmetric = i
                for y in temporalobject:
                    temporalobject_sql = y
                    for x in businessobject:
                        business_sql = x
                        sentencetemp_sql = "(SELECT " + tempmetric + "(" + temporalobject_sql + ")"+" AS " + tempmetric+temporalobject_sql+ ", " +business_sql +" FROM train_raw GROUP BY "+ business_sql +") " + "a"+ str(rownumsql) + "\n"
                        metricnamestemp = metricnamestemp.strip() + tempmetric+temporalobject_sql+", " 
                        rownumsql = rownumsql + 1
                        rownumtempsql = rownumtempsql + 1
                        basictempsql_post = basictempsql_post + sentencetemp_sql+" \n"+ "on " + "a"+str(rownumsql-2)+"."+business_sql+"="+"a"+str(rownumsql-1)+"."+business_sql +"\n"+" LEFT JOIN \n"          
            basictempsql_post = basictempsql_post[:-12]

            #Präambel und Temporllogik (differenzen bilden)#
            tempbez = metricnamestemp.split(',')

            tempsaetze = ""
            for index, firstelem in enumerate(tempbez):
                    if(index<(len(tempbez)-1)):
                        #saetze = saetze + "JULIANDAY("+elem+")" + " - " 
                        for index, elem in enumerate(tempbez): 
                            if(index<(len(tempbez)-1)):
                                tempsaetze = tempsaetze + "JULIANDAY("+firstelem+")" + " - " + "JULIANDAY("+elem+")" + " AS " "Diff"+str(firstelem)+str(elem)+ " , "
            basictempsql_pre = "SELECT "+tempsaetze + "a0."+business_sql + " FROM \n"

            ##3. Temporal Bestand Features   
            for i in metricobject:
                metric_sql = i
                for y in investigationobject:
                    investigation_sql = y
                    for x in businessobject:
                        business_sql = x
                        if metric_sql == "COUNT(DISTINCT":
                            metricnameststock = metric_sql + " " + investigation_sql + ")"+ " AS " + "DISTINCT"+investigation_sql +"stock" + ","
                            metricnameststock_fin = metricnameststock_fin + metricnameststock
                        else:
                            metricnameststock = metric_sql + "(" + investigation_sql + ")"+ " AS " + metric_sql + investigation_sql +"stock" + ","
                            metricnameststock_fin = metricnameststock_fin + metricnameststock
                        
                        basicstocksql_mid = "a." + business_sql +" FROM train_raw a \n left outer join (" \
                            + "SELECT DATE(" + "JULIANDAY("+temporalstockmetric[0]+ temporalobject[0]+")" + " - " + "((JULIANDAY("+temporalstockmetric[0]+ temporalobject[0] +")" +  "- JULIANDAY("+temporalstockmetric[1]+ temporalobject[0]+")) / 2 )) AS MEDIAN_DATE" + ",\n" \
                            + businessobject[0] + ", " + temporalstockmetric[0]+ temporalobject[0] + ", " +temporalstockmetric[1]+ temporalobject[0] + "\n FROM ("
           
            basicstocksql_post = "SELECT " + temporalstockmetric[0] + "(" + temporalobject[0] + ")" + " AS " + temporalstockmetric[0] + temporalobject[0] + ", " \
                + temporalstockmetric[1] + "(" + temporalobject[0] + ")" + " AS " + temporalstockmetric[1] + temporalobject[0] + ", "+businessobject[0] + " FROM train_raw GROUP BY " + businessobject[0]\
                    +"\n)\n group by " + businessobject[0] + ") b \n on a.msno=b.msno"+ "\n" \
                        + " WHERE " + temporalobject[0] + " BETWEEN MEDIAN_DATE AND " + temporalstockmetric[0]+ temporalobject[0]  +  " \n GROUP BY " + "a." + businessobject[0]
            SQLStock = "SELECT " + "\n" + metricnameststock_fin + basicstocksql_mid +basicstocksql_post
           
            #Ausgabe in Datei: letzte und erste Zeile Korrigiere und Temporale Objekte hinzufügen der Features Datei
            with open(r'cfg\features.cfg', 'w+') as fp:            
                # Preamble mit Spaltenbezeichnungen füllen
                preamble = "SELECT * FROM \n ( SELECT " + metricnames + tempsaetze +"a0."+business_sql + " FROM \n" 
                fp.writelines(preamble)
                fp.writelines(basicsql_post + basictempsql_post + ") z left join (" + SQLStock + ") l \n on z.msno = l.msno")

            #Ausgabe in Datei: letzte und erste Zeile Korrigiere und Temporale Objekte hinzufügen der Features Datei
            with open(r'cfg\features_temp.cfg', 'w+') as fp:            
                # Preamble mit Spaltenbezeichnungen füllen
                fp.writelines(basictempsql_pre)
                fp.writelines(basictempsql_post)

            with open(r'cfg\features_stock.cfg', 'w+') as fp:            
                # Preamble mit Spaltenbezeichnungen füllen
                fp.writelines(SQLStock)

        # SQLite Datenbank Funktionen zum Absetzen von Befehlen
        # 1. Profiling der Features
        def showprofile():
            global SERVER_NAME 
            global DATABASE_NAME 
            global USERNAME
            global PASSWORD
         
            with open(r'cfg\database.cfg') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    global databaseconfig
                    databaseconfig = row 

            SERVER_NAME = databaseconfig[0]
            DATABASE_NAME = databaseconfig[1]
            USERNAME = databaseconfig[2]
            PASSWORD = databaseconfig[3]
            connString = DATABASE_NAME
                    #f'DRIVER={{SQL Server}};'\
                    #f'SERVER={SERVER_NAME};'\
                    #f'DATABASE={DATABASE_NAME}'
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(connString)

            # Feature SQL vorbereiten
            with open(r'cfg\features.cfg', 'r+') as fp:    
                sqlstatement = fp.read().replace('\n', '')          
                #print(sqlstatement)
                fp.close

            if db.open():
                print('connect to SQL Server successfully')
                print('processing query...')
                SQL_STATEMENT = sqlstatement
                #SQL_STATEMENT = 'SELECT DST as Store_Code, COUNT(PARTNER) as [Sum of accounts] FROM dbo.hs_trans group by DST order by 2 desc'
                #SQL_STATEMENT = 'SELECT * FROM insurance_claims'
                qry = QSqlQuery(db)
                ##qry.prepare(sqlStatement)
                qry.exec(SQL_STATEMENT)

                model = QSqlQueryModel()
                model.setQuery(qry)
              
                self.tableView_SQL.setModel(model)

                ##Objekte auslesen
                i = 0
                while i < 20:
                    global bo_plot
                    global metr_plot
                    bo_plot.append(model.record(i).value("AVGregistered_via"))
                    metr_plot.append(i)
                    i = i+1
                
                ## Show Graph
                self.graphicsView.setTitle("<span style=\"color:black;font-size:8pt\">{}</span>".format("Durchschnittliche Registriertueber pro Kundennummer"))
                # resizing the plot window 
                self.graphicsView.resize(380, 330) 
                self.graphicsView.showFullScreen()
                self.graphicsView.windowTitle()



                self.graphicsView.setBackground('w')
                pen = pg.mkPen(color=(255, 0, 0)) 
                self.graphicsView.plot(metr_plot,bo_plot)
                    #[10,20,30,40,50],[10,10,20,30,40])
                    #list(bo_plot), list(metr_plot), pen=pen)#this line doesn't work
                db.close
                return True
            else:
                print('connection failed')
                return False       

        # 2. Speichern des CSV Exports
        def saveCSV():
            global SERVER_NAME
            global DATABASE_NAME
            global USERNAME
            global PASSWORD
            global connString
            global db
            connString = DATABASE_NAME
            sqlstatement = ''

            # Feature SQL vorbereiten
            with open(r'cfg\features.cfg', 'r+') as fp:    
                sqlstatement = fp.read().replace('\n', '') 
                fp.close         
                #print(sqlstatement)

            con = sqlite3.connect(DATABASE_NAME) 
            cur = con.cursor()
            k = cur.execute(sqlstatement) # Generiertes SQL ausführen
            
            #Header extrahieren für spätere Ausgabe
            headernames = list(map(lambda x: x[0], cur.description))
            # Ausgabe der Feature Matrix in CSV Datei
            with open(r'cfg\export.csv', "w+", newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(headernames)
                csv_writer.writerows(k)
            cur.close
            saveexportgmsg = QMessageBox()
            saveexportgmsg.setIcon(QMessageBox.Information)
            saveexportgmsg.setWindowTitle("Datensatz exportiert")
            saveexportgmsg.setText("Der Trainingsdatensatz wurde exportiert")
            saveexportgmsg.exec_()
            

        self.setObjectName("Dialog")
        self.resize(1480, 1000)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(130, 130, 1200, 800))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        ##Input Objects
        self.listWidget_2 = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setAcceptDrops(True)
        self.listWidget_2.setDragEnabled(False)
        #self.listWidget_2.setMinimumSize(QtCore.QSize(0, 400))
        self.gridLayout.addWidget(self.listWidget_2, 0, 1, 1, 1)

        ##Semantic feature builder
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        #self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        #self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setAcceptDrops(False)
        #self.listWidget.setMinimumSize(QtCore.QSize(0, 250))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        ## Generate Button 
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.pushButton_2.clicked.connect(generate_featureexpression) 
        #self.pushButton_2.clicked.connect(generate_temp_featureexpression) 

        ##Load Config Button
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(load_configuration_featuregenerator) 
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        ## Profiling SQL
        self.pushButton_profile = QtWidgets.QPushButton(self.gridLayoutWidget)
        #self.pushButton_profile.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ic_charts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_profile.setIcon(icon)
        self.pushButton_profile.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_profile.setObjectName("pushButton_3")
        self.pushButton_profile.clicked.connect(showprofile)
        self.gridLayout.addWidget(self.pushButton_profile, 2, 0, 1, 2)

        ##saveFeatures Button
        self.saveFeatures = QtWidgets.QPushButton(self.gridLayoutWidget)
        icon_savemap = QtGui.QIcon()
        icon_savemap.addPixmap(QtGui.QPixmap("ic_savemap.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveFeatures.setIcon(icon_savemap)
        self.saveFeatures.setIconSize(QtCore.QSize(25, 25))
        self.saveFeatures.setObjectName("Save Features")
        self.saveFeatures.clicked.connect(saveCSV) 
        self.gridLayout.addWidget(self.saveFeatures, 6, 0, 1, 2)

        ##Feature Text Label
        #self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        #font = QtGui.QFont()
        #font.setPointSize(12)
        #self.label_4.setFont(font)
        #self.label_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.label_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        #self.label_4.setText(" ")
        #self.label_4.setMinimumSize(0,150)
        #self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        #self.label_4.setObjectName("label_4")
        #self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        
        ## Tableview
        
        self.tableView_SQL = QtWidgets.QTableView(MainWindow)
        self.tableView_SQL.setGeometry(QtCore.QRect(50, 390, 830, 220))
        self.tableView_SQL.setObjectName("tableViewsql")
        self.tableView_SQL.setObjectName("label_3")
        #self.tableView_SQL.setMinimumSize(QtCore.QSize(0, 400))
        self.gridLayout.addWidget(self.tableView_SQL, 4, 0, 1, 1)
        
        ## Graphen
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        #self.graphicsView.setMinimumSize(QtCore.QSize(0, 400))
        self.gridLayout.addWidget(self.graphicsView, 4, 1, 1, 1)
        self.graphicsView = pg.PlotWidget(self.graphicsView)

        ##Labels / Headers Semantics and Input
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(400, 60, 150, 110))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(980, 60, 150, 110))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
   

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Feature Generierung"))
        self.pushButton_2.setText(_translate("Dialog", "Erzeuge Features"))
        self.pushButton.setText(_translate("Dialog", "Lade Konfiguration"))
        self.label.setText(_translate("Dialog", "Eingabeobjekte"))
        self.label_2.setText(_translate("Dialog", "Features in klartext"))
        self.pushButton_profile.setText(_translate("Dialog", "Erzeuge Featurematrix und Graph (Distributions, Min/Max, AVG, Mean, VAR etc.)"))
        self.saveFeatures.setText(_translate("Dialog","Features speichern"))

### Main Klasse - Hauptmenü
class Ui_Window(QMainWindow):
    def setupUi(self, Window):

        MainWindow.setObjectName("FeatureCase")
        MainWindow.resize(1480, 1000)
        #MainWindow.showMaximized()
        
        # def whoGotSelected(self, selection):
        # # Getting the selected button obj, taking the given text name.
        # # Print the name selected.
        #     print(f"Tool-Bar |{selection.text()}|")

        # icons = QtWidgets.QFileIconProvider()
        # toolbar.addAction(icons.icon(icons.Folder), 'Folder')
        # toolbar.addAction(icons.icon(icons.Desktop), 'Desktop')
        # toolbar.actionTriggered[QtWidgets.QAction].connect(whoGotSelected)
        
        ##Toolbar icons
        # featureeditor = QAction(QIcon('semanticicon.png'), 'Define Feature semantics', self)
        # featureeditor.setShortcut('Ctrl+E')
        # self.w = Ui_Dialog()
        # featureeditor.triggered.connect(lambda action: self.w.show())

        with open(r'cfg\businessobject_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global businessobject_text
                businessobject_text = row

        with open(r'cfg\temporalobject_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalobject_text
                temporalobject_text = row  

        with open(r'cfg\temporalmetric_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalmetric_text
                temporalmetric_text = row  

        with open(r'cfg\investigationobject_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global investigationobject_text
                investigationobject_text = row
        
        with open(r'cfg\propertyobject_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global propertyobject_text
                propertyobject_text = row

        with open(r'cfg\metricobject_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global metricobject_text
                metricobject_text = row

        with open(r'cfg\businessobject.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global businessobject
                businessobject = row

        with open(r'cfg\temporalobject.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalobject
                temporalobject = row  

        with open(r'cfg\temporalmetric.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalmetric
                temporalmetric = row  

        with open(r'cfg\investigationobject.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global investigationobject
                investigationobject = row
        
        with open(r'cfg\propertyobject.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global propertyobject
                propertyobject = row

        with open(r'cfg\metricobject.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global metricobject
                metricobject = row

        with open(r'cfg\temporalstockmetric.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalstockmetric
                temporalstockmetric = row  

        with open(r'cfg\temporalstockmetric_text.cfg') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                global temporalstockmetric_text
                temporalstockmetric_text = row  
    


        featureeditor = QAction(QIcon(r'assets\sequenceicon.png'), 'Feature Generator', self)
        featureeditor.setShortcut('Ctrl+S')
        self.s = Ui_Dialog()
        featureeditor.triggered.connect(lambda action: self.s.show())

        dbconfig = QAction(QIcon(r'assets\config_dbicon.png'), 'Database Configuration', self)
        dbconfig.setShortcut('Ctrl+D')
        self.c = Ui_Config()
        dbconfig.triggered.connect(lambda action: self.c.show())

        toolbar = MainWindow.addToolBar('Featureeditor')
        toolbar.addAction(featureeditor)     
        toolbar = MainWindow.addToolBar('Databaseconfiguration')
        toolbar.addAction(dbconfig)     

        ##DB Browser
        self.tableView = QtWidgets.QTableView(MainWindow)
        self.tableView.setGeometry(QtCore.QRect(20, 640, 1361, 331))
        self.tableView.setObjectName("tableView")

        def connect_db():
            global SERVER_NAME
            global DATABASE_NAME
            global USERNAME
            global PASSWORD
            global connString
            global db


            with open(r'cfg\database.cfg') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    global databaseconfig
                    databaseconfig = row 

            SERVER_NAME = databaseconfig[0]
            DATABASE_NAME = databaseconfig[1]
            USERNAME = databaseconfig[2]
            PASSWORD = databaseconfig[3]
            connString = DATABASE_NAME
                    #f'DRIVER={{SQL Server}};'\
                    #f'SERVER={SERVER_NAME};'\
                    #f'DATABASE={DATABASE_NAME}'
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(connString)
          
            if db.open():
                print('connect to Database successfully')
                print('processing query...')
                SQL_STATEMENT = 'SELECT * FROM train_raw limit 5000'
                qry = QSqlQuery(db)
                ##qry.prepare(sqlStatement)
                qry.exec(SQL_STATEMENT)
                
                model = QSqlQueryModel()
                model.setQuery(qry)
              
                self.tableView.setModel(model)
                for column in range(model.columnCount()):
                    QListWidgetItem(QIcon(''), model.headerData(column, QtCore.Qt.Horizontal), self.myListWidget2)
                    #print(model.headerData(column, QtCore.Qt.Horizontal))
                #View = QTableView()

                #Aktualisiere die Zeitreihenattribute (Datentyp: DATE)   + Wichtig für die Extraktion der Zeitfeatures          
                qry2 = QSqlQuery(db)
                qry2.exec('select sql from sqlite_master')
                model2 = QSqlQueryModel()
                model2.setQuery(qry2)
                ddltext = model2.record(0).value(0)
                x = ddltext.split('\n')
                str_match = [s for s in x if "date" in s]
                newstr = [s.strip('\t"') for s in str_match]
                newstr2 = [s.replace('"\tTEXT,', '') for s in newstr]
                ##print(x.group())
                self.cb.addItems(newstr2)

                return True
            else:
                print('connection failed')
                return False       
        
        ##Save Feature objects
        def saveSettings():
            self.myListWidget3.setCurrentRow(0)
            self.myListWidget4.setCurrentRow(0)
            self.cb.itemText(0)
            self.myListWidget6.setCurrentRow(0)
            self.myListWidget8.setCurrentRow(0)
            metricobject = ""
            businessobject = ""
            investigationobject = ""
            propertyobject = ""
            temporalmetric = ""
            temporalobject = ""
            businessobject_text = ""
            investigationobject_text = ""
            propertyobject_text = ""
            metricobject_text = ""
            temporalmetric_text = ""
            temporalobject_text = ""

            #  # investigationobject
            # for x in range(self.myListWidget6.count()):
            #      self.myListWidget6.setCurrentRow(x)
            #      investigationobject = self.myListWidget6.currentItem().text()

            #  ## Businessobject
            for y in range(self.myListWidget3.count()):
                  self.myListWidget3.setCurrentRow(y)
                  businessobject = self.myListWidget3.currentItem().text() + ',' + businessobject
            
            #  ## investigationobject
            for y in range(self.myListWidget4.count()):
                  self.myListWidget4.setCurrentRow(y)
                  investigationobject = self.myListWidget4.currentItem().text() + ',' + investigationobject
            
            
            #  ## Propertyobject
            for y in range(self.myListWidget6.count()):
                  self.myListWidget6.setCurrentRow(y)
                  propertyobject = self.myListWidget6.currentItem().text() + ',' + propertyobject
            
            #  ## Metricobject
            for y in range(self.myListWidget7.count()):
                  self.myListWidget7.setCurrentRow(y)
                  metricobject = self.myListWidget7.currentItem().text() + ',' + metricobject

            #  ## Businessobject_text
            for y in range(self.myListWidget8.count()):
                  self.myListWidget8.setCurrentRow(y)
                  businessobject_text = self.myListWidget8.currentItem().text() + ',' + businessobject_text
                   

            #  ## investigationobject_text
            for y in range(self.myListWidget9.count()):
                  self.myListWidget9.setCurrentRow(y)
                  investigationobject_text = self.myListWidget9.currentItem().text() + ',' + investigationobject_text

            #  ## Propertyobject_text
            for y in range(self.myListWidget10.count()):
                  self.myListWidget10.setCurrentRow(y)
                  propertyobject_text = self.myListWidget10.currentItem().text() + ',' + propertyobject_text
                   
            #  ## metricobject_text
            for y in range(self.myListWidget11.count()):
                  self.myListWidget11.setCurrentRow(y)
                  metricobject_text = self.myListWidget11.currentItem().text() + ',' + metricobject_text
                   
            #  ## temporalobject_text
            for y in range(self.myListWidget12.count()):
                  self.myListWidget12.setCurrentRow(y)
                  temporalobject_text = self.myListWidget12.currentItem().text() + ',' + temporalobject_text

            ## Temporalobject_text
            temporalobject_text = "Datum"

            ## Save Objects
            f = open(r'cfg\businessobject.cfg', "w")
            f.write(businessobject[:-1])
            f.close()

            f = open(r'cfg\investigationobject.cfg', "w")
            f.write(investigationobject[:-1])
            f.close()

            f = open(r'cfg\propertyobject.cfg', "w")
            f.write(propertyobject[:-1])
            f.close()

            f = open(r'cfg\metricobject.cfg', "w")
            f.write(metricobject[:-1])
            f.close()

            f = open(r'cfg\businessobject_text.cfg', "w")
            f.write(businessobject_text[:-1])
            f.close()

            f = open(r'cfg\investigationobject_text.cfg', "w")
            f.write(investigationobject_text[:-1])
            f.close()

            f = open(r'cfg\propertyobject_text.cfg', "w")
            f.write(propertyobject_text[:-1])
            f.close()

            f = open(r'cfg\metricobject_text.cfg', "w")
            f.write(metricobject_text[:-1])
            f.close()

            f = open(r'cfg\temporalobject_text.cfg', "w")
            f.write(temporalobject_text)
            f.close()

        def reset_configuration():
            self.cb.setCurrentIndex(0)
            self.myListWidget3.clear()
            self.myListWidget4.clear()
            self.myListWidget6.clear()
            self.myListWidget7.clear()

            self.myListWidget8.clear()
            self.myListWidget9.clear()
            self.myListWidget10.clear()
            self.myListWidget11.clear()
            self.myListWidget12.clear()

        ## Layout befüllen
        ## Feature-engine Icon
        self.label_4 = QtWidgets.QLabel(MainWindow)
        self.label_4.setGeometry(QtCore.QRect(1160, 60, 201, 71))
        self.label_4.setStyleSheet("")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(r'assets\featureengine.png'))
        self.label_4.setObjectName("label_4")


        ##Connect Database Button
        icon_connect = QtGui.QIcon()
        icon_connect.addPixmap(QtGui.QPixmap(r'assets\ic_connectdb.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(290, 530, 481, 71))
        self.pushButton.setObjectName("Verbinde Datenbank")
        self.pushButton.setIcon(icon_connect)
        self.pushButton.setIconSize(QtCore.QSize(42, 42))
        self.pushButton.clicked.connect(connect_db) 

        ##Save settings Button
        icon_savemap = QtGui.QIcon()
        icon_savemap.addPixmap(QtGui.QPixmap(r'assets\ic_savemap.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton = QtWidgets.QPushButton(MainWindow)
        self.saveButton.setGeometry(QtCore.QRect(1180, 160, 181, 331))
        self.saveButton.setObjectName("Save Settings")
        self.saveButton.setIcon(icon_savemap)
        self.saveButton.setIconSize(QtCore.QSize(42, 42))
        self.saveButton.clicked.connect(saveSettings) 

        ##Reset configuration lists Button
        icon_reset = QtGui.QIcon()
        icon_reset.addPixmap(QtGui.QPixmap(r'assets\ic_resetmap.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetButton = QtWidgets.QPushButton(MainWindow)
        self.resetButton.setGeometry(QtCore.QRect(800, 530, 361, 71))
        self.resetButton.setObjectName("Reset cofiguration")
        self.resetButton.setIcon(icon_reset)
        self.resetButton.setIconSize(QtCore.QSize(42, 42))
        self.resetButton.clicked.connect(reset_configuration) 

        self.myLayout = QHBoxLayout()
        
        ##Dataset
        self.myListWidget2 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget2.setAcceptDrops(False)
        self.myListWidget2.setDragEnabled(True)
        self.myListWidget2.setGeometry(QtCore.QRect(20, 80, 251, 531))
        self.myLayout.addWidget(self.myListWidget2)

        ##Assign Columns
        self.myListWidget3 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget3.setGeometry(QtCore.QRect(460, 160, 311, 51))
        self.myListWidget3.setObjectName("myListWidget3")
        self.myListWidget3.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget3)

        self.myListWidget4 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget4.setGeometry(QtCore.QRect(460, 230, 311, 51))
        self.myListWidget4.setObjectName("myListWidget4")
        self.myListWidget4.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget4)


        self.myListWidget6 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget6.setGeometry(QtCore.QRect(460, 300, 311, 51))
        self.myListWidget6.setObjectName("myListWidget6")
        self.myListWidget6.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget6)


        self.myListWidget7 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget7.setGeometry(QtCore.QRect(460, 370, 311, 51))
        self.myListWidget7.setObjectName("listView_7")
        self.myListWidget7.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget7)

        ##Zeitreihenobjekte
        self.cb = QComboBox(MainWindow)
        self.cb.setGeometry(QtCore.QRect(460, 440, 311, 51))
        #self.cb.addItems(["date", "transaction_date", "membership_expire_date"])
        ##self.cb.currentIndexChanged.connect(self.selectionchange)
        self.myLayout.addWidget(self.cb)

        ## Toolicon
        self.toolButton_2 = QtWidgets.QToolButton(MainWindow)
        self.toolButton_2.setGeometry(QtCore.QRect(290, 230, 151, 51))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r'assets\ic_investigation.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(MainWindow)
        self.toolButton_3.setGeometry(QtCore.QRect(290, 160, 151, 51))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r'assets\ic_business.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon1)
        self.toolButton_3.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(MainWindow)
        self.toolButton_4.setGeometry(QtCore.QRect(290, 300, 151, 51))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r'assets\ic_property.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_4.setObjectName("toolButton_5")

        self.toolButton_5 = QtWidgets.QToolButton(MainWindow)
        self.toolButton_5.setGeometry(QtCore.QRect(290, 370, 151, 51))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r'assets\ic_metric.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5.setIcon(icon2)
        self.toolButton_5.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_5.setObjectName("toolButton_4")
       
        self.toolButton_6 = QtWidgets.QToolButton(MainWindow)
        self.toolButton_6.setGeometry(QtCore.QRect(290, 440, 151, 51))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r'assets\ic_sequence.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_6.setIcon(icon4)
        self.toolButton_6.setIconSize(QtCore.QSize(25, 25))
        self.toolButton_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolButton_6.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButton_6.setObjectName("toolButton_6")

        ## Style
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        ## Column header 
       
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(540, 125, 141, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setFont(font)
        self.label_2.setGeometry(QtCore.QRect(330, 125, 141, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setFont(font)
        self.label_3.setGeometry(QtCore.QRect(920, 125, 161, 19))
        self.label_3.setObjectName("label_3")


        ##Objektbezeichnungen
        self.myListWidget8 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget8.setGeometry(QtCore.QRect(800, 160, 361, 51))
        self.myListWidget8.setObjectName("myListWidget8")
        self.myListWidget8.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget8)

        self.myListWidget9 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget9.setGeometry(QtCore.QRect(800, 230, 361, 51))
        self.myListWidget9.setObjectName("myListWidget9")
        self.myListWidget9.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget9)

        self.myListWidget10 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget10.setGeometry(QtCore.QRect(800, 300, 361, 51))
        self.myListWidget10.setObjectName("myListWidget10")
        self.myListWidget10.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget10)

        self.myListWidget11 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget11.setGeometry(QtCore.QRect(800, 370, 361, 51))
        self.myListWidget11.setObjectName("myListWidget11")
        self.myListWidget11.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget11)

        self.myListWidget12 = QtWidgets.QListWidget(MainWindow)
        self.myListWidget12.setGeometry(QtCore.QRect(800, 440, 361, 51))
        self.myListWidget12.setObjectName("myListWidget12")
        self.myListWidget12.setAcceptDrops(True)
        self.myLayout.addWidget(self.myListWidget12)

        # Lade Inhalte für Labeling
        for i in businessobject_text:
            rownum = 0
            self.myListWidget8.insertItem(rownum,i.strip())
            item = self.myListWidget8.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in investigationobject_text:
            rownum = 0
            self.myListWidget9.insertItem(rownum,i.strip())
            item = self.myListWidget9.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in propertyobject_text:
            rownum = 0
            self.myListWidget10.insertItem(rownum,i.strip())
            item = self.myListWidget10.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in metricobject_text:
            rownum = 0
            self.myListWidget11.insertItem(rownum,i.strip())
            item = self.myListWidget11.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in temporalobject_text:
            rownum = 0
            self.myListWidget12.insertItem(rownum,i.strip())
            item = self.myListWidget12.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in businessobject:
            rownum = 0
            self.myListWidget3.insertItem(rownum,i.strip())
            item = self.myListWidget3.item(rownum)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            rownum += 1

        for i in investigationobject:
            rownum = 0
            self.myListWidget4.insertItem(rownum,i.strip())
            rownum += 1

        for i in propertyobject:
            rownum = 0
            self.myListWidget6.insertItem(rownum,i.strip())
            rownum += 1

        for i in metricobject:
            rownum = 0
            self.myListWidget7.insertItem(rownum,i.strip())
            rownum += 1


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Hauptmenue", "Hauptmenue"))
        self.pushButton.setText(_translate("Verbinde Datenbank", "Verbinde Datenbank"))  
        self.saveButton.setText(_translate("Speichern", "Speichern"))   
        self.resetButton.setText(_translate("Zuruecksetzen", "Zuruecksetzen")) 
        self.toolButton_2.setText(_translate("Dialog", "Eigenschaft (kategorial)"))
        self.toolButton_3.setText(_translate("Dialog", "Geschäftsobjekt"))
        self.toolButton_4.setText(_translate("Dialog", "Eigenschaft (stetig)"))
        self.toolButton_5.setText(_translate("Dialog", "Metrik"))
        self.toolButton_6.setText(_translate("Dialog", "Zeitreihenobjekt"))

        self.label.setText(_translate("Objects", "Spalten Zuordnung"))
        self.label_2.setText(_translate("Object", "Objekttyp"))
        self.label_3.setText(_translate("Object name", "Objektbezeichnung"))
        self.toolButton_2.setFont(QFont('Arial', 10))
        self.toolButton_3.setFont(QFont('Arial', 10))
        self.toolButton_4.setFont(QFont('Arial', 10))
        self.toolButton_5.setFont(QFont('Arial', 10))
        self.toolButton_6.setFont(QFont('Arial', 10))

        self.myListWidget8.setFont(QFont('Arial', 8))
        self.myListWidget9.setFont(QFont('Arial', 8))
        self.myListWidget10.setFont(QFont('Arial', 8))
        self.myListWidget11.setFont(QFont('Arial', 8))
        self.myListWidget12.setFont(QFont('Arial', 8))
        
        self.myListWidget3.setFont(QFont('Arial', 8))
        self.myListWidget4.setFont(QFont('Arial', 8))
        self.myListWidget6.setFont(QFont('Arial', 8))
        self.myListWidget7.setFont(QFont('Arial', 8))
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

