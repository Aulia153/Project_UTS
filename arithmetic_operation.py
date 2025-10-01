import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

import file_menu  # ambil gambar dari modul file_menu


def display_image(label, img_pil):
    """Tampilkan gambar PIL ke Label Tkinter."""
    if img_pil is None:
        return

    max_width, max_height = 250, 250
    w, h = img_pil.size
    scale = min(max_width / w, max_height / h)
    new_size = (int(w * scale), int(h * scale))

    img_resized = img_pil.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    label.config(image=img_tk)
    label.image = img_tk


def open_window(root):
    arithmetic_window = tk.Toplevel(root)
    arithmetic_window.title("Arithmetic Operation")
    arithmetic_window.geometry("950x450")
    arithmetic_window.configure(bg="white")

    # ===== FRAME ATAS (3 kolom untuk gambar) =====
    frame_images = tk.Frame(arithmetic_window, bg="white")
    frame_images.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame Input 1
    frame_in1 = tk.Frame(frame_images, bd=2, relief="groove")
    frame_in1.pack(side="left", expand=True, fill="both", padx=5)
    tk.Label(frame_in1, text="Input 1", font=("Arial", 10, "bold")).pack()
    input1_label = tk.Label(frame_in1, bg="#eaeaea", relief="sunken")
    input1_label.pack(fill="both", expand=True, padx=5, pady=5)

    # Frame Input 2
    frame_in2 = tk.Frame(frame_images, bd=2, relief="groove")
    frame_in2.pack(side="left", expand=True, fill="both", padx=5)
    tk.Label(frame_in2, text="Input 2", font=("Arial", 10, "bold")).pack()
    input2_label = tk.Label(frame_in2, bg="#eaeaea", relief="sunken")
    input2_label.pack(fill="both", expand=True, padx=5, pady=5)

    # Frame Output
    frame_out = tk.Frame(frame_images, bd=2, relief="groove")
    frame_out.pack(side="left", expand=True, fill="both", padx=5)
    tk.Label(frame_out, text="Output", font=("Arial", 10, "bold")).pack()
    output_label = tk.Label(frame_out, bg="#eaeaea", relief="sunken")
    output_label.pack(fill="both", expand=True, padx=5, pady=5)

    # ===== FRAME BAWAH (Kontrol) =====
    frame_controls = tk.Frame(arithmetic_window, bg="white")
    frame_controls.pack(fill="x", pady=10)

    tk.Label(frame_controls, text="Pilih Operasi:").pack(side="left", padx=5)

    operations = ["Penjumlahan", "Pengurangan", "Perkalian", "Pembagian"]
    operation_var = tk.StringVar(value=operations[0])
    operation_combo = ttk.Combobox(frame_controls, textvariable=operation_var, values=operations, state="readonly", width=18)
    operation_combo.pack(side="left", padx=5)

    # Tombol Load
    tk.Button(
        frame_controls,
        text="Load Gambar",
        command=lambda: load_images(input1_label, input2_label),
        bg="#4CAF50", fg="white", width=15
    ).pack(side="left", padx=5)

    # Tombol Proses
    tk.Button(
        frame_controls,
        text="Proses Operasi",
        command=lambda: process_arithmetic(operation_var.get(), input1_label, input2_label, output_label),
        bg="#2196F3", fg="white", width=15
    ).pack(side="left", padx=5)


def load_images(input1_label, input2_label):
    """Ambil gambar dari file_menu.py dan tampilkan ke Input 1 & Input 2."""
    img1_pil = file_menu.get_input_image_pil()
    img2_pil = file_menu.get_output_image_pil()

    if img1_pil is None or img2_pil is None:
        messagebox.showerror("Error", "Harap buka gambar terlebih dahulu dari menu utama.")
        return

    display_image(input1_label, img1_pil)
    display_image(input2_label, img2_pil)


def process_arithmetic(operation, input1_label, input2_label, output_label):
    """Lakukan operasi aritmatika dan tampilkan di Output."""
    img1_cv = file_menu.get_input_image_cv()
    img2_cv = file_menu.get_output_image_cv()

    if img1_cv is None or img2_cv is None:
        messagebox.showerror("Error", "Input 1 dan Input 2 belum di-load.")
        return

    if img1_cv.shape != img2_cv.shape:
        messagebox.showerror("Error", "Ukuran gambar harus sama.")
        return

    if operation == "Penjumlahan":
        result = cv2.add(img1_cv, img2_cv)
    elif operation == "Pengurangan":
        result = cv2.subtract(img1_cv, img2_cv)
    elif operation == "Perkalian":
        result = cv2.multiply(img1_cv, img2_cv)
    elif operation == "Pembagian":
        img2_safe = np.where(img2_cv == 0, 1, img2_cv)
        result = cv2.divide(img1_cv.astype(np.float32), img2_safe.astype(np.float32))
        result = np.clip(result, 0, 255).astype(np.uint8)
    else:
        messagebox.showerror("Error", "Operasi tidak dikenali.")
        return

    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result_pil = Image.fromarray(result_rgb)

    display_image(output_label, result_pil)
    file_menu.set_output_image(result_pil, result, output_label)
