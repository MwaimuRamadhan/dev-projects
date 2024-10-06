import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import os.path
import json
from deepface import DeepFace
import cv2



class Ui_MainWindow(QtWidgets.QMainWindow):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UI_FILE = os.path.join(BASE_DIR, 'system_version2.ui')
    db_path = os.path.join(BASE_DIR, 'knof1.db')
    dbConnection = ''


    def initDBConnection(self):
        self.dbConnection = sqlite3.connect(self.db_path)
        #prepareDBTable()
        pass

    # def prepareDBTable(self):
    #     query = """CREATE TABLE IF NOT EXISTS 'employees'(
    #                 "FIRST NAME" TEXT,
    #                 "SECOND NAME" TEXT,
    #                 "IMAGE" BLOB)"""
    #     #query ='SELECT * FROM TABLE employees'
    #     results = self.dbConnection.execute(query)


    # def insertRowInDB(self,rowData):
    #     qr = " INSERT INTO employee_knof(FIRST NAME, SECOND NAME, IMAGE) " \
    #          "values(imuu,platnum,img1.jpg)"
    #     self.dbConnection.execute(qr, rowData)
    #     self.dbConnection.commit()



    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        uic.loadUi(self.UI_FILE, self)
        self.next_row = 0
        self.viewButton.clicked.connect(self.readTableData)
        self.showButton.clicked.connect(self.show_data)
        self.nextButton.clicked.connect(self.next_data)
        self.duplicatButton.clicked.connect(self.duplicate)
        self.initDBConnection()






    def readTableData(self):
        results = self.dbConnection.cursor().execute('select * from employee_knof')
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()
        for row_no, row_data in enumerate(results):
            self.tableWidget.insertRow(row_no)
            for col_no, col_data in enumerate(row_data):
                item = str(col_data)
                if (col_no == columnCount -1):
                    item = bytearray(col_data)
                    item1 = self.getImageLabel(item)
                    self.tableWidget.setCellWidget(row_no, col_no, item1)
                else:
                    self.tableWidget.setItem(row_no, col_no, QtWidgets.QTableWidgetItem(item))
            self.tableWidget.verticalHeader().setDefaultSectionSize(80)

    def show_data(self):
        results = self.dbConnection.cursor().execute('select * from employee_knof')
        rowCount = self.tableWidget.rowCount()
        columnCount = self.tableWidget.columnCount()
        print('onyesha', list(results))
        for row_no, row_data in enumerate(results):
            print('row_no', row_no, 'row_data', row_data)
            #self.tableWidget.insertRow(row_no)
            if row_no == self.next_row:
                for col_no, col_data in enumerate(row_data):
                    item = str(col_data)
                    if col_no == 0:
                        self.fname_label.setText(item)
                    if col_no == 1:
                        self.sname_label.setText(item)
                    if col_no == 2:
                        self.lname_label.setText(item)
                    if col_no == 3:
                        self.age_label.setText(item)
                    if col_no == 4:
                        self.gender_label.setText(item)
                    if col_no == 5:
                        self.pbook_label.setText(item)
                    if col_no == columnCount - 1:
                        item = bytearray(col_data)
                        self.p1 = item
                        # item1 = self.getImageLabel(item)
                        # print(item1)
                        # self.tableWidget.setCellWidget(self.image1, item1)
                        # self.image1_label = QtWidgets.QLabel(self.centralWidget())
                        self.image1_label.setText('')
                        self.image1_label.setScaledContents(True)
                        self.pixel = QtGui.QPixmap()
                        self.pixel.loadFromData(item, 'jpg')
                        self.image1_label.setPixmap(self.pixel)
                        self.rowDup1 = row_no
            if row_no == self.next_row+1:
                for col_no, col_data in enumerate(row_data):
                    #('umeonaje', col_data)                #
                    item = str(col_data)
                    if col_no == 0:
                        self.fname2_label.setText(item)
                    if col_no == 1:
                        self.sname2_label.setText(item)
                    if col_no == 2:
                        self.lname2_label.setText(item)
                    if col_no == 3:
                        self.age2_label.setText(item)
                    if col_no == 4:
                        self.gender2_label.setText(item)
                    if col_no == 5:
                        self.pbook2_label.setText(item)
                    if col_no == columnCount - 1:
                        item = bytearray(col_data)
                        #print(item)
                        self.p2 = item
                        item1 = self.getImageLabel(item)
                       # print(item1)
                #         # self.tableWidget.setCellWidget(self.image1, item1)
                #         # self.image1_label = QtWidgets.QLabel(self.centralWidget())
                        self.image2_label.setText('')
                        self.image2_label.setScaledContents(True)
                        self.pixel = QtGui.QPixmap()
                        self.pixel.loadFromData(item, 'jpg')
                        self.image2_label.setPixmap(self.pixel)
                        self.rowDup2 = row_no
    def next_data(self):
        print('imeingia', self.next_row)
        self.results = self.dbConnection.cursor().execute('select * from employee_knof')
        self.rowCount = self.tableWidget.rowCount()
        Ui_MainWindow.show_data(self)
        #('kabla', self.next_row, self.next_row+1)
        if self.next_row == 0:
            print('mara ya  kwanza')
        self.next_row=self.next_row+1
        print('inaondoka',self.next_row)
        print('****************************************************')

    def duplicate(self):
        rst = self.dbConnection.cursor().execute('select * from employee_knof')
        colcount = self.tableWidget.columnCount()
        #print('ndio hiiyo', self.rowDup1, self.rowDup2)
        for id, data in enumerate(rst):
            if id == self.rowDup1:
                for col, coldata in enumerate(data):
                    if col == colcount -1:
                        self.img1 = coldata
                        self.img1arr = np.frombuffer(self.img1, np.uint8)
                        self.image1 = cv2.imdecode(self.img1arr, cv2.IMREAD_COLOR)

            if id == self.rowDup2:
                for col, coldata in enumerate(data):
                    if col == colcount - 1:
                        self.img2 = coldata
                        self.img2arr = np.frombuffer(self.img2, np.uint8)
                        self.image2 = cv2.imdecode(self.img2arr, cv2.IMREAD_COLOR)
            #print('hii ndio image1:',type(self.image1),(self.image1))
            #print('hii ndio image1:',type(self.image2),(self.image2))
        self.duplicate = DeepFace.verify(self.image1, self.image2)
        print(self.duplicate)
        msg = QMessageBox()
        msg.setWindowTitle('DUPLICATE RESULTS')
        msg.setText(f'Same person??:{self.duplicate["verified"]}')
        x = msg.exec_()



    def getImageLabel(self, image):
        imglabel = QtWidgets.QLabel(self.centralWidget())
        imglabel.setText("")
        imglabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'jpg')
        #print('passed2')
        imglabel.setPixmap(pixmap)
        return imglabel


if __name__== '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    #window.getImageLabel('imuuKido.jpg')
    window.show()
    sys.exit(app.exec_())

