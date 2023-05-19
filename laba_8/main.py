import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
QTabWidget, QAbstractScrollArea,
QVBoxLayout, QHBoxLayout,
QTableWidget, QGroupBox,
QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    
    def __init__(self):
        
        super(MainWindow, self).__init__()
        
        self._connect_to_db()
        
        self.setWindowTitle("Shedule")
        
        self.vbox = QVBoxLayout(self)
        
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        
        self._create_shedule_tab()
        self._create_subjects_table()
        self._create_teacher_table()


    def _connect_to_db(self):
        
        self.conn = psycopg2.connect(database="schedule_bot", user="postgres", password="justdoit8", host="localhost", port="5432")
        
        self.cursor = self.conn.cursor()
        
        
    def _create_shedule_tab(self):
        
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")
        
        
        self.monday_gbox = QGroupBox("Monday")
        self.Tuesday_gbox = QGroupBox("Tuesday")
        self.Wednesday_gbox = QGroupBox("Wednesday")
        self.Thursday_gbox = QGroupBox("Thursday")
        self.Friday_gbox = QGroupBox("Friday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        
        self.tabs_days1 = QTabWidget(self)
        self.shbox1.addWidget(self.tabs_days1)
    
        
        self.monday_tab = QWidget(self)
        self.tabs_days1.addTab(self.monday_tab, "Monday")
        self.Tuesday_tab = QWidget(self)
        self.tabs_days1.addTab(self.Tuesday_tab, "Tuesday")
        self.Wednesday_tab = QWidget(self)
        self.tabs_days1.addTab(self.Wednesday_tab, "Wednesday")
        self.Thursday_tab = QWidget(self)
        self.tabs_days1.addTab(self.Thursday_tab, "Thursday")
        self.Friday_tab = QWidget(self)
        self.tabs_days1.addTab(self.Friday_tab, "Friday")
        
        self._create_monday_table()
        self._create_Tuesday_table()
        self._create_Wednesday_table()
        self._create_Thursday_table()
        self._create_Friday_table()
        
        self.update_shedule_button = QPushButton("Update")
     
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)
        
        self.shedule_tab.setLayout(self.svbox)
    
    def _create_subjects_table(self):
        
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")
        
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        
        self.subject_table = QTableWidget()

        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Name"])
        
        self._update_subject_table()
        
        self.svbox = QVBoxLayout()
        self.svbox.addWidget(self.subject_table)

        self.subject_tab.setLayout(self.svbox)
        
    def _update_subject_table(self):
        
        self.cursor.execute("SELECT * FROM subject;")
        records = list(self.cursor.fetchall())
 
        self.subject_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(1):
                self.subject_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")

            self.subject_table.setCellWidget(i, 1, joinButton)
            self.subject_table.setCellWidget(i, 2, DeleteButton)
            
            # Для изменения Name в таблице subject автоматически удалятся все преподы и пары с таким предметом(subject)!
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'subject', data))
            
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('subject', data))

            self.subject_table.resizeRowsToContents()
            
        Add_Button = QPushButton("ADD")
        self.subject_table.setCellWidget(i+1, 1, Add_Button)
        self.subject_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'subject'))
            
    def _create_teacher_table(self):
        
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")
        
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        
        self.teacher_table = QTableWidget()

        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["ID", "Full_name", "Subject"])
        
        self._update_teacher_table()
        
        self.svbox = QVBoxLayout()
        self.svbox.addWidget(self.teacher_table)

        self.teacher_tab.setLayout(self.svbox)


    def _update_teacher_table(self):
        
        self.cursor.execute("SELECT * FROM teacher;")
        records = list(self.cursor.fetchall())
 
        self.teacher_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(3):
                self.teacher_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")

            self.teacher_table.setCellWidget(i, 3, joinButton)
            self.teacher_table.setCellWidget(i, 4, DeleteButton)
            
        
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'teacher', data))
            
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('teacher', data))

            self.teacher_table.resizeRowsToContents()
            
        Add_Button = QPushButton("ADD")
        self.teacher_table.setCellWidget(i+1, 3, Add_Button)
        self.teacher_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'teacher'))
      

    def _create_monday_table(self):
        
        self.monday_table = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(
            ["Week", "Subject", "Classroom", "Time", "Join", 'Delete'])
        
        self._update_monday_table()
        
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_tab.setLayout(self.mvbox)
        
    def _create_Tuesday_table(self):
        
        self.Tuesday_table = QTableWidget()
        self.Tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.Tuesday_table.setColumnCount(6)
        self.Tuesday_table.setHorizontalHeaderLabels(
            ["Week", "Subject", "Classroom", "Time", "Join", 'Delete'])
        
        self._update_Tuesday_table()
        
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.Tuesday_table)
        self.Tuesday_tab.setLayout(self.mvbox) 

    def _create_Wednesday_table(self):
        
        self.Wednesday_table = QTableWidget()

        self.Wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.Wednesday_table.setColumnCount(6)
        self.Wednesday_table.setHorizontalHeaderLabels(
            ["Week", "Subject", "Classroom", "Time", "Join", 'Delete'])
        
        self._update_Wednesday_table()
        
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.Wednesday_table)
        self.Wednesday_tab.setLayout(self.mvbox)

    def _create_Thursday_table(self):
        
        self.Thursday_table = QTableWidget()
        self.Thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.Thursday_table.setColumnCount(6)
        self.Thursday_table.setHorizontalHeaderLabels(
            ["Week", "Subject", "Classroom", "Time", "Join", 'Delete'])
        
        self._update_Thursday_table()
        
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.Thursday_table)
        self.Thursday_tab.setLayout(self.mvbox)     

    def _create_Friday_table(self):
        
        self.Friday_table = QTableWidget()
        self.Friday_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.Friday_table.setColumnCount(6)
        self.Friday_table.setHorizontalHeaderLabels(
            ["Week", "Subject", "Classroom", "Time", "Join", 'Delete'])
        
        self._update_Friday_table()
        
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.Friday_table)
        self.Friday_tab.setLayout(self.mvbox)
        
        
    def _update_monday_table(self):
        
        self.cursor.execute("SELECT week, subject, room_numb, start_time FROM timetable WHERE day='Понедельник' ORDER BY 1 DESC;")
        records = list(self.cursor.fetchall())
 
        self.monday_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(4):
                self.monday_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")

            self.monday_table.setCellWidget(i, 4, joinButton)
            self.monday_table.setCellWidget(i, 5, DeleteButton)
            
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'Понедельник', data))
            
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('Понедельник', data))

            self.monday_table.resizeRowsToContents()
            


        Add_Button = QPushButton("ADD")
        self.monday_table.setCellWidget(i+1, 4, Add_Button)
        self.monday_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'Понедельник'))
        
        
    def _delete_day_from_table(self, day, data):

        if day == 'subject':
            try:
                self.cursor.execute(f"DELETE FROM teacher where subject='{data[0]}';")
                self.conn.commit()
                self.cursor.execute(f"DELETE FROM timetable where subject='{data[0]}';")
                self.conn.commit()
                self.cursor.execute(f"DELETE FROM subject where name='{data[0]}';")
                self.conn.commit()
                self._update_shedule()
            except:
                QMessageBox.about(self, "Error", "Subject delete error")
        elif day == 'teacher':
            try:
                self.cursor.execute(f"DELETE FROM teacher where id={int(data[0])} AND full_name='{data[1]}' AND subject='{data[2]}';")
                self.conn.commit()
                self._update_shedule()
            except:
                QMessageBox.about(self, "Error", "Teacher delete error")
        else:
            try:
                self.cursor.execute(f"delete from timetable where day ='{day}' AND week='{data[0]}' AND subject='{data[1]}' AND room_numb='{data[2]}' AND start_time='{data[3]}';")
                self.conn.commit()
                self._update_shedule()
            except:
                QMessageBox.about(self, "Error", "Day delete error")
        


    def _add_row_tabale(self, rowNum, day):
        
        row = list()

        match day:
            case 'Понедельник':
                
                for i in range(self.monday_table.columnCount()):
                
                    try:
                        row.append(self.monday_table.item(rowNum, i).text())

                    except:
                        row.append(None)
                    
            case 'Вторник': 

                for i in range(self.Tuesday_table.columnCount()):
                
                    try:
                        row.append(self.Tuesday_table.item(rowNum, i).text())

                    except:
                        row.append(None)                
            case 'Среда':

                for i in range(self.Wednesday_table.columnCount()):
                
                    try:
                        row.append(self.Wednesday_table.item(rowNum, i).text())

                    except:
                        row.append(None)   
                                     
            case 'Четверг':
                for i in range(self.Thursday_table.columnCount()):
                
                    try:
                        row.append(self.Thursday_table.item(rowNum, i).text())

                    except:
                        row.append(None)  
                                      
            case 'Пятница':
                for i in range(self.Friday_table.columnCount()):
                
                    try:
                        row.append(self.Friday_table.item(rowNum, i).text())

                    except:
                        row.append(None)
            case 'subject':
                for i in range(self.subject_table.columnCount()):
                
                    try:
                        row.append(self.subject_table.item(rowNum, i).text())

                    except:
                        row.append(None)
                        

                try:
                    self.cursor.execute(f"INSERT INTO subject (name) VALUES ('{row[0]}');")
                    self.conn.commit()
                    self._update_shedule()
                except:
                    QMessageBox.about(self, "Error", "Subject insert error")
            case 'teacher':
                for i in range(self.teacher_table.columnCount()):
                
                    try:
                        row.append(self.teacher_table.item(rowNum, i).text())

                    except:
                        row.append(None)
                        

                try:

                    self.cursor.execute(f"INSERT INTO teacher (full_name, subject) VALUES ('{row[1]}', '{row[2]}');")
                    self.conn.commit()
                    self._update_shedule()
                except:
                    QMessageBox.about(self, "Error", "Teacher insert error")

        if '' not in row[:-2:] and day != 'subject' and day != 'teacher':
            
            try:
                self.cursor.execute(f"INSERT INTO timetable (week, day, subject, room_numb, start_time) VALUES ('{row[0]}', '{day}', '{row[1]}', '{row[2]}', '{row[3]}');")
                self.conn.commit()
                self._update_shedule()
            except:
                QMessageBox.about(self, "Error", "Day insert error")
        

            
    def _update_Tuesday_table(self):
        
        self.cursor.execute("SELECT week, subject, room_numb, start_time FROM timetable WHERE day='Вторник' ORDER BY 1 DESC;")
        records = list(self.cursor.fetchall())
 
        self.Tuesday_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):
            r = list(r)
            for number in range(4):
                self.Tuesday_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")
            self.Tuesday_table.setCellWidget(i, 4, joinButton)
            self.Tuesday_table.setCellWidget(i, 5, DeleteButton)
            
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'Вторник', data))
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('Вторник', data))
            
            self.Tuesday_table.resizeRowsToContents()
        Add_Button = QPushButton("ADD")
        self.Tuesday_table.setCellWidget(i+1, 4, Add_Button)
        self.Tuesday_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'Вторник'))

    def _update_Wednesday_table(self):
        
        self.cursor.execute("SELECT week, subject, room_numb, start_time FROM timetable WHERE day='Среда' ORDER BY 1 DESC;")
        records = list(self.cursor.fetchall())
 
        self.Wednesday_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(4):
                self.Wednesday_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")
            self.Wednesday_table.setCellWidget(i, 4, joinButton)
            self.Wednesday_table.setCellWidget(i, 5, DeleteButton)
            
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'Среда', data))
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('Среда', data))
            
            self.Wednesday_table.resizeRowsToContents()
        Add_Button = QPushButton("ADD")
        self.Wednesday_table.setCellWidget(i+1, 4, Add_Button)
        self.Wednesday_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'Среда'))  
            
    def _update_Thursday_table(self):
        
        self.cursor.execute("SELECT week, subject, room_numb, start_time FROM timetable WHERE day='Четверг' ORDER BY 1 DESC;")
        records = list(self.cursor.fetchall())
 
        self.Thursday_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(4):
                self.Thursday_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")
            self.Thursday_table.setCellWidget(i, 4, joinButton)
            self.Thursday_table.setCellWidget(i, 5, DeleteButton)
            
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'Четверг', data))
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('Четверг', data))

            self.Thursday_table.resizeRowsToContents()
        Add_Button = QPushButton("ADD")
        self.Thursday_table.setCellWidget(i+1, 4, Add_Button)
        self.Thursday_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'Четверг')) 

    def _update_Friday_table(self):
        
        self.cursor.execute("SELECT week, subject, room_numb, start_time FROM timetable WHERE day='Пятница' ORDER BY 1 DESC;")
        records = list(self.cursor.fetchall())
 
        self.Friday_table.setRowCount(len(records) + 1)
        
        for i, r in enumerate(records):

            r = list(r)
            for number in range(4):
                self.Friday_table.setItem(i, number, QTableWidgetItem(str(r[number])))
            
            joinButton = QPushButton("Join")
            DeleteButton = QPushButton("Delete")
            self.Friday_table.setCellWidget(i, 4, joinButton)
            self.Friday_table.setCellWidget(i, 5, DeleteButton)
            
            joinButton.clicked.connect(
                lambda ch, num=i, data=r:self._change_day_from_table(num, 'Пятница', data))
            DeleteButton.clicked.connect(
                lambda ch, data=r:self._delete_day_from_table('Пятница', data))

            self.Friday_table.resizeRowsToContents()
        Add_Button = QPushButton("ADD")
        self.Friday_table.setCellWidget(i+1, 4, Add_Button)
        self.Friday_table.resizeRowsToContents()
        Add_Button.clicked.connect(lambda ch, num=i+1, data=r:self._add_row_tabale(num, 'Пятница'))
                                  
    def _change_day_from_table(self, rowNum, day, data):

        
            
        row = list()

        match day:
            case 'Понедельник':
                
                for i in range(self.monday_table.columnCount()):
                
                    try:
                        row.append(self.monday_table.item(rowNum, i).text())

                    except:
                        row.append(None)
                    
            case 'Вторник': 

                for i in range(self.Tuesday_table.columnCount()):
                
                    try:
                        row.append(self.Tuesday_table.item(rowNum, i).text())

                    except:
                        row.append(None)                
            case 'Среда':

                for i in range(self.Wednesday_table.columnCount()):
                
                    try:
                        row.append(self.Wednesday_table.item(rowNum, i).text())

                    except:
                        row.append(None)   
                                     
            case 'Четверг':
                for i in range(self.Thursday_table.columnCount()):
                
                    try:
                        row.append(self.Thursday_table.item(rowNum, i).text())

                    except:
                        row.append(None)  
                                      
            case 'Пятница':
                for i in range(self.Friday_table.columnCount()):
                
                    try:
                        row.append(self.Friday_table.item(rowNum, i).text())

                    except:
                        row.append(None)
            case 'subject':
                for i in range(self.subject_table.columnCount()):
                
                    try:
                        row.append(self.subject_table.item(rowNum, i).text())

                    except:
                        row.append(None)
                

                if row[0] != data[0]:
                    try:
                        self.cursor.execute(f"DELETE FROM teacher where subject='{data[0]}';")
                        self.conn.commit()
                        self.cursor.execute(f"DELETE FROM timetable where subject='{data[0]}';")
                        self.conn.commit()
                        self.cursor.execute(f"UPDATE subject SET name='{row[0]}' where name='{data[0]}';")
                        self.conn.commit()
                        self._update_shedule()
                    except:
                        QMessageBox.about(self, "Error", "Subject update error")
                        
            case 'teacher':
                for i in range(self.teacher_table.columnCount()):
                
                    try:
                        row.append(self.teacher_table.item(rowNum, i).text())

                    except:
                        row.append(None)

                if row[:-2:] != data[0]:
                    try:
                        self.cursor.execute(f"UPDATE teacher SET id={int(row[0])}, full_name='{row[1]}', subject='{row[2]}' where id ={int(data[0])} AND full_name='{data[1]}' AND subject='{data[2]}';")
                        self.conn.commit()
                        self._update_shedule()
                    except:
                        QMessageBox.about(self, "Error", "Teacher update error")
 
                                        
        if data != row[:-2:] and day != 'subject' and day != 'teacher':
            
            try:
                self.cursor.execute(f"UPDATE timetable SET week='{row[0]}', subject='{row[1]}', room_numb ='{row[2]}', start_time='{row[3]}' WHERE day='{day}' AND week='{data[0]}' AND subject = '{data[1]}'AND room_numb = '{data[2]}' AND start_time = '{data[3]}';")
                self.conn.commit()
                self._update_shedule()
            except:
                QMessageBox.about(self, "Error", "Enter all fields")
        
   
                
    def _update_shedule(self):

        self._update_monday_table() 
        self._update_Tuesday_table()
        self._update_Wednesday_table()
        self._update_Thursday_table()
        self._update_Friday_table()
        self._update_subject_table()
        self._update_teacher_table()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())