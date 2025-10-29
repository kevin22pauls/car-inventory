const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
// 1. Replaced 'mysql2' with 'pg' (Node-Postgres)
const { Client } = require('pg');

const app = express();
// 2. Use 'process.env.PORT' for Render, with 3000 as a local fallback
const PORT = process.env.PORT || 3000;

// Middleware setup
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// 3. New PostgreSQL connection logic
// Uses Render's DATABASE_URL when deployed, or a local URL for testing
const connectionString = process.env.DATABASE_URL || 'postgresql://root:kevinsql123@localhost:5432/cars_used_inventory';

const client = new Client({
  connectionString: connectionString,
  // 4. Added SSL requirement for Render's free PostgreSQL tier
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Check connection
client.connect((err) => {
  if (err) {
    console.error('❌ PostgreSQL connection failed:', err);
  } else {
    console.log('✅ Connected to PostgreSQL database.');
  }
});

// 5. IMPORTANT: Modified routes to pass the 'client' object
// Your route files must be updated to accept this 'client'
const searchRoute = require('./routes/search')(client);
const emiDetailsRoute = require('./routes/emiDetails')(client);
const carDetailsRoute = require('./routes/carDetails')(client);
const bookTestDriveRoute = require('./routes/bookTestDrive')(client);

// Use routes
app.use('/search', searchRoute);
app.use('/emi-details', emiDetailsRoute);
app.use('/car-details', carDetailsRoute);
app.use('/book-testdrive', bookTestDriveRoute);

// ✅ redirect root URL to search page (this is still correct)
app.get('/', (req, res) => {
  res.redirect('/search');
});

// Start server
app.listen(PORT, () => {
  // Updated log message to show the correct port
  console.log(`🚀 Server running on port ${PORT}`);
});