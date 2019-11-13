import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import pymysql
from PyQt5.uic import loadUiType
from index import MainApp

window1 ,_ = loadUiType('SchoolManagement.ui')
registerUi ,_ = loadUiType('student_registration.ui')
editstudent , _= loadUiType('student_registration_edit.ui')
admissionTab ,_ = loadUiType('admissiontab.ui')


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
        self.actionEdit_Student_Details.triggered.connect(self.Edit_student_tab)
        self.actionDelete.triggered.connect(self.Edit_student_tab)
        self.actionAdmit_Student.triggered.connect(self.showAdmission)
        self.actionEdit_Studet_Admitted.triggered.connect(self.showeditadmission)
        self.actionTimeTable.triggered.connect(self.ShowTimeTable)
        # self.pushButton.clicked.connect(self.Register_Student_to_db)

    def ShowTimeTable(self):
        self.window = MainApp()
        self.window.show()
    def Edit_student_tab(self):
        self.window = EditStudentDeatils()
        self.window.show() 


    def show_studentReg(self):
        self.window = StudentRegistration()
        self.window.show()

    def showAdmission(self):
        self.window =AdmissionTab()
        self.window.show()
    def showeditadmission(self):
        self.window = EditDeleteAdmiision()
        self.window.show()
        




class StudentRegistration(QMainWindow, registerUi):
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
        self.cur.execute('''INSERT INTO studentregistration(student_firstname, student_lastname, student_address, student_sex, student_state, student_previoussch,student_age)
        VALUES (%s, %s, %s, %s, %s, %s, %s)''', ( fname, lname, address, sex, state, previous_sch, age))
        self.db.commit()
        self.db.close()
        general_message('User Registered', 'User Successfully Registered to Database')
        self.close()
        
class EditStudentDeatils(QWidget, editstudent):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.searchStudent)
        self.pushButton_3.clicked.connect(self.DeteleStudent)

        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()

        searchId = self.comboBox_11.currentText()
        self.cur.execute('SELECT student_firstname from studentregistration')
        name = self.cur.fetchall()

        for names in name:
            self.comboBox_11.addItem(str(names[0]))

    def searchStudent(self):
        StudentsearchID = self.comboBox_11.currentText()
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('SELECT * FROM studentregistration WHERE student_firstname=%s', StudentsearchID)
        Sdetail = self.cur.fetchall()
        print(Sdetail)
        
        for detail in Sdetail:
            self.lineEdit.setText(detail[1])
            self.lineEdit_6.setText(detail[2])
            self.lineEdit_7.setText(detail[3])
            self.comboBox.addItem(str(detail[6]))
            self.lineEdit_10.setText(detail[7])
            self.comboBox_12.addItem(str(detail[8]))



    def DeteleStudent(self):
        DeleteId1 = self.lineEdit.text()
        DeleteId2 = self.lineEdit_6.text()

        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()

        SQL = ''' DELETE FROM studentregistration WHERE student_firstname=%s AND student_lastname=%s '''
        self.cur.execute(SQL, [DeleteId1, DeleteId2])
        self.db.commit()
        self.db.close()
        general_message('User Deleted', 'Student has been succesfully deleted')
        self.close()



########################################################
###########      AdmissionTab       ####################
########################################################

class AdmissionTab(QMainWindow, admissionTab):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.show()
        self.pushButton_4.clicked.connect(self.searchEdit)
        self.pushButton_5.clicked.connect(self.AdmitToClass)

    #######################################
    ####     Connecting to db          ####

        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('SELECT student_firstname FROM studentregistration' )
        Sdetail = self.cur.fetchall()

        for detail in Sdetail:
            self.comboBox_3.addItem(str(detail[0]))

    def searchEdit(self):
        searchId = self.comboBox_3.currentText()
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('SELECT * FROM studentregistration WHERE student_firstname=%s', searchId )
        DBB = self.cur.fetchall()
        for i in DBB:
            self.lineEdit_3.setText(str(i[1])+ ' ' + str((i[2])))

    def AdmitToClass(self):
        fname = self.lineEdit_3.text()
        classAdmitTo = self.comboBox_4.currentText()
        sch = self.comboBox_7.currentText()
        year = self.comboBox_8.currentText()
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('''INSERT INTO admissionlist (student_name, class_admitted_to, sch_admitted_to, year_of_admission) 
            VALUES(%s, %s, %s, %s)''', (fname, classAdmitTo, sch, year))
        self.db.commit()
        self.db.close()
        general_message('Admitted', 'Student Succesfully admitted to ' + classAdmitTo)
        self.close()
        # except:
        #     general_message('User Exist', 'User already admitted before, please Check details')



EditAdmission, _ = loadUiType('edit_deleteAdmission.ui')

class EditDeleteAdmiision(QMainWindow, EditAdmission):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.searchAdmissionList)
        self.pushButton_6.clicked.connect(self.edit_deleteAdmission)
        self.pushButton_7.clicked.connect(self.deleteAdm)



        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('SELECT student_name FROM admissionlist')
        dbb = self.cur.fetchall()

        for i in dbb:
            self.comboBox_3.addItem(str(i[0]))

    def searchAdmissionList(self):
        searchId = self.comboBox_3.currentText()
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        
        self.cur.execute(''' SELECT * FROM admissionlist WHERE student_name=%s ''', searchId)
        DBB = self.cur.fetchall()

        for i in DBB:
            self.lineEdit_3.setText(str(i[1]))
            self.lineEdit_4.setText(str(i[2]))
            self.lineEdit_5.setText(str(i[3]))
            self.lineEdit_6.setText(str(i[4]))

    def edit_deleteAdmission(self, btnpressed):
        searchId = self.comboBox_3.currentText()
        fname = self.lineEdit_3.text()
        classnew = self.lineEdit_4.text()
        scnew = self.lineEdit_5.text()
        year = self.lineEdit_6.text()
        print(btnpressed)

        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="Sunlabi001.",
            db="schoolmanagement",)
            
        self.cur = self.db.cursor()
        self.cur.execute('''UPDATE admissionlist SET student_name=%s, class_admitted_to=%s, sch_admitted_to=%s, year_of_admission=%s WHERE student_name=%s ''',
        (fname,classnew,scnew,year, searchId))
        dbb = self.cur.fetchall()
        self.db.commit()
        self.db.close()
        general_message('User Updated', fname + ' has been succesfully Updated')
        self.close()


    def deleteAdm(self):
        # msg = QMessageBox.Warning(self, 'Delete User', 'This User will be Parmanently deleted From the school record', QMessageBox.Yes | QMessageBox.No)
        # if msg == QMessageBox.Yes:
        deletId = self.comboBox_3.currentText()
        self.db = pymysql.connect(
                host="localhost",
                user="root",
                password="Sunlabi001.",
                db="schoolmanagement",)

        self.cur = self.db.cursor()
        sql = '''DELETE FROM admissionlist WHERE student_name=%s '''
        self.cur.execute(sql, [deletId])
        self.db.commit()
        general_message('User', deletId +' has been succuessfull deleted from Admission list')
        self.close()

    

#delete from all db when deleted from one
        

      


def RunAll():
    app = QApplication(sys.argv)
    window = MainAll()
    window.show()
    app.exec()


if __name__ == '__main__':
    RunAll()
