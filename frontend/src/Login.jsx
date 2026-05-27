import { useState } from "react";
import axios from "axios";

function Login({ setToken }) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await axios.post(
        "https://breathe-esg-production-d49f.up.railway.app/api/token/",
        { username, password }
      );

      const token = res.data.access;   // ✅ FIX HERE

      localStorage.setItem("token", token);
      setToken(token);

    } catch (err) {
      alert("Login failed");
      console.log(err.response?.data);
    }
  };

  return (
    <div style={{ padding: "50px" }}>
      <h2>Login</h2>

      <input
        placeholder="username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        placeholder="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>
    </div>
  );
}

export default Login;