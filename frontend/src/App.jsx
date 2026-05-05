import { useRef, useState} from "react";
import "./App.css";

function App() {
  const fileInputRef = useRef(null);
  const [fileSelected, setFileSelected] = useState(false);

  const handleSelectClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileSelected(true);
      console.log("Selected file:", file.name);
    }
  };

  const handleProcessClick = () => {
    console.log("Processing PDF...");
    
  }
  return (
    <>
      <div className="file-selector">
        <button onClick={handleSelectClick} className="file-selector-btn">
          Select PDF
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
      </div>
      {fileSelected && 
        <button className="process-btn" onClick={handleProcessClick}>
          Process PDF
        </button>
      }
    </>
  );
}

export default App;
