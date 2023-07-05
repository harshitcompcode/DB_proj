import React, { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [data, setData] = useState([]);

  // Function to handle the file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-data/", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage("Error uploading file");
    }
  };

  // Function to fetch data from the backend
  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:8000/get-data/");
      const data = await response.json();
      setData(data);
    } catch (error) {
      setMessage("Error fetching data");
    }
  };

  return (
    <div>
      <h1>CSV Upload App</h1> (App.js):


      <h1>CSV Upload App</h1>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      <button onClick={fetchData}>Get Data</button>
      <p>{message}</p>
      <table>
        <thead>
          <tr>
            <th>Volume</th>
            <th>Instrument</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.volume}</td>
              <td>{item.instrument}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
