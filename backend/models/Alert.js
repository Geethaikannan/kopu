const mongoose = require('mongoose');

// Alert Schema for managing alerts generated from high-risk activities
const alertSchema = new mongoose.Schema({
  userId: {
    type: String,
    required: [true, 'User ID is required'],
    trim: true,
  },
  alertType: {
    type: String,
    required: [true, 'Alert type is required'],
    enum: ['HIGH_RISK_ACTIVITY', 'FREQUENT_KEYWORD', 'TIME_ANOMALY'], // Possible alert types
  },
  severity: {
    type: String,
    required: [true, 'Severity is required'],
    enum: ['LOW', 'MEDIUM', 'HIGH'],
  },
  status: {
    type: String,
    required: [true, 'Status is required'],
    enum: ['OPEN', 'RESOLVED'],
    default: 'OPEN',
  },
  description: {
    type: String,
    trim: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  resolvedAt: {
    type: Date,
  },
});

// Index for efficient querying by userId and status
alertSchema.index({ userId: 1, status: 1 });

module.exports = mongoose.model('Alert', alertSchema);
