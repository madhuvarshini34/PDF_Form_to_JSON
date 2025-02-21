# **PDF Checkbox & Text Extractor API**  

🚀 **A FastAPI-based service that extracts text fields and ticked checkboxes from PDFs and returns structured JSON output.**  

---

## **📌 Overview**  
This project is designed to extract **transaction details, checkbox selections, and other form data** from PDF documents dynamically.  

### **🛠 Technologies Used**  
✅ **FastAPI** – For API development  
✅ **PyMuPDF (fitz)** – For PDF text extraction  
✅ **OpenCV** – For checkbox detection  
✅ **Regex** – For structured data extraction  

---

## **⚙️ Features**  
✔️ **Extracts transaction details** (amount, merchant, date, etc.)  
✔️ **Detects ticked checkboxes dynamically**  
✔️ **Formats amounts as floats (e.g., `$149.99`)**  
✔️ **Converts dates to `MM/DD/YYYY` format**  
✔️ **Returns structured JSON output**  

---

## **📂 Project Structure**  
```
📁 project-directory/
│── 📜 main.py           # FastAPI application
│── 📜 parser.py         # Extracts structured data from PDFs
│── 📜 checkbox_parser.py  # Detects and extracts ticked checkboxes
│── 📜 pdf_extractor.py  # Handles PDF text extraction
│── 📜 config.py         # Configurations (e.g., PDF file path)
│── 📜 Requirements.txt  # Dependencies
│── 📜 README.md         # Project documentation
```

---

## **📜 Main Functions & Classes Used**  

### **1️⃣ `main.py`** – FastAPI Server  
**Purpose:** Starts the API server and defines the main endpoint `/extract`.  

#### **Functions**  
- `extract_pdf()` – Calls `pdf_extractor.py` to extract text and passes it to `parser.py` for JSON conversion.  

---

### **2️⃣ `parser.py`** – Extracts structured data from PDFs  
**Purpose:** Parses text and checkbox selections, formats data, and returns a JSON response.  

#### **Functions**  
- `parse_text_to_json(text, pdf_path)`  
  **✅ Extracts:**  
  - **Card number**
  - **Transaction amount**
  - **Date of transaction**
  - **Merchant name**
  - **Ticked checkbox value**
  - **User responses** 

---

### **3️⃣ `checkbox_parser.py`** – Detects checkboxes & extracts ticked options  
**Purpose:** Uses **OpenCV** to detect checkboxes in PDFs and identifies the **ticked checkbox**.  

#### **Class: `CheckboxParser`**  
- `preprocess_image(img)` – Converts images to grayscale and applies thresholding.  
- `extract_ticked_checkbox(debug=False)` –  
  **✅ Detects checkboxes & determines which is ticked**  
  **✅ Uses OpenCV to extract checkbox locations**  
  **✅ Returns the selected option (e.g., `"In my possession"`)**


 **Checkbox Parser:** The parser is hard-coded via a dictionary mapping each checkbox label to fixed (x, y) coordinates on the PDF.
Any change in the PDF layout requires manually updating these coordinate values.
```
checkbox_labels = {
    "Lost": (200, 2640),
    "Stolen": (400, 2640),
    "In my possession": (600, 2640),
    "Never Received": (800, 2640)
}
```

---

### **4️⃣ `pdf_extractor.py`** – Extracts text from PDFs  
**Purpose:** Uses **PyMuPDF** (`fitz`) to extract raw text from a PDF.  

#### **Functions**  
- `extract_text_from_pdf(pdf_path)`  
  **✅ Reads PDF & extracts text for parsing**  

---

## **📥 Installation**  

### **1️⃣ Clone the repository**  
```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### **2️⃣ Create a virtual environment & activate it**  
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install dependencies**  
```bash
pip install -r requirements.txt
```

---

### **🚀 Running the API**  
```bash
uvicorn main:app --reload
```
Open **http://127.0.0.1:8000/extract** in your browser or use:  
```bash
curl -X 'GET' 'http://127.0.0.1:8000/extract' 
```

---

### **🛠 API Endpoints**  
| Method | Endpoint | Description |
|--------|----------|------------|
| **GET** | `/extract` | Extracts text & checkbox selection from the PDF |

---

## **📜 Requirements.txt:**

```
fastapi             # Web framework for API
uvicorn             # ASGI server for running FastAPI
pymupdf             # PyMuPDF for PDF processing (imported as fitz)
opencv-python       # Image processing for checkbox detection
numpy               # Numerical operations for image processing
pytesseract         # OCR tool for reading checkboxes
pdfplumber          # Extracts text from PDFs
pypdf2              # PDF manipulation (reading, extracting pages)
```
---

## **📌 How It Works (Flow Diagram)**  
```plaintext
 User requests data  →  FastAPI (`main.py`)  
                      →  Extracts text (`pdf_extractor.py`)  
                      →  Parses fields (`parser.py`)  
                      →  Detects checkboxes (`checkbox_parser.py`)  
                      →  Returns structured JSON output  
```


## **📌 Conclusion**  
This project provides a **robust solution for automated data extraction from PDFs**, including **checkbox detection and structured text parsing**. With its modular design and **FastAPI integration**, it can be easily extended for additional document processing tasks.  

If you're looking for a **fast, scalable, and accurate** PDF extraction tool, this API is a great starting point. 🚀  
