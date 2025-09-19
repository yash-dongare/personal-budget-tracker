const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    maxLength: [50, 'Name cannot exceed 50 characters']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minLength: [6, 'Password must be at least 6 characters'],
    select: false // Don't include password in queries by default
  },
  avatar: {
    type: String,
    default: ''
  },
  currency: {
    type: String,
    default: 'USD',
    enum: ['USD', 'EUR', 'GBP', 'INR', 'CAD', 'AUD', 'JPY']
  },
  timezone: {
    type: String,
    default: 'UTC'
  },
  preferences: {
    theme: {
      type: String,
      enum: ['light', 'dark', 'auto'],
      default: 'light'
    },
    notifications: {
      email: { type: Boolean, default: true },
      budgetAlerts: { type: Boolean, default: true },
      weeklyReports: { type: Boolean, default: true }
    },
    privacy: {
      showBalances: { type: Boolean, default: true },
      shareData: { type: Boolean, default: false }
    }
  },
  resetPasswordToken: String,
  resetPasswordExpire: Date,
  emailVerified: {
    type: Boolean,
    default: false
  },
  emailVerificationToken: String,
  lastLogin: Date,
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Virtual for user's full profile
userSchema.virtual('profile').get(function() {
  return {
    id: this._id,
    name: this.name,
    email: this.email,
    avatar: this.avatar,
    currency: this.currency,
    preferences: this.preferences
  };
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  // Only hash password if it has been modified
  if (!this.isModified('password')) {
    return next();
  }

  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Method to compare password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Method to generate auth token (placeholder - implement JWT in auth controller)
userSchema.methods.generateAuthToken = function() {
  // This will be implemented in the auth controller using JWT
  return this._id.toString();
};

// Static method to find by credentials
userSchema.statics.findByCredentials = async function(email, password) {
  const user = await this.findOne({ email, isActive: true }).select('+password');
  
  if (!user) {
    throw new Error('Invalid login credentials');
  }
  
  const isMatch = await user.comparePassword(password);
  
  if (!isMatch) {
    throw new Error('Invalid login credentials');
  }
  
  // Update last login
  user.lastLogin = new Date();
  await user.save();
  
  return user;
};

// Instance method to remove sensitive data
userSchema.methods.toPublicJSON = function() {
  const user = this.toObject();
  delete user.password;
  delete user.resetPasswordToken;
  delete user.resetPasswordExpire;
  delete user.emailVerificationToken;
  return user;
};

// Indexes for better query performance
userSchema.index({ email: 1 });
userSchema.index({ createdAt: -1 });
userSchema.index({ isActive: 1 });

const User = mongoose.model('User', userSchema);

module.exports = User;