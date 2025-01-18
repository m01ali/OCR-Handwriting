import tkinter as tk
from canvas_widget import DrawingCanvas
from ocr_processor import perform_ocr

class DrawingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Canvas with OCR")
        
        self.canvas = DrawingCanvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)
        
        self.label = tk.Label(self.root, text="Detected Text: ", font=("Arial", 14))
        self.label.pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.activate_btn = tk.Button(button_frame, text="Activate Pen", command=self.canvas.activate_pen)
        self.activate_btn.grid(row=0, column=0, padx=5)
        
        self.deactivate_btn = tk.Button(button_frame, text="Deactivate Pen", command=self.canvas.deactivate_pen)
        self.deactivate_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_canvas)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        self.ocr_btn = tk.Button(button_frame, text="Detect Text", command=self.detect_text)
        self.ocr_btn.grid(row=0, column=3, padx=5)
    
    def clear_canvas(self):
        self.canvas.clear()
        self.label.config(text="Detected Text: ")
    
    def detect_text(self):
        image = self.canvas.get_image()
        detected_text = perform_ocr(image)
        self.label.config(text=f"Detected Text: {detected_text}")
    
    def run(self):
        self.root.mainloop()
