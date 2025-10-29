const express = require('express');
const router = express.Router();

// 1. REMOVED all 'mysql' require and connection setup.
// The connection is now passed in from server.js.

// 2. Wrap all routes in a function that accepts the 'client'
module.exports = (client) => {

  // Route to fetch car details for selected cars
  router.post('/', (req, res) => {
    const carIds = req.body.car_ids || [];
    if (carIds.length === 0) return res.status(400).json({ error: 'No cars selected' });
  
    // 3. PostgreSQL-safe query for an array
    // We use " = ANY($1)" which is a standard and safe way
    // to check if a value exists in a PostgreSQL array parameter.
    // NOTE: I changed 'modelName' to 'model' to match your schema
    const query = `
      SELECT s.car_id, s.model, s.make, s.year, s.kms, s.mileage, 
             si.status, si.delivery_date, si.price, si.advance_amt, si.emi_av
      FROM car_specs s
      JOIN sales_info si ON s.car_id = si.car_id
      WHERE s.car_id = ANY($1::int[])
    `;
  
    // The 'params' array just contains the single carIds array
    const params = [carIds];
  
    // 4. Execute the query using 'client'
    client.query(query, params, (error, results) => {
      if (error) {
        console.error('Database error:', error);
        return res.status(500).json({ error: 'Database error' });
      }
      // 5. IMPORTANT: PostgreSQL results are in 'results.rows'
      res.json(results.rows);
    });
  });

  // 6. Return the configured router
  return router;
};
