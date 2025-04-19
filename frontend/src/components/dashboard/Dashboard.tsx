import React from 'react';
import { useSelector } from 'react-redux';
import { Box, Typography, Paper, Button } from '@mui/material';
import { RootState } from '../../store';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
    const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);
    const navigate = useNavigate();

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Welcome to AyurAI
            </Typography>
            <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
                <Box sx={{ flex: 1, minWidth: 300 }}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Health Assessment
                        </Typography>
                        <Typography variant="body1" paragraph>
                            Take our health assessment to get personalized Ayurvedic insights and recommendations.
                        </Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => navigate('/assessment')}
                        >
                            Start Assessment
                        </Button>
                    </Paper>
                </Box>
                {isAuthenticated && (
                    <Box sx={{ flex: 1, minWidth: 300 }}>
                        <Paper sx={{ p: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                User Information
                            </Typography>
                            <Typography variant="body1">
                                Name: {user?.first_name} {user?.last_name}
                            </Typography>
                            <Typography variant="body1">
                                Email: {user?.email}
                            </Typography>
                            {user?.phone_number && (
                                <Typography variant="body1">
                                    Phone: {user.phone_number}
                                </Typography>
                            )}
                        </Paper>
                    </Box>
                )}
            </Box>
        </Box>
    );
};

export default Dashboard; 