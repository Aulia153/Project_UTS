from tkinter import Menu, messagebox
from PIL import Image, ImageTk, ImageEnhance
import file_menu
import math
import cv2
import numpy as np

class ColorMenu:
    def __init__(self, root, menu_bar, input_label, output_label, status_label):
        self.root = root
        self.input_label = input_label
        self.output_label = output_label
        self.status_label = status_label

        self.input_image = None
        self.output_image = None

        # Menu Colors utama
        self.menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Colors", menu=self.menu)

        # === RGB ===
        rgb_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="RGB", menu=rgb_menu)
        for color in ["Kuning", "Orange", "Cyan", "Purple", "Grey", "Coklat", "Merah"]:
            rgb_menu.add_command(label=color, command=lambda c=color: self.apply_rgb_filter(c))

        # === RGB to Grayscale ===
        grayscale_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="RGB to Grayscale", menu=grayscale_menu)
        for mode in ["Average", "Lightness", "Luminance"]:
            grayscale_menu.add_command(label=mode, command=lambda m=mode: self.apply_grayscale(m))

        # === Brightness ===
        self.menu.add_command(label="Brightness", command=self.adjust_brightness)

        # === Brightness - Contrast ===
        bc_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Brightness - Contrast", menu=bc_menu)
        bc_menu.add_command(label="Brightness", command=self.adjust_brightness)
        bc_menu.add_command(label="Contrast", command=self.adjust_contrast)

        # === Invers ===
        self.menu.add_command(label="Invers", command=self.apply_inverse)

        # === Log Brightness ===
        self.menu.add_command(label="Log Brightness", command=self.apply_log_brightness)

        # === Bit Depth ===
        bit_depth_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Bit Depth", menu=bit_depth_menu)
        for i in range(1, 8):
            bit_depth_menu.add_command(label=f"{i} bit", command=lambda b=i: self.apply_bit_depth(b))

        # === Gamma Correction ===
        self.menu.add_command(label="Gamma Correction", command=self.apply_gamma_correction)

    # Set input image
    def set_input_image(self, img):
        self.input_image = img
        self.output_image = img.copy()

    # Check apakah image sudah di-load
    def check_image_loaded(self):
        if self.input_image is None:
            messagebox.showerror("Error", "Input image belum dibuka.")
            return False
        return True

    # Update output ke file_menu dan GUI
    def update_output_display(self):
        if self.output_image:
            # Konversi PIL -> OpenCV
            cv_img = cv2.cvtColor(np.array(self.output_image), cv2.COLOR_RGB2BGR)
            # Simpan ke slot 'main' di file_menu
            file_menu.set_output_image("main", self.output_image, cv_img, self.output_label)
            self.status_label.config(text="Output berhasil diperbarui.")

    # ========== FILTERS ==========
    def apply_rgb_filter(self, color):
        if not self.check_image_loaded():
            return
        r, g, b = self.input_image.split()

        if color == "Merah":
            self.output_image = Image.merge("RGB", (r, r.point(lambda i: 0), r.point(lambda i: 0)))
        elif color == "Cyan":
            self.output_image = Image.merge("RGB", (r.point(lambda i: 0), g, b))
        elif color == "Kuning":
            self.output_image = Image.merge("RGB", (r, g, b.point(lambda i: 0)))
        elif color == "Orange":
            self.output_image = Image.merge("RGB", (r, g.point(lambda i: int(i * 0.5)), b.point(lambda i: 0)))
        elif color == "Purple":
            self.output_image = Image.merge("RGB", (r, g.point(lambda i: 0), b))
        elif color == "Grey":
            grey = self.input_image.convert("L")
            self.output_image = Image.merge("RGB", (grey, grey, grey))
        elif color == "Coklat":
            self.output_image = Image.merge("RGB", (r, g.point(lambda i: int(i * 0.5)), b.point(lambda i: int(i * 0.2))))

        self.update_output_display()

    def apply_grayscale(self, mode):
        if not self.check_image_loaded():
            return
        pixels = self.input_image.convert("RGB").load()
        w, h = self.input_image.size
        grey_img = Image.new("L", (w, h))

        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                if mode == "Average":
                    grey = (r + g + b) // 3
                elif mode == "Lightness":
                    grey = (max(r, g, b) + min(r, g, b)) // 2
                elif mode == "Luminance":
                    grey = int(0.3 * r + 0.59 * g + 0.11 * b)
                grey_img.putpixel((x, y), grey)

        self.output_image = grey_img.convert("RGB")
        self.update_output_display()

    def adjust_brightness(self):
        if not self.check_image_loaded():
            return
        enhancer = ImageEnhance.Brightness(self.input_image)
        self.output_image = enhancer.enhance(1.5)
        self.update_output_display()

    def adjust_contrast(self):
        if not self.check_image_loaded():
            return
        enhancer = ImageEnhance.Contrast(self.input_image)
        self.output_image = enhancer.enhance(1.5)
        self.update_output_display()

    def apply_inverse(self):
        if not self.check_image_loaded():
            return
        self.output_image = self.input_image.point(lambda i: 255 - i)
        self.update_output_display()

    def apply_log_brightness(self):
        if not self.check_image_loaded():
            return
        c = 45  # konstanta log
        img = self.input_image.convert("L")
        w, h = img.size
        log_img = Image.new("L", (w, h))

        for x in range(w):
            for y in range(h):
                val = img.getpixel((x, y))
                log_val = int(c * math.log(1 + val))
                log_img.putpixel((x, y), min(255, log_val))

        self.output_image = log_img.convert("RGB")
        self.update_output_display()

    def apply_bit_depth(self, bits):
        if not self.check_image_loaded():
            return
        levels = 2 ** bits
        factor = 256 // levels
        self.output_image = self.input_image.point(lambda i: (i // factor) * factor)
        self.update_output_display()

    def apply_gamma_correction(self):
        if not self.check_image_loaded():
            return
        gamma = 2.2
        inv_gamma = 1.0 / gamma
        self.output_image = self.input_image.point(lambda i: int((i / 255.0) ** inv_gamma * 255))
        self.update_output_display()
