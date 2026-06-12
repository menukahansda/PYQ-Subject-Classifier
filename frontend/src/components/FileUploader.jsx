import { useRef, useState } from "react";

export default function FileUploader() {
  const fileInputRef = useRef(null);
  const [fileSelected, setFileSelected] = useState(false);
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
    fetch(`${import.meta.env.VITE_API_URL}/process-pdfs`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("POST request sent successfully");
        } else {
          console.log("POST request failed with status:", response.status);
        }
      })
      .catch((error) => {
        console.error("Network error or server not reachable:", error);
      });
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
      {fileSelected && (
        <button className="process-btn" onClick={handleProcessClick}>
          Process PDF
        </button>
      )}
    </>
  );
}
