from tkinter import Menu, messagebox
from PIL import Image
import cv2
import numpy as np
import file_menu


# ==============================
# APPLY FILTER
# ==============================
def apply_filter(filter_type, output_label):
    """Terapkan filter sesuai pilihan menu"""
    input_cv = file_menu.get_input_image_cv()

    if input_cv is None:
        messagebox.showerror("Error", "Belum ada gambar input.")
        return

    try:
        # Konversi grayscale bila perlu
        gray = cv2.cvtColor(input_cv, cv2.COLOR_BGR2GRAY)

        # ===== BASIC FILTERS =====
        if filter_type == "identity":
            result_cv = input_cv.copy()

        elif filter_type == "sharpen":
            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ], dtype=np.float32)
            result_cv = cv2.filter2D(input_cv, -1, kernel)

        elif filter_type == "gaussian3":
            result_cv = cv2.GaussianBlur(input_cv, (3, 3), 0)

        elif filter_type == "gaussian5":
            result_cv = cv2.GaussianBlur(input_cv, (5, 5), 0)

        elif filter_type == "average":
            result_cv = cv2.blur(input_cv, (5, 5))

        elif filter_type == "lowpass":
            kernel = np.ones((5, 5), np.float32) / 25
            result_cv = cv2.filter2D(input_cv, -1, kernel)

        elif filter_type == "highpass":
            kernel = np.array([
                [-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]
            ], dtype=np.float32)
            result_cv = cv2.filter2D(input_cv, -1, kernel)

        elif filter_type == "unsharp":
            gaussian = cv2.GaussianBlur(input_cv, (5, 5), 0)
            result_cv = cv2.addWeighted(input_cv, 1.5, gaussian, -0.5, 0)

        elif filter_type == "bandstop":
            lowpass = cv2.GaussianBlur(input_cv, (7, 7), 0)
            highpass = cv2.subtract(input_cv, lowpass)
            # bandstop lebih aman langsung hasil lowpass (supaya tidak error overflow)
            bandstop = cv2.subtract(input_cv, highpass)
            result_cv = cv2.convertScaleAbs(bandstop)

        # ===== EDGE DETECTION =====
        elif filter_type == "edge1":  # Sobel
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_mag = cv2.magnitude(sobelx, sobely)
            result_cv = cv2.convertScaleAbs(sobel_mag)

        elif filter_type == "edge2":  # Prewitt
            kernelx = np.array([
                [-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1]
            ], dtype=np.float32)
            kernely = np.array([
                [-1, -1, -1],
                [ 0,  0,  0],
                [ 1,  1,  1]
            ], dtype=np.float32)
            x = cv2.filter2D(gray, -1, kernelx)
            y = cv2.filter2D(gray, -1, kernely)
            prewitt_mag = cv2.magnitude(x.astype(np.float32), y.astype(np.float32))
            result_cv = cv2.convertScaleAbs(prewitt_mag)

        elif filter_type == "edge3":  # Canny
            result_cv = cv2.Canny(gray, 100, 200)

        else:
            result_cv = input_cv.copy()

        # ===== KONVERSI KE PIL =====
        if result_cv is None or result_cv.size == 0:
            messagebox.showerror("Error", "Filter gagal menghasilkan gambar.")
            return

        if len(result_cv.shape) == 2:  # Grayscale
            result_pil = Image.fromarray(result_cv.astype(np.uint8))
        else:  # Warna (BGR ke RGB)
            result_pil = Image.fromarray(cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB))

        # Simpan ke output utama (KEY = "main")
        file_menu.set_output_image("main", result_pil, result_cv, output_label)

    except Exception as e:
        messagebox.showerror("Error", f"Gagal menerapkan filter: {str(e)}")


# ==============================
# FILTER MENU
# ==============================
def add_filter_menu(menu_bar, output_label):
    """Tambahkan menu Filter ke menu bar utama"""
    filter_menu = Menu(menu_bar, tearoff=0)

    # ===== Basic Filters =====
    filter_menu.add_command(label="Identity",
                            command=lambda: apply_filter("identity", output_label))
    filter_menu.add_command(label="Sharpen",
                            command=lambda: apply_filter("sharpen", output_label))

    # ===== Submenu Gaussian Blur =====
    gaussian_menu = Menu(filter_menu, tearoff=0)
    gaussian_menu.add_command(label="Gaussian Blur 3x3",
                              command=lambda: apply_filter("gaussian3", output_label))
    gaussian_menu.add_command(label="Gaussian Blur 5x5",
                              command=lambda: apply_filter("gaussian5", output_label))
    filter_menu.add_cascade(label="Gaussian Blur", menu=gaussian_menu)

    # Tambahan filter
    filter_menu.add_command(label="Unsharp Masking",
                            command=lambda: apply_filter("unsharp", output_label))
    filter_menu.add_command(label="Average Filter",
                            command=lambda: apply_filter("average", output_label))
    filter_menu.add_command(label="Low Pass Filter",
                            command=lambda: apply_filter("lowpass", output_label))
    filter_menu.add_command(label="High Pass Filter",
                            command=lambda: apply_filter("highpass", output_label))
    filter_menu.add_command(label="Bandstop Filter",
                            command=lambda: apply_filter("bandstop", output_label))

    # ===== Submenu Edge Detection =====
    edge_menu = Menu(filter_menu, tearoff=0)
    edge_menu.add_command(label="Edge Detection 1",
                          command=lambda: apply_filter("edge1", output_label))
    edge_menu.add_command(label="Edge Detection 2",
                          command=lambda: apply_filter("edge2", output_label))
    edge_menu.add_command(label="Edge Detection 3",
                          command=lambda: apply_filter("edge3", output_label))
    filter_menu.add_cascade(label="Edge Detection", menu=edge_menu)

    # Tambah ke menu utama
    menu_bar.add_cascade(label="Filter", menu=filter_menu)
