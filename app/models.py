from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('name', 'subject', name='uix_name_subject'),
    )

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



