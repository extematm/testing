app.get("/user", async (req, res) => {
  const id = req.query.id;

  const result = await db.query(`SELECT * FROM users WHERE id = ${id}`);

  res.json(result.rows);
});
