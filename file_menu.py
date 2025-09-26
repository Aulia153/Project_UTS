from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

# Variabel global
input_image_pil = None
output_image_pil = None
input_image_cv = None
output_image_cv = None

def open_file(input_label, output_label, status_label, color_menu):
    global input_image_pil, output_image_pil, input_image_cv, output_image_cv

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return

    try:
        # Load untuk GUI (PIL)
        pil_img = Image.open(file_path)
        input_image_pil = pil_img
        output_image_pil = pil_img.copy()

        # Load untuk OpenCV (Processing)
        cv_img = cv2.imread(file_path)
        if cv_img is None:
            raise ValueError("OpenCV gagal membaca gambar.")
        input_image_cv = cv_img
        output_image_cv = cv_img.copy()

        color_menu.set_input_image(pil_img)

        display_image(input_label, pil_img)
        display_image(output_label, pil_img)

        status_label.config(text=f"Gambar berhasil dibuka: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka gambar: {str(e)}")

def save_output(status_label):
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

def exit_app(root):
    root.quit()

def display_image(label, img):
    max_width, max_height = 400, 300
    w, h = img.size
    scale = min(max_width / w, max_height / h)
    new_size = (int(w * scale), int(h * scale))

    img_resized = img.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    label.config(image=img_tk)
    label.image = img_tk

# Getter
def get_input_image_pil():
    return input_image_pil

def get_output_image_pil():
    return output_image_pil

def get_input_image_cv():
    return input_image_cv

def get_output_image_cv():
    return output_image_cv

# Setter
def set_output_image(new_pil_image, new_cv_image, output_label):
    global output_image_pil, output_image_cv
    output_image_pil = new_pil_image
    output_image_cv = new_cv_image
    display_image(output_label, new_pil_image)
