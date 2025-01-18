from trocr_model import TrOCRModel

def perform_ocr(image):
    model = TrOCRModel()
    detected_text = model.predict(image)
    return detected_text