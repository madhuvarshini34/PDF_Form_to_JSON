import fitz  # PyMuPDF
import cv2
import numpy as np
import pytesseract
import os

# Ensure Tesseract is installed
pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class CheckboxParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        self.doc = fitz.open(pdf_path)

    def preprocess_image(self, img):
        """Convert image to grayscale and apply thresholding"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)[1]

    def extract_ticked_checkbox(self, debug=False):
        """Extract the ticked checkbox option from the PDF"""
        try:
            pix = self.doc[0].get_pixmap(dpi=300)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n).copy()

            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

            processed_img = self.preprocess_image(img)
            contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            checkboxes = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if 10 <= w <= 40 and 10 <= h <= 40:  # Ensure it's a checkbox size
                    cx, cy = x + w // 2, y + h // 2  # Calculate center
                    filled_ratio = cv2.countNonZero(processed_img[y:y + h, x:x + w]) / (w * h)
                    is_checked = filled_ratio > 0.3  # Threshold for tick detection
                    checkboxes.append({"x": cx, "y": cy, "checked": is_checked})

            # Label positions (update these values if necessary)
            checkbox_labels = {
                "Lost": (200, 2640),
                "Stolen": (400, 2640),
                "In my possession": (600, 2640),
                "Never Received": (800, 2640)
            }

            selected_option = None
            min_distance = float("inf")

            for label, (lx, ly) in checkbox_labels.items():
                for checkbox in checkboxes:
                    distance = ((checkbox["x"] - lx) ** 2 + (checkbox["y"] - ly) ** 2) ** 0.5  # Euclidean distance
                    if checkbox["checked"] and distance < min_distance:
                        min_distance = distance
                        selected_option = label

            # Debugging: Save image with detected checkboxes
            if debug:
                for checkbox in checkboxes:
                    color = (0, 255, 0) if checkbox["checked"] else (0, 0, 255)  # Green for checked, Red for unchecked
                    cv2.rectangle(img, (checkbox["x"] - 10, checkbox["y"] - 10), 
                                  (checkbox["x"] + 10, checkbox["y"] + 10), color, 2)
                cv2.imwrite("debug_checkbox.png", img)

            return selected_option if selected_option else "No checkbox detected"

        except Exception as e:
            return f"Error extracting checkbox: {str(e)}"
