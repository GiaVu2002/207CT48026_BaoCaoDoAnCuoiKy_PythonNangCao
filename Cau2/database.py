import psycopg2
from tkinter import messagebox

class StudentDatabase:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connect_db()

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi kết nối cơ sở dữ liệu: {e}")

    def add_student(self, name, age, gender, major):
        try:
            self.cur.execute("""
                INSERT INTO students (name, age, gender, major)
                VALUES (%s, %s, %s, %s)
            """, (name, age, gender, major))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi thêm sinh viên: {e}")

    def update_student(self, student_id, name, age, gender, major):
        try:
            self.cur.execute("""
                UPDATE students
                SET name = %s, age = %s, gender = %s, major = %s
                WHERE id = %s
            """, (name, age, gender, major, student_id))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi cập nhật sinh viên: {e}")

    def delete_student(self, student_id):
        try:
            self.cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi xóa sinh viên: {e}")

    def load_students(self):
        try:
            self.cur.execute("SELECT * FROM students")
            return self.cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi tải dữ liệu sinh viên: {e}")
            return []

    def reset_id_sequence(self):
        try:
            self.cur.execute("SELECT setval(pg_get_serial_sequence('students', 'id'), COALESCE(MAX(id), 1), FALSE) FROM students;")
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi reset ID: {e}")
