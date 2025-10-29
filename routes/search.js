const express = require('express');
const path = require('path');
const router = express.Router();

// 1. REMOVED all 'mysql' require and connection setup.
// The connection is now passed in from server.js.

// 2. Wrap all routes in a function that accepts the 'client'
module.exports = (client) => {

  // GET route to serve the search form (no change needed here)
  router.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, '../public/search.html'));
  });
  
  // POST route to handle form submissions and perform searches
  router.post('/', (req, res) => {
      const { modelName, make, year, kms, mileage } = req.body;
  
      // 3. Rebuild the query for PostgreSQL
      // We must build the 'params' array and 'conditions' string together
      // to keep the $1, $2, $3... placeholders in order.
      let conditions = [];
      let params = [];
      let placeholderIndex = 1;
  
      let query = `SELECT * FROM car_specs WHERE 1=1`;
  
      // NOTE: I changed 'modelName' to 'model' to match your DB schema from the first prompt
      if (modelName) {
        conditions.push(`model LIKE $${placeholderIndex}`);
          params.push(`%${modelName}%`);
          placeholderIndex++;
      }
      if (make) {
        conditions.push(`make LIKE $${placeholderIndex}`);
        params.push(`%${make}%`);
          placeholderIndex++;
      }
      if (year) {
        conditions.push(`year >= $${placeholderIndex}`);
        params.push(year);
          placeholderIndex++;
      }
      if (kms) {
        conditions.push(`kms <= $${placeholderIndex}`);
        params.push(kms);
          placeholderIndex++;
      }
      if (mileage) {
        conditions.push(`mileage >= $${placeholderIndex}`);
        params.push(mileage);
          placeholderIndex++;
      }
  
      // Add all conditions to the query
      if (conditions.length > 0) {
        query += ` AND ${conditions.join(' AND ')}`;
      }
  
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
