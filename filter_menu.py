import cv2
from PIL import Image, ImageTk
import numpy as np

def _update_output_image(output_img, output_label):
    if output_img is None:
        return
    img_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    output_label.config(image=imgtk)
    output_label.image = imgtk

def filter_identity(img, output_label):
    if img is None: return
    _update_output_image(img, output_label)

def edge_detection1(img, output_label):
    if img is None: return
    edges = cv2.Canny(img, 100, 200)
    _update_output_image(edges, output_label)

def edge_detection2(img, output_label):
    if img is None: return
    edges = cv2.Laplacian(img, cv2.CV_64F)
    edges = cv2.convertScaleAbs(edges)
    _update_output_image(edges, output_label)

def edge_detection3(img, output_label):
    if img is None: return
    edges = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    edges = cv2.convertScaleAbs(edges)
    _update_output_image(edges, output_label)

def filter_sharpen(img, output_label):
    if img is None: return
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    _update_output_image(sharpened, output_label)

def gaussian_blur_3(img, output_label):
    if img is None: return
    blur = cv2.GaussianBlur(img, (3,3), 0)
    _update_output_image(blur, output_label)

def gaussian_blur_5(img, output_label):
    if img is None: return
    blur = cv2.GaussianBlur(img, (5,5), 0)
    _update_output_image(blur, output_label)

def unsharp_masking(img, output_label):
    if img is None: return
    gaussian = cv2.GaussianBlur(img, (9,9), 10.0)
    unsharp = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)
    _update_output_image(unsharp, output_label)

def average_filter(img, output_label):
    if img is None: return
    avg = cv2.blur(img, (3,3))
    _update_output_image(avg, output_label)

def low_pass_filter(img, output_label):
    if img is None: return
    low = cv2.blur(img, (15,15))
    _update_output_image(low, output_label)

def high_pass_filter(img, output_label):
    if img is None: return
    kernel = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
    high = cv2.filter2D(img, -1, kernel)
    _update_output_image(high, output_label)

def bandstop_filter(img, output_label):
    if img is None: return
    blur = cv2.GaussianBlur(img, (15,15), 0)
    bandstop = cv2.addWeighted(img, 1.5, blur, -0.5, 0)
    _update_output_image(bandstop, output_label)
