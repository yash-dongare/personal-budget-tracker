const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection URI - replace with your real URI
const mongoURI = 'mongodb+srv://yash_db_user:UzpCok8BDsG39hMI@budgettrackercluster.cvnlfwp.mongodb.net/?retryWrites=true&w=majority&appName=BudgetTrackerCluster';

// Connect to MongoDB
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('MongoDB connected'))
.catch((err) => console.error('MongoDB connection error:', err));

// Import routes
const transactionRoutes = require('./routes/transactions');
const budgetRoutes = require('./routes/budgets');

// Use routes
app.use('/api/transactions', transactionRoutes);
app.use('/api/budgets', budgetRoutes);

// Basic test route
app.get('/', (req, res) => {
  res.send('Backend server is running');
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
