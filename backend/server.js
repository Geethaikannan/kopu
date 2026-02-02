const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const connectDB = require('./config/db');
const errorHandler = require('./middleware/errorHandler');

// Load environment variables
dotenv.config();

// Connect to database
connectDB();

// Initialize Express app
const app = express();

// Middleware
app.use(cors()); // Enable CORS
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: false })); // Parse URL-encoded bodies

// Routes
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/activity', require('./routes/activityRoutes'));
app.use('/api/alerts', require('./routes/alertRoutes'));

// Health check route
app.get('/api/health', (req, res) => {
  res.json({ message: 'PC Activity Monitoring Backend is running' });
});

// Error handling middleware (must be last)
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
