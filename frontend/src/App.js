import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [msg, setMsg] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000")
      .then(res => {
        setMsg(res.data.message);
      });
  }, []);

  return (
    <div style={{textAlign:"center", marginTop:"100px"}}>
      <h1>TruthGuard</h1>
      <h2>{msg}</h2>
    </div>
  );
}

export default App;