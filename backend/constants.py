import os

# Folders
IMG_FOLDER = "extracted_images"
CLUSTER_FOLDER = "clusters"
OUTPUT_PDF_FOLDER = "pdfs_output"
PDF_INPUT_FOLDER = "uploaded_pdfs"
TEST_PDFS_FOLDER = "test_pdfs"

# PDF extraction
POPPLER_PATH = os.getenv("POPPLER_PATH")  

# OCR 
KEYWORD_SEARCH_DEPTH = 500
EXAM_KEYWORDS = [
    "examinations",
    "examination",
    "mid-term examination",
    "end-term examination",
    "sem examination",
    "semester examination",
    "national institute of technology durgapur",
    "b. tech",
    "b.tech",
    "btech",
    "mid sem",
    "mid-sem",
    "mid term",
    "mid-term",
    "national institute of technology",
    "department of computer science",
    "full marks",
    "subject:",
    "course code",
    "nit durgapur",
    
    "odd semester",
    "even semester",
    "odd sem",
    "even sem",
    "odd.",
    "even.",
    
    # registration / academic year
    "reg.",
    "reg ",
    "regular",
    
    # institution variants
    "nitdgp",
    "nitdgp/btech",
    "n.i.t. durgapur",
    
    # paper/header terminology
    "course code:",
    "course name:",
    "subject code",
    "paper code",
    "question paper no.:",
    "date of exam:",
]

# DBSCAN clustering
DBSCAN_EPS = 0.8
DBSCAN_MIN_SAMPLES = 3
DBSCAN_METRIC = "cosine"