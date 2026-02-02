const express = require('express');
const { logActivity, getRecentActivities, getActivityStats } = require('../controllers/activityController');
const { protect } = require('../middleware/authMiddleware');

const router = express.Router();

// All routes require authentication
router.use(protect);

// @route   POST /api/activity/log
router.post('/log', logActivity);

// @route   GET /api/activity/recent
router.get('/recent', getRecentActivities);

// @route   GET /api/activity/stats
router.get('/stats', getActivityStats);

module.exports = router;
