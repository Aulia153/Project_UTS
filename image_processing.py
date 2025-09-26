import cv2
import numpy as np
from PIL import Image, ImageTk
import file_menu

# Fungsi untuk menampilkan output ke GUI
def update_output_image(output_image_cv, output_image_label):
    """
    Konversi dari OpenCV (BGR) ke PIL (RGB) lalu tampilkan di GUI.
    """
    rgb_image = cv2.cvtColor(output_image_cv, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    # Update global di file_menu
    file_menu.set_output_image(pil_image, output_image_cv, output_image_label)

# =========================
# 1. Histogram Equalization
# =========================
def histogram_equalization(input_image_cv, output_image_label):
    if input_image_cv is None:
        return

    # Jika gambar grayscale
    if len(input_image_cv.shape) == 2:
        equalized = cv2.equalizeHist(input_image_cv)
    else:
        # Jika gambar berwarna (BGR)
        channels = cv2.split(input_image_cv)
        eq_channels = [cv2.equalizeHist(ch) for ch in channels]
        equalized = cv2.merge(eq_channels)

    update_output_image(equalized, output_image_label)

# =========================
# 2. Fuzzy Enhancement RGB
# =========================
def fuzzy_he_rgb(input_image_cv, output_image_label):
    """
    Fuzzy Histogram Enhancement untuk gambar RGB.
    """
    if input_image_cv is None:
        return

    # Pisahkan channel B, G, R
    b, g, r = cv2.split(input_image_cv)

    # Fungsi fuzzy untuk setiap channel
    def fuzzy_enhance(channel):
        # Normalisasi channel ke [0, 1]
        normalized = channel / 255.0

        # Fungsi fuzzy sederhana: kontras meningkat dengan fungsi kuadratik
        fuzzy_output = np.power(normalized, 0.8)  # bisa diubah nilai exponent untuk efek
        fuzzy_output = np.clip(fuzzy_output * 255.0, 0, 255).astype(np.uint8)

        return fuzzy_output

    # Terapkan fuzzy pada setiap channel
    enhanced_b = fuzzy_enhance(b)
    enhanced_g = fuzzy_enhance(g)
    enhanced_r = fuzzy_enhance(r)

    # Gabungkan kembali channel
    output_cv = cv2.merge([enhanced_b, enhanced_g, enhanced_r])

    update_output_image(output_cv, output_image_label)

# =========================
# 3. Fuzzy Enhancement Grayscale
# =========================
def fuzzy_grayscale(input_image_cv, output_image_label):
    """
    Fuzzy Enhancement untuk gambar grayscale.
    """
    if input_image_cv is None:
        return

    # Jika gambar warna, konversi ke grayscale dulu
    if len(input_image_cv.shape) == 3:
        gray_img = cv2.cvtColor(input_image_cv, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = input_image_cv.copy()

    # Normalisasi ke [0, 1]
    normalized = gray_img / 255.0

    # Fungsi fuzzy sederhana
    fuzzy_output = np.power(normalized, 0.8)  # bisa diubah exponent untuk efek yang berbeda
    fuzzy_output = np.clip(fuzzy_output * 255.0, 0, 255).astype(np.uint8)

    # Konversi kembali ke BGR agar tetap konsisten
    output_cv = cv2.cvtColor(fuzzy_output, cv2.COLOR_GRAY2BGR)

    update_output_image(output_cv, output_image_label)
