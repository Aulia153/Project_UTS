from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

# ===== Variabel Global =====
input_image_pil = None
input_image_cv = None

# Simpan output di dictionary supaya fleksibel
outputs_pil = {"main": None, "alt1": None, "alt2": None}
outputs_cv = {"main": None, "alt1": None, "alt2": None}


# ===== Fungsi Membuka Gambar =====
def open_file(input_label, output_label, status_label, color_menu=None):
    global input_image_pil, input_image_cv

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return False

    try:
        # Load dengan PIL
        pil_img = Image.open(file_path)
        input_image_pil = pil_img
        outputs_pil["main"] = pil_img.copy()

        # Load dengan OpenCV
        cv_img = cv2.imread(file_path)
        if cv_img is None:
            raise ValueError("OpenCV gagal membaca gambar.")
        input_image_cv = cv_img
        outputs_cv["main"] = cv_img.copy()

        if color_menu is not None:
            color_menu.set_input_image(pil_img)

        # Tampilkan gambar di GUI
        display_image(input_label, pil_img)
        display_image(output_label, pil_img)

        status_label.config(text=f"Gambar berhasil dibuka: {os.path.basename(file_path)}")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka gambar: {str(e)}")
        return False


# ===== Fungsi Menyimpan Output =====
def save_output(status_label):
    if outputs_pil["main"] is None:
        messagebox.showerror("Error", "Tidak ada gambar untuk disimpan.")
        return False

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
    )
    if not file_path:
        return False

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # pastikan direktori ada
        outputs_pil["main"].save(file_path)
        status_label.config(text=f"Gambar berhasil disimpan: {os.path.basename(file_path)}")
        return True
    except PermissionError:
        messagebox.showerror("Error", "Izin ditolak. Tidak bisa menyimpan file.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar: {str(e)}")
        return False


# ===== Fungsi Menutup Aplikasi =====
def exit_app(root):
    root.quit()


# ===== Fungsi Menampilkan Gambar =====
def display_image(label, img):
    if img is None:
        return

    max_width, max_height = 400, 300
    w, h = img.size
    if w <= 0 or h <= 0:
        return

    scale = min(max_width / w, max_height / h, 1.0)  # jangan perbesar
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))

    img_resized = img.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    label.config(image=img_tk)
    label.image = img_tk


# ===== Getter Fleksibel =====
def get_input_image_pil(): 
    return input_image_pil.copy() if input_image_pil else None

def get_input_image_cv(): 
    return input_image_cv.copy() if input_image_cv is not None else None

def get_output_image_pil(key="main"): 
    return outputs_pil[key].copy() if outputs_pil.get(key) else None

def get_output_image_cv(key="main"): 
    return outputs_cv[key].copy() if outputs_cv.get(key) is not None else None


# ===== Setter Fleksibel =====
def set_output_image(key, new_pil_image, new_cv_image, output_label=None):
    """Simpan gambar output ke slot tertentu (default: key='main')"""
    outputs_pil[key] = new_pil_image
    outputs_cv[key] = new_cv_image
    if output_label is not None:
        display_image(output_label, new_pil_image)


# ===== Helper =====
def has_input_image():
    return input_image_pil is not None

def has_output_image(key="main"):
    return outputs_pil.get(key) is not None
