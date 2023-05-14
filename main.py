import sqlite3
from faker import Faker
import random

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу "студенты"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        group_id INTEGER NOT NULL
    )
''')

# Создаем таблицу "группы"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

# Создаем таблицу "преподаватели"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

# Создаем таблицу "предметы"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
''')

# Создаем таблицу "оценки"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
''')
# Создаем экземпляр Faker
fake = Faker()

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Список групп
groups = ['Group A', 'Group B', 'Group C']

# Генерируем случайные данные для студентов
students = []
for _ in range(30):
    student_name = fake.name()
    group_id = random.choice(range(1, 4))
    students.append((student_name, group_id))

# Вставляем данные студентов в таблицу
cursor.executemany('INSERT INTO students (name, group_id) VALUES (?, ?)', students)

# Генерируем случайные данные для групп
group_data = [(group_name,) for group_name in groups]

# Вставляем данные групп в таблицу
cursor.executemany('INSERT INTO groups (name) VALUES (?)', group_data)

# Генерируем случайные данные для преподавателей
teachers = []
for _ in range(4):
    teacher_name = fake.name()
    teachers.append((teacher_name,))

# Вставляем данные преподавателей в таблицу
cursor.executemany('INSERT INTO teachers (name) VALUES (?)', teachers)

# Генерируем случайные данные для предметов
subjects = []
for _ in range(6):
    subject_name = fake.word().capitalize()
    teacher_id = random.choice(range(1, 5))
    subjects.append((subject_name, teacher_id))

# Вставляем данные предметов в таблицу
cursor.executemany('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', subjects)

# Генерируем случайные данные для оценок
grades = []
for student_id in range(1, 31):
    for subject_id in range(1, 7):
        grade = random.randint(2, 5)
        date = fake.date_between(start_date='-1y', end_date='today')
        grades.append((student_id, subject_id, grade, date))

# Вставляем данные оценок в таблицу
cursor.executemany('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)', grades)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
