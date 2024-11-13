import tkinter as tk
from tkinter import messagebox, ttk
from database import StudentDatabase

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.root.geometry("450x350")

        # Các biến kết nối đến cơ sở dữ liệu
        self.db_name = tk.StringVar(value='Students')  # Tên database
        self.user = tk.StringVar(value='postgres')  # Tài khoản
        self.password = tk.StringVar(value='12345')  # Mật khẩu
        self.host = tk.StringVar(value='localhost')  # Địa chỉ host
        self.port = tk.StringVar(value='5432')  # Cổng kết nối

        # Thiết kế giao diện đăng nhập
        tk.Label(self.root, text="Tên Database:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.db_name).pack(pady=5)

        tk.Label(self.root, text="Tên tài khoản:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.user).pack(pady=5)

        tk.Label(self.root, text="Mật khẩu:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show='*').pack(pady=5)

        tk.Label(self.root, text="Host:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.host).pack(pady=5)

        tk.Label(self.root, text="Port:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.port).pack(pady=5)

        tk.Button(self.root, text="Kết nối", command=self.login).pack(pady=10)

    def login(self):
        db_name = self.db_name.get()
        user = self.user.get()
        password = self.password.get()
        host = self.host.get()
        port = self.port.get()

        try:
            # Tạo kết nối database và đóng cửa sổ đăng nhập
            self.database = StudentDatabase(db_name, user, password, host, port)
            messagebox.showinfo("Thành công", "Kết nối cơ sở dữ liệu thành công!")
            self.root.destroy()
            
            # Mở giao diện quản lý sinh viên
            root = tk.Tk()
            app = StudentDatabaseApp(root, self.database)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")


class StudentDatabaseApp:
    def __init__(self, root, database):
        self.root = root
        self.root.title("Quản Lý Sinh Viên")
        self.root.geometry("550x300")

        # Lưu đối tượng database
        self.database = database

        # Các biến lưu trữ thông tin sinh viên
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.major_var = tk.StringVar()

        # Tạo giao diện người dùng
        self.create_widgets()

    def create_widgets(self):
        # Form nhập liệu
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Tên:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Tuổi:").grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(form_frame, textvariable=self.age_var).grid(row=0, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Giới tính:").grid(row=1, column=0, padx=10, pady=5)
        
        # Combobox for gender selection
        self.gender_combobox = ttk.Combobox(form_frame, textvariable=self.gender_var, state='readonly')
        self.gender_combobox['values'] = ("Nam", "Nữ")
        self.gender_combobox.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Ngành học:").grid(row=1, column=2, padx=10, pady=5)
        tk.Entry(form_frame, textvariable=self.major_var).grid(row=1, column=3, padx=10, pady=5)

        # Các nút chức năng
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Thêm sinh viên", command=self.add_student).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Cập nhật thông tin", command=self.update_student).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Xóa sinh viên", command=self.delete_student).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Tải lại danh sách", command=self.load_students).grid(row=0, column=3, padx=10)

        # Treeview để hiển thị danh sách sinh viên
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.student_tree = ttk.Treeview(tree_frame, columns=("ID", "Tên", "Tuổi", "Giới tính", "Ngành"), show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.student_tree.yview)

        self.student_tree.heading("ID", text="ID")
        self.student_tree.heading("Tên", text="Tên")
        self.student_tree.heading("Tuổi", text="Tuổi")
        self.student_tree.heading("Giới tính", text="Giới tính")
        self.student_tree.heading("Ngành", text="Ngành")

        self.student_tree.column("ID", width=50, anchor=tk.CENTER)
        self.student_tree.column("Tên", width=150, anchor=tk.W)
        self.student_tree.column("Tuổi", width=50, anchor=tk.CENTER)
        self.student_tree.column("Giới tính", width=100, anchor=tk.CENTER)
        self.student_tree.column("Ngành", width=150, anchor=tk.W)

        self.student_tree.pack()

        self.load_students()

    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        major = self.major_var.get()

        if not name or not age or not gender or not major:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            age = int(age)  # Ensure age is a number
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi phải là một số hợp lệ.")
            return

        self.database.add_student(name, age, gender, major)
        self.clear_form()
        self.load_students()

    def update_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn một sinh viên để cập nhật.")
            return

        student_id = self.student_tree.item(selected[0], 'values')[0]
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        major = self.major_var.get()

        if not name or not age or not gender or not major:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            age = int(age)  # Ensure age is a number
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi phải là một số hợp lệ.")
            return

        self.database.update_student(student_id, name, age, gender, major)
        self.clear_form()
        self.load_students()

    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Chọn sinh viên", "Vui lòng chọn một sinh viên để xóa.")
            return

        student_id = self.student_tree.item(selected[0], 'values')[0]
        self.database.delete_student(student_id)
        self.load_students()
        self.database.reset_id_sequence()

    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)

        rows = self.database.load_students()
        for row in rows:
            self.student_tree.insert('', tk.END, values=row)

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.major_var.set("")
        self.gender_combobox.set("")  # Clear the selected value in the combobox


if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()


