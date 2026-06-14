import { useRef, useState } from "react";

export default function FileUploader() {
  const fileInputRef = useRef(null);
  const [fileSelected, setFileSelected] = useState(false);
  const [isResult, setIsResult] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [blob, setBlob] = useState(null); // blob is used in handleDownloadClick but never stored
  const handleSelectClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      setFileSelected(true);
      console.log(
        "Selected files:",
        Array.from(files).map((f) => f.name),
      );
    }
  };

  const handleProcessClick = () => {
    console.log("Processing PDF...");

    const files = fileInputRef.current.files;
    if (files.length > 0) {
      console.log(
        "Processing files:",
        Array.from(files).map((f) => f.name),
      );
    }

    if (!files.length) {
      console.log("No files selected to process.");
      return;
    }

    const formData = new FormData();
    Array.from(files).forEach((file) => {
      formData.append("pdfs", file);
    });

    // fecth logic
    setIsLoading(true);
    fetch(`${import.meta.env.VITE_API_URL}/process-pdfs`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok)
          throw new Error(`HTTP error! status: ${response.status}`);

        const message = response.headers.get("X-Message");
        console.log(message);

        return response.blob();
      })
      .then((blob) => {
        setBlob(blob);
        setIsResult(true);
      })
      .catch((error) => {
        console.error("Network error or server not reachable:", error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };
  const handleDownloadClick = () => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "output.zip";
    a.click();
    URL.revokeObjectURL(url);
  };
  return (
    <>
      <div className="file-selector">
        <button onClick={handleSelectClick} className="file-selector-btn">
          Select PDF
        </button>
        <input
          type="file"
          accept="application/pdf"
          ref={fileInputRef}
          onChange={handleFileChange}
          multiple
          style={{ display: "none" }}
        />
      </div>
      {fileSelected && !isLoading && !isResult && (
        <div>
          <button className="process-btn" onClick={handleProcessClick}>
            Process PDF
          </button>
        </div>
      )}

      {isResult && (
        <div>
          <button className="download-btn" onClick={handleDownloadClick}>
            {isLoading ? "Processing..." : "Download ZIP"}
          </button>
        </div>
      )}
    </>
  );
}
