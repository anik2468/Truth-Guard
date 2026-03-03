import { useState } from "react";
import axios from "axios";

function App(){

const [text,setText] = useState("")
const [result,setResult] = useState("")
const [score,setScore] = useState("")

const checkNews = async () => {

const res = await axios.post(
"http://127.0.0.1:8000/check-news",
{ text:text }
)

setResult(res.data.result)
setScore(res.data.credibility_score)

}

return(

<div style={{textAlign:"center",marginTop:"100px"}}>

<h1>TruthGuard Fake News Detector</h1>

<textarea
rows="6"
cols="50"
placeholder="Paste news text here"
onChange={(e)=>setText(e.target.value)}
></textarea>

<br/><br/>

<button onClick={checkNews}>
Analyze News
</button>

<h2>{result}</h2>
<h3>Credibility Score: {score}</h3>

</div>

)

}

export default App