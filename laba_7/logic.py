import datetime


def get_date():
    
    starting_date = datetime.date(2023,5,8)
    
    current_datetime = datetime.datetime.now().date()

    passed_days = (current_datetime -  starting_date).days
    
    week = 'Проблема с определением четности недели'
    if 0 <= (passed_days % 14) <= 6:
        week = 'Нечётная'
    elif 7 <= (passed_days % 14) <= 13:
        week = 'Чётная'
        
    return week


def sort_data(schedule):
    some = {
    'Нечётная':
            {
            'Понедельник': [],
            'Вторник': [],
            'Среда': [],
            'Четверг': [],
            'Пятница': [],
            'Суббота': []
            },
    'Чётная' :
            {
            'Понедельник': [],
            'Вторник': [],
            'Среда': [],
            'Четверг': [],
            'Пятница': [],
            'Суббота': []
            }
    }
    for item in schedule:

        some[item[1]][item[2]].append(item[3::])

    return some


def which_day_logic(week, schedule, msg):
    
    result = '\n'
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг','Пятница', 'Суббота']
    
    if msg in days_of_week:
        
        result += msg + '\n'
        result += ('------------------------------') + '\n'
        day = schedule[week][msg]
        count_par = len(day)
        
        if count_par == 0:
            result += ('Пар нет') + '\n'
            
            
        elif count_par > 0:
            for para in range(len(day)):
                result += ('  '.join(day[para])) + '\n'
        result += ('------------------------------') + '\n'
    elif msg == 'Расписание на текущую неделю':
        
        result += (msg) + '\n'
        
        for day_of_week in days_of_week:
            result += (day_of_week) + '\n'
            result += ('------------------------------') + '\n'
            day = schedule[week][day_of_week]
            count_par = len(day)
            
            if count_par == 0:
                result += ('Пар нет') + '\n'
                
            elif count_par > 0:   
                for para in range(count_par):
                    result += ('  '.join(day[para])) + '\n'
                    
            result += ('------------------------------') + '\n' + '\n'
            
    elif msg == 'Расписание на следующую неделю':
        
        if week == 'Чётная':
            week = 'Нечётная'
            
        elif week == 'Нечётная':
            week = 'Чётная'
            
        result += (msg) + '\n'
        for day_of_week in days_of_week:
            result += (day_of_week) + '\n'
            result += ('------------------------------') + '\n'
            day = schedule[week][day_of_week]
            count_par = len(day)
            
            if count_par == 0:
                result += ('Пар нет') + '\n'
                
            elif count_par > 0:   
                for para in range(count_par):
                    result +=('  '.join(day[para])) + '\n'
            result += ('------------------------------') + '\n' + '\n'
            
    return result
    
