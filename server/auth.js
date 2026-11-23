// server/auth.js

/**
 * Authentication Routes
 * ---------------------
 * POST /api/auth/register
 * POST /api/auth/login
 */

const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('./models/User');

const router = express.Router();

// Registration endpoint
router.post('/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    // Basic validation
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'All fields are required.' });
    }
    // Check if user exists
    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ error: 'Email already in use.' });
    }
    // Hash password
    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);
    // Create user
    const newUser = new User({ username, email, passwordHash });
    await newUser.save();
    res.status(201).json({ message: 'User registered successfully.' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error.' });
  }
});

// Login endpoint
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    // Basic validation
    if (!email || !password || typeof email !== 'string' || typeof password !== 'string') {
      return res.status(400).json({ error: 'All fields are required.' });
    }
    const user = await User.findOne({ email: { $eq: email } });
    if (!user) {
      return res.status(400).json({ error: 'Invalid credentials.' });
    }
    const isMatch = await bcrypt.compare(password, user.passwordHash);
    if (!isMatch) {
      return res.status(400).json({ error: 'Invalid credentials.' });
    }
    // Issue JWT
    const payload = { id: user._id, username: user.username };
    const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, username: user.username });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error.' });
  }
});

module.exports = router;
