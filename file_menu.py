from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

# ===== Variabel Global =====
# Menyimpan gambar input & output untuk mode PIL (GUI) dan OpenCV (Processing)
input_image_pil = None
output_image_pil = None
input_image_cv = None
output_image_cv = None

# Menyimpan gambar tambahan untuk Arithmetic Operation
output1_image_pil = None
output2_image_pil = None
output1_image_cv = None
output2_image_cv = None


# ===== Fungsi Membuka Gambar =====
def open_file(input_label, output_label, status_label, color_menu=None):
    """
    Membuka file gambar, load ke PIL dan OpenCV, lalu ditampilkan
    di Input dan Output utama.
    """
    global input_image_pil, output_image_pil, input_image_cv, output_image_cv

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return

    try:
        # Load dengan PIL (untuk ditampilkan di GUI)
        pil_img = Image.open(file_path)
        input_image_pil = pil_img
        output_image_pil = pil_img.copy()

        # Load dengan OpenCV (untuk proses image processing)
        cv_img = cv2.imread(file_path)
        if cv_img is None:
            raise ValueError("OpenCV gagal membaca gambar.")
        input_image_cv = cv_img
        output_image_cv = cv_img.copy()

        # Update color_menu jika ada
        if color_menu is not None:
            color_menu.set_input_image(pil_img)

        # Tampilkan gambar di GUI
        display_image(input_label, pil_img)
        display_image(output_label, pil_img)

        # Update status bar
        status_label.config(text=f"Gambar berhasil dibuka: {os.path.basename(file_path)}")

    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka gambar: {str(e)}")


# ===== Fungsi Menyimpan Output =====
def save_output(status_label):
    """Menyimpan output_image_pil ke file"""
    global output_image_pil
    if output_image_pil is None:
        messagebox.showerror("Error", "Tidak ada gambar untuk disimpan.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
    )
    if not file_path:
        return

    try:
        output_image_pil.save(file_path)
        status_label.config(text=f"Gambar berhasil disimpan: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar: {str(e)}")


# ===== Fungsi Menutup Aplikasi =====
def exit_app(root):
    root.quit()


# ===== Fungsi Menampilkan Gambar ke Label =====
def display_image(label, img):
    """Menampilkan gambar PIL pada Label Tkinter"""
    if img is None:
        return

    max_width, max_height = 400, 300
    w, h = img.size
    scale = min(max_width / w, max_height / h)
    new_size = (int(w * scale), int(h * scale))

    img_resized = img.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    label.config(image=img_tk)
    label.image = img_tk  # Mencegah garbage collection


# ===== Getter untuk gambar utama =====
def get_input_image_pil():
    return input_image_pil

def get_output_image_pil():
    return output_image_pil

def get_input_image_cv():
    return input_image_cv

def get_output_image_cv():
    return output_image_cv


# ===== Getter khusus untuk Arithmetic Operation =====
def get_output1_image_pil():
    return output1_image_pil

def get_output2_image_pil():
    return output2_image_pil

def get_output1_image_cv():
    return output1_image_cv

def get_output2_image_cv():
    return output2_image_cv


# ===== Setter untuk update output utama =====
def set_output_image(new_pil_image, new_cv_image, output_label):
    """
    Mengupdate output utama (menu Image Processing)
    """
    global output_image_pil, output_image_cv
    output_image_pil = new_pil_image
    output_image_cv = new_cv_image
    display_image(output_label, new_pil_image)


# ===== Setter untuk update Output 1 dan Output 2 =====
def set_output1_image(new_pil_image, new_cv_image, output_label):
    """Mengupdate Output 1 (Arithmetic Window)"""
    global output1_image_pil, output1_image_cv
    output1_image_pil = new_pil_image
    output1_image_cv = new_cv_image
    display_image(output_label, new_pil_image)

def set_output2_image(new_pil_image, new_cv_image, output_label):
    """Mengupdate Output 2 (Arithmetic Window)"""
    global output2_image_pil, output2_image_cv
    output2_image_pil = new_pil_image
    output2_image_cv = new_cv_image
    display_image(output_label, new_pil_image)
