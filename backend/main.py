from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os

from constants import PDF_INPUT_FOLDER, IMG_FOLDER, CLUSTER_FOLDER, OUTPUT_PDF_FOLDER
from pipeline import run_pipeline

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Message"],
)

port = int(os.getenv("PORT", 8000))
ZIP_FILENAME = "testResults"
ZIP_FILE = ZIP_FILENAME + ".zip"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/reset")
def reset():
    if os.path.isdir(IMG_FOLDER):
        shutil.rmtree(IMG_FOLDER)

    if os.path.isdir(CLUSTER_FOLDER):
        shutil.rmtree(CLUSTER_FOLDER)

    if os.path.isdir(OUTPUT_PDF_FOLDER):
        shutil.rmtree(OUTPUT_PDF_FOLDER)

    if os.path.exists(PDF_INPUT_FOLDER):
        shutil.rmtree(PDF_INPUT_FOLDER)
        print(f"Cleaned up {PDF_INPUT_FOLDER}")

    if os.path.exists(ZIP_FILE):  
        os.remove(ZIP_FILE)
        print("cleaned zip")

    return JSONResponse(content={"message": "Input folder cleared"}, status_code=200)

@app.post("/process-pdfs")
async def process_pdfs(pdfs: list[UploadFile] = File(...)):
    if not pdfs:
        return JSONResponse(status_code=400, content={"error": "No PDF files uploaded"})
    print("Received PDF files:", [pdf.filename for pdf in pdfs])
    
    # create folder and add pdf
    os.makedirs(PDF_INPUT_FOLDER , exist_ok=True)

    for pdf in pdfs:
        with open(f"{PDF_INPUT_FOLDER}/{pdf.filename}", "wb") as f:
            f.write(await pdf.read())

    print("PDF files saved to disk...")

    # run the actual pipeline
    try:
        run_pipeline(ZIP_FILENAME)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    if not os.path.exists(ZIP_FILE):
        return JSONResponse(status_code=500, content={"error": "ZIP file was not created"})

    return FileResponse(
        path=ZIP_FILE,
        filename="output.zip",
        media_type="application/zip",
        headers={"X-Message": "PDF processed successfully"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)