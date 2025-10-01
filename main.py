import tkinter as tk
from tkinter import Menu
import file_menu
import view
from color_menu import ColorMenu
import image_processing
import tentang
import arithmetic_operation  # <-- Tambahan baru

def main():
    root = tk.Tk()
    root.title("Form1 - Image Processing (Python Port)")
    root.geometry("850x500")  # Window lebih kecil
    root.configure(bg="#f9f9f9")

    # ===== Frame Utama =====
    main_frame = tk.Frame(root, bg="#f9f9f9")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame kiri (Input)
    left_frame = tk.Frame(main_frame, bg="#ffffff", relief="groove", borderwidth=1)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

    tk.Label(left_frame, text="Input", font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=6, pady=4)
    input_image_label = tk.Label(left_frame, bg="#f0f0f0", relief="sunken")
    input_image_label.pack(fill="both", expand=True, padx=6, pady=6)

    # Frame kanan (Output)
    right_frame = tk.Frame(main_frame, bg="#ffffff", relief="groove", borderwidth=1)
    right_frame.pack(side="left", fill="both", expand=True)

    tk.Label(right_frame, text="Output", font=("Arial", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=6, pady=4)
    output_image_label = tk.Label(right_frame, bg="#f0f0f0", relief="sunken")
    output_image_label.pack(fill="both", expand=True, padx=6, pady=6)

    # ===== Status Bar =====
    status_frame = tk.Frame(root, relief="sunken", borderwidth=1, bg="#f0f0f0")
    status_frame.pack(side="bottom", fill="x")
    status_label = tk.Label(status_frame, text="Siap.", anchor="w", bg="#f0f0f0", font=("Arial", 9))
    status_label.pack(side="left", padx=8)

    # ===== Menu Bar =====
    menu_bar = Menu(root)

    # ===== File Menu =====
    file_menu_main = Menu(menu_bar, tearoff=0)
    file_menu_main.add_command(
        label="Buka",
        command=lambda: file_menu.open_file(input_image_label, output_image_label, status_label, color_menu)
    )
    file_menu_main.add_command(
        label="Simpan Output",
        command=lambda: file_menu.save_output(status_label)
    )
    file_menu_main.add_separator()
    file_menu_main.add_command(label="Keluar", command=lambda: file_menu.exit_app(root))
    menu_bar.add_cascade(label="File", menu=file_menu_main)

    # ===== View Menu =====
    view_menu = Menu(menu_bar, tearoff=0)
    histogram_menu = Menu(view_menu, tearoff=0)
    histogram_menu.add_command(
        label="Input",
        command=lambda: view.show_histogram_input(file_menu.get_input_image_pil())
    )
    histogram_menu.add_command(
        label="Output",
        command=lambda: view.show_histogram_output(file_menu.get_output_image_pil())
    )
    histogram_menu.add_command(
        label="Input & Output",
        command=lambda: view.show_histogram_input_output(
            file_menu.get_input_image_pil(),
            file_menu.get_output_image_pil()
        )
    )
    view_menu.add_cascade(label="Histogram", menu=histogram_menu)
    menu_bar.add_cascade(label="View", menu=view_menu)

    # ===== Colors Menu =====
    color_menu = ColorMenu(root, menu_bar, input_image_label, output_image_label, status_label)

    # ===== Tentang Menu =====
    tentang_menu = Menu(menu_bar, tearoff=0)
    tentang_menu.add_command(label="Tentang Aplikasi", command=lambda: tentang.show_about(root))
    menu_bar.add_cascade(label="Tentang", menu=tentang_menu)

    # ===== Image Processing Menu =====
    img_proc_menu = Menu(menu_bar, tearoff=0)
    img_proc_menu.add_command(
        label="Histogram Equalization",
        command=lambda: image_processing.histogram_equalization(
            file_menu.get_input_image_cv(),
            output_image_label
        )
    )
    img_proc_menu.add_command(
        label="Fuzzy HE RGB",
        command=lambda: image_processing.fuzzy_he_rgb(
            file_menu.get_input_image_cv(),
            output_image_label
        )
    )
    img_proc_menu.add_command(
        label="Fuzzy Grayscale",
        command=lambda: image_processing.fuzzy_grayscale(
            file_menu.get_input_image_cv(),
            output_image_label
        )
    )
    menu_bar.add_cascade(label="Image Processing", menu=img_proc_menu)

    # ===== Arithmetic Operation Menu =====
    arithmetic_menu = Menu(menu_bar, tearoff=0)
    arithmetic_menu.add_command(
        label="Operasi Aritmatika",
        command=lambda: arithmetic_operation.open_window(root)
    )
    menu_bar.add_cascade(label="Arithmetic Operation", menu=arithmetic_menu)

        # ===== Filter Menu =====
    import filter_menu  # pastikan ada file filter_menu.py

    filter_menu_main = Menu(menu_bar, tearoff=0)
    filter_menu_main.add_command(
        label="Identity",
        command=lambda: filter_menu.filter_identity(file_menu.get_input_image_cv(), output_image_label)
    )

    # Submenu Edge Detection
    edge_menu = Menu(filter_menu_main, tearoff=0)
    edge_menu.add_command(label="Edge Detection 1",
        command=lambda: filter_menu.edge_detection1(file_menu.get_input_image_cv(), output_image_label))
    edge_menu.add_command(label="Edge Detection 2",
        command=lambda: filter_menu.edge_detection2(file_menu.get_input_image_cv(), output_image_label))
    edge_menu.add_command(label="Edge Detection 3",
        command=lambda: filter_menu.edge_detection3(file_menu.get_input_image_cv(), output_image_label))
    filter_menu_main.add_cascade(label="Edge Detection", menu=edge_menu)

    filter_menu_main.add_command(
        label="Sharpen",
        command=lambda: filter_menu.filter_sharpen(file_menu.get_input_image_cv(), output_image_label)
    )

    # Submenu Gaussian Blur
    gaussian_menu = Menu(filter_menu_main, tearoff=0)
    gaussian_menu.add_command(label="Gaussian Blur 3x3",
        command=lambda: filter_menu.gaussian_blur_3(file_menu.get_input_image_cv(), output_image_label))
    gaussian_menu.add_command(label="Gaussian Blur 5x5",
        command=lambda: filter_menu.gaussian_blur_5(file_menu.get_input_image_cv(), output_image_label))
    filter_menu_main.add_cascade(label="Gaussian Blur", menu=gaussian_menu)

    filter_menu_main.add_command(
        label="Unsharp Masking",
        command=lambda: filter_menu.unsharp_masking(file_menu.get_input_image_cv(), output_image_label)
    )
    filter_menu_main.add_command(
        label="Average Filter",
        command=lambda: filter_menu.average_filter(file_menu.get_input_image_cv(), output_image_label)
    )
    filter_menu_main.add_command(
        label="Low Pass Filter",
        command=lambda: filter_menu.low_pass_filter(file_menu.get_input_image_cv(), output_image_label)
    )
    filter_menu_main.add_command(
        label="High Pass Filter",
        command=lambda: filter_menu.high_pass_filter(file_menu.get_input_image_cv(), output_image_label)
    )
    filter_menu_main.add_command(
        label="Bandstop Filter",
        command=lambda: filter_menu.bandstop_filter(file_menu.get_input_image_cv(), output_image_label)
    )

    menu_bar.add_cascade(label="Filter", menu=filter_menu_main)

    # ===== Set Menu ke Root =====
    root.config(menu=menu_bar)
    root.mainloop()

if __name__ == "__main__":
    main()
