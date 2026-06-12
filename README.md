# PYQ Subject Classifier

It is an unsupervised learning model that classifies a given PDF input into different subjects and returns a ZIP archive containing the classified subject-wise PDFs.

## Features

- Automatic extraction of pages from PDF documents
- OCR-based text extraction using Tesseract
- Unsupervised clustering using TF-IDF and DBSCAN
- Subject-wise grouping without requiring labeled training data
- Reconstruction of clustered pages into separate PDFs
- Downloadable ZIP archive containing all classified PDFs

---

## Dataset

- Test Data: Previous Year Question Papers (PYQs) collected (mixed subjects in single pdf)
- User Input : Supports scanned and digital PDF documents
- No labeled dataset required

---

## Project Structure

```text
project-root/
├── backend/
│   ├── pipeline.py
│   └── main.py
│   
├── frontend/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   
├── .gitignore
├── README.md

```

---

## Tech Stack

### Backend 
- FastAPI (Python)

### Frontend
- React
- JavaScript

### Libraries & Tools for model

- OpenCV
- Tesseract OCR
- pdf2image
- Pillow
- scikit-learn
- DBSCAN
- TF-IDF Vectorizer

---


## Installation

### Clone the Repository

```bash
git clone https://github.com/menukahansda/PYQ-Subject-Classifier.git
cd PYQ-Subject-Classifier
```

### Backend Setup

```bash
pip install -r requirements.txt
```

### Frontend Setup

```bash
npm install
```

---

## Usage

### Run Backend

```bash
python main.py 
    or 
py main.py
```

### Run Frontend

```bash
npm run dev
```

---

## Workflow

1. Upload PDF containing multiple question papers.
2. Convert PDF pages into images.
3. Extract text from images using OCR.
4. Generate TF-IDF vectors from extracted text.
5. Cluster similar question papers using DBSCAN.
6. Group pages belonging to the same subject.
7. Recreate subject-wise PDFs.
8. Generate and return a ZIP archive containing classified PDFs.

---

<!-- ## Screenshots

### Home Page

<!-- image -->

<!-- ### Classification Result -->

<!-- image  -->

<!-- --- -->

## Future Improvements

- Improve OCR accuracy for low-quality scans
- Support handwritten question papers
- Add subject name prediction
- Improve clustering performance

---

## Known Limitations

- OCR accuracy depends on image quality
- Subject separation may be affected by noisy scans
- Requires Tesseract OCR

---

## Author

- Name: Menuka Hansda
- GitHub: [github link](https://github.com/menukahansda)
