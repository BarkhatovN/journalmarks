# import requests 
from grab import Grab
from bs4 import BeautifulSoup
import sys

def get_user_subject_marks(
        login,
        password,
        auth_url='https://petersburgedu.ru/user/auth/login',
        marks_url='https://petersburgedu.ru/dnevnik/lessons/'):
    #Authorization
    g = Grab()
    try:
        g.go(auth_url)
    except Exception:
        raise Exception("Can not get", auth_url)

    g.doc.set_input_by_id('Login', login)
    g.doc.set_input_by_id('Password', password)
    g.doc.submit(submit_name="Войти")
    g.doc.submit(submit_name="Войти")

    if g.doc.url != 'https://petersburgedu.ru/user/content/':
        raise Exception("Error: Authorization has been failed <br>" + 
                "Try another pair of Login and Password")

    g.go(marks_url)

    #Parsing
    soup = BeautifulSoup(g.doc.body.decode('utf-8'), 'html.parser')

    #Parsing user
    if soup.find('h2', 'student-title') != None:
        user = soup.find('h2', 'student-title').text
    #Parsing subjects
    subjects_div_div = soup.find('div', 'lessons-list')
    subjects_div = subjects_div_div.find_all('div', 'cell')
    subjects = []
    for subject in subjects_div:
        subject_a = subject.find('a')
        if not 'Элективный учебный предмет' in subject_a['title']:
            subjects.append(subject_a['title'])

    #Parsing marks
    marks = {}
    for i in range(len(subjects)):
        marks[i] = []
    marks_table = soup.find('table', 'marks-table')
    marks_tbody = marks_table.find('tbody')
    i = 0
    for marks_tr in marks_tbody.find_all('tr'):
        for marks_td in marks_tr.find_all('td'):
            mark_span = marks_td.find('span')
            if mark_span != None:
                mark = mark_span.text
                if mark != '+' and mark != 'Н':
                    marks[i].append(int(mark))
        i += 1

    subject_marks = {subjects[i]: marks[i] for i in range(len(subjects))}

    for subject in subject_marks:
        marks = subject_marks[subject]
        if len(marks) != 0:
            average_mark = round(sum(marks) / len(marks),2)
            subject_marks[subject].append(average_mark)
    return user, subject_marks


