const express = require("express");
const app = express();
const db = require("./db");

// VULNERABLE ENDPOINT
app.get("/user", (req, res) => {
  const id = req.query.id;

  // ❌ SQL Injection vulnerability
  const query = "SELECT * FROM users WHERE id = " + id;

  db.query(query, (err, result) => {
    if (err) throw err;
    res.json(result);
  });
});

app.listen(3000);
