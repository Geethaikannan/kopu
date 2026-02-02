const mongoose = require('mongoose');

// ActivityLog Schema for logging filtered PC activities
const activityLogSchema = new mongoose.Schema({
  userId: {
    type: String,
    required: [true, 'User ID is required'],
    trim: true,
  },
  appName: {
    type: String,
    required: [true, 'App name is required'],
    trim: true,
  },
  eventType: {
    type: String,
    required: [true, 'Event type is required'],
    enum: ['KEYWORD', 'APP_USAGE'], // Only allowed event types
  },
  riskScore: {
    type: Number,
    required: [true, 'Risk score is required'],
    min: [0, 'Risk score must be at least 0'],
    max: [10, 'Risk score must be at most 10'],
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

// Index for efficient querying by userId and timestamp
activityLogSchema.index({ userId: 1, timestamp: -1 });

module.exports = mongoose.model('ActivityLog', activityLogSchema);
