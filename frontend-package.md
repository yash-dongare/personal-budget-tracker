{
  "name": "budget-tracker-frontend",
  "version": "1.0.0",
  "private": true,
  "description": "React frontend for Personal Budget Tracker application",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "react-router-dom": "^6.14.2",
    "axios": "^1.4.0",
    "chart.js": "^4.3.3",
    "react-chartjs-2": "^5.2.0",
    "date-fns": "^2.30.0",
    "react-datepicker": "^4.16.0",
    "react-hot-toast": "^2.4.1",
    "react-icons": "^4.10.1",
    "framer-motion": "^10.16.1",
    "formik": "^2.4.3",
    "yup": "^1.2.0",
    "react-select": "^5.7.4",
    "react-modal": "^3.16.1",
    "react-loading-skeleton": "^3.3.1",
    "recharts": "^2.7.2",
    "currency.js": "^2.0.4",
    "lodash": "^4.17.21",
    "uuid": "^9.0.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "web-vitals": "^2.1.4",
    "eslint": "^8.45.0",
    "eslint-plugin-react": "^7.33.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "prettier": "^3.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "lint": "eslint src/**/*.{js,jsx}",
    "lint:fix": "eslint src/**/*.{js,jsx} --fix",
    "format": "prettier --write src/**/*.{js,jsx,css,md}",
    "analyze": "npm run build && npx source-map-explorer 'build/static/js/*.js'"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ],
    "rules": {
      "no-unused-vars": "warn",
      "no-console": "warn",
      "react-hooks/exhaustive-deps": "warn"
    }
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000",
  "engines": {
    "node": ">=16.0.0"
  }
}