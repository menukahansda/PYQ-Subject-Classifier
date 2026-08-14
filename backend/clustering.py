from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import shutil
import os

from image_processing import img_to_text
from constants import IMG_FOLDER, CLUSTER_FOLDER, EXAM_KEYWORDS, KEYWORD_SEARCH_DEPTH

# region associate images with text


def _associate_images_with_text(img_files_list, texts, img2txt, txt2img):
    textIndex = 0
    for i, img_file in enumerate(img_files_list):
        img_file_path = os.path.join(IMG_FOLDER, img_file)
        text = img_to_text(img_file_path)

        # check if it is starting page then only it is start of text, else it is part of curr text
        if not texts or any(kw in text[:KEYWORD_SEARCH_DEPTH].lower() for kw in EXAM_KEYWORDS):
            texts.append(text)

            img2txt[img_file] = textIndex
            txt2img[textIndex] = []
            txt2img[textIndex].append(img_file)
            textIndex += 1
            with open("headers.txt", "a") as f:
                f.write(f"Page {i}")
                f.write(
                    "-------------------------------------------------------------------------------------------\n"
                )
                f.write(text)
                f.write("...\n\n")
        else:
            texts[-1] += text
            img2txt[img_file] = textIndex - 1
            txt2img[textIndex - 1].append(img_file)

        print(i)

        # print(text[:KEYWORD_SEARCH_DEPTH])
        # print("-------------------------------------------------------")


# endregion


# region Classify Text
# classify the text and save with numbering
def _classify_text(texts):
    vectorizer = TfidfVectorizer(stop_words="english")
    X_vectors = vectorizer.fit_transform(texts)

    db = DBSCAN(eps=0.8, min_samples=3, metric="cosine").fit(X_vectors)
    labels = db.labels_
    return labels


# endregion


# region Create Clusters
# -------------------------------------------------------------------------------------------------------------


# making clustered folder with similar images
def _create_clusters(labels, txt2img):
    os.makedirs(CLUSTER_FOLDER, exist_ok=True)
    newlabel = max(labels) + 1

    for i, label in enumerate(labels):
        # if it is left or right half of the same page and one of the half has cluster then we can change it to the same cluster,
        # if i-1 > 0 and labels[i-1] != -1:
        #     if img_files_list[i-1].split('-')[0] == img_files_list[i].split('-')[0]:
        #         label = labels[i-1]
        # elif i+1 < len(labels) and labels[i+1] != -1:
        #     if img_files_list[i+1].split('-')[0] == img_files_list[i].split('-')[0]:
        #         label = labels[i+1]

        if label == -1:
            img_files = txt2img[i]
            # check if any image in this document shares a base filename with an image in an adjacent document
            if i - 1 >= 0:
                prev_img_files = txt2img[i - 1]
                if any(
                    img.split("-")[0] == prev.split("-")[0]
                    for img in img_files
                    for prev in prev_img_files
                ):
                    label = newlabel
                    newlabel += 1
            elif i + 1 < len(labels):
                next_img_files = txt2img[i + 1]
                if any(
                    img.split("-")[0] == nxt.split("-")[0]
                    for img in img_files
                    for nxt in next_img_files
                ):
                    label = newlabel
                    newlabel += 1
            if label == -1:
                continue

        cluster_dir = os.path.join(CLUSTER_FOLDER, f"cluster_{label}")
        os.makedirs(cluster_dir, exist_ok=True)

        img_files = txt2img[i]
        for img_file in img_files:
            shutil.move(
                os.path.join(IMG_FOLDER, img_file), os.path.join(cluster_dir, img_file)
            )

    print(labels)


# endregion


def run_clustering():
    # keep a dict or something to associate images with their text version
    texts = []
    img2txt = {}
    txt2img = {}
    img_files_list = sorted(os.listdir(IMG_FOLDER))

    _associate_images_with_text(img_files_list, texts, img2txt, txt2img)
    print("Texts associated...")

    labels = _classify_text(texts)
    print("Texts classified...")

    _create_clusters(labels, txt2img)
    print("CLusters created...")
