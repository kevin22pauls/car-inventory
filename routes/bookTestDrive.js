const express = require('express');
const router = express.Router();

// 1. REMOVED all 'mysql' require and connection setup.
// The connection is now passed in from server.js.

// 2. Wrap all routes in a function that accepts the 'client'
module.exports = (client) => {

  // POST route to book a test drive
  router.post('/', (req, res) => {
    const carId = req.body.car_id;
    const status = 'booked';
  
    // Ensure car ID is provided
    if (!carId) {
      return res.status(400).json({ error: 'Car ID not provided' });
    }
  
    // 3. Converted query to PostgreSQL placeholders ($1, $2)
    const query = `
      UPDATE sales_info
      SET status = $1
      WHERE car_id = $2 AND status NOT IN ('sold', 'booked')
    `;
  
    const params = [status, carId];

    // 4. Execute the query using 'client'
    client.query(query, params, (error, result) => {
      if (error) {
        console.error('Database error:', error);
        return res.status(500).json({ error: 'Database error' });
      }
  
      // 5. IMPORTANT: PostgreSQL uses 'rowCount' for affected rows
      if (result.rowCount === 0) {
    g     return res.status(400).json({ error: 'Car is already booked or sold' });
      }
  
      res.json({ message: 'Test drive booked successfully!' });
    });
  });

  // 6. Return the configured router
  return router;
};
