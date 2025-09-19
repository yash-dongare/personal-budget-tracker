# Create the project structure for the Personal Budget Tracker
import os
import json

# Define the project structure
project_structure = {
    "personal-budget-tracker": {
        "README.md": "",
        "package.json": "",
        "backend": {
            "package.json": "",
            "server.js": "",
            "config": {
                "database.js": "",
                "auth.js": ""
            },
            "models": {
                "User.js": "",
                "Transaction.js": "",
                "Budget.js": "",
                "Group.js": ""
            },
            "routes": {
                "auth.js": "",
                "transactions.js": "",
                "budgets.js": "",
                "groups.js": "",
                "analytics.js": ""
            },
            "middleware": {
                "auth.js": "",
                "validation.js": ""
            },
            "controllers": {
                "authController.js": "",
                "transactionController.js": "",
                "budgetController.js": "",
                "groupController.js": "",
                "analyticsController.js": ""
            }
        },
        "frontend": {
            "package.json": "",
            "public": {
                "index.html": "",
                "manifest.json": ""
            },
            "src": {
                "App.js": "",
                "index.js": "",
                "components": {
                    "Dashboard": {
                        "Dashboard.js": "",
                        "Dashboard.css": ""
                    },
                    "Transactions": {
                        "TransactionForm.js": "",
                        "TransactionList.js": "",
                        "TransactionItem.js": ""
                    },
                    "Budgets": {
                        "BudgetForm.js": "",
                        "BudgetList.js": "",
                        "BudgetProgress.js": ""
                    },
                    "Groups": {
                        "GroupDashboard.js": "",
                        "GroupForm.js": "",
                        "ExpenseSplit.js": "",
                        "SettleBalance.js": ""
                    },
                    "Charts": {
                        "ExpenseChart.js": "",
                        "BudgetChart.js": "",
                        "TrendChart.js": ""
                    },
                    "Auth": {
                        "Login.js": "",
                        "Register.js": "",
                        "AuthForm.css": ""
                    },
                    "Common": {
                        "Navbar.js": "",
                        "Footer.js": "",
                        "LoadingSpinner.js": ""
                    }
                },
                "context": {
                    "AuthContext.js": "",
                    "BudgetContext.js": ""
                },
                "utils": {
                    "api.js": "",
                    "helpers.js": "",
                    "constants.js": ""
                },
                "styles": {
                    "App.css": "",
                    "index.css": "",
                    "variables.css": ""
                }
            }
        },
        "docs": {
            "project-specification.md": "",
            "api-documentation.md": "",
            "database-design.md": "",
            "deployment-guide.md": ""
        }
    }
}

print("Personal Budget Tracker Project Structure")
print("=" * 50)

def print_structure(structure, indent=0):
    for name, content in structure.items():
        print("  " * indent + "📁 " + name + "/")
        if isinstance(content, dict):
            print_structure(content, indent + 1)
        else:
            # This represents a file
            if name.endswith(('.js', '.json', '.md', '.css', '.html')):
                file_icon = "📄"
            else:
                file_icon = "📄"
            print("  " * (indent + 1) + file_icon + " " + name)

print_structure(project_structure)

print("\n" + "=" * 50)
print("Total Structure Overview:")
print("- Backend: Node.js + Express + MongoDB")
print("- Frontend: React.js + Context API + Chart.js")
print("- Authentication: JWT-based")
print("- Database: MongoDB with Mongoose ODM")
print("- Styling: CSS3 with responsive design")