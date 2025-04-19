import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { RootState } from '../../store';
import { logout } from '../../store/slices/authSlice';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        AyurAI
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        {isAuthenticated ? (
                            <>
                                <Typography variant="body1" sx={{ display: 'flex', alignItems: 'center' }}>
                                    Welcome, {user?.first_name} {user?.last_name}
                                </Typography>
                                <Button color="inherit" onClick={handleLogout}>
                                    Logout
                                </Button>
                            </>
                        ) : (
                            <>
                                <Button color="inherit" onClick={() => navigate('/login')}>
                                    Login
                                </Button>
                                <Button color="inherit" onClick={() => navigate('/register')}>
                                    Register
                                </Button>
                            </>
                        )}
                    </Box>
                </Toolbar>
            </AppBar>
            <Container component="main" sx={{ flex: 1, py: 4 }}>
                {children}
            </Container>
            <Box component="footer" sx={{ py: 3, bgcolor: 'background.paper' }}>
                <Container maxWidth="lg">
                    <Typography variant="body2" color="text.secondary" align="center">
                        © {new Date().getFullYear()} AyurAI. All rights reserved.
                    </Typography>
                </Container>
            </Box>
        </Box>
    );
};

export default Layout; 