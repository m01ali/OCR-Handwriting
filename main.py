from canvas_widget import CanvasApp
from trocr_model import TrOCRModel
import tkinter as tk

if __name__ == "__main__":
    # Initialize the Tkinter root window
    root = tk.Tk()
    
    # Initialize the OCR model
    ocr_model = TrOCRModel()
    
    # Pass the model to the Canvas app
    app = CanvasApp(root, ocr_model)
    
    # Run the Tkinter event loop
    root.mainloop()
