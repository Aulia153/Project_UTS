import cv2
from tkinter import Menu
from PIL import Image, ImageTk
import file_menu

# ==== Fungsi Operasi Morfologi ====
def apply_morphology(operation, shape, ksize, output_label):
    img = file_menu.get_input_image_cv()
    if img is None:
        print("⚠ Tidak ada gambar input.")
        return

    # Pilih bentuk kernel
    if shape == "square":
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    elif shape == "cross":
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (ksize, ksize))
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Pilih operasi morfologi
    if operation == "erosion":
        result = cv2.erode(img, kernel, iterations=1)
    elif operation == "dilation":
        result = cv2.dilate(img, kernel, iterations=1)
    elif operation == "opening":
        result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif operation == "closing":
        result = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    else:
        result = img

    # Konversi ke PIL
    img_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    # Update GUI
    img_tk = ImageTk.PhotoImage(img_pil)
    output_label.config(image=img_tk)
    output_label.image = img_tk  # simpan referensi supaya tidak hilang

    # Simpan hasil ke file_menu dengan key 'main'
    file_menu.set_output_image("main", img_pil, result, output_label)

# ==== Tambahkan Menu Morfologi ke Menu Bar ====
def add_morphology_menu(menu_bar, output_label):
    morfologi_menu = Menu(menu_bar, tearoff=0)

    # Submenu Erosion
    erosion_menu = Menu(morfologi_menu, tearoff=0)
    erosion_menu.add_command(label="Square 3", command=lambda: apply_morphology("erosion", "square", 3, output_label))
    erosion_menu.add_command(label="Square 5", command=lambda: apply_morphology("erosion", "square", 5, output_label))
    erosion_menu.add_command(label="Cross 3", command=lambda: apply_morphology("erosion", "cross", 3, output_label))
    morfologi_menu.add_cascade(label="Erosion", menu=erosion_menu)

    # Submenu Dilation
    dilation_menu = Menu(morfologi_menu, tearoff=0)
    dilation_menu.add_command(label="Square 3", command=lambda: apply_morphology("dilation", "square", 3, output_label))
    dilation_menu.add_command(label="Square 5", command=lambda: apply_morphology("dilation", "square", 5, output_label))
    dilation_menu.add_command(label="Cross 3", command=lambda: apply_morphology("dilation", "cross", 3, output_label))
    morfologi_menu.add_cascade(label="Dilation", menu=dilation_menu)

    # Submenu Opening
    opening_menu = Menu(morfologi_menu, tearoff=0)
    opening_menu.add_command(label="Square 9", command=lambda: apply_morphology("opening", "square", 9, output_label))
    morfologi_menu.add_cascade(label="Opening", menu=opening_menu)

    # Submenu Closing
    closing_menu = Menu(morfologi_menu, tearoff=0)
    closing_menu.add_command(label="Square 9", command=lambda: apply_morphology("closing", "square", 9, output_label))
    morfologi_menu.add_cascade(label="Closing", menu=closing_menu)

    # Tambahkan ke Menu Utama
    menu_bar.add_cascade(label="Morfologi", menu=morfologi_menu)
