import React, { useState } from "react";
import axios from "axios";

function App() {

  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [score, setScore] = useState("");
  const [image, setImage] = useState(null);

  // -----------------------
  // TEXT NEWS CHECK
  // -----------------------
  const checkNews = async () => {

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/check-news",
        { text: text }
      );

      setResult(res.data.result);
      setScore(res.data.credibility_score);

    } catch (error) {
      console.error(error);
      alert("Backend connection error");
    }

  };

  // -----------------------
  // IMAGE CHECK
  // -----------------------
  const checkImage = async () => {

    if (!image) {
      alert("Please upload an image first");
      return;
    }

    try {

      const formData = new FormData();
      formData.append("file", image);

      const res = await axios.post(
        "http://127.0.0.1:8000/check-image",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      setResult(res.data.result);
      setScore(res.data.credibility_score);

    } catch (error) {
      console.error(error);
      alert("Image analysis failed");
    }

  };

  return (

    <div style={{ textAlign: "center", marginTop: "100px" }}>

      <h1>TruthGuard Fake News Detector</h1>

      <textarea
        rows="6"
        cols="50"
        placeholder="Paste news text here"
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />

      <button onClick={checkNews}>
        Analyze News
      </button>

      <h2>{result}</h2>
      <h3>Credibility Score: {score}</h3>

      <br /><br />

      <h2>Upload Image</h2>

      <input
        type="file"
        onChange={(e) => setImage(e.target.files[0])}
      />

      <br /><br />

      <button onClick={checkImage}>
        Analyze Image
      </button>

    </div>
  );

}

export default App;