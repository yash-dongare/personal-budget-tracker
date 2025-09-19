# Personal Budget Tracker - Implementation Guide

## Week 1: Planning & Design (CURRENT)

### Completed ✅
- [x] Project structure design
- [x] Technology stack selection (MERN)
- [x] Database schema design
- [x] UI wireframe concepts
- [x] Package.json configurations
- [x] Core file structure setup
- [x] Authentication system architecture
- [x] API endpoint planning

### Tasks Remaining for Week 1

#### 1. Environment Setup (Day 1-2)
```bash
# Initialize project
mkdir personal-budget-tracker
cd personal-budget-tracker

# Backend setup
mkdir backend && cd backend
npm init -y
npm install express mongoose bcryptjs jsonwebtoken cors dotenv express-validator helmet morgan express-rate-limit moment

# Frontend setup
cd ../
npx create-react-app frontend
cd frontend
npm install react-router-dom axios chart.js react-chartjs-2 date-fns react-datepicker react-hot-toast react-icons framer-motion formik yup react-select react-modal
```

#### 2. Database Setup (Day 2)
```bash
# Install MongoDB locally or use MongoDB Atlas
# Create .env file in backend:
PORT=5000
MONGODB_URI=mongodb://localhost:27017/budget-tracker
JWT_SECRET=your-super-secret-jwt-key
NODE_ENV=development
```

#### 3. Complete File Creation (Day 2-3)
- Copy all provided code files to appropriate directories
- Set up the complete backend server with all models
- Set up frontend with routing and context providers

#### 4. Initial Testing (Day 3)
```bash
# Start backend
cd backend
npm run dev

# Start frontend (new terminal)
cd frontend
npm start
```

## Week 2: Core Development

### Backend Development Tasks (Day 4-7)

#### Authentication Controllers
```javascript
// backend/controllers/authController.js
const User = require('../models/User');
const jwt = require('jsonwebtoken');

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, { expiresIn: '30d' });
};

const register = async (req, res) => {
  try {
    const { name, email, password } = req.body;
    
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({
        success: false,
        message: 'User already exists'
      });
    }

    const user = await User.create({ name, email, password });
    const token = generateToken(user._id);

    res.status(201).json({
      success: true,
      token,
      user: user.toPublicJSON()
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: error.message
    });
  }
};

module.exports = { register, login, getProfile };
```

#### Transaction Controllers
```javascript
// backend/controllers/transactionController.js
const Transaction = require('../models/Transaction');

const getTransactions = async (req, res) => {
  try {
    const { page = 1, limit = 10, category, type, startDate, endDate } = req.query;
    
    const query = { user: req.user.id };
    
    if (category) query.category = category;
    if (type) query.type = type;
    if (startDate && endDate) {
      query.date = {
        $gte: new Date(startDate),
        $lte: new Date(endDate)
      };
    }

    const transactions = await Transaction.find(query)
      .sort({ date: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit);

    const total = await Transaction.countDocuments(query);

    res.json({
      success: true,
      data: {
        transactions,
        totalPages: Math.ceil(total / limit),
        currentPage: page,
        total
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: error.message
    });
  }
};

module.exports = { getTransactions, createTransaction, updateTransaction, deleteTransaction };
```

### Frontend Development Tasks (Day 4-7)

#### API Utility Setup
```javascript
// frontend/src/utils/api.js
import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-url.com/api' 
  : 'http://localhost:5000/api';

const createAPI = (baseURL) => {
  const api = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json'
    }
  });

  // Request interceptor
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('budgetToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('budgetToken');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return api;
};

export const authAPI = createAPI(`${API_BASE_URL}/auth`);
export const transactionAPI = createAPI(`${API_BASE_URL}/transactions`);
export const budgetAPI = createAPI(`${API_BASE_URL}/budgets`);
export const groupAPI = createAPI(`${API_BASE_URL}/groups`);
```

## Week 3: Data Visualization & Features

### Chart.js Integration Tasks (Day 8-10)

#### Expense Chart Component
```javascript
// frontend/src/components/Charts/ExpenseChart.js
import React from 'react';
import { Bar } from 'react-chartjs-2';

const ExpenseChart = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.category),
    datasets: [{
      label: 'Expenses',
      data: data.map(item => item.amount),
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 205, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 205, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1
    }]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Expenses by Category'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return <Bar data={chartData} options={options} />;
};

export default ExpenseChart;
```

### Group Expense Splitting (Day 11-12)

#### Group Expense Algorithm
```javascript
// frontend/src/utils/expenseSplitter.js
export const calculateSplit = (amount, splitType, members, splitData) => {
  const result = [];

  switch (splitType) {
    case 'equal':
      const equalAmount = amount / members.length;
      members.forEach(member => {
        result.push({
          memberId: member._id,
          memberName: member.name,
          amount: equalAmount
        });
      });
      break;

    case 'percentage':
      splitData.forEach(split => {
        result.push({
          memberId: split.memberId,
          memberName: split.memberName,
          amount: (amount * split.percentage) / 100
        });
      });
      break;

    case 'amount':
      splitData.forEach(split => {
        result.push({
          memberId: split.memberId,
          memberName: split.memberName,
          amount: split.amount
        });
      });
      break;

    case 'shares':
      const totalShares = splitData.reduce((sum, split) => sum + split.shares, 0);
      splitData.forEach(split => {
        result.push({
          memberId: split.memberId,
          memberName: split.memberName,
          amount: (amount * split.shares) / totalShares
        });
      });
      break;

    default:
      break;
  }

  return result;
};

export const settleBalances = (groupExpenses) => {
  const balances = {};
  
  // Calculate net balances for each member
  groupExpenses.forEach(expense => {
    const paidBy = expense.paidBy;
    const splits = expense.splitDetails;
    
    if (!balances[paidBy]) balances[paidBy] = 0;
    balances[paidBy] += expense.amount;
    
    splits.forEach(split => {
      if (!balances[split.memberId]) balances[split.memberId] = 0;
      balances[split.memberId] -= split.amount;
    });
  });

  // Generate settlement transactions
  const settlements = [];
  const debtors = [];
  const creditors = [];
  
  Object.entries(balances).forEach(([memberId, balance]) => {
    if (balance > 0) {
      creditors.push({ memberId, amount: balance });
    } else if (balance < 0) {
      debtors.push({ memberId, amount: Math.abs(balance) });
    }
  });

  // Minimize transactions
  debtors.forEach(debtor => {
    let remainingDebt = debtor.amount;
    
    for (let i = 0; i < creditors.length && remainingDebt > 0; i++) {
      const creditor = creditors[i];
      const settleAmount = Math.min(remainingDebt, creditor.amount);
      
      if (settleAmount > 0) {
        settlements.push({
          from: debtor.memberId,
          to: creditor.memberId,
          amount: settleAmount
        });
        
        remainingDebt -= settleAmount;
        creditor.amount -= settleAmount;
      }
    }
  });

  return settlements;
};
```

## Week 4: Testing, Deployment & Documentation

### Testing Setup (Day 13-14)
```bash
# Backend testing
cd backend
npm install --save-dev jest supertest
npm test

# Frontend testing
cd frontend
npm test
```

### Deployment Options (Day 15-16)

#### Option 1: Vercel + MongoDB Atlas
```bash
# Frontend deployment
npm run build
# Deploy to Vercel

# Backend deployment
# Deploy to Vercel serverless functions or Railway/Render
```

#### Option 2: Docker Deployment
```dockerfile
# Dockerfile for backend
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

### Environment Variables for Production
```env
# Backend .env
PORT=5000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/budget-tracker
JWT_SECRET=super-secure-production-secret
NODE_ENV=production
CLIENT_URL=https://your-frontend-url.com

# Frontend .env
REACT_APP_API_URL=https://your-backend-url.com/api
REACT_APP_ENV=production
```

## Development Commands Reference

### Daily Development Workflow
```bash
# Start development servers
npm run dev:backend    # Terminal 1
npm run dev:frontend   # Terminal 2

# Run tests
npm run test:backend
npm run test:frontend

# Check code quality
npm run lint
npm run format

# Build for production
npm run build
```

### Database Operations
```bash
# Backup database
mongodump --db budget-tracker

# Restore database
mongorestore --db budget-tracker

# Seed sample data
npm run seed
```

## Key Implementation Notes

1. **Security**: All API endpoints require authentication except login/register
2. **Validation**: Use Yup for frontend validation, express-validator for backend
3. **Error Handling**: Implement global error handlers and user-friendly messages
4. **Performance**: Implement lazy loading for components and pagination for lists
5. **Responsive Design**: Mobile-first approach with breakpoints at 768px, 1024px
6. **Accessibility**: Include ARIA labels, keyboard navigation, and screen reader support

## Troubleshooting Common Issues

1. **CORS Issues**: Configure CORS properly in backend server.js
2. **MongoDB Connection**: Ensure MongoDB is running and connection string is correct
3. **JWT Token Issues**: Check token expiration and storage
4. **Chart.js Issues**: Register required Chart.js components
5. **Build Errors**: Check for missing dependencies and proper imports

This implementation guide provides a complete roadmap for building the Personal Budget Tracker from scratch following the 4-week timeline.