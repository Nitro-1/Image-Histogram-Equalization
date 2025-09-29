🖼️ Image Histogram Equalizer & Advanced Processing 🔧

An Advanced Image Processing Tool that allows users to load an image, apply Histogram Equalization, Blurs, Sharpening, Edge Detection, and various Brightness/Contrast Adjustments, complete with an Undo/Reset history and Histogram Visualization, built using Python, OpenCV, NumPy, Matplotlib, Pillow, and Tkinter.
 
✨ Features

•	Load & Save Images

•	Histogram Equalization for contrast enhancement

•	Extra Filters: Grayscale • Sepia • Emboss • Flip Horizontal/Vertical • Rotate 90°

•	Gaussian & Median Blurs

•	Sharpening and Edge Detection

•	Brightness/Contrast Adjustments with live preview

•	Processing History: Undo & Reset

•	Show Histogram of pixel intensity
 
 
⚙️ Prerequisites

•	Python 3.7+

•	GUI support (Tkinter)
 

(Optional) Virtual environment

env="venv"

python3 -m venv $env


▶️ Usage

python hist_eq_app.py

1.	Load Image from File menu.
2.	Apply Filters: Click buttons under Filters or select from Extra Filters.
3.	Adjust Brightness/Contrast sliders and click Apply Adjustments.
4.	Undo/Reset actions via History.
5.	Show Histogram to view pixel distribution.
6.	Save Image when done.
 

 
🛠️ Customization Tips
•	Kernel Sizes: Adjust filter kernels in methods like gaussian_blur() and median_blur().
•	Filter Options: Extend apply_extra_filter() with more convolution kernels or transformations.
•	Window Size: Change geometry in __init__ to modify UI dimensions.
 
🐛 Troubleshooting
•	No Image Loaded: Ensure an image is selected before applying operations.
•	Matplotlib Issues: Install python3-tk for TkAgg backend support.
•	Performance: Increase delay between updates or reduce image display size.
 
 
📝 requirements.txt

opencv-python>=4.5.0

numpy>=1.19.0

matplotlib>=3.3.0

Pillow>=8.0.0

