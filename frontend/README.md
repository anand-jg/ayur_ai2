# AyurAI Frontend

This is the frontend application for AyurAI, built with React and TypeScript.

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory with the following variables:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

3. Start the development server:
```bash
npm start
```

## Project Structure

```
src/
├── components/         # Reusable UI components
│   ├── common/        # Common components (buttons, inputs, etc.)
│   ├── layout/        # Layout components (header, footer, etc.)
│   └── features/      # Feature-specific components
├── pages/             # Page components
│   ├── auth/          # Authentication pages
│   ├── dashboard/     # User dashboard
│   ├── questions/     # Question tree pages
│   └── doctors/       # Doctor recommendation pages
├── store/             # Redux store
│   ├── slices/        # Redux slices
│   └── hooks/         # Custom hooks
├── services/          # API services
├── utils/             # Utility functions
└── types/             # TypeScript type definitions
```

## Key Features

### Authentication
- User registration and login
- Role-based access control
- Session management

### Question Tree
- Dynamic question flow
- Response collection
- Progress tracking
- Result generation

### Doctor Recommendations
- Doctor search and filtering
- Profile viewing
- Appointment scheduling
- Reviews and ratings

## Development Guidelines

1. Follow TypeScript best practices
2. Use functional components with hooks
3. Implement proper error handling
4. Write unit tests for critical components
5. Document complex logic and components

## Available Scripts

- `npm start`: Start development server
- `npm build`: Build for production
- `npm test`: Run tests
- `npm lint`: Run linter
- `npm format`: Format code

## Dependencies

- React 18
- TypeScript
- Redux Toolkit
- React Router
- Material-UI
- Axios
- Socket.io-client
