import shutil
import os
from constants import IMG_FOLDER, CLUSTER_FOLDER, OUTPUT_PDF_FOLDER, PDF_INPUT_FOLDER
from pdf_utils import extract_from_single_pdf, extract_images, rebuild_pdfs
from image_processing import split_two_page_images
from clustering import run_clustering


#region Clean up

# clean up folder after use
def _cleanup():
    if os.path.isdir(IMG_FOLDER):
        shutil.rmtree(IMG_FOLDER)

    if os.path.isdir(CLUSTER_FOLDER):
        shutil.rmtree(CLUSTER_FOLDER)

    if os.path.isdir(OUTPUT_PDF_FOLDER):
        shutil.rmtree(OUTPUT_PDF_FOLDER)

#endregion

def run_pipeline(zip_name):             # pass user name as zip name
    _cleanup()
    pdfs = os.listdir(PDF_INPUT_FOLDER)
    if not pdfs:
        print("PDF path is empty")
        return
    
    if len(pdfs) == 1:
        extract_from_single_pdf(pdfs[0])
    else:
        extract_images(pdfs)
    print("Images extracted...")

    split_two_page_images()
    print("Images splitted if 1 image contains 2 pages...")

    run_clustering()
    print(f"Cluster folders: {os.listdir(CLUSTER_FOLDER)}") 
    
    rebuild_pdfs()
    print(f"Files in OUTPUT_PDF_FOLDER: {os.listdir(OUTPUT_PDF_FOLDER)}")
    
    shutil.make_archive(zip_name, 'zip', OUTPUT_PDF_FOLDER)
    _cleanup()