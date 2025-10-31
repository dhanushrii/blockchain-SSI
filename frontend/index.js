<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Degree Verification (Demo)</title>
  <style>
    body {
      font-family: "Poppins", sans-serif;
      background: #f4f7fb;
      color: #333;
      margin: 0;
      padding: 30px;
    }

    h1 {
      text-align: center;
      color: #1a1a1a;
      margin-bottom: 20px;
    }

    .container {
      max-width: 600px;
      margin: 0 auto;
      background: #fff;
      padding: 30px;
      border-radius: 15px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }

    h3 {
      color: #0078d7;
      border-left: 4px solid #0078d7;
      padding-left: 10px;
      margin-top: 25px;
    }

    input {
      width: 100%;
      padding: 10px;
      margin: 8px 0;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 15px;
      transition: border 0.2s;
    }

    input:focus {
      border-color: #0078d7;
      outline: none;
      box-shadow: 0 0 4px rgba(0, 120, 215, 0.2);
    }

    button {
      padding: 10px 18px;
      background: #0078d7;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 15px;
      transition: background 0.3s;
    }

    button:hover {
      background: #005fa3;
    }

    .message {
      margin-top: 15px;
      padding: 12px;
      border-radius: 6px;
      display: none;
      animation: fadeIn 0.4s ease-in-out;
    }

    .success {
      background: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }

    .warning {
      background: #fff3cd;
      color: #856404;
      border: 1px solid #ffeeba;
    }

    pre {
      background: #f1f3f5;
      padding: 10px;
      border-radius: 6px;
      max-height: 200px;
      overflow-y: auto;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-5px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .footer {
      text-align: center;
      margin-top: 20px;
      color: #888;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <h1>Degree Verification</h1>

  <div class="container">
    <h3>Issue Degree</h3>
    <input id="studentName" placeholder="Student Name">
    <input id="studentId" placeholder="Student ID">
    <input id="degreeName" placeholder="Degree Name">
    <input id="yearOfPassing" placeholder="Year of Passing">
    <button onclick="issueDegree()">Issue</button>

    <h3>Verify Degree</h3>
    <input id="verifyHash" placeholder="Enter Degree Hash">
    <button onclick="verifyDegree()">Verify</button>

    <h3>All Degrees</h3>
    <button onclick="fetchDegrees()">Refresh List</button>
    <pre id="list"></pre>

    <div id="messageBox" class="message"></div>
  </div>

  <div class="footer">
    © 2025 Degree Verification Demo | Blockchain-Powered System
  </div>

  <script>
    const BASE = "http://127.0.0.1:5000";

    function showMessage(text, type = "success") {
      const box = document.getElementById("messageBox");
      box.textContent = text;
      box.className = `message ${type}`;
      box.style.display = "block";
      setTimeout(() => (box.style.display = "none"), 4000);
    }

    async function generateHash(text) {
      const msgBuffer = new TextEncoder().encode(text);
      const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
      return "0x" + hashHex;
    }

    async function issueDegree() {
      const nameVal = document.getElementById("studentName").value.trim();
      const idVal = document.getElementById("studentId").value.trim();
      const degreeVal = document.getElementById("degreeName").value.trim();
      const yearVal = document.getElementById("yearOfPassing").value.trim();

      if (!nameVal || !idVal || !degreeVal || !yearVal) {
        showMessage("⚠️ Please fill all fields!", "warning");
        return;
      }

      const inputData = `${nameVal}-${idVal}-${degreeVal}-${yearVal}`;
      const degree_hash = await generateHash(inputData);

      try {
        const res = await fetch(`${BASE}/issue-degree`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            student_name: nameVal,
            student_id: idVal,
            degree_name: degreeVal,
            year_of_passing: yearVal,
            degree_hash,
          }),
        });

        const data = await res.json();
        showMessage(data.message || "✅ Degree issued successfully!");
      } catch (err) {
        showMessage("❌ Failed to connect to backend.", "warning");
      }
    }

    async function verifyDegree() {
      const hashVal = document.getElementById("verifyHash").value.trim();
      if (!hashVal) {
        showMessage("⚠️ Enter a hash to verify!", "warning");
        return;
      }

      try {
        const res = await fetch(`${BASE}/verify-degree`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ degree_hash: hashVal }),
        });

        const data = await res.json();
        if (data.message && data.message.toLowerCase().includes("not found")) {
          showMessage("⚠️ Degree not found!", "warning");
        } else {
          showMessage("✅ Degree verified successfully!", "success");
        }
      } catch (err) {
        showMessage("❌ Failed to connect to backend.", "warning");
      }
    }

    async function fetchDegrees() {
      try {
        const res = await fetch(`${BASE}/degrees`);
        const data = await res.json();
        document.getElementById("list").textContent = JSON.stringify(data, null, 2);
      } catch (err) {
        showMessage("❌ Failed to load degrees.", "warning");
      }
    }
  </script>
</body>
</html>
