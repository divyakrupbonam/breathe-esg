import { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";
import Login from "./Login";

function App() {

  const [records, setRecords] = useState([]);
  const [file, setFile] = useState(null);
  const [sourceType, setSourceType] = useState("SAP");

  const [token, setToken] = useState(null);

  // ✅ LOAD TOKEN ON FIRST LOAD
  useEffect(() => {
    const saved = localStorage.getItem("token");
    setToken(saved);
  }, []);

  // ✅ FETCH DATA AFTER LOGIN
  useEffect(() => {
    if (token) {
      fetchRecords(token);
    }
  }, [token]);

  const fetchRecords = async (authToken) => {
    try {
      const response = await axios.get(
        "https://breathe-esg-production-83b0.up.railway.app/api/emissions/",
        {
          headers: {
            Authorization: `Bearer ${authToken}`
          }
        }
      );

      setRecords(response.data);
    } catch (err) {
      console.log("Fetch error:", err);
    }
  };

  const approveRecord = async (id) => {
    await axios.post(
      `https://breathe-esg-production-83b0.up.railway.app/api/emissions/${id}/approve/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    fetchRecords(token);
  };

  const uploadFile = async () => {

  console.log(token);

  if (!file) {
    alert("Please select a file");
    return;
  }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("source_type", sourceType);
    formData.append("company_id", 1);

    await axios.post(
      "https://breathe-esg-production-83b0.up.railway.app/api/ingestion/upload/",
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    alert("Upload successful");
    fetchRecords(token);
  };

  // ✅ LOGIN SCREEN
  if (!token) {
    return <Login setToken={setToken} />;
  }

  const chartData = records.map((r) => ({
    name: r.category,
    co2e: r.co2e_emission
  }));

  return (
    <div style={{ padding: "20px" }}>

      <h1>Breathe ESG Dashboard</h1>

      <h2>Upload ESG Data</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <select
        value={sourceType}
        onChange={(e) => setSourceType(e.target.value)}
      >
        <option value="SAP">SAP</option>
        <option value="UTILITY">UTILITY</option>
        <option value="TRAVEL">TRAVEL</option>
      </select>

      <br /><br />

      <button onClick={uploadFile}>
        Upload Data
      </button>

      <hr />

      <h2>Emissions Chart</h2>

      <BarChart width={600} height={300} data={chartData}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="co2e" />
      </BarChart>

      <hr />

      <h2>Emission Records</h2>

      <table border="1" cellPadding="10">

        <thead>
          <tr>
            <th>ID</th>
            <th>Category</th>
            <th>Scope</th>
            <th>CO2e</th>
            <th>Status</th>
            <th>Flagged</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {records.map((record) => (
            <tr key={record.id}>
              <td>{record.id}</td>
              <td>{record.category}</td>
              <td>{record.scope}</td>
              <td>{record.co2e_emission}</td>
              <td>{record.status}</td>
              <td>{record.is_flagged ? "Yes" : "No"}</td>

              <td>
                {record.status !== "APPROVED" && (
                  <button onClick={() => approveRecord(record.id)}>
                    Approve
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>

      </table>

    </div>
  );
}

export default App;