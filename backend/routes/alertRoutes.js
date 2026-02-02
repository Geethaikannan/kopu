const express = require('express');
const { getAlerts, resolveAlert } = require('../controllers/alertController');
const { protect } = require('../middleware/authMiddleware');

const router = express.Router();

// All routes require authentication
router.use(protect);

// @route   GET /api/alerts
router.get('/', getAlerts);

// @route   POST /api/alerts/resolve
router.post('/resolve', resolveAlert);

module.exports = router;
