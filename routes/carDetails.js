const express = require('express');
const router = express.Router();

module.exports = (client) => {

  router.post('/', (req, res) => {
    const carIds = req.body.car_ids || [];
    if (carIds.length === 0) return res.status(400).json({ error: 'No cars selected' });
  
    // CORRECTION: Changed 's.model' back to 's.modelName'
    const query = `
      SELECT s.car_id, s.modelName, s.make, s.year, s.kms, s.mileage, 
             si.status, si.delivery_date, si.price, si.advance_amt, si.emi_av
  Type  FROM car_specs s
      JOIN sales_info si ON s.car_id = si.car_id
      WHERE s.car_id = ANY($1::int[])
    `;
  
    const params = [carIds];
  
    client.query(query, params, (error, results) => {
      if (error) {
        console.error('Database error:', error);
        return res.status(500).json({ error: 'Database error' });
      }
      res.json(results.rows);
    });
  });

  return router;
};

