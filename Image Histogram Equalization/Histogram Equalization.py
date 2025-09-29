import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

class AdvancedImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Processing Tool")
        self.root.geometry("1000x700")
        self.root.minsize(900, 700)

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.processing_history = []
        self.base_image_for_adjustments = None 

        self.create_gui()

    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        file_frame = ttk.LabelFrame(main_frame, text="File", padding="10")
        file_frame.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        load_button = ttk.Button(file_frame, text="Load Image", command=self.load_image, width=30)
        load_button.grid(row=0, column=0, padx=5, pady=3)
        save_button = ttk.Button(file_frame, text="Save Image", command=self.save_image, width=30)
        save_button.grid(row=0, column=1, padx=5, pady=3)

        filter_frame = ttk.LabelFrame(main_frame, text="Filters", padding="10")
        filter_frame.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        equalize_button = ttk.Button(filter_frame, text="Equalize Histogram", command=self.equalize_histogram, width=20)
        equalize_button.grid(row=0, column=0, padx=5, pady=3)
        gaussian_blur_button = ttk.Button(filter_frame, text="Gaussian Blur", command=self.gaussian_blur, width=20)
        gaussian_blur_button.grid(row=1, column=0, padx=5, pady=3)
        median_blur_button = ttk.Button(filter_frame, text="Median Blur", command=self.median_blur, width=20)
        median_blur_button.grid(row=0, column=1, padx=5, pady=3)
        sharpen_button = ttk.Button(filter_frame, text="Sharpen", command=self.sharpen, width=20)
        sharpen_button.grid(row=1, column=1, padx=5, pady=3)
        edge_detection_button = ttk.Button(filter_frame, text="Edge Detection", command=self.edge_detection, width=20)
        edge_detection_button.grid(row=0, column=2, padx=5, pady=3)

        adjust_frame = ttk.LabelFrame(main_frame, text="Adjustments", padding="10")
        adjust_frame.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(adjust_frame, text="Brightness:").grid(row=0, column=0, sticky=tk.W)
        self.brightness_scale = ttk.Scale(adjust_frame, from_=-100, to=100, orient=tk.HORIZONTAL, length=200,
                                          command=self.adjust_brightness)
        self.brightness_scale.set(0)
        self.brightness_scale.grid(row=0, column=1, padx=5, pady=3)
        
        ttk.Label(adjust_frame, text="Contrast:").grid(row=1, column=0, sticky=tk.W)
        self.contrast_scale = ttk.Scale(adjust_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, length=200,
                                        command=self.adjust_contrast)
        self.contrast_scale.set(1.0)
        self.contrast_scale.grid(row=1, column=1, padx=5, pady=3)
        
        apply_adjust_button = ttk.Button(adjust_frame, text="Apply Adjustments", command=self.apply_adjustments, width=20)
        apply_adjust_button.grid(row=0, column=2, rowspan=2, padx=5, pady=3)

        history_frame = ttk.LabelFrame(main_frame, text="History", padding="10")
        history_frame.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        undo_button = ttk.Button(history_frame, text="Undo", command=self.undo, width=15)
        undo_button.grid(row=0, column=0, padx=5, pady=3)
        reset_button = ttk.Button(history_frame, text="Reset", command=self.reset, width=15)
        reset_button.grid(row=0, column=1, padx=5, pady=3)
        histogram_button = ttk.Button(history_frame, text="Show Histogram", command=self.show_histogram, width=15)
        histogram_button.grid(row=0, column=2, padx=5, pady=3)

        extra_filter_frame = ttk.LabelFrame(main_frame, text="Extra Filters", padding="10")
        extra_filter_frame.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Label(extra_filter_frame, text="Select Filter:").grid(row=0, column=0, sticky=tk.W)
        self.filter_combobox = ttk.Combobox(extra_filter_frame, values=["None", "Grayscale", "Sepia", "Emboss",
                                                                        "Flip Horizontal", "Flip Vertical", "Rotate 90"],
                                            state="readonly", width=20)
        self.filter_combobox.set("None")
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=3)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_extra_filter)

        self.image_frame = ttk.Frame(main_frame, borderwidth=2, relief="sunken")
        self.image_frame.grid(row=0, column=1, rowspan=5, sticky=(tk.N, tk.E, tk.S, tk.W), padx=10, pady=5)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True, fill=None, anchor="center")

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    messagebox.showerror("Error", "Could not load the image. Please check the file format.")
                    return
                self.processed_image = self.original_image.copy()
                self.base_image_for_adjustments = self.original_image.copy()
                self.processing_history = [self.original_image.copy()]
                self.display_image(self.processed_image)
                # Reset sliders
                self.brightness_scale.set(0)
                self.contrast_scale.set(1.0)
                self.filter_combobox.set("None")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        else:
            messagebox.showinfo("Info", "No image selected.")

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(
                title="Save Image As",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    cv2.imwrite(file_path, self.processed_image)
                    messagebox.showinfo("Info", f"Image saved successfully to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No image to save.")

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

        max_width = 1000  
        zoom_factor = 1.2  

        img_width, img_height = image_pil.size

        new_width = int(img_width * zoom_factor)
        new_height = int(img_height * zoom_factor)

        if new_width > max_width:
            scale = max_width / new_width
            new_width = int(new_width * scale)
            new_height = int(new_height * scale)

        image_pil = image_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)

        image_tk = ImageTk.PhotoImage(image_pil)
        self.image_label.config(image=image_tk)
        self.image_label.image = image_tk  

    def equalize_histogram(self):
        if self.processed_image is not None:
            gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            equalized_image = cv2.equalizeHist(gray_image)
            self.processed_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR)
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def gaussian_blur(self):
        if self.processed_image is not None:
            self.processed_image = cv2.GaussianBlur(self.processed_image, (5, 5), 0)
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def median_blur(self):
        if self.processed_image is not None:
            self.processed_image = cv2.medianBlur(self.processed_image, 5)
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def sharpen(self):
        if self.processed_image is not None:
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            self.processed_image = cv2.filter2D(self.processed_image, -1, kernel)
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def edge_detection(self):
        if self.processed_image is not None:
            gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, 100, 200)
            self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def adjust_brightness(self, value):
        if self.base_image_for_adjustments is not None:
            brightness = int(float(value))
            contrast = float(self.contrast_scale.get())
            
            img = self.base_image_for_adjustments.copy().astype(np.float32)
            
            # Apply contrast first, then brightness
            img = img * contrast + brightness
            img = np.clip(img, 0, 255).astype(np.uint8)
            
            self.processed_image = img
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def adjust_contrast(self, value):
        if self.base_image_for_adjustments is not None:
            contrast = float(value)
            brightness = int(float(self.brightness_scale.get()))
            
            img = self.base_image_for_adjustments.copy().astype(np.float32)
            
            # Apply contrast first, then brightness
            img = img * contrast + brightness
            img = np.clip(img, 0, 255).astype(np.uint8)
            
            self.processed_image = img
            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def apply_adjustments(self):
        """Apply current brightness/contrast adjustments to processing history"""
        if self.processed_image is not None:
            self.base_image_for_adjustments = self.processed_image.copy()
            self.update_processing_history()
            # Reset sliders
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)

    def update_processing_history(self):
        self.processing_history.append(self.processed_image.copy())

    def undo(self):
        if len(self.processing_history) > 1:
            self.processing_history.pop()
            self.processed_image = self.processing_history[-1].copy()
            self.base_image_for_adjustments = self.processed_image.copy()
            self.display_image(self.processed_image)
            # Reset sliders
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
        else:
            messagebox.showwarning("Warning", "No more actions to undo.")

    def reset(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.base_image_for_adjustments = self.original_image.copy()
            self.processing_history = [self.original_image.copy()]
            self.display_image(self.processed_image)
            self.brightness_scale.set(0)
            self.contrast_scale.set(1.0)
            self.filter_combobox.set("None")
        else:
            messagebox.showwarning("Warning", "No image to reset.")

    def show_histogram(self):
        if self.processed_image is not None:
            gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            plt.hist(gray_image.ravel(), bins=256, histtype='step', color='black')
            plt.title("Histogram")
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.show()
        else:
            messagebox.showwarning("Warning", "No image loaded.")

    def apply_extra_filter(self, event=None):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image loaded.")
            return
        option = self.filter_combobox.get()
        if option == "None":
            return
            
        img = self.processed_image.copy()
        if option == "Grayscale":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif option == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            img = cv2.transform(img, kernel)
            img = np.clip(img, 0, 255).astype(np.uint8)
        elif option == "Emboss":
            kernel = np.array([[-2, -1, 0],
                               [-1, 1, 1],
                               [0, 1, 2]])
            img = cv2.filter2D(img, -1, kernel)
        elif option == "Flip Horizontal":
            img = cv2.flip(img, 1)
        elif option == "Flip Vertical":
            img = cv2.flip(img, 0)
        elif option == "Rotate 90":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
        self.processed_image = img
        self.base_image_for_adjustments = img.copy()
        self.update_processing_history()
        self.display_image(self.processed_image)
        self.brightness_scale.set(0)
        self.contrast_scale.set(1.0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedImageProcessingApp(root)
    root.mainloop()
