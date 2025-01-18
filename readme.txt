# Handwritten Text Recognition with EasyOCR and TrOCR

This project is a handwritten text recognition application that allows users to draw on a canvas and detect the handwritten text using OCR models. The project uses EasyOCR and TrOCR for text recognition.

## Project Structure

## Files

- `canvas_widget.py`: Contains the `CanvasApp` class for drawing on the canvas.
- `gui.py`: Contains the `DrawingApp` class for the main GUI application.
- `main.py`: Entry point of the application.
- `ocr_processor.py`: Contains the `OCRProcessor` class for processing OCR text.
- `trocr_model.py`: Contains the `TrOCRModel` class for TrOCR model integration.

## Installation

1. Clone the repository:
    ```sh
    git clone <https://github.com/m01ali/OCR-Handwriting.git>
    cd <repository-directory>
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Use the canvas to draw handwritten text.

3. Click the "Detect Text" button to recognize the handwritten text.

4. Two images will be displayed in the workspace files:
 - output.png: captures the output (word you wrote on canvas)
 - enhanced_image.png: enhances the output image for the OCR model
 (This step has been added for better debugging purposes)

## OCR Models

- **EasyOCR**: Used for general OCR tasks.
- **TrOCR**: Used for handwritten text recognition.

## Acknowledgements

- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [TrOCR](https://huggingface.co/transformers/model_doc/trocr.html)

## License

This project is licensed under the MIT License.
