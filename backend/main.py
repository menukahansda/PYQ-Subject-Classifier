from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os

from constants import PDF_INPUT_FOLDER
from pipeline import run_pipeline

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

port = int(os.getenv("PORT", 8000))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/process-pdfs")
async def process_pdfs(pdfs: list[UploadFile] = File(...)):
    if not pdfs:
        return JSONResponse(status_code=400, content={"error": "No PDF files uploaded"})
    print("Received PDF files:", [pdf.filename for pdf in pdfs])
    
    # add the processing logic
    os.makedirs(PDF_INPUT_FOLDER , exist_ok=True)

    for pdf in pdfs:
        with open(f"{PDF_INPUT_FOLDER}/{pdf.filename}", "wb") as f:
            f.write(await pdf.read())

    print("PDF files saved to disk...")
    run_pipeline("testResult")
    return JSONResponse(content={"message": "PDF files received and processed successfully"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)