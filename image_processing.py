import cv2
import numpy as np
from PIL import Image
import file_menu

# Fungsi untuk menampilkan output ke GUI
def update_output_image(output_image_cv, output_image_label):
    """
    Konversi dari OpenCV (BGR) ke PIL (RGB) lalu tampilkan di GUI.
    Update ke slot 'main' di file_menu.
    """
    rgb_image = cv2.cvtColor(output_image_cv, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    file_menu.set_output_image("main", pil_image, output_image_cv, output_image_label)

# =========================
# 1. Histogram Equalization
# =========================
def histogram_equalization(input_image_cv, output_image_label):
    if input_image_cv is None:
        return

    # Jika gambar grayscale
    if len(input_image_cv.shape) == 2:
        equalized = cv2.equalizeHist(input_image_cv)
        equalized = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
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
    if input_image_cv is None:
        return

    b, g, r = cv2.split(input_image_cv)

    def fuzzy_enhance(channel):
        normalized = channel / 255.0
        fuzzy_output = np.power(normalized, 0.8)
        return np.clip(fuzzy_output * 255.0, 0, 255).astype(np.uint8)

    enhanced_b = fuzzy_enhance(b)
    enhanced_g = fuzzy_enhance(g)
    enhanced_r = fuzzy_enhance(r)

    output_cv = cv2.merge([enhanced_b, enhanced_g, enhanced_r])
    update_output_image(output_cv, output_image_label)

# =========================
# 3. Fuzzy Enhancement Grayscale
# =========================
def fuzzy_grayscale(input_image_cv, output_image_label):
    if input_image_cv is None:
        return

    if len(input_image_cv.shape) == 3:
        gray_img = cv2.cvtColor(input_image_cv, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = input_image_cv.copy()

    normalized = gray_img / 255.0
    fuzzy_output = np.power(normalized, 0.8)
    fuzzy_output = np.clip(fuzzy_output * 255.0, 0, 255).astype(np.uint8)

    output_cv = cv2.cvtColor(fuzzy_output, cv2.COLOR_GRAY2BGR)
    update_output_image(output_cv, output_image_label)
