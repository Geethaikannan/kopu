const ActivityLog = require('../models/ActivityLog');
const { calculateRiskScore, generateAlertIfNeeded } = require('../utils/riskScoring');

// @desc    Log activity from PC agent
// @route   POST /api/activity/log
// @access  Private (requires JWT)
const logActivity = async (req, res, next) => {
  try {
    const { userId, appName, eventType, riskScore } = req.body;

    // Validate required fields
    if (!userId || !appName || !eventType) {
      return res.status(400).json({ message: 'Missing required fields' });
    }

    // Calculate risk score if not provided (for additional processing)
    const calculatedScore = riskScore || (await calculateRiskScore(req.body));

    // Create activity log
    const activity = await ActivityLog.create({
      userId,
      appName,
      eventType,
      riskScore: calculatedScore,
    });

    // Generate alert if risk score is high
    await generateAlertIfNeeded(req.body, calculatedScore);

    res.status(201).json({
      message: 'Activity logged successfully',
      activity,
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get recent activities for dashboard
// @route   GET /api/activity/recent
// @access  Private
const getRecentActivities = async (req, res, next) => {
  try {
    const { userId } = req.query; // Assuming userId from query or middleware
    const limit = parseInt(req.query.limit) || 50;

    const activities = await ActivityLog.find({ userId })
      .sort({ timestamp: -1 })
      .limit(limit);

    res.json(activities);
  } catch (error) {
    next(error);
  }
};

// @desc    Get activity statistics for dashboard
// @route   GET /api/activity/stats
// @access  Private
const getActivityStats = async (req, res, next) => {
  try {
    const { userId } = req.query;

    // Aggregate stats: total activities, average risk score, etc.
    const stats = await ActivityLog.aggregate([
      { $match: { userId } },
      {
        $group: {
          _id: null,
          totalActivities: { $sum: 1 },
          averageRiskScore: { $avg: '$riskScore' },
          highRiskCount: {
            $sum: { $cond: [{ $gte: ['$riskScore', 7] }, 1, 0] },
          },
        },
      },
    ]);

    res.json(stats[0] || { totalActivities: 0, averageRiskScore: 0, highRiskCount: 0 });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  logActivity,
  getRecentActivities,
  getActivityStats,
};
