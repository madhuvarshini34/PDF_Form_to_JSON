import fitz  # PyMuPDF for handling PDFs
import cv2
import numpy as np
import pytesseract
import os

# Ensure Tesseract OCR is installed and correctly configured
pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class CheckboxParser:
    """
    Extracts ticked checkboxes from a given PDF using image processing.
    """

    def __init__(self, pdf_path):
        """
        Initialize the CheckboxParser with the provided PDF path.

        :param pdf_path: Path to the PDF file.
        """
        self.pdf_path = pdf_path

        # Ensure the file exists before processing
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Load the PDF document
        self.doc = fitz.open(pdf_path)

    def preprocess_image(self, img):
        """
        Convert image to grayscale, apply Gaussian blur, and use thresholding.

        :param img: Input image in RGB format.
        :return: Processed binary image with enhanced checkbox visibility.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
        return cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)[1]  # Apply inverse binary thresholding

    def extract_ticked_checkbox(self, debug=False):
        """
        Extracts the selected checkbox from the PDF.

        :param debug: If True, saves a debug image showing detected checkboxes.
        :return: The label of the selected checkbox or "No checkbox detected".
        """
        try:
            # Convert first PDF page to an image at 300 DPI
            pix = self.doc[0].get_pixmap(dpi=300)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n).copy()

            # Convert RGBA to RGB if necessary
            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

            # Process image to enhance checkbox visibility
            processed_img = self.preprocess_image(img)

            # Detect contours (shapes) in the processed image
            contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            checkboxes = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)  # Get bounding box

                # Check if contour size falls within checkbox range
                if 10 <= w <= 40 and 10 <= h <= 40:
                    cx, cy = x + w // 2, y + h // 2  # Calculate center
                    filled_ratio = cv2.countNonZero(processed_img[y:y + h, x:x + w]) / (w * h)  # Check fill percentage
                    is_checked = filled_ratio > 0.3  # Define threshold for detecting a tick
                    checkboxes.append({"x": cx, "y": cy, "checked": is_checked})

            # Define expected checkbox positions (adjust as necessary)
            checkbox_labels = {
                "Lost": (200, 2640),
                "Stolen": (400, 2640),
                "In my possession": (600, 2640),
                "Never Received": (800, 2640)
            }

            # Identify the closest selected checkbox
            selected_option = None
            min_distance = float("inf")

            for label, (lx, ly) in checkbox_labels.items():
                for checkbox in checkboxes:
                    distance = ((checkbox["x"] - lx) ** 2 + (checkbox["y"] - ly) ** 2) ** 0.5  # Euclidean distance
                    if checkbox["checked"] and distance < min_distance:
                        min_distance = distance
                        selected_option = label

            # Debugging: Save an image with highlighted checkboxes
            if debug:
                for checkbox in checkboxes:
                    color = (0, 255, 0) if checkbox["checked"] else (0, 0, 255)  # Green = checked, Red = unchecked
                    cv2.rectangle(img, (checkbox["x"] - 10, checkbox["y"] - 10), 
                                  (checkbox["x"] + 10, checkbox["y"] + 10), color, 2)
                cv2.imwrite("debug_checkbox.png", img)

            return selected_option if selected_option else "No checkbox detected"

        except Exception as e:
            return f"Error extracting checkbox: {str(e)}"
