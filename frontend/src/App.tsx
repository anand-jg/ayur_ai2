import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './components/dashboard/Dashboard';
import HealthAssessment from './components/health/HealthAssessment';
import Diagnosis from './components/health/Diagnosis';
import PrivateRoute from './components/auth/PrivateRoute';
import Layout from './components/layout/Layout';

const App: React.FC = () => {
    return (
        <Provider store={store}>
            <Router>
                <Routes>
                    <Route path="/login" element={<LoginForm />} />
                    <Route path="/register" element={<RegisterForm />} />
                    <Route
                        path="/dashboard"
                        element={
                            <Layout>
                                <Dashboard />
                            </Layout>
                        }
                    />
                    <Route
                        path="/assessment"
                        element={
                            <Layout>
                                <HealthAssessment />
                            </Layout>
                        }
                    />
                    <Route
                        path="/diagnosis"
                        element={
                            <Layout>
                                <Diagnosis />
                            </Layout>
                        }
                    />
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                </Routes>
            </Router>
        </Provider>
    );
};

export default App;
