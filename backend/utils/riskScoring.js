const ActivityLog = require('../models/ActivityLog');
const Alert = require('../models/Alert');
const { checkKeyword } = require('./keywordRules');

// Risk scoring engine for activity monitoring
// Implements keyword-based, frequency-based, and time-window anomaly scoring

// Function to calculate risk score for an activity
const calculateRiskScore = async (activityData) => {
  let score = 0;

  // Keyword-based scoring
  if (activityData.eventType === 'KEYWORD') {
    const keywordResult = checkKeyword(activityData.appName); // Assuming appName contains keyword for simplicity
    score += keywordResult.score;
  }

  // Frequency-based scoring: Check recent activities for the user
  const recentActivities = await ActivityLog.find({
    userId: activityData.userId,
    timestamp: { $gte: new Date(Date.now() - 60 * 60 * 1000) }, // Last 1 hour
  });

  const frequencyScore = recentActivities.length > 10 ? 3 : 0; // Arbitrary threshold
  score += frequencyScore;

  // Time-window anomaly scoring: Check for unusual hours (e.g., late night)
  const currentHour = new Date().getHours();
  const anomalyScore = (currentHour < 6 || currentHour > 22) ? 2 : 0; // Outside 6 AM - 10 PM
  score += anomalyScore;

  return Math.min(score, 10); // Cap at 10
};

// Function to generate alert if risk score exceeds threshold
const generateAlertIfNeeded = async (activityData, riskScore) => {
  const threshold = parseInt(process.env.RISK_THRESHOLD) || 5;

  if (riskScore >= threshold) {
    const alert = new Alert({
      userId: activityData.userId,
      alertType: 'HIGH_RISK_ACTIVITY', // Can be customized based on scoring
      severity: riskScore >= 8 ? 'HIGH' : riskScore >= 6 ? 'MEDIUM' : 'LOW',
      description: `High-risk activity detected: ${activityData.eventType} in ${activityData.appName} with score ${riskScore}`,
    });

    await alert.save();
    console.log(`Alert generated for user ${activityData.userId}: ${alert.description}`);
  }
};

module.exports = {
  calculateRiskScore,
  generateAlertIfNeeded,
};
