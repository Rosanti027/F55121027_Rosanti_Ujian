#Rosanti
#F55121027

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# fungsi mengubah gambar ke grayscale
def grayscale(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

# fungsi untuk meningkatkan kontras gambar dengan memperluas rentang kecerahan gambar
def histogram_equalization(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eq_img = cv2.equalizeHist(gray_img)
    return eq_img

# fungsi untuk meningkatkan tepi pada citra
def edge_enhancement(img):
    gray_img = grayscale(img)
    sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
    abs_sobel_x = cv2.convertScaleAbs(sobel_x)
    abs_sobel_y = cv2.convertScaleAbs(sobel_y)
    edge_img = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)
    return edge_img

# fungsi untuk menghilangkan blur pada citra
def deblurring(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    blurred_img = cv2.filter2D(img, -1, kernel)
    fft_blurred_img = np.fft.fft2(blurred_img)
    fft_kernel = np.fft.fft2(kernel, s=img.shape[:2])
    fft_kernel = np.stack([fft_kernel] * 3, axis=-1)
    fft_deblurred_img = np.divide(fft_blurred_img, fft_kernel)
    deblurred_img = np.real(np.fft.ifft2(fft_deblurred_img))
    deblurred_img = np.clip(deblurred_img, 0, 255).astype(np.uint8)
    return deblurred_img

# fungsi untuk menampilkan gambar dalam kotak
def show_image(img, x, y, title):
    img = cv2.resize(img, (150, 150))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=img)
    label.image = img
    label.place(x=x, y=y)
    title_label = tk.Label(root, text=title)
    title_label.place(x=x, y=y-20)

# fungsi untuk memproses citra dan menampilkan hasilnya
def process_image(method):
    global original_img
    if method == 'grayscale':
        corrected_img = grayscale(original_img)
        show_image(corrected_img, 458, 40, 'Metode Perbaikan 1')
    elif method == 'histogram_equalization':
        corrected_img = histogram_equalization(original_img)
        show_image(corrected_img, 698, 40, 'Metode Perbaikan 2')
    elif method == 'edge_enhancement':
        corrected_img = edge_enhancement(original_img)
        show_image(corrected_img, 938, 40, 'Metode Perbaikan 3')

# fungsi untuk menampilkan informasi pembuat program
def show_creator():
    creator_label = tk.Label(root, text='Nama : ROSANTI                                                                                                                                                                '
                                        'NIM : F55121027                                                                                                                                                                 '
                                        'Kelas : A', anchor='s')
    creator_label.place(x=50, y=580)

# fungsi untuk membuka gambar
def open_image():
    global original_img
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img = cv2.imread(file_path)
        show_image(original_img, 218, 40, 'Original Image')

# membuat jendela utama
root = tk.Tk()
root.geometry('1500x1000')
root.title('Aplikasi Penerapan Perbaikan Citra')

# menambahkan kotak untuk perbaikan citra
correction_box = tk.LabelFrame(root, text='Perbaikan Citra', padx=5, pady=5)
correction_box.place(x=20, y=20, width=160, height=595)

# tombol untuk membuka gambar
open_button = tk.Button(correction_box, text='Select an Image', command=open_image)
open_button.pack(side=tk.TOP, padx=5, pady=10)

# tombol untuk perbaikan metode 1 (grayscaling)
smoothing_button = tk.Button(correction_box, text='1. Grayscaling', command=lambda: process_image('grayscale'))
smoothing_button.pack(side=tk.TOP, padx=5, pady=6)

# tombol untuk perbaikan metode 2 (histogram_equalization)
histogram_equalization_button = tk.Button(correction_box, text='2. Histogram Equalization', command=lambda: process_image('histogram_equalization'))
histogram_equalization_button.pack(side=tk.TOP, padx=5, pady=6)

# tombol untuk perbaikan metode 3 (edge_enhancement)
edge_enhancement_button = tk.Button(correction_box, text='3. Edge Enhancement', command=lambda: process_image('edge_enhancement'))
edge_enhancement_button.pack(side=tk.TOP, padx=5, pady=6)

# menambahkan kotak untuk informasi pembuat program
creator_box = tk.LabelFrame(root, text='Creator', padx=10, pady=10)
creator_box.place(x=20, y=550, width=1245, height=65)

# menampilkan informasi pembuat program
show_creator()

# menjalankan program
root.mainloop()