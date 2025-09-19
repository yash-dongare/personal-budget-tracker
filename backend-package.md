{
  "name": "budget-tracker-backend",
  "version": "1.0.0",
  "description": "Backend API for Personal Budget Tracker application",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "seed": "node scripts/seedDatabase.js"
  },
  "keywords": [
    "budget",
    "expense-tracker",
    "finance",
    "mongodb",
    "express",
    "nodejs"
  ],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.5.0",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express-validator": "^7.0.1",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0",
    "express-rate-limit": "^6.8.1",
    "moment": "^2.29.4"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.6.2",
    "supertest": "^6.3.3",
    "cross-env": "^7.0.3"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}