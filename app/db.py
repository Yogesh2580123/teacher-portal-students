from app.models import Student, db, SQLAlchemy
import os
import bcrypt
import sqlite3

# # ========= DB PATH HELPERS ========= #
def get_db_path():
    return 'test_portal.db' if os.environ.get('TESTING') == '1' else 'portal.db'

def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

# # ========= DB INITIALIZER ========= #
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Teachers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    ''')

    # Insert sample teacher
    hashed_pw = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    c.execute("INSERT OR IGNORE INTO teachers (username, password) VALUES (?, ?)", ('teacher1', hashed_pw))

    conn.commit()
    conn.close()

# ========= TEACHER FUNCTIONS ========= #
def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def update_password(username, hashed_password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE teachers SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()

# ========= STUDENT FUNCTIONS ========= #
def get_all_students():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, subject, marks FROM students")
    students = c.fetchall()
    conn.close()
    return students

def update_student(student_id, name, subject, marks):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE students SET name = ?, subject = ?, marks = ? WHERE id = ?", (name, subject, marks, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

def find_student_by_name_subject(name, subject):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, marks FROM students WHERE name = ? AND subject = ?", (name, subject))
    result = c.fetchone()
    conn.close()
    return result

def add_or_update_student(name, subject, marks):
    student = find_student_by_name_subject(name, subject)
    conn = get_db_connection()
    c = conn.cursor()

    if student:
        student_id, _ = student
        c.execute("UPDATE students SET marks = ? WHERE id = ?", (marks, student_id))  # 🔁 Replace marks
    else:
        c.execute("INSERT INTO students (name, subject, marks) VALUES (?, ?, ?)", (name, subject, marks))

    conn.commit()
    conn.close()
        

def search_students_single(search_term=None):
    conn = get_db_connection()
    c = conn.cursor()

    query = "SELECT id, name, subject, marks FROM students WHERE 1=1"
    params = []

    if search_term:
        query += """
            AND (
                name LIKE ?
                OR subject LIKE ?
                OR CAST(marks AS TEXT) LIKE ?
            )
        """
        term = f"%{search_term}%"
        params = [term, term, term]

    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return [dict(row) for row in results]
# def add_or_update_student_record(name, subject, marks):
#     student = Student.query.filter_by(name=name, subject=subject).first()
#     if student:
#         student.marks = marks  # ✅ REPLACE, not add
#     else:
#         student = Student(name=name, subject=subject, marks=marks)
#         db.session.add(student)

#     try:
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e