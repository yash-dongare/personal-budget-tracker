import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Context Providers
import { AuthProvider, useAuth } from './context/AuthContext';
import { BudgetProvider } from './context/BudgetContext';

// Components
import Navbar from './components/Common/Navbar';
import Footer from './components/Common/Footer';
import LoadingSpinner from './components/Common/LoadingSpinner';

// Pages
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import TransactionList from './components/Transactions/TransactionList';
import BudgetList from './components/Budgets/BudgetList';
import GroupDashboard from './components/Groups/GroupDashboard';

// Styles
import './styles/App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  return user ? children : <Navigate to="/login" replace />;
};

// Public Route Component (redirect to dashboard if authenticated)
const PublicRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  return user ? <Navigate to="/dashboard" replace /> : children;
};

function AppContent() {
  const { user, loading, checkAuth } = useAuth();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="app">
      <Navbar />
      
      <main className="main-content">
        <Routes>
          {/* Public Routes */}
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          <Route 
            path="/register" 
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            } 
          />
          
          {/* Protected Routes */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/transactions" 
            element={
              <ProtectedRoute>
                <TransactionList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/budgets" 
            element={
              <ProtectedRoute>
                <BudgetList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/groups" 
            element={
              <ProtectedRoute>
                <GroupDashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Default Route */}
          <Route 
            path="/" 
            element={
              user ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />
            } 
          />
          
          {/* 404 Route */}
          <Route 
            path="*" 
            element={
              <div className="error-page">
                <h1>404 - Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
                <button onClick={() => window.history.back()}>Go Back</button>
              </div>
            } 
          />
        </Routes>
      </main>
      
      <Footer />
      
      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        reverseOrder={false}
        gutter={8}
        containerStyle={{
          top: 20,
          left: 20,
          bottom: 20,
          right: 20,
        }}
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            style: {
              background: '#10b981',
            },
          },
          error: {
            duration: 5000,
            style: {
              background: '#ef4444',
            },
          },
        }}
      />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <BudgetProvider>
        <Router>
          <AppContent />
        </Router>
      </BudgetProvider>
    </AuthProvider>
  );
}

export default App;