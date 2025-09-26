import tkinter as tk

def show_about(parent):
    about_window = tk.Toplevel(parent)
    about_window.title("Tentang")
    about_window.geometry("300x180")
    about_window.configure(bg="#ffffff")
    about_window.resizable(False, False)

    tk.Label(about_window, text="Tugas Praktikum", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=8)
    tk.Label(about_window, text="V 1.0", font=("Arial", 10), bg="#ffffff").pack(pady=2)
    tk.Label(about_window, text="Creator:", font=("Arial", 10, "bold"), bg="#ffffff").pack(pady=(10,2))
    tk.Label(about_window, text="Aulia Silmi Mardiyanti", font=("Arial", 10), bg="#ffffff").pack()
    tk.Label(about_window, text="E41231471 | Teknik Informatika", font=("Arial", 10), bg="#ffffff").pack()

    tk.Button(about_window, text="OK", width=8, command=about_window.destroy).pack(pady=10)
