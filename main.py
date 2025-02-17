import uvicorn
from fastapi import FastAPI
from pdf_extractor import extract_text_from_pdf
from parser import parse_text_to_json
from config import PDF_PATH
import os

app = FastAPI()

@app.get("/extract")
def extract_pdf():
    # Debugging: Ensure PDF path exists
    if not os.path.exists(PDF_PATH):
        return {"error": f"PDF file not found at {PDF_PATH}"}

    extracted_text = extract_text_from_pdf(PDF_PATH)
    return parse_text_to_json(extracted_text, PDF_PATH)  # Pass PDF path here

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
