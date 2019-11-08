import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import pymysql
from PyQt5.uic import loadUiType

window1 ,_ = loadUiType('SchoolManagement.ui')
registerUi ,_ = loadUiType('student_registration.ui')


def general_message(title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Question)
        msg.exec_()


class MainAll(QMainWindow, window1):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #self.tabWidget.tabBar().setVisible(False)
        self.Handle_all_btn()
        #self.Register_Student_tab()


    def Handle_all_btn(self):
        self.actionRegister_Student.triggered.connect(self.show_studentReg)
        # self.actionEdit_Student_Details.triggered.connect(self.Edit_student_tab)
        # self.pushButton.clicked.connect(self.Register_Student_to_db)


    def show_studentReg(self):
        self.window = StudentRegistration()
        self.window.show()




def StudentRegistration(QMainWindow, registerUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleBTN()
        self.labelChange()



    def labelChange(self):
        if MainAll.show_studentReg:
            self.label.setText('STUDENT REGISTRATION PAGE')

        else:
            self.label.setText('STUDENT Edit PAGE')



    def handleBTN(self):
        self.comboBox.addItems(["Abia","Adamawa","Akwa Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross","River","Delta","Ebonyi","Enugu","Edo","Ekiti","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Lagos","Nasarawa","Niger","Ogun","Ondo","Osun","Oyo","Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"])
        for num in range(1, 100):
            self.comboBox_11.addItem(str(num))

        self.pushButton.clicked.connect(self.Register_Student_to_db)





    # def Edit_student_tab(self):
    #     # self.tab_3.close()
    #     # self.tab_4.close()
    #     # self.tab_5.close()
    #     self.tab_2.show()
    #     self.groupBox.setEnabled(False)
    #     self.groupBox_2.setEnabled(True)

    # def search_student_inDB(self):
    #     searchId = self.comboBox_12.currentText()
    #     self.db = pymysql.connect(
    #         host="localhost",
    #         user="root",
    #         password="Sunlabi001.",
    #         db="schoolmanagement",)
            
    #     self.cur = self.db.cursor()

    #     self.cur.execute('SELECT * FROM studentregistration WHERE student_firstname=%s', searchId)
    #     dbb = self.cur.fetchAll()
    #     print(dbb)


    def Register_Student_to_db(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_6.text()
        address = self.lineEdit_7.text()
        #Dob = self.dateEdit.text()
        sex = self.radioButton.isChecked()
        if sex == True:
            sex = "Male"
        else:
            sex = "Female"
        state = self.comboBox.currentText()
        previous_sch = self.lineEdit_10.text()
        age = self.comboBox_11.currentText()

        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        dbb = self.cur.execute('''INSERT INTO studentregistration(student_firstname, student_lastname, student_address, student_sex, student_state, student_previoussch,student_age)
        VALUES (%s, %s, %s, %s, %s, %s, %s)''', ( fname, lname, address, sex, state, previous_sch, age))
        print(fname,lname,sex,age)
        self.db.commit()
        self.db.close()
        general_message('User Registered', 'User Successfully Registered to Database')
        self.close()
        


    # def Register_Student_tab(self):
    #     self.tab_4.close()
    #     self.tab_3.close()
    #     self.tab_5.close()
    #     self.tab_2.show()
    #     self.groupBox_2.setEnabled(False)
        
        

      


def RunAll():
    app = QApplication(sys.argv)
    window = MainAll()
    window.show()
    app.exec()


if __name__ == '__main__':
    RunAll()
