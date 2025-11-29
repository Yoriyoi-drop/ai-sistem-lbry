// 🌐 NEXAFORGE - NODE.JS API GATEWAY (L7 Component)

const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 8080;

// Security middleware
app.use(helmet());

// Parse JSON bodies
app.use(express.json());

// Enable CORS
app.use(cors());

// In-memory storage for demo purposes (use Redis/db in production)
let users = new Map();
let tokens = new Map();
let rateLimits = new Map();

// Mock User class
class User {
  constructor(id, username, email) {
    this.id = id;
    this.username = username;
    this.email = email;
    this.role = 'user';
    this.subscriptionTier = 'free';
    this.createdAt = new Date();
    this.isActive = true;
  }
}

// Mock Token class  
class Token {
  constructor(token, userId) {
    this.token = token;
    this.userId = userId;
    this.createdAt = new Date();
    this.expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
  }
}

// Generate API key
function generateApiKey() {
  return 'nexa_' + Math.random().toString(36).substr(2, 16) + Math.random().toString(36).substr(2, 16);
}

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  // In a real app, validate token against database
  const tokenData = tokens.get(token);
  if (!tokenData) {
    return res.status(403).json({ error: 'Invalid or expired token' });
  }

  // Check if token is expired
  if (new Date() > tokenData.expiresAt) {
    tokens.delete(token);
    return res.status(403).json({ error: 'Token expired' });
  }

  req.userId = tokenData.userId;
  next();
};

// Rate limiting middleware
const getRateLimit = (userId) => {
  // Default limits based on subscription tier (simplified)
  const user = users.get(userId);
  let maxRequests = 1000; // default for free tier
  
  if (user) {
    switch(user.subscriptionTier) {
      case 'standard': maxRequests = 5000; break;
      case 'professional': maxRequests = 20000; break;
      case 'enterprise': maxRequests = 100000; break;
    }
  }
  
  return rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: maxRequests,
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
  });
};

// Routes

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'NexaForge Node.js API Gateway'
  });
});

// Create user
app.post('/api/users', (req, res) => {
  const { username, email } = req.body;
  
  if (!username || !email) {
    return res.status(400).json({ error: 'Username and email are required' });
  }

  const userId = 'user_' + Math.random().toString(36).substr(2, 9);
  const user = new User(userId, username, email);
  
  users.set(userId, user);
  
  res.status(201).json({
    id: user.id,
    username: user.username,
    email: user.email,
    role: user.role,
    subscriptionTier: user.subscriptionTier,
    createdAt: user.createdAt
  });
});

// Get current user profile
app.get('/api/users/me', authenticateToken, (req, res) => {
  const user = users.get(req.userId);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json({
    id: user.id,
    username: user.username,
    email: user.email,
    role: user.role,
    subscriptionTier: user.subscriptionTier,
    createdAt: user.createdAt,
    isActive: user.isActive
  });
});

// Create API token
app.post('/api/tokens', authenticateToken, (req, res) => {
  const token = generateApiKey();
  const tokenData = new Token(token, req.userId);
  
  tokens.set(token, tokenData);
  
  res.status(201).json({
    token: token,
    message: 'Token created successfully',
    expiresAt: tokenData.expiresAt
  });
});

// Get subscription info
app.get('/api/subscription', authenticateToken, (req, res) => {
  const user = users.get(req.userId);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // Mock subscription features based on tier
  const features = {
    free: { maxAPICalls: 1000, storageGB: 1, support: 'community' },
    standard: { maxAPICalls: 10000, storageGB: 10, support: 'email' },
    professional: { maxAPICalls: 100000, storageGB: 100, support: 'priority_email' },
    enterprise: { maxAPICalls: 1000000, storageGB: 1000, support: '24_7_phone' }
  };
  
  res.json({
    subscription: {
      tier: user.subscriptionTier,
      cost: user.subscriptionTier === 'free' ? 0 : 
            user.subscriptionTier === 'standard' ? 9.99 :
            user.subscriptionTier === 'professional' ? 29.99 : 99.99,
      features: features[user.subscriptionTier]
    }
  });
});

// Update subscription tier
app.post('/api/subscription', authenticateToken, (req, res) => {
  const { tier } = req.body;
  const validTiers = ['free', 'standard', 'professional', 'enterprise'];
  
  if (!validTiers.includes(tier)) {
    return res.status(400).json({ error: 'Invalid subscription tier' });
  }
  
  const user = users.get(req.userId);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  user.subscriptionTier = tier;
  
  res.json({ message: `Subscription updated to ${tier}` });
});

// Get rate limit usage for user
app.get('/api/usage', authenticateToken, (req, res) => {
  // In a real system, this would query actual usage data
  // For demo, return mock data
  const mockData = {
    minuteUsage: Math.floor(Math.random() * 10),
    hourUsage: Math.floor(Math.random() * 100),
    dayUsage: Math.floor(Math.random() * 1000),
    minuteLimit: 100,
    hourLimit: 1000,
    dayLimit: 10000
  };
  
  res.json({ usage: mockData });
});

// Apply rate limiting to all requests (except health check)
app.use(/\/api\/.*/, (req, res, next) => {
  // Get user ID from token to apply personalized rate limits
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (token) {
    const tokenData = tokens.get(token);
    if (tokenData) {
      // Apply user-specific rate limiting
      return getRateLimit(tokenData.userId)(req, res, next);
    }
  }
  
  // Apply default rate limiting for requests without token
  return rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
  })(req, res, next);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`🌐 NexaForge Node.js API Gateway running on port ${PORT}`);
    console.log(`📖 OpenAPI docs would be available at /docs if implemented`);
    console.log(`🔧 Health check: GET /health`);
  });
}

module.exports = app;