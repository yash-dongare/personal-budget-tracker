import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { authAPI } from '../utils/api';
import toast from 'react-hot-toast';

// Action Types
const AUTH_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGOUT: 'LOGOUT',
  UPDATE_USER: 'UPDATE_USER',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Initial State
const initialState = {
  user: null,
  token: localStorage.getItem('budgetToken') || null,
  loading: true,
  error: null,
  isAuthenticated: false
};

// Auth Reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };
      
    case AUTH_ACTIONS.LOGIN_SUCCESS:
      localStorage.setItem('budgetToken', action.payload.token);
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        loading: false,
        error: null
      };
      
    case AUTH_ACTIONS.LOGOUT:
      localStorage.removeItem('budgetToken');
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
        error: null
      };
      
    case AUTH_ACTIONS.UPDATE_USER:
      return {
        ...state,
        user: { ...state.user, ...action.payload },
        error: null
      };
      
    case AUTH_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        loading: false
      };
      
    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };
      
    default:
      return state;
  }
};

// Create Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Clear Error
  const clearError = useCallback(() => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  }, []);

  // Check Authentication Status
  const checkAuth = useCallback(async () => {
    const token = localStorage.getItem('budgetToken');
    
    if (!token) {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
      return;
    }

    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      
      // Set token in axios defaults
      authAPI.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      const response = await authAPI.get('/profile');
      
      if (response.data.success) {
        dispatch({
          type: AUTH_ACTIONS.LOGIN_SUCCESS,
          payload: {
            user: response.data.user,
            token: token
          }
        });
      } else {
        throw new Error('Invalid token');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      
      // Remove invalid token
      localStorage.removeItem('budgetToken');
      delete authAPI.defaults.headers.common['Authorization'];
      
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
      
      if (error.response?.status !== 401) {
        toast.error('Authentication check failed');
      }
    }
  }, []);

  // Register User
  const register = useCallback(async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      clearError();

      const response = await authAPI.post('/register', userData);
      
      if (response.data.success) {
        // Set token in axios defaults
        authAPI.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
        
        dispatch({
          type: AUTH_ACTIONS.LOGIN_SUCCESS,
          payload: {
            user: response.data.user,
            token: response.data.token
          }
        });
        
        toast.success('Registration successful! Welcome to Budget Tracker.');
        return { success: true };
      } else {
        throw new Error(response.data.message || 'Registration failed');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Registration failed';
      
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: errorMessage
      });
      
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, [clearError]);

  // Login User
  const login = useCallback(async (credentials) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      clearError();

      const response = await authAPI.post('/login', credentials);
      
      if (response.data.success) {
        // Set token in axios defaults
        authAPI.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
        
        dispatch({
          type: AUTH_ACTIONS.LOGIN_SUCCESS,
          payload: {
            user: response.data.user,
            token: response.data.token
          }
        });
        
        toast.success(`Welcome back, ${response.data.user.name}!`);
        return { success: true };
      } else {
        throw new Error(response.data.message || 'Login failed');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Login failed';
      
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: errorMessage
      });
      
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    }
  }, [clearError]);

  // Logout User
  const logout = useCallback(async () => {
    try {
      // Attempt to logout on server (optional)
      if (state.token) {
        await authAPI.post('/logout');
      }
    } catch (error) {
      console.warn('Server logout failed:', error);
    } finally {
      // Always clear local state
      delete authAPI.defaults.headers.common['Authorization'];
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
      toast.success('Logged out successfully');
    }
  }, [state.token]);

  // Update User Profile
  const updateUser = useCallback(async (userData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      clearError();

      const response = await authAPI.put('/profile', userData);
      
      if (response.data.success) {
        dispatch({
          type: AUTH_ACTIONS.UPDATE_USER,
          payload: response.data.user
        });
        
        toast.success('Profile updated successfully');
        return { success: true };
      } else {
        throw new Error(response.data.message || 'Profile update failed');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Profile update failed';
      
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: errorMessage
      });
      
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
    }
  }, [clearError]);

  // Change Password
  const changePassword = useCallback(async (passwordData) => {
    try {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: true });
      clearError();

      const response = await authAPI.put('/change-password', passwordData);
      
      if (response.data.success) {
        toast.success('Password changed successfully');
        return { success: true };
      } else {
        throw new Error(response.data.message || 'Password change failed');
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Password change failed';
      
      dispatch({
        type: AUTH_ACTIONS.SET_ERROR,
        payload: errorMessage
      });
      
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
    }
  }, [clearError]);

  // Context Value
  const value = {
    // State
    user: state.user,
    token: state.token,
    loading: state.loading,
    error: state.error,
    isAuthenticated: state.isAuthenticated,
    
    // Actions
    register,
    login,
    logout,
    updateUser,
    changePassword,
    checkAuth,
    clearError
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom Hook to use Auth Context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default AuthContext;