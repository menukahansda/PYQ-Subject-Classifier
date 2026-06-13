import "./App.css";
import FileUploader from "./components/FileUploader";
import { useEffect } from "react";

export default function App() {
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/reset`);
  }, []);
  return <FileUploader />;
}
