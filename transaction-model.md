const mongoose = require('mongoose');

const transactionSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'Transaction must belong to a user']
  },
  group: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Group',
    default: null // null for personal transactions
  },
  title: {
    type: String,
    required: [true, 'Transaction title is required'],
    trim: true,
    maxLength: [100, 'Title cannot exceed 100 characters']
  },
  description: {
    type: String,
    trim: true,
    maxLength: [500, 'Description cannot exceed 500 characters']
  },
  amount: {
    type: Number,
    required: [true, 'Amount is required'],
    min: [0.01, 'Amount must be greater than 0']
  },
  type: {
    type: String,
    required: [true, 'Transaction type is required'],
    enum: {
      values: ['income', 'expense'],
      message: 'Type must be either income or expense'
    }
  },
  category: {
    type: String,
    required: [true, 'Category is required'],
    trim: true
  },
  subcategory: {
    type: String,
    trim: true
  },
  date: {
    type: Date,
    required: [true, 'Date is required'],
    default: Date.now
  },
  currency: {
    type: String,
    required: true,
    default: 'USD',
    enum: ['USD', 'EUR', 'GBP', 'INR', 'CAD', 'AUD', 'JPY']
  },
  paymentMethod: {
    type: String,
    enum: ['cash', 'credit_card', 'debit_card', 'bank_transfer', 'paypal', 'other'],
    default: 'cash'
  },
  location: {
    type: String,
    trim: true
  },
  receipt: {
    url: String,
    filename: String,
    uploadedAt: Date
  },
  tags: [{
    type: String,
    trim: true,
    lowercase: true
  }],
  isRecurring: {
    type: Boolean,
    default: false
  },
  recurringDetails: {
    frequency: {
      type: String,
      enum: ['weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'],
      required: function() { return this.isRecurring; }
    },
    nextDue: {
      type: Date,
      required: function() { return this.isRecurring; }
    },
    endDate: Date
  },
  groupSplit: {
    isShared: {
      type: Boolean,
      default: false
    },
    splitType: {
      type: String,
      enum: ['equal', 'percentage', 'amount', 'shares'],
      required: function() { return this.groupSplit.isShared; }
    },
    splitDetails: [{
      member: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      amount: Number,
      percentage: Number,
      shares: Number,
      paid: {
        type: Boolean,
        default: false
      }
    }],
    paidBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    }
  },
  status: {
    type: String,
    enum: ['pending', 'completed', 'cancelled'],
    default: 'completed'
  },
  metadata: {
    source: {
      type: String,
      enum: ['manual', 'import', 'bank_sync', 'receipt_scan'],
      default: 'manual'
    },
    confidence: {
      type: Number,
      min: 0,
      max: 1
    },
    verified: {
      type: Boolean,
      default: true
    }
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Virtual for formatted amount
transactionSchema.virtual('formattedAmount').get(function() {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: this.currency
  });
  return formatter.format(this.amount);
});

// Virtual for transaction age
transactionSchema.virtual('daysOld').get(function() {
  return Math.floor((Date.now() - this.date) / (1000 * 60 * 60 * 24));
});

// Virtual for month/year
transactionSchema.virtual('monthYear').get(function() {
  const date = new Date(this.date);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
});

// Pre-save middleware
transactionSchema.pre('save', function(next) {
  // Ensure group transactions have proper split details
  if (this.group && this.groupSplit.isShared) {
    if (!this.groupSplit.paidBy) {
      this.groupSplit.paidBy = this.user;
    }
  }
  
  // Set next recurring date
  if (this.isRecurring && this.recurringDetails.frequency && !this.recurringDetails.nextDue) {
    const next = new Date(this.date);
    switch (this.recurringDetails.frequency) {
      case 'weekly':
        next.setDate(next.getDate() + 7);
        break;
      case 'biweekly':
        next.setDate(next.getDate() + 14);
        break;
      case 'monthly':
        next.setMonth(next.getMonth() + 1);
        break;
      case 'quarterly':
        next.setMonth(next.getMonth() + 3);
        break;
      case 'yearly':
        next.setFullYear(next.getFullYear() + 1);
        break;
    }
    this.recurringDetails.nextDue = next;
  }
  
  next();
});

// Static method for expense categories
transactionSchema.statics.getExpenseCategories = function() {
  return [
    'Food & Dining', 'Shopping', 'Transportation', 'Bills & Utilities',
    'Entertainment', 'Health & Fitness', 'Travel', 'Education',
    'Personal Care', 'Gifts & Donations', 'Business Services', 'Other'
  ];
};

// Static method for income categories
transactionSchema.statics.getIncomeCategories = function() {
  return [
    'Salary', 'Freelance', 'Investment', 'Business', 'Rental', 
    'Gift', 'Bonus', 'Refund', 'Other'
  ];
};

// Instance method to calculate user's share in group expense
transactionSchema.methods.getUserShare = function(userId) {
  if (!this.groupSplit.isShared) return 0;
  
  const userSplit = this.groupSplit.splitDetails.find(
    split => split.member.toString() === userId.toString()
  );
  
  if (!userSplit) return 0;
  
  switch (this.groupSplit.splitType) {
    case 'equal':
      return this.amount / this.groupSplit.splitDetails.length;
    case 'amount':
      return userSplit.amount || 0;
    case 'percentage':
      return (this.amount * (userSplit.percentage || 0)) / 100;
    case 'shares':
      const totalShares = this.groupSplit.splitDetails.reduce(
        (sum, split) => sum + (split.shares || 0), 0
      );
      return totalShares > 0 ? (this.amount * (userSplit.shares || 0)) / totalShares : 0;
    default:
      return 0;
  }
};

// Indexes for better query performance
transactionSchema.index({ user: 1, date: -1 });
transactionSchema.index({ group: 1, date: -1 });
transactionSchema.index({ category: 1 });
transactionSchema.index({ type: 1 });
transactionSchema.index({ date: -1 });
transactionSchema.index({ 'groupSplit.isShared': 1 });
transactionSchema.index({ 'recurringDetails.nextDue': 1 });
transactionSchema.index({ tags: 1 });

const Transaction = mongoose.model('Transaction', transactionSchema);

module.exports = Transaction;