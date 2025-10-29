const express = require('express');
const router = express.Router();

module.exports = (client) => {

  router.post('/', (req, res) => {
    const carId = req.body.car_id;
    const status = 'booked';

    if (!carId) {
      return res.status(400).json({ error: 'Car ID not provided' });
    }

    // SINGLE LINE QUERY to guarantee no whitespace errors
    const query = `UPDATE sales_info SET status = $1 WHERE car_id = $2 AND status NOT IN ('sold', 'booked')`;
    
    const params = [status, carId];

    client.query(query, params, (error, result) => {
      if (error) {
        console.error('Database error:', error);
        return res.status(500).json({ error: 'Database error' });
      }

      if (result.rowCount === 0) {
        return res.status(400).json({ error: 'Car is already booked or sold' });
      }

      res.json({ message: 'Test drive booked successfully!' });
    });
  });

  return router;
};

