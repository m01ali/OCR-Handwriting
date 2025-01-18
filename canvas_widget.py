import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageDraw

class CanvasApp:
    def __init__(self, root, model):
        self.root = root
        self.model = model

        self.root.title("Canvas with OCR")
        self.root.geometry("900x900")

        # Create a frame for buttons and label
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, anchor=tk.W, pady=10, padx=10)

        # Buttons
        self.detect_button = Button(self.control_frame, text="Detect Text", command=self.detect_text)
        self.detect_button.grid(row=0, column=0, padx=5)

        self.clear_button = Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.eraser_button = Button(self.control_frame, text="Eraser", command=self.activate_eraser)
        self.eraser_button.grid(row=0, column=2, padx=5)

        # Status label
        self.status_label = Label(self.control_frame, text="Detected Text: None")
        self.status_label.grid(row=0, column=3, padx=5)

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=800, bg="white")
        self.canvas.pack(pady=20)

        # Create PIL image to store drawing
        self.image = Image.new("RGB", (800, 800), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Variables for drawing
        self.old_x = None
        self.old_y = None
        self.pen_active = False
        self.eraser_active = False

        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.activate_pen)
        self.canvas.bind("<ButtonRelease-1>", self.deactivate_pen)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

    def activate_pen(self, event):
        self.pen_active = True
        self.old_x = event.x
        self.old_y = event.y

    def deactivate_pen(self, event):
        self.pen_active = False
        self.old_x = None
        self.old_y = None

    def draw_on_canvas(self, event):
        if self.pen_active and self.old_x and self.old_y:
            x, y = event.x, event.y
            color = "white" if self.eraser_active else "black"
            self.canvas.create_line(self.old_x, self.old_y, x, y, fill=color, width=15 if self.eraser_active else 3)
            self.draw.line([self.old_x, self.old_y, x, y], fill=color, width=15 if self.eraser_active else 3)
            self.old_x, self.old_y = x, y

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 800), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.status_label.config(text="Detected Text: None")

    def save_image(self, file_path="output.png"):
        self.image.save(file_path)
        print(f"Image saved to {file_path}")
        return file_path

    def detect_text(self):
        # Save the image and process it for OCR
        saved_image_path = self.save_image()
        enhanced_image_path = "enhanced_image.png"
        enhanced_image = self.model.enhance_image(Image.open(saved_image_path))
        enhanced_image.save(enhanced_image_path)
        print(f"Enhanced image saved to {enhanced_image_path}")
        detected_text = self.model.predict(enhanced_image_path)
        self.status_label.config(text=f"Detected Text: {detected_text}")

    def activate_eraser(self):
        self.eraser_active = not self.eraser_active
        self.eraser_button.config(relief=tk.SUNKEN if self.eraser_active else tk.RAISED)