# import unittest
# import sqlite3
# import os
# import bcrypt
# from app.db import init_db, get_user, update_password, add_or_update_student, get_all_students, find_student_by_name_subject

# TEST_DB = 'test_portal.db'

# class TestCoreFeatures(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Override database file
#         cls.original_db = 'portal.db'
#         cls.test_db = TEST_DB
#         if os.path.exists(TEST_DB):
#             os.remove(TEST_DB)
#         os.environ['TESTING'] = '1'
#         sqlite3.connect(TEST_DB).close()
#         init_db()

#     def test_teacher_login(self):
#         user = get_user('teacher1')
#         self.assertIsNotNone(user)
#         self.assertTrue(bcrypt.checkpw('password123'.encode('utf-8'), user[2].encode('utf-8')))

#     def test_password_reset(self):
#         new_pw = bcrypt.hashpw(b'newpass456', bcrypt.gensalt())
#         update_password('teacher1', new_pw)
#         user = get_user('teacher1')
#         self.assertTrue(bcrypt.checkpw(b'newpass456', user[2].encode('utf-8')))

#     def test_add_student(self):
#         add_or_update_student('Alice', 'Math', 80)
#         student = find_student_by_name_subject('Alice', 'Math')
#         self.assertIsNotNone(student)

#     def test_update_existing_student(self):
#         # Add again — should update marks
#         add_or_update_student('Alice', 'Math', 20)
#         student = find_student_by_name_subject('Alice', 'Math')
#         self.assertGreaterEqual(student[1], 100)  # 80 + 20

#     def test_get_all_students(self):
#         students = get_all_students()
#         self.assertGreaterEqual(len(students), 1)

# if __name__ == '__main__':
#     unittest.main()
