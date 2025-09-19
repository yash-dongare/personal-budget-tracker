# Personal Budget Tracker

A comprehensive financial management tool designed to help users track income, expenses, budgets, and spending behavior. The platform supports both individual and group-based expense tracking with clean interfaces, CRUD operations, budget setting, and detailed data visualization.

## 🚀 Features

### Core Features
- **Daily Financial Entry Logging**: Add, edit, and delete income and expense entries
- **Category-Based Budget Setting**: Define monthly budgets for specific categories
- **Data Visualization**: Generate bar graphs, pie charts, and trend lines
- **Financial Summaries & Insights**: Monthly summaries with overspending alerts
- **Group Expense Management**: Create groups for shared financial activities
- **Secure Authentication**: JWT-based user authentication

### Technical Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live budget tracking and expense updates
- **Data Export**: CSV and JSON export capabilities
- **Advanced Filtering**: Search and filter transactions by date, category, amount
- **Secure Storage**: Encrypted data storage with backup options

## 🛠️ Technology Stack

### Frontend
- **React.js** - User interface framework
- **Chart.js** - Data visualization library
- **Context API** - State management
- **CSS3** - Styling and responsive design
- **Axios** - HTTP client for API calls

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - NoSQL database
- **Mongoose** - ODM for MongoDB
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

## 📁 Project Structure

```
personal-budget-tracker/
├── backend/
│   ├── config/
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   └── server.js
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── utils/
│   │   └── styles/
│   └── package.json
└── docs/
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (v4.4 or higher)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-budget-tracker.git
   cd personal-budget-tracker
   ```

2. **Backend Setup**
   ```bash
   cd backend
   npm install
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Configuration**
   Create `.env` file in backend directory:
   ```env
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/budget-tracker
   JWT_SECRET=your-secret-key
   NODE_ENV=development
   ```

5. **Start Development Servers**
   
   Backend (Terminal 1):
   ```bash
   cd backend
   npm run dev
   ```
   
   Frontend (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 📊 Database Schema

### Collections
- **Users**: User authentication and profile data
- **Transactions**: Income and expense records
- **Budgets**: Budget limits and categories
- **Groups**: Shared expense groups and members

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Transactions
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/:id` - Update transaction
- `DELETE /api/transactions/:id` - Delete transaction

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Create new budget
- `PUT /api/budgets/:id` - Update budget

### Groups
- `GET /api/groups` - Get user groups
- `POST /api/groups` - Create new group
- `POST /api/groups/:id/expenses` - Add group expense

## 🎯 Implementation Plan

### Week 1: Planning & Design
- [ ] Requirements analysis and SRS document
- [ ] UI wireframes and database schema
- [ ] Technology stack setup
- [ ] Project architecture design

### Week 2: Core Development
- [ ] Backend APIs and database connectivity
- [ ] Frontend forms and CRUD operations
- [ ] Group management and expense splitting
- [ ] Basic authentication implementation

### Week 3: Data Visualization
- [ ] Chart.js integration
- [ ] Dashboard with summary widgets
- [ ] Filtering and search functionality
- [ ] Budget tracking and alerts

### Week 4: Testing & Deployment
- [ ] Unit and integration testing
- [ ] Bug fixes and optimization
- [ ] Deployment setup
- [ ] Documentation and user guide



## 👨‍💻 Author

**Your Name**
- GitHub: [@yash-dongare](https://github.com/yash-dongare)
- Email: yashanilkumardongare@gmail.com

## 🙏 Acknowledgments

- Chart.js for excellent data visualization
- MongoDB team for the robust database
- React community for comprehensive documentation
- All contributors and testers
