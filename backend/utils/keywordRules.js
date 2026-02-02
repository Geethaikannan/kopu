// Keyword-based rules for risk scoring
// This module defines keywords and their associated risk scores

const keywordRules = {
  // High-risk keywords (score 5-10)
  highRisk: {
    keywords: ['password', 'credit card', 'bank', 'login', 'hack', 'exploit'],
    score: 8,
  },
  // Medium-risk keywords (score 3-5)
  mediumRisk: {
    keywords: ['email', 'social media', 'chat', 'download'],
    score: 4,
  },
  // Low-risk keywords (score 1-3)
  lowRisk: {
    keywords: ['news', 'weather', 'sports', 'music'],
    score: 2,
  },
};

// Function to check if a keyword matches and return score
const checkKeyword = (text) => {
  const lowerText = text.toLowerCase();

  // Check high-risk keywords
  for (const keyword of keywordRules.highRisk.keywords) {
    if (lowerText.includes(keyword)) {
      return { match: true, score: keywordRules.highRisk.score };
    }
  }

  // Check medium-risk keywords
  for (const keyword of keywordRules.mediumRisk.keywords) {
    if (lowerText.includes(keyword)) {
      return { match: true, score: keywordRules.mediumRisk.score };
    }
  }

  // Check low-risk keywords
  for (const keyword of keywordRules.lowRisk.keywords) {
    if (lowerText.includes(keyword)) {
      return { match: true, score: keywordRules.lowRisk.score };
    }
  }

  // No match
  return { match: false, score: 0 };
};

module.exports = {
  checkKeyword,
};
