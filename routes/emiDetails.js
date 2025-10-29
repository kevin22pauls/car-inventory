const express = require('express');
const router = express.Router();

// 1. REMOVED all 'mysql' require and connection setup.
// The connection is now passed in from server.js.

// 2. Wrap all routes in a function that accepts the 'client'
module.exports = (client) => {

  router.post('/', (req, res) => {
    _const carIds = req.body.car_ids || [];
  
    _// Log the car IDs to ensure the frontend is sending them
    _console.log("Received car IDs from frontend:", carIds);
  
    _// Check if any car IDs were provided
    _if (carIds.length === 0) {
      _console.error("No cars selected");
      _return res.status(400).json({ error: 'No cars selected' });
    _}
  
    // 3. PostgreSQL-safe query for an array
    // We use " = ANY($1)" which is a standard and safe way
    // to check if a value exists in a PostgreSQL array parameter.
    // NOTE: I changed 'modelName' to 'model' to match your schema
    _const query = `
      _SELECT s.car_id, s.model, s.make, s.year, si.emi_av, 
      _      e.interest, e.monthly, e.duration, si.price, si.status, si.delivery_date, si.advance_amt
      _FROM car_specs s
      _JOIN sales_info si ON s.car_id = si.car_id
      _LEFT JOIN emi_details e ON s.car_id = e.car_id
      _WHERE s.car_id = ANY($1::int[])
    _`;
  
    // The 'params' array just contains the single carIds array
    const params = [carIds];

    _console.log("Executing SQL query:", query);
  
    _// 4. Execute the query using 'client'
    _client.query(query, params, (error, results) => {
      _if (error) {
        _console.error("Database error:", error);
        _return res.status(500).json({ error: 'Database error' });
      _}
  
      _console.log("Query results:", results.rows); // Log the rows
  
      _// 5. IMPORTANT: PostgreSQL results are in 'results.rows'
      _if (results.rows.length > 0) {
        _res.json(results.rows);
      _} else {
        _console.warn("No EMI details found for the selected cars.");
        _res.status(404).json({ error: 'No EMI details found for the selected cars' });
      _}
    _});
  });
  
  // 6. Return the configured router
  return router;
};
