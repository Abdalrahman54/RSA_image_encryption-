#!/usr/bin/env python
# coding: utf-8

# In[10]:


import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption App")

        # Initialize OpenCV camera capture
        self.cap = cv2.VideoCapture(0)

        # Create buttons
        self.btn_capture = tk.Button(root, text="Capture Image", command=self.capture_image)
        self.btn_encrypt = tk.Button(root, text="Encrypt Image", command=self.encrypt_image)
        self.btn_decrypt = tk.Button(root, text="Decrypt Image", command=self.decrypt_image)

        # Create image label
        self.img_label = tk.Label(root)

        # Pack widgets
        self.btn_capture.pack(pady=10)
        self.btn_encrypt.pack(pady=10)
        self.btn_decrypt.pack(pady=10)
        self.img_label.pack()

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite('captured_image.png', frame)
            print("Image captured and saved as 'captured_image.png'")
            self.display_image(frame)

    def encrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("PNG files", "*.png")])
        if file_path:
            print("Selected File Path:", file_path)  # Print the selected file path

            image_path = os.path.normpath(file_path)
            img = cv2.imread(image_path)
            row,col=img.shape[0],img.shape[1]
        for i in range(0, row):
            for j in range(0, col):
                r, g, b = img[i, j]
                C1 = (r + 256) / 10
                C2 = (g * 256) / 10
                C3 = (b + 256) / 10
                img[i, j] = [C1, C2, C3]

        cv2.imwrite('encrypted_image.png', img)
        print("Image encrypted and saved as 'encrypted_image.png'")
        self.display_image(img)



    def decrypt_image(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("PNG files", "*.png")])
        if file_path:
            print("Selected File Path:", file_path)  # Print the selected file path

            # Convert the file path to Unicode using os.path
            unicode_file_path = os.path.normpath(file_path)

            img = cv2.imread(unicode_file_path)
            if img is not None:  # Check if the image was loaded successfully
                decrypted_img = np.zeros_like(img, dtype=np.uint8)  # Create an empty array for decrypted image
                
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        r, g, b = img[i, j]
                        M1 = (r * 10) - 256
                        M2 = (g * 10) / 256
                        M3 = (b * 10) - 256
                        decrypted_img[i, j] = [M1, M2, M3]

                cv2.imwrite('decrypted_image.jpg', decrypted_img)
                print("Image decrypted and saved as 'decrypted_image.jpg'")
                self.display_image(decrypted_img)
            else:
                print("Error: Unable to load the encrypted image.")





    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.img_label.configure(image=img)
        self.img_label.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()

