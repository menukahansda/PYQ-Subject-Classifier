from pdf2image import convert_from_path 
import os
# import cv2      # kept in case BGR handling is needed later
from PIL import Image
from constants import POPPLER_PATH, PDF_INPUT_FOLDER,IMG_FOLDER, CLUSTER_FOLDER, OUTPUT_PDF_FOLDER

# region Extract images 
#  extract the images from all the pdfs and save them in single folder
def extract_images(pdf_filenames):
    os.makedirs(IMG_FOLDER, exist_ok =True)
    for i, pdf in enumerate(pdf_filenames):
        convert_from_path(
            pdf_path = os.path.join(PDF_INPUT_FOLDER, pdf),
            output_folder= IMG_FOLDER,
            fmt = "jpg",
            poppler_path=POPPLER_PATH,
            output_file=f"Pdf_{i}_"
        )

def extract_from_single_pdf(pdf):
    os.makedirs(IMG_FOLDER, exist_ok =True)
    convert_from_path(
        pdf_path = os.path.join(PDF_INPUT_FOLDER, pdf),
        output_folder= IMG_FOLDER,
        fmt="jpg",
        poppler_path=POPPLER_PATH,
        output_file="Pdf_0_"
    )


#endregion

#region Create PDFs 

# either create new doc if possible or group the images, and recreate the pdf
def rebuild_pdfs():
    cluster_folders = os.listdir(CLUSTER_FOLDER)
    os.makedirs(OUTPUT_PDF_FOLDER, exist_ok=True)
    for cluster in cluster_folders:
        cluster_dir = os.path.join(CLUSTER_FOLDER, cluster)

        img_files = sorted(
            os.listdir(cluster_dir),
            key=lambda x: int(x.split('-')[1].split('.')[0])    # might be related to another or else can cause error
        )

        img_list = []
        for img_file in img_files:
            img_path = os.path.join(cluster_dir, img_file)

            # Using Pillow directly instead of cv2 for simplicity
            # cv2 kept below in case BGR handling is needed later
            # img = cv2.imread(img_path)
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img_list.append(Image.fromarray(img_rgb))

            img_list.append(Image.open(img_path).convert("RGB"))
        
        pdf_path = os.path.join(OUTPUT_PDF_FOLDER, f"{cluster}.pdf")
        img_list[0].save(pdf_path, save_all=True, append_images=img_list[1:])

#endregion  