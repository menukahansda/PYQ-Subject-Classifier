import "./App.css";
import FileUploader from "./components/FileUploader";
import { useEffect, useState } from "react";

export default function App() {
  const [serverReachable, setServerReachable] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initialize = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/reset`);
        setServerReachable(res.ok);
      } catch (err) {
        console.error(err);
        setServerReachable(false);
      } finally {
        setIsLoading(false);
      }
    };

    initialize();
  }, []);

  if (isLoading) {
    return (
      <div className="loader">
        <p>Loading...</p>
      </div>
    );
  }

  if (!serverReachable) {
    return (
      <div className="loader">
        <p>Server Not Reachable</p>
      </div>
    );
  }

  return <FileUploader />;
}
