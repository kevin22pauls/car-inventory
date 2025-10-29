const express = require('express');
const router = express.Router();

module.exports = (client) => {

  router.post('/', (req, res) => {
    const carIds = req.body.car_ids || [];
  
    console.log("Received car IDs from frontend:", carIds);
  
    if (carIds.length === 0) {
      console.error("No cars selected");
      return res.status(400).json({ error: 'No cars selected' });
    }
  
    // CORRECTION: Changed 's.model' back to 's.modelName'
    const query = `
      SELECT s.car_id, s.modelName, s.make, s.year, si.emi_av, 
            e.interest, e.monthly, e.duration, si.price, si.status, si.delivery_date, si.advance_amt
  _   FROM car_specs s
      JOIN sales_info si ON s.car_id = si.car_id
      LEFT JOIN emi_details e ON s.car_id = e.car_id
      WHERE s.car_id = ANY($1::int[])
    `;
  
    const params = [carIds];

    console.log("Executing SQL query:", query);
  
    client.query(query, params, (error, results) => {
      if (error) {
        console.error("Database error:", error);
        return res.status(500).json({ error: 'Database error' });
      }
  
      console.log("Query results:", results.rows);
  
      if (results.rows.length > 0) {
        res.json(results.rows);
      } else {
        console.warn("No EMI details found for the selected cars.");
        res.status(404).json({ error: 'No EMI details found for the selected cars' });
      }
    });
  });
  
  return router;
};

