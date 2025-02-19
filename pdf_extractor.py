import pdfplumber  # Library for extracting text from PDFs

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from all pages of a given PDF file.
    
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a single string.
    """
    extracted_text = ""  # Initialize an empty string to store extracted text
    
    with pdfplumber.open(pdf_path) as pdf:  # Open the PDF file
        for page in pdf.pages:  # Iterate through each page
            extracted_text += page.extract_text() + "\n"  # Extract and append text
    
    return extracted_text  # Return the complete extracted text
