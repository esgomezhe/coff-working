// src/App.js

import React, { useContext } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const Login = () => {
    const { setUser } = useContext(AuthContext);

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/auth/google/`, {
                access_token: credentialResponse.credential,
            });
            localStorage.setItem('token', res.data.key);
            setUser(res.data.user);
        } catch (error) {
            console.error('Error during Google login', error);
        }
    };

    const handleGoogleFailure = (error) => {
        console.error('Google login failed', error);
    };

    return (
        <div>
            <h2>Login</h2>
            <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleFailure}
            />
        </div>
    );
};

const Dashboard = () => {
    const { user } = useContext(AuthContext);

    if (!user) {
        return <Navigate to="/login" />;
    }

    return (
        <div>
            <h2>Dashboard</h2>
            <p>Welcome, {user.username}!</p>
        </div>
    );
};

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="*" element={<Navigate to="/dashboard" />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;