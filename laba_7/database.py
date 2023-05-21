import psycopg2
from cfg import database_Password

conn = psycopg2.connect(database="schedule_bot", user="postgres",
                        password=database_Password, host="localhost", port="5432")

cursor = conn.cursor()

subjects = (
            ('English',), ('Higher mathematics',), ('German',), ('Introduction into IT',),
            ('The basics of DevOps',), ('Gaming sports',), ('Physics',), ('History',),
            ('Mathematical basis of databases',),('Project Practice',)
            )

teachers = (
           ('Лапаев Л. Л.', 'English',),
           ('Шаймарданова Л. К.', 'Higher mathematics',),
           ('Зелкина Ю. М.', 'German',),
           ('Фурлетов Ю. М.', 'Introduction into IT',),
           ('Королёв И. В.', 'Gaming sports',),
           ('Вальковский С. Н.', 'Physics',),
           ('Скляр Л. Н.', 'History',),
           ('Изотова А. А.', 'Mathematical basis of databases',),
           ('Городничев М. Г.', 'The basics of DevOps',),
           ('Потапченко Т. Д.', 'Project Practice',)
           )

timetables = (
             ('Нечётная', 'Понедельник', 'English', '412', '13:10',),
             ('Нечётная', 'Понедельник', 'Higher mathematics', '314', '15:25',),
             ('Нечётная', 'Понедельник', 'German', '301', '17:15',),
             ('Нечётная', 'Вторник', 'Introduction into IT', '203', '09:30',),
             ('Нечётная', 'Вторник', 'The basics of DevOps', '302', '11:20',),
             ('Нечётная', 'Среда', 'Gaming sports', 'спортзал', '11:20',),
             ('Нечётная', 'Среда', 'Higher mathematics', '514', '13:10',),
             ('Нечётная', 'Среда', 'Physics', '226', '15:25',),
             ('Нечётная', 'Четверг', 'Physics', '301', '09:30',),
             ('Нечётная', 'Четверг', 'History', '318', '11:20',),
             ('Нечётная', 'Четверг', 'Gaming sports', 'спортзал', '13:10',),
             ('Нечётная', 'Пятница', 'History', '227', '09:30',),
             ('Нечётная', 'Пятница', 'Mathematical basis of databases', '535', '11:20',),
             ('Нечётная', 'Пятница', 'Mathematical basis of databases', '401', '13:10',),
             ('Нечётная', 'Пятница', 'Mathematical basis of databases', '519', '15:25',),
             ('Чётная', 'Понедельник', 'Higher mathematics', '514', '11:20',),
             ('Чётная', 'Понедельник', 'Higher mathematics', '308', '13:10',),
             ('Чётная', 'Понедельник', 'Gaming sports', 'спортзал', '15:25',),
             ('Чётная', 'Понедельник', 'English', '418', '17:15',),
             ('Чётная', 'Вторник', 'Gaming sports', 'спортзал', '09:30',),
             ('Чётная', 'Вторник', 'History', '318', '11:20',),
             ('Чётная', 'Вторник', 'Physics', '340', '13:10',),
             ('Чётная', 'Среда', 'The basics of DevOps', '414', '13:10',),
             ('Чётная', 'Среда', 'The basics of DevOps', '302', '15:25',),
             ('Чётная', 'Пятница', 'Project Practice', '211', '11:20',),
             ('Чётная', 'Пятница', 'Introduction into IT', '203', '13:10',),
             ('Чётная', 'Пятница', 'Introduction into IT', '208', '15:25',),
             )
              

def create_table_subject():
    cursor.execute('CREATE TABLE subject(name varchar(255) primary key);')
    conn.commit()
    
def create_table_timetable():
    cursor.execute('CREATE TABLE timetable (id serial primary key, week varchar(255),\
                    day varchar(255), subject varchar(255) references subject(name),\
                    room_numb varchar(255), start_time varchar(255));')
    conn.commit()
    
def create_table_teacher():
    cursor.execute('CREATE TABLE teacher (id serial primary key, full_name varchar(1023),\
                    subject varchar(255) references subject(name));')
    conn.commit()
    

def insert_into_subject(tuples):
    cursor.executemany('INSERT INTO subject (name) VALUES (%s)', tuples)
    conn.commit()
    
def insert_into_teacher(tuples):
    cursor.executemany('INSERT INTO teacher (full_name, subject) VALUES (%s, %s)', tuples)
    conn.commit()

def insert_into_timetable(tuples):
    cursor.executemany('INSERT INTO timetable (week, day, subject, room_numb, start_time) VALUES (%s, %s, %s, %s, %s)', tuples)
    conn.commit()
    
def get_schedule():
        cursor.execute('select t.id, t.week, t.day, t.subject,  t.room_numb, t.start_time,\
            te.full_name from timetable t join subject s on s.name=t.subject join teacher te on s.name=te.subject order by 1;')
        records = list(cursor.fetchall())
        return records
    
    
if __name__ == '__main__':
    # create_table_subject()
    # create_table_timetable()
    # create_table_teacher()
    # insert_into_subject(subjects)
    # insert_into_teacher(teachers)
    # insert_into_timetable(timetables)
    # print(get_schedule())
    pass
