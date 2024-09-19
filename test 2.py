from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import customtkinter as ctk

current_result = None
file_content = None
key = 0
previous_window = None

substitution_table = {
    'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R', 'E': 'T', 'F': 'Y', 'G': 'U',
    'H': 'I', 'I': 'O', 'J': 'P', 'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F',
    'O': 'G', 'P': 'H', 'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z', 'U': 'X',
    'V': 'C', 'W': 'V', 'X': 'B', 'Y': 'N', 'Z': 'M',
    'a': 'q', 'b': 'w', 'c': 'e', 'd': 'r', 'e': 't', 'f': 'y', 'g': 'u',
    'h': 'i', 'i': 'o', 'j': 'p', 'k': 'a', 'l': 's', 'm': 'd', 'n': 'f',
    'o': 'g', 'p': 'h', 'q': 'j', 'r': 'k', 's': 'l', 't': 'z', 'u': 'x',
    'v': 'c', 'w': 'v', 'x': 'b', 'y': 'n', 'z': 'm'
}
def convert(a, m):
    x = ' '.join(m)
    chu_ma_hoa = []
    for word in m:
        ls = []
        for char in word:
            if char.isalpha():
                if char.islower():
                    base = ord('a')
                else:
                    base = ord('A')
                E = ord(char) - base
                E1 = (a + E) % 26
                ls.append(chr(E1 + base))
            else:
                ls.append(char)
        chu_ma_hoa.append(''.join(ls))

    ma_hoa = ' '.join(chu_ma_hoa)
    return ma_hoa, x

def solve(a, m):
    x = ' '.join(m)
    chu_giai_ma = []
    for word in m:
        ls = []
        for char in word:
            if char.isalpha():
                if char.islower():
                    base = ord('a')
                else:
                    base = ord('A')
                E = ord(char) - base
                E1 = (E - a) % 26
                ls.append(chr(E1 + base))
            else:
                ls.append(char)
        chu_giai_ma.append(''.join(ls))

    giai_ma = ' '.join(chu_giai_ma)
    return giai_ma, x


def affine_encrypt(a, b, m):
    encrypted_message = []
    for word in m:
        ls = []
        for char in word:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                E = ord(char) - base
                E1 = (a * E + b) % 26
                ls.append(chr(E1 + base))
            else:
                ls.append(char)
        encrypted_message.append(''.join(ls))
    return ' '.join(encrypted_message)

def affine_decrypt(a, b, m):
    decrypted_message = []
    def mod_inverse(x, m):
        for i in range(1, m):
            if (x * i) % m == 1:
                return i
        return None
    
    inv_a = mod_inverse(a, 26)
    if inv_a is None:
        return "Invalid key for decryption"
    
    for word in m:
        ls = []
        for char in word:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                E = ord(char) - base
                E1 = (inv_a * (E - b)) % 26
                ls.append(chr(E1 + base))
            else:
                ls.append(char)
        decrypted_message.append(''.join(ls))
    return ' '.join(decrypted_message)
def open_file():
    global file_content, key
    file_path = filedialog.askopenfilename(title="Chọn tệp tin", filetypes=(("All Files", "*.*"),))
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                key_line = file.readline().strip()
                if key_line.isdigit():
                    key = int(key_line)
                else:
                    raise ValueError("Khóa mã hóa không hợp lệ. Vui lòng đảm bảo dòng đầu tiên của tệp là số nguyên.")
                file_content = file.read().split()
                
                
                root.withdraw()
                open_new_window()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi đọc tệp: {str(e)}")

current_result = None  
def substitute_encrypt(text):
    encrypted_text = []
    for char in text:
        if char in substitution_table:
            encrypted_text.append(substitution_table[char])
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)


def substitute_decrypt(text):
    reversed_table = {v: k for k, v in substitution_table.items()}
    decrypted_text = []
    for char in text:
        if char in reversed_table:
            decrypted_text.append(reversed_table[char])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)
def substitute_encrypt_action(current_window):
    global current_result  
    if file_content:
        encrypted_text = substitute_encrypt(' '.join(file_content))
        current_result = encrypted_text  
        current_window.destroy()  
        open_results_window(encrypted_text)

def substitute_decrypt_action(current_window):
    global current_result  
    if file_content:
        decrypted_text = substitute_decrypt(' '.join(file_content))
        current_result = decrypted_text  
        current_window.destroy()  
        open_results_window(decrypted_text)
def encrypt(current_window):
    global current_result  
    if file_content:
        ma_hoa, _ = convert(key, file_content)
        current_result = ma_hoa
        current_window.destroy()  
        open_results_window(ma_hoa)

def decrypt(current_window):
    global current_result  
    if file_content:
        giai_ma, _ = solve(key, file_content)
        current_result = giai_ma  
        current_window.destroy()  
        open_results_window(giai_ma)


def open_new_window():
    new_window = tk.Toplevel(root, bg="#5f9ea0")
    new_window.title("Nội dung và tùy chọn")
    new_window.geometry("800x600")  # Set window size

    text_widget = tk.Text(new_window, width=60, height=20, bg="#fff0f5", fg="black")
    text_widget.pack(pady=20)
    text_widget.insert(tk.END, ' '.join(file_content))
    text_widget.config(state=tk.DISABLED)

    button_frame = tk.Frame(new_window, bg="#5f9ea0")
    button_frame.pack(pady=20)

    encrypt_button = ctk.CTkButton(button_frame, text="Mã hóa Caesar", command=lambda: encrypt(new_window), hover_color="#4682B4")
    encrypt_button.grid(row=0, column=0, padx=10, pady=10)

    decrypt_button = ctk.CTkButton(button_frame, text="Giải mã Caesar", command=lambda: decrypt(new_window), hover_color="#4682B4")
    decrypt_button.grid(row=0, column=1, padx=10, pady=10)

    sub_encrypt_button = ctk.CTkButton(button_frame, text="Mã hóa thay thế", command=lambda: substitute_encrypt_action(new_window), hover_color="#4682B4")
    sub_encrypt_button.grid(row=1, column=0, padx=10, pady=10)

    sub_decrypt_button = ctk.CTkButton(button_frame, text="Giải mã thay thế", command=lambda: substitute_decrypt_action(new_window), hover_color="#4682B4")
    sub_decrypt_button.grid(row=1, column=1, padx=10, pady=10)

    affine_encrypt_button = ctk.CTkButton(button_frame, text="Mã hóa Affine", command=lambda: open_affine_window('encrypt', new_window), hover_color="#4682B4")
    affine_encrypt_button.grid(row=2, column=0, padx=10, pady=10)

    affine_decrypt_button = ctk.CTkButton(button_frame, text="Giải mã Affine", command=lambda: open_affine_window('decrypt', new_window), hover_color="#4682B4")
    affine_decrypt_button.grid(row=2, column=1, padx=10, pady=10)

def open_affine_window(action, parent_window):
    affine_window = tk.Toplevel(root, bg="#add8e6")
    affine_window.title("Chọn khóa Affine (a và b)")

    a_label = tk.Label(affine_window, text="Khóa a:", font=("Arial", 12), bg="#add8e6")
    a_label.grid(row=0, column=0, padx=10, pady=10)
    a_entry = tk.Entry(affine_window)
    a_entry.grid(row=0, column=1, padx=10, pady=10)

    b_label = tk.Label(affine_window, text="Khóa b:", font=("Arial", 12), bg="#add8e6")
    b_label.grid(row=1, column=0, padx=10, pady=10)
    b_entry = tk.Entry(affine_window)
    b_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_affine_submit():
        global affine_a, affine_b
        try:
            affine_a = int(a_entry.get())
            affine_b = int(b_entry.get())
            if action == 'encrypt':
                affine_encrypt_action(parent_window)
            else:
                affine_decrypt_action(parent_window)
            affine_window.destroy()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho a và b!")

    submit_button = ctk.CTkButton(affine_window, text="Xác nhận", command=on_affine_submit, hover_color="#4682B4")
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

def affine_encrypt_action(current_window):
    global current_result
    if file_content:
        ma_hoa = affine_encrypt(affine_a, affine_b, file_content)
        current_result = ma_hoa
        current_window.destroy()
        open_results_window(ma_hoa)

def affine_decrypt_action(current_window):
    global current_result
    if file_content:
        giai_ma = affine_decrypt(affine_a, affine_b, file_content)
        current_result = giai_ma
        current_window.destroy()
        open_results_window(giai_ma)

def open_results_window(result):
    global previous_window
    results_window = tk.Toplevel(root, bg="#add8e6")
    results_window.title("Kết quả")

    result_label = tk.Label(results_window, text="Kết quả:", font=("Times New Roman", 12))
    result_label.pack(pady=10)

    result_text = tk.Text(results_window, width=60, height=20, bg="#dcdcdc", fg="black")
    result_text.pack(pady=10)
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)

    save_button = ctk.CTkButton(results_window, text="Lưu kết quả", command=save_file, hover_color="#4682B4")
    save_button.pack(pady=10)
    
    back_button = tk.Button(results_window, text="Trở lại", command=lambda: go_back(results_window))
    back_button.pack(pady=10)

    previous_window = root if not previous_window else previous_window  # Lưu lại cửa sổ hiện tại

def go_back(current_window):
    global previous_window
    current_window.destroy()  # Đóng cửa sổ hiện tại
    if previous_window:
        previous_window.deiconify()  # Hiển thị lại cửa sổ trước đó
        previous_window = None  # Xóa tham chiếu đến cửa sổ trước
import os
def save_file():
    global current_result, key  
    if current_result:
       
        file_path = filedialog.asksaveasfilename(
            title="Đặt tên tệp tin", 
            defaultextension=".txt", 
            filetypes=[("Text file", "*.txt")],
            initialfile="result"  
        )
        if file_path:
            try:
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"{key}\n") 
                    f.write(current_result + "\n")  
                messagebox.showinfo("Lưu thành công", f"Kết quả và khóa mã hóa đã được lưu vào:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi lưu tệp: {str(e)}")
        root.destroy()  
    else:
        messagebox.showwarning("Không có kết quả", "Không có kết quả nào để lưu!")

root = tk.Tk()
root.title("Mã hóa và Giải mã với Caesar Cipher")
root.geometry("800x600")

# Centering the main canvas
canvas = tk.Canvas(root, width=800, height=600, bg="#5f9ea0")
canvas.pack(fill="both", expand=True)

label = tk.Label(root, text="Phần Mềm Mã Hóa", font=("Times New Roman", 20), bg="#5f9ea0", fg="white")
canvas.create_window(400, 150, anchor="center", window=label)

rounded_button = ctk.CTkButton(root, text="Select Files", command=open_file, hover_color="#4682B4", text_color="white", font=("Times New Roman", 18))
canvas.create_window(400, 300, anchor="center", window=rounded_button)

root.mainloop()
