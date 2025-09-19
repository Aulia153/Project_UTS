import tkinter as tk
from tkinter import Menu
import file_menu
import view
from color_menu import ColorMenu

def main():
    root = tk.Tk()
    root.title("Form1 - Image Processing (Python Port)")
    root.geometry("900x550")
    root.configure(bg="#f9f9f9")

    # ===== Frame utama =====
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

    # File Menu
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

    # View Menu
    view_menu = Menu(menu_bar, tearoff=0)
    histogram_menu = Menu(view_menu, tearoff=0)
    histogram_menu.add_command(label="Input", command=lambda: view.show_histogram_input(file_menu.get_input_image()))
    histogram_menu.add_command(label="Output", command=lambda: view.show_histogram_output(file_menu.get_output_image()))
    histogram_menu.add_command(label="Input Output",
                               command=lambda: view.show_histogram_input_output(
                                   file_menu.get_input_image(),
                                   file_menu.get_output_image()
                               ))
    view_menu.add_cascade(label="Histogram", menu=histogram_menu)
    menu_bar.add_cascade(label="View", menu=view_menu)

    # Colors Menu
    color_menu = ColorMenu(root, menu_bar, input_image_label, output_image_label, status_label)

    root.config(menu=menu_bar)
    root.mainloop()

if __name__ == "__main__":
    main()
