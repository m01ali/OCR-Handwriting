import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import re

class TrOCRModel:
    def __init__(self):
        # Load the model and processor
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

    def enhance_image(self, image):
        # Convert to grayscale
        image = image.convert("L")
        # Enhance the contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        # Binarize the image
        image = image.point(lambda p: p > 128 and 255)
        return image

    def reduce_noise(self, image):
        # Convert PIL image to numpy array
        image_np = np.array(image)
        # Apply median blur to reduce noise while preserving edges
        image_np = cv2.medianBlur(image_np, 3)
        # Convert back to PIL image
        image = Image.fromarray(image_np)
        return image

    def segment_lines(self, image):
        # Convert PIL image to grayscale numpy array
        image_np = np.array(image.convert("L"))
        # Binarize the image
        _, binary_image = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY_INV)
        
        # Calculate the horizontal projection profile
        horizontal_projection = np.sum(binary_image, axis=1)
        
        # Detect lines based on horizontal projection profile
        line_indices = np.where(horizontal_projection > 0)[0]
        
        # Group consecutive indices to form lines
        lines = []
        current_line = []
        for index in line_indices:
            if len(current_line) == 0 or index == current_line[-1] + 1:
                current_line.append(index)
            else:
                lines.append(current_line)
                current_line = [index]
        if current_line:
            lines.append(current_line)
        
        # Add increased padding between lines
        padding = 15
        line_images = []
        for line in lines:
            top = max(0, line[0] - padding)
            bottom = min(image.height, line[-1] + 1 + padding)
            line_image = image.crop((0, top, image.width, bottom)).convert("RGB")
            line_images.append(line_image)
        
        return line_images

    def preprocess_image(self, image_path):
        # Open the image
        image = Image.open(image_path).convert("RGB")
        # Enhance the image
        image = self.enhance_image(image)
        # Reduce noise
        image = self.reduce_noise(image)
        # Segment the image into lines
        line_images = self.segment_lines(image)
        return line_images

    #Post Processing method to clean up the detected text:-
    
    def clean_text(self, text):
        # Remove unwanted characters or artifacts, but keep numbers and symbols
        cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        # Heuristic to filter out hallucinated numbers
        words = cleaned_text.split()
        filtered_words = []
        for i, word in enumerate(words):
            # Allow numbers if they are part of a larger context or not isolated
            if re.match(r'^\d+$', word):
                if (i > 0 and re.match(r'\D', words[i-1])) or (i < len(words) - 1 and re.match(r'\D', words[i+1])):
                    filtered_words.append(word)
                else:
                    filtered_words.append(word)  # Less aggressive filtering
            else:
                filtered_words.append(word)
        
        return ' '.join(filtered_words)

    def merge_lines(self, lines):
        # Merge lines if they appear to be part of the same sentence or phrase
        merged_lines = []
        for i in range(len(lines)):
            if i > 0 and (lines[i][0].islower() or len(lines[i].split()) == 1):
                merged_lines[-1] += ' ' + lines[i]
            else:
                merged_lines.append(lines[i])
        return merged_lines

    def predict(self, image_path):
        # Preprocess the image
        line_images = self.preprocess_image(image_path)
        detected_text = []
        for line_image in line_images:
            # Convert image to tensor
            pixel_values = self.processor(images=line_image, return_tensors="pt").pixel_values
            generated_ids = self.model.generate(pixel_values)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            cleaned_text = self.clean_text(generated_text)
            detected_text.append(cleaned_text)
        merged_text = self.merge_lines(detected_text)
        return "\n".join(merged_text)