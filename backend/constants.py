import os

# Folders
IMG_FOLDER = "extracted_images"
CLUSTER_FOLDER = "clusters"
OUTPUT_PDF_FOLDER = "pdfs_output"
PDF_INPUT_FOLDER = "uploaded_pdfs"

# PDF extraction
POPPLER_PATH = os.getenv("POPPLER_PATH")  

# OCR 
KEYWORD_SEARCH_DEPTH = 80
EXAM_KEYWORDS = [
    "examinations",
    "examination",
    "mid-term examination",
    "end-term examination",
    "sem examination",
    "semester examination",
    "national institute of technology durgapur"
]

# DBSCAN clustering
DBSCAN_EPS = 0.8
DBSCAN_MIN_SAMPLES = 3
DBSCAN_METRIC = "cosine"