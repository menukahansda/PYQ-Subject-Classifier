import shutil
from pdf2image import convert_from_path 
import cv2
import os
import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from PIL import Image


# list all the pdfs
files = os.listdir("./pdfs")
pdf_files = [f for f in files if f.lower().endswith('.pdf')]

img_folder_path = "extracted_images"
os.makedirs(img_folder_path, exist_ok =True)

#region extract images 
#  extract the images from all the pdfs and save them in single folder
# for i, pdf_file in enumerate(pdf_files):
#     convert_from_path(
#         pdf_path = os.path.join("./pdfs", pdf_file),
#         output_folder= img_folder_path,
#         fmt = "jpg",
#         poppler_path=r"C:\Program Files\poppler-25.12.0\Library\bin",
#         output_file=f"Page_{i}_"
#     )
\
convert_from_path(
    pdf_path = f"./pdfs/{pdf_files[0]}",
    output_folder= img_folder_path,
    fmt="jpg",
    poppler_path=r"C:\Program Files\poppler-25.12.0\Library\bin",
    output_file="Pdf"
)

#endregion


#region crop images

# figure out the pixel position where there is much space and cut it out from there
# separate 2 page image using the pixels, calculate the vertical middle point
# remove prev image and add these 2 new images

def crop_img(grey_img, file_name, ext, mid_page):
    
    left_half = grey_img[:, :mid_page]
    right_half = grey_img[:, mid_page:]
    # cv2.imshow("Left Half", left_half)
    # cv2.imshow("Right Half", right_half)

    os.remove(os.path.join(img_folder_path, f"{file_name}{ext}"))
    cv2.imwrite(os.path.join(img_folder_path, f"{file_name}-01{ext}"), left_half)
    cv2.imwrite(os.path.join(img_folder_path, f"{file_name}-02{ext}"), right_half)

for img_file in os.listdir(img_folder_path):
    image = cv2.imread(os.path.join(img_folder_path, img_file))
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grey Image", grey_img)
    # cv2.waitKey(0)

    height, width = grey_img.shape
    mid_page = width // 2

    file_name, ext = os.path.splitext(img_file)

    if(width > height):
        crop_img(grey_img, file_name, ext, mid_page)

# cut from point which has least noise or least dark pixels
#endregion




#region image to text
# extract text from images and save the text
def img_to_text(img_path):
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(gray)
    return text
#endregion



#region associate images with text

# keep a dict or something to associate images with their text version
texts = []
img2txt = {}
txt2img = {}
i = 0
img_files_list = sorted(
        os.listdir(img_folder_path),
        key=lambda x: int(x.split('-')[1].split('.')[0])
    )
for img_file in img_files_list:
    img_file_path = os.path.join(img_folder_path, img_file)
    text = img_to_text(img_file_path)
    texts.append(text)
    img2txt[img_file] = text
    txt2img[text] = img_file
    print(i)
    i += 1
    # print(text[:100])
#endregion


#region Classify Text
# classify the text and save with numbering

vectorizer = TfidfVectorizer(stop_words='english')
X_vectors = vectorizer.fit_transform(texts)

db = DBSCAN(eps=0.8, min_samples=3, metric='cosine').fit(X_vectors)
labels = db.labels_
#endregion



#region Create Clusters
#-------------------------------------------------------------------------------------------------------------
# check if it is starting page then only it is start of text, else it is part of curr text


# making clustered folder with similar images
cluster_folder_path = "clusters"
os.makedirs(cluster_folder_path, exist_ok=True)
newlabel = max(labels) + 1
for i, label in enumerate(labels):
    # if it is left or right half of the same page and one of the half has cluster then we can change it to the same cluster, 
    if i-1 > 0 and labels[i-1] != -1:
        if img_files_list[i-1].split('-')[0] == img_files_list[i].split('-')[0]: 
            label = labels[i-1]
    elif i+1 < len(labels) and labels[i+1] != -1:
        if img_files_list[i+1].split('-')[0] == img_files_list[i].split('-')[0]: 
            label = labels[i+1]

    if label == -1:
        # if it is still -1 and we have it is part of the same page
        if i-1 > 0 and img_files_list[i-1].split('-')[0] == img_files_list[i].split('-')[0]:
            label = newlabel
            newlabel += 1
        elif i+1 < len(labels) and img_files_list[i+1].split('-')[0] == img_files_list[i].split('-')[0]:
            label = newlabel
            newlabel += 1

        continue
    cluster_dir = os.path.join(cluster_folder_path, f"cluster_{label}")
    os.makedirs(cluster_dir, exist_ok=True)
    img_file = txt2img[texts[i]]
    shutil.move(os.path.join(img_folder_path, img_file), os.path.join(cluster_dir, img_file))

print(labels)
#endregion

#region Create PDFs 

# either create new doc if possible or group the images, and recreate the pdf
cluster_folders = os.listdir(cluster_folder_path)
output_pdf_folder_path = "pdfs_output"
os.makedirs(output_pdf_folder_path, exist_ok=True)
for cluster in cluster_folders:
    cluster_dir = os.path.join(cluster_folder_path, cluster)

    img_files = sorted(
        os.listdir(cluster_dir),
        key=lambda x: int(x.split('-')[1].split('.')[0])
    )

    img_list = []
    for img_file in img_files:
        img_path = os.path.join(cluster_dir, img_file)
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_list.append(Image.fromarray(img_rgb))
    
    pdf_path = os.path.join(output_pdf_folder_path, f"{cluster}.pdf")
    img_list[0].save(pdf_path, save_all=True, append_images=img_list[1:])

#endregion  
    
#region Clean up

# clean up folder after use
# if os.path.isdir(img_folder_path):
#     shutil.rmtree(img_folder_path)

# if os.path.isdir(cluster_folder_path):
#     shutil.rmtree(cluster_folder_path)

# if os.path.isdir(output_pdf_folder_path):
#     shutil.rmtree(output_pdf_folder_path)

#endregion
shutil.make_archive(output_pdf_folder_path, 'zip', output_pdf_folder_path)

