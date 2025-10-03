import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# Warna tema
BG_COLOR = "#f4f6f9"
FRAME_COLOR = "#ffffff"
BUTTON_COLOR = "#4a90e2"
BUTTON_TEXT = "#ffffff"

def open_arithmetic_window(root):
    window = Toplevel(root)
    window.title("Arithmetic Operation")
    window.geometry("900x500")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)

    # Judul
    title = tk.Label(window, text="🔹 Arithmetic Image Operation 🔹",
                     font=("Arial", 16, "bold"), bg=BG_COLOR, fg="#333")
    title.pack(pady=15)

    # Frame utama
    frame = tk.Frame(window, bg=BG_COLOR)
    frame.pack(fill="both", expand=True, padx=15, pady=10)

    # ==== Input 1 ====
    frame1 = tk.LabelFrame(frame, text="Input 1", width=280, height=320,
                           bg=FRAME_COLOR, font=("Arial", 11, "bold"))
    frame1.grid(row=0, column=0, padx=10, pady=10)
    frame1.grid_propagate(False)

    img1_cv = [None]
    img1_label = tk.Label(frame1, text="Belum dipilih", bg="#d9d9d9")
    img1_label.pack(fill="both", expand=True, padx=5, pady=5)

    def select_input1():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            img1_cv[0] = cv2.imread(path)
            show_image_on_label(img1_cv[0], img1_label)

    create_button(frame1, "Pilih Input 1", select_input1)

    # ==== Input 2 ====
    frame2 = tk.LabelFrame(frame, text="Input 2", width=280, height=320,
                           bg=FRAME_COLOR, font=("Arial", 11, "bold"))
    frame2.grid(row=0, column=1, padx=10, pady=10)
    frame2.grid_propagate(False)

    img2_cv = [None]
    img2_label = tk.Label(frame2, text="Belum dipilih", bg="#d9d9d9")
    img2_label.pack(fill="both", expand=True, padx=5, pady=5)

    def select_input2():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            img2_cv[0] = cv2.imread(path)
            show_image_on_label(img2_cv[0], img2_label)

    create_button(frame2, "Pilih Input 2", select_input2)

    # ==== Output ====
    frame3 = tk.LabelFrame(frame, text="Output", width=280, height=320,
                           bg=FRAME_COLOR, font=("Arial", 11, "bold"))
    frame3.grid(row=0, column=2, padx=10, pady=10)
    frame3.grid_propagate(False)

    output_label = tk.Label(frame3, text="Hasil operasi", bg="#d9d9d9")
    output_label.pack(fill="both", expand=True, padx=5, pady=5)

    result_img = [None]

    # ==== Panel Kontrol ====
    control_frame = tk.Frame(window, bg=BG_COLOR)
    control_frame.pack(pady=15)

    tk.Label(control_frame, text="Operasi (+, -, *, /):",
             bg=BG_COLOR, font=("Arial", 11)).pack(side="left", padx=5)
    operation_entry = tk.Entry(control_frame, width=5, font=("Arial", 12))
    operation_entry.pack(side="left", padx=5)
    operation_entry.insert(0, "+")

    def apply_operation():
        if img1_cv[0] is None or img2_cv[0] is None:
            messagebox.showerror("Error", "Pilih kedua input image terlebih dahulu!")
            return

        op = operation_entry.get()
        img1 = img1_cv[0]
        img2 = img2_cv[0]

        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        try:
            if op == "+":
                result = cv2.add(img1, img2)
            elif op == "-":
                result = cv2.subtract(img1, img2)
            elif op == "*":
                result = cv2.multiply(img1 / 255.0, img2 / 255.0)
                result = np.clip(result * 255, 0, 255).astype(np.uint8)
            elif op == "/":
                img2_safe = np.where(img2 == 0, 1, img2)
                result = cv2.divide(img1, img2_safe)
                result = np.clip(result, 0, 255).astype(np.uint8)
            else:
                messagebox.showerror("Error", "Operasi tidak valid! Gunakan +, -, *, /")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi: {str(e)}")
            return

        show_image_on_label(result, output_label)
        result_img[0] = result

    def save_output():
        if result_img[0] is None:
            messagebox.showwarning("Peringatan", "Belum ada hasil yang bisa disimpan!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        if path:
            cv2.imwrite(path, result_img[0])
            messagebox.showinfo("Sukses", f"Hasil berhasil disimpan ke {path}")

    create_button(control_frame, "Apply", apply_operation, side="left")
    create_button(control_frame, "Save Output", save_output, side="left")


# ==== Helper Function untuk tampilkan gambar ====
def show_image_on_label(img_cv, label_widget):
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.resize(img_rgb, (260, 260))
    pil_image = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(pil_image)
    label_widget.config(image=img_tk, text="")
    label_widget.image = img_tk

# ==== Helper Function untuk tombol dengan style ====
def create_button(parent, text, command, side="top"):
    btn = tk.Button(parent, text=text, command=command,
                    bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                    activebackground="#357ABD", activeforeground="white",
                    font=("Arial", 10, "bold"), relief="flat", padx=10, pady=5, cursor="hand2")
    if side == "top":
        btn.pack(pady=8)
    else:
        btn.pack(side=side, padx=8)
    return btn


# Fungsi untuk main.py panggil
def open_window(root):
    open_arithmetic_window(root)
