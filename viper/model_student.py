import sqlite3


# 创建表
def create_table():
    sql_str = '''
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            student_number TEXT NOT NULL UNIQUE,
            gender INTEGER NOT NULL,
            class_id INTEGER NOT NULL,
            chinese_score REAL,
            math_score REAL,
            english_score REAL
        );
    '''
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql_str)
        conn.commit()
    finally:
        cursor.close()
        conn.close()
