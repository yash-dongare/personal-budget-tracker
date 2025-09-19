import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { 
  FaDollarSign, 
  FaArrowUp, 
  FaArrowDown, 
  FaWallet, 
  FaCreditCard,
  FaUsers,
  FaPlus,
  FaEye,
  FaEyeSlash
} from 'react-icons/fa';

import { useAuth } from '../../context/AuthContext';
import { transactionAPI, budgetAPI, groupAPI } from '../../utils/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import TransactionForm from '../Transactions/TransactionForm';
import BudgetProgress from '../Budgets/BudgetProgress';

import './Dashboard.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [showBalances, setShowBalances] = useState(true);
  const [showTransactionForm, setShowTransactionForm] = useState(false);
  
  // Dashboard Data State
  const [dashboardData, setDashboardData] = useState({
    summary: {
      totalIncome: 0,
      totalExpenses: 0,
      balance: 0,
      transactionCount: 0
    },
    recentTransactions: [],
    monthlyData: [],
    categoryData: [],
    budgets: [],
    groups: []
  });

  // Fetch Dashboard Data
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      const [summaryRes, transactionsRes, budgetsRes, groupsRes] = await Promise.allSettled([
        transactionAPI.get('/summary'),
        transactionAPI.get('/?limit=5&sort=-date'),
        budgetAPI.get('/'),
        groupAPI.get('/')
      ]);

      const summary = summaryRes.status === 'fulfilled' ? summaryRes.value.data.data : {};
      const transactions = transactionsRes.status === 'fulfilled' ? transactionsRes.value.data.data : [];
      const budgets = budgetsRes.status === 'fulfilled' ? budgetsRes.value.data.data : [];
      const groups = groupsRes.status === 'fulfilled' ? groupsRes.value.data.data : [];

      setDashboardData({
        summary: summary.summary || {
          totalIncome: 0,
          totalExpenses: 0,
          balance: 0,
          transactionCount: 0
        },
        recentTransactions: transactions.transactions || [],
        monthlyData: summary.monthlyData || [],
        categoryData: summary.categoryData || [],
        budgets: budgets.budgets || [],
        groups: groups.groups || []
      });
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Chart Data Preparation
  const monthlyChartData = {
    labels: dashboardData.monthlyData.map(item => item.month),
    datasets: [
      {
        label: 'Income',
        data: dashboardData.monthlyData.map(item => item.income),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 2
      },
      {
        label: 'Expenses',
        data: dashboardData.monthlyData.map(item => item.expenses),
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2
      }
    ]
  };

  const categoryChartData = {
    labels: dashboardData.categoryData.map(item => item.category),
    datasets: [
      {
        data: dashboardData.categoryData.map(item => item.amount),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#FF9F40',
          '#FF6384', '#C9CBCF', '#4BC0C0', '#9966FF'
        ],
        borderWidth: 2,
        borderColor: '#ffffff'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  // Format Currency
  const formatCurrency = (amount) => {
    if (!showBalances) return '****';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: user?.currency || 'USD'
    }).format(amount);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <motion.div 
      className="dashboard"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Welcome back, {user?.name}!</h1>
          <p>Here's your financial overview</p>
        </div>
        <div className="header-actions">
          <button
            className="toggle-visibility-btn"
            onClick={() => setShowBalances(!showBalances)}
            title={showBalances ? 'Hide balances' : 'Show balances'}
          >
            {showBalances ? <FaEyeSlash /> : <FaEye />}
          </button>
          <button
            className="add-transaction-btn"
            onClick={() => setShowTransactionForm(true)}
          >
            <FaPlus />
            Add Transaction
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <motion.div 
          className="summary-card income"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="card-icon">
            <FaArrowUp />
          </div>
          <div className="card-content">
            <h3>Total Income</h3>
            <p className="amount">{formatCurrency(dashboardData.summary.totalIncome)}</p>
          </div>
        </motion.div>

        <motion.div 
          className="summary-card expense"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="card-icon">
            <FaArrowDown />
          </div>
          <div className="card-content">
            <h3>Total Expenses</h3>
            <p className="amount">{formatCurrency(dashboardData.summary.totalExpenses)}</p>
          </div>
        </motion.div>

        <motion.div 
          className="summary-card balance"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="card-icon">
            <FaWallet />
          </div>
          <div className="card-content">
            <h3>Net Balance</h3>
            <p className={`amount ${dashboardData.summary.balance >= 0 ? 'positive' : 'negative'}`}>
              {formatCurrency(dashboardData.summary.balance)}
            </p>
          </div>
        </motion.div>

        <motion.div 
          className="summary-card transactions"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="card-icon">
            <FaCreditCard />
          </div>
          <div className="card-content">
            <h3>Transactions</h3>
            <p className="amount">{dashboardData.summary.transactionCount}</p>
          </div>
        </motion.div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <div className="chart-header">
            <h2>Monthly Income vs Expenses</h2>
          </div>
          <div className="chart-content">
            {dashboardData.monthlyData.length > 0 ? (
              <Bar data={monthlyChartData} options={chartOptions} />
            ) : (
              <div className="no-data">
                <p>No monthly data available</p>
              </div>
            )}
          </div>
        </div>

        <div className="chart-container">
          <div className="chart-header">
            <h2>Expenses by Category</h2>
          </div>
          <div className="chart-content">
            {dashboardData.categoryData.length > 0 ? (
              <Doughnut 
                data={categoryChartData} 
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'right',
                    }
                  }
                }} 
              />
            ) : (
              <div className="no-data">
                <p>No category data available</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Transactions & Budget Progress */}
      <div className="dashboard-grid">
        {/* Recent Transactions */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Recent Transactions</h2>
            <button className="view-all-btn">View All</button>
          </div>
          <div className="transactions-list">
            {dashboardData.recentTransactions.length > 0 ? (
              dashboardData.recentTransactions.map(transaction => (
                <div key={transaction._id} className="transaction-item">
                  <div className="transaction-info">
                    <h4>{transaction.title}</h4>
                    <p>{transaction.category}</p>
                  </div>
                  <div className={`transaction-amount ${transaction.type}`}>
                    {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                  </div>
                </div>
              ))
            ) : (
              <div className="no-data">
                <p>No recent transactions</p>
              </div>
            )}
          </div>
        </div>

        {/* Budget Progress */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Budget Progress</h2>
            <button className="view-all-btn">View All</button>
          </div>
          <div className="budget-list">
            {dashboardData.budgets.length > 0 ? (
              dashboardData.budgets.slice(0, 3).map(budget => (
                <BudgetProgress key={budget._id} budget={budget} />
              ))
            ) : (
              <div className="no-data">
                <p>No budgets set</p>
              </div>
            )}
          </div>
        </div>

        {/* Groups Overview */}
        {dashboardData.groups.length > 0 && (
          <div className="dashboard-card">
            <div className="card-header">
              <h2>Group Expenses</h2>
              <button className="view-all-btn">View All</button>
            </div>
            <div className="groups-list">
              {dashboardData.groups.slice(0, 3).map(group => (
                <div key={group._id} className="group-item">
                  <div className="group-info">
                    <h4>{group.name}</h4>
                    <p><FaUsers /> {group.members.length} members</p>
                  </div>
                  <div className="group-balance">
                    {formatCurrency(group.totalExpenses || 0)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Transaction Form Modal */}
      {showTransactionForm && (
        <div className="modal-overlay" onClick={() => setShowTransactionForm(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <TransactionForm
              onClose={() => setShowTransactionForm(false)}
              onSuccess={() => {
                setShowTransactionForm(false);
                fetchDashboardData();
              }}
            />
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default Dashboard;