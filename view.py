import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tkinter import messagebox

# ===== Fungsi untuk Histogram =====
def show_histogram_input(input_image):
    if input_image is None:
        messagebox.showwarning("Peringatan", "Tidak ada gambar input yang dipilih.")
        return

    img = input_image.convert("RGB")
    pixels = np.array(img)

    plt.figure("Histogram Input", figsize=(4.5, 3))  # Window lebih kecil
    plot_histogram(pixels, "Histogram Input")
    plt.tight_layout()
    plt.show()


def show_histogram_output(output_image):
    if output_image is None:
        messagebox.showwarning("Peringatan", "Tidak ada gambar output yang dipilih.")
        return

    img = output_image.convert("RGB")
    pixels = np.array(img)

    plt.figure("Histogram Output", figsize=(4.5, 3))  # Window lebih kecil
    plot_histogram(pixels, "Histogram Output")
    plt.tight_layout()
    plt.show()


def show_histogram_input_output(input_image, output_image):
    if input_image is None or output_image is None:
        messagebox.showwarning("Peringatan", "Input atau Output belum tersedia.")
        return

    img_in = np.array(input_image.convert("RGB"))
    img_out = np.array(output_image.convert("RGB"))

    # Window lebih kecil
    fig, axs = plt.subplots(2, 1, figsize=(6, 4.5))
    fig.suptitle("Histogram Input & Output", fontsize=12)

    # Histogram input
    plot_histogram(img_in, "Input", axs[0])

    # Histogram output
    plot_histogram(img_out, "Output", axs[1])

    plt.tight_layout()
    plt.show()


def plot_histogram(pixels, title, ax=None):
    """Helper function untuk menampilkan histogram RGB yang lebih kontras"""
    if ax is None:
        ax = plt.gca()

    # Pisahkan channel RGB
    r = pixels[:, :, 0].flatten()
    g = pixels[:, :, 1].flatten()
    b = pixels[:, :, 2].flatten()

    bins = 256

    # Plot RGB dengan edgecolor untuk kontras lebih baik
    ax.hist(r, bins=bins, color='red', alpha=0.4, edgecolor='black', linewidth=0.5, label='Red')
    ax.hist(g, bins=bins, color='green', alpha=0.4, edgecolor='black', linewidth=0.5, label='Green')
    ax.hist(b, bins=bins, color='blue', alpha=0.4, edgecolor='black', linewidth=0.5, label='Blue')

    # Batas nilai pixel
    ax.set_xlim([0, 255])
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Pixel Intensity (0-255)", fontsize=8)
    ax.set_ylabel("Frequency", fontsize=8)

    # Grid halus
    ax.grid(True, linestyle='--', alpha=0.3)

    # Legend lebih kecil
    ax.legend(loc='upper right', fontsize=7)