import uvicorn  
from fastapi import FastAPI
from pdf_extractor import extract_text_from_pdf
from parser import parse_text_to_json
from config import PDF_PATH
import os
import uvicorn  # Required to run FastAPI

# Initialize FastAPI app
app = FastAPI()

@app.get("/extract")
def extract_pdf():
    """
    Extracts text from the PDF and converts it into structured JSON.

    Returns:
        dict: JSON containing extracted data or an error message.
    """
    # Ensure the PDF file exists before processing
    if not os.path.exists(PDF_PATH):
        return {"error": f"PDF file not found at {PDF_PATH}"}

    try:
        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(PDF_PATH)
        
        # Convert extracted text into structured JSON
        parsed_data = parse_text_to_json(extracted_text, PDF_PATH)

        return parsed_data  # Return the structured JSON response
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}

# Run the FastAPI application (only if executed directly)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

