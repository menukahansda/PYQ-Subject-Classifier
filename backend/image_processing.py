import pytesseract
import cv2
import os
from constants import IMG_FOLDER

#region crop images

# figure out the pixel position where there is much space and cut it out from there
# separate 2 page image using the pixels, calculate the vertical middle point
# remove prev image and add these 2 new images

def _crop_img(grey_img, file_name, ext, mid_page):
    
    left_half = grey_img[:, :mid_page]
    right_half = grey_img[:, mid_page:]
    # cv2.imshow("Left Half", left_half)
    # cv2.imshow("Right Half", right_half)

    os.remove(os.path.join(IMG_FOLDER, f"{file_name}{ext}"))
    cv2.imwrite(os.path.join(IMG_FOLDER, f"{file_name}-01{ext}"), left_half)
    cv2.imwrite(os.path.join(IMG_FOLDER, f"{file_name}-02{ext}"), right_half)

def split_two_page_images():
    for img_file in os.listdir(IMG_FOLDER):
        image = cv2.imread(os.path.join(IMG_FOLDER, img_file))
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Grey Image", grey_img)
        # cv2.waitKey(0)

        height, width = grey_img.shape
        mid_page = width // 2

        file_name, ext = os.path.splitext(img_file)

        if(width > height):
            _crop_img(grey_img, file_name, ext, mid_page)

# cut from point which has least noise or least dark pixels
#endregion



#region image to text
# extract text from images and save the text
def img_to_text(img_path):
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(gray)
    return text
#endregion