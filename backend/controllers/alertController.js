const Alert = require('../models/Alert');

// @desc    Get all alerts for the user
// @route   GET /api/alerts
// @access  Private
const getAlerts = async (req, res, next) => {
  try {
    // Assuming userId is passed in query or from middleware
    const { userId } = req.query;

    const alerts = await Alert.find({ userId }).sort({ createdAt: -1 });

    res.json(alerts);
  } catch (error) {
    next(error);
  }
};

// @desc    Resolve an alert
// @route   POST /api/alerts/resolve
// @access  Private
const resolveAlert = async (req, res, next) => {
  try {
    const { alertId } = req.body;

    if (!alertId) {
      return res.status(400).json({ message: 'Alert ID is required' });
    }

    const alert = await Alert.findById(alertId);

    if (!alert) {
      return res.status(404).json({ message: 'Alert not found' });
    }

    // Update alert status to resolved
    alert.status = 'RESOLVED';
    alert.resolvedAt = new Date();
    await alert.save();

    res.json({ message: 'Alert resolved successfully', alert });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getAlerts,
  resolveAlert,
};
