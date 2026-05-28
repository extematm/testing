const express = require('express');
const app = express();

app.get('/', (req, res) => {
  const userInput = req.query.q;
  res.send('<h1>' + userInput + '</h1>');
});

app.listen(3000);