from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Variabel global untuk gambar
input_image = None
output_image = None

def open_file(input_label, output_label, status_label, color_menu):
    global input_image, output_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path)
        input_image = img
        output_image = img.copy()  # salin sebagai awal output

        # Set gambar ke class ColorMenu
        color_menu.set_input_image(img)

        display_image(input_label, img)
        display_image(output_label, img)

        status_label.config(text=f"Gambar berhasil dibuka: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka gambar: {str(e)}")


def save_output(status_label):
    global output_image
    if output_image is None:
        messagebox.showerror("Error", "Tidak ada gambar untuk disimpan.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
    )
    if not file_path:
        return

    try:
        output_image.save(file_path)
        status_label.config(text=f"Gambar berhasil disimpan: {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar: {str(e)}")


def exit_app(root):
    root.quit()


def display_image(label, img):
    """Tampilkan gambar di label dengan otomatis resize agar pas di frame."""
    max_width, max_height = 400, 300  # batas ukuran

    w, h = img.size
    scale = min(max_width / w, max_height / h)
    new_size = (int(w * scale), int(h * scale))

    img_resized = img.resize(new_size, Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    label.config(image=img_tk)
    label.image = img_tk  # simpan referensi


# Getter
def get_input_image():
    return input_image


def get_output_image():
    return output_image


def set_output_image(new_image, output_label):
    global output_image
    output_image = new_image
    display_image(output_label, new_image)
