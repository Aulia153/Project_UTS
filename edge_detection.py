from tkinter import Menu, messagebox
from PIL import Image
import cv2
import numpy as np
import file_menu

# ==============================
# EDGE DETECTION
# ==============================
def apply_edge(edge_type, output_label):
    """Terapkan edge detection (Prewitt / Sobel)"""
    input_cv = file_menu.get_input_image_cv()

    if input_cv is None:
        messagebox.showerror("Error", "Belum ada gambar input.")
        return

    try:
        # ubah ke grayscale
        gray = cv2.cvtColor(input_cv, cv2.COLOR_BGR2GRAY)

        if edge_type == "prewitt":
            # Kernel Prewitt
            kernelx = np.array([[-1, 0, 1],
                                [-1, 0, 1],
                                [-1, 0, 1]])
            kernely = np.array([[-1, -1, -1],
                                [ 0,  0,  0],
                                [ 1,  1,  1]])
            x = cv2.filter2D(gray, -1, kernelx)
            y = cv2.filter2D(gray, -1, kernely)
            magnitude = cv2.magnitude(x.astype(np.float32), y.astype(np.float32))
            result_cv = cv2.convertScaleAbs(magnitude)

        elif edge_type == "sobel":
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_mag = cv2.magnitude(sobelx, sobely)
            result_cv = cv2.convertScaleAbs(sobel_mag)

        else:
            result_cv = gray.copy()

        # Convert ke PIL
        result_pil = Image.fromarray(result_cv)

        # ✅ panggil dengan key
        file_menu.set_output_image("main", result_pil, result_cv, output_label)

    except Exception as e:
        messagebox.showerror("Error", f"Gagal menerapkan edge detection: {str(e)}")


# ==============================
# EDGE DETECTION MENU
# ==============================
def add_edge_menu(menu_bar, output_label):
    edge_menu = Menu(menu_bar, tearoff=0)
    edge_menu.add_command(label="Prewitt", command=lambda: apply_edge("prewitt", output_label))
    edge_menu.add_command(label="Sobel", command=lambda: apply_edge("sobel", output_label))
    menu_bar.add_cascade(label="Edge Detection", menu=edge_menu)
