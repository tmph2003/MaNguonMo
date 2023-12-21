import tkinter as tk
from tkinter import messagebox
import main_func
import threading
import time

main = main_func.Main()

def import_data():
    main = main_func.Main()
    if main.stop_import_flag == False:
        messagebox.showinfo("Thông báo", "Getting data")
        import_thread = threading.Thread(target=main.ImportData)
        import_thread.start()
        time.sleep(10)
        main.stop_import_flag = True
        time.sleep(1)
        main.stop_import_flag = False
    else:
        messagebox.showinfo("Thông báo", "Stop getting data")
        main.stop_import_flag = False

def display_data():
    main.display_dataframe()

def build_chart():
    main.BuildChart()

def predict():
    entry_value = entry.get()
    if entry_value != "":
        try:
            numeric_value = float(entry_value)
            main.Predict(numeric_value)
        except ValueError:
            messagebox.showinfo("Thông báo", "Please enter a valid number")
    else:
        messagebox.showinfo("Thông báo", "Please enter open price")

root = tk.Tk()
root.title('Crypto Analysis')
root.geometry('430x200')

frame = tk.Frame(root)
frame.pack(pady=10)

label_open = tk.Label(frame, text="Giá mở")
label_open.pack(side='left', padx=5)

entry = tk.Entry(frame, width=30)
entry.pack(side='left', padx=5)

button1 = tk.Button(root, text='Lấy dữ liệu', command=import_data)
button2 = tk.Button(root, text='Hiển thị dữ liệu', command=display_data)
button3 = tk.Button(root, text='Thống kê mô tả', command=build_chart)
button4 = tk.Button(root, text='Dự đoán', command=predict)

button1.pack(side='left', padx=5)
button2.pack(side='left', padx=5)
button3.pack(side='left', padx=5)
button4.pack(side='left', padx=5)

result_label = tk.Label(root, text='')
result_label.pack()

root.mainloop()