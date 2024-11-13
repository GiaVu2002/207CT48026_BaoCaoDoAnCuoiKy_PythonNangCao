import tkinter as tk
from tkinter import messagebox

class TinhToan:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm Tính Toán")
        self.root.geometry("450x450")
        
        self.equation = ""
        self.display_text = tk.StringVar()
        
        # Hiển thị màn hình
        display_frame = tk.Frame(self.root)
        display_frame.pack(pady=20)
        
        display = tk.Entry(display_frame, textvariable=self.display_text, font=("Arial", 16), bd=10, insertwidth=4, width=16, justify="right")
        display.grid(row=0, column=0, columnspan=4)
        
        # Các nút trình bày
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        row_val = 0
        col_val = 0
        for button in buttons:
            button_action = lambda x=button: self.action_button(x)
            b = tk.Button(button_frame, text=button, width=8, height=3, font=("Arial", 13), command=button_action)
            b.grid(row=row_val, column=col_val, padx=5, pady=5)
            
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
                
    def action_button(self, char):
        if char == "C":
            self.equation = ""
        elif char == "=":
            try:
                self.equation = str(eval(self.equation))
            except Exception as e:
                messagebox.showerror("Lỗi", "Đầu vào không hợp lệ")
                self.equation = ""
        else:
            self.equation += str(char)
        
        self.display_text.set(self.equation)

# Chạy phần mềm
if __name__ == "__main__":
    root = tk.Tk()
    tinhToan = TinhToan(root)
    root.mainloop()
