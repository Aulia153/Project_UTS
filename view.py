import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tkinter import messagebox

def show_histogram_input_output(input_image, output_image):
    if input_image is None or output_image is None:
        messagebox.showwarning("Peringatan", "Input atau Output belum tersedia.")
        return

    img_in = np.array(input_image.convert("RGB"))
    img_out = np.array(output_image)

    # Cek apakah output grayscale
    is_gray = len(img_out.shape) == 2 or (img_out.ndim == 3 and img_out.shape[2] == 1)

    if is_gray:
        # 3 histogram input RGB + 1 grayscale output
        fig, axs = plt.subplots(2, 2, figsize=(9, 6))
        fig.suptitle("Histogram Input (RGB) dan Output (Grayscale)", fontsize=12, y=1.03)

        axs[0, 0].set_title("Red (Input)")
        axs[0, 1].set_title("Green (Input)")
        axs[1, 0].set_title("Blue (Input)")
        axs[1, 1].set_title("Grayscale (Output)")

        r, g, b = img_in[:, :, 0], img_in[:, :, 1], img_in[:, :, 2]

        axs[0, 0].hist(r.flatten(), bins=256, color='red', edgecolor='black', linewidth=0.3)
        axs[0, 1].hist(g.flatten(), bins=256, color='green', edgecolor='black', linewidth=0.3)
        axs[1, 0].hist(b.flatten(), bins=256, color='blue', edgecolor='black', linewidth=0.3)
        axs[1, 1].hist(img_out.flatten(), bins=256, color='gray', edgecolor='black', linewidth=0.3)

    else:
        # Output masih RGB
        fig, axs = plt.subplots(3, 2, figsize=(9, 7))
        fig.suptitle("Histogram Input & Output per Channel", fontsize=12, y=1.03)
        axs[0, 0].set_title("Input")
        axs[0, 1].set_title("Output")

        r_in, g_in, b_in = img_in[:, :, 0], img_in[:, :, 1], img_in[:, :, 2]
        r_out, g_out, b_out = img_out[:, :, 0], img_out[:, :, 1], img_out[:, :, 2]

        plot_hist(axs[0, 0], r_in, 'red', 'Red (Input)')
        plot_hist(axs[0, 1], r_out, 'red', 'Red (Output)')
        plot_hist(axs[1, 0], g_in, 'green', 'Green (Input)')
        plot_hist(axs[1, 1], g_out, 'green', 'Green (Output)')
        plot_hist(axs[2, 0], b_in, 'blue', 'Blue (Input)')
        plot_hist(axs[2, 1], b_out, 'blue', 'Blue (Output)')

    # Rapiin tampilan
    for ax in axs.flat:
        ax.set_xlim([0, 255])
        ax.set_xlabel("Intensitas (0–255)", fontsize=8)
        ax.set_ylabel("Frekuensi", fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_hist(ax, data, color, label):
    ax.hist(data.flatten(), bins=256, color=color, edgecolor='black', linewidth=0.4)
    ax.set_ylabel(label, fontsize=9)
