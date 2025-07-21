from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db import get_user, get_all_students, update_student, delete_student, update_password, add_or_update_student, search_students_single
from flask import jsonify
from flask import request
import bcrypt
from app.models import Student
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = get_user(username)

    if user:
        stored_hash = user[2]  # e.g., hashed password from DB

        # Make sure it's a valid string and encode it
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.strip().encode('utf-8')

        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('main.main_home'))
        except ValueError as e:
            print("bcrypt error:", e)
            return render_template('login.html', error="Password hash is invalid. Please reset your password.")

    return render_template('login.html', error="Invalid username or password.")

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = get_user(username)
        if user:
            return render_template('reset_password.html', username=username)
        else:
            return render_template('forgot_password.html', error="Username not found.")
    return render_template('forgot_password.html')

@main.route('/reset-password', methods=['POST'])
def reset_password():
    username = request.form['username']
    new_password = request.form['password']
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    update_password(username, hashed_password)
    return redirect(url_for('main.index'))


@main.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))

    students = get_all_students()
    return render_template('student.html', students=students)


@main.route('/main_home')
def main_home():
    return render_template('main_home.html')
    
@main.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))  # Redirect to the home route


@main.route('/students', methods=['POST'])
def add_student():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('name')
    subject = data.get('subject')
    marks = data.get('marks')

    if not name or not subject or not isinstance(marks, int):
        return jsonify({"error": "Invalid input"}), 400

    try:
        add_or_update_student(name, subject, marks)  # ✅ this is your sqlite3 function
        return jsonify({"message": "Student added or updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/students/<int:student_id>', methods=['PUT'])
def update_student_route(student_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('name')
    subject = data.get('subject')
    marks = data.get('marks')

    if not name or not subject or not isinstance(marks, int):
        return jsonify({"error": "Invalid data"}), 400

    update_student(student_id, name, subject, marks)
    return jsonify({"message": "Student updated"}), 200


@main.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student_route(student_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    delete_student(student_id)
    return jsonify({"message": "Student deleted"}), 200


@main.route('/students/search')
def students_search():
    search = request.args.get('q')  # search query from frontend
    results = search_students_single(search_term=search)
    return jsonify(results)



