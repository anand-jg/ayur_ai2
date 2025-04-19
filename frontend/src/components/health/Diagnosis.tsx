import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
    Box,
    Typography,
    Button,
    Paper,
    List,
    ListItem,
    ListItemText,
    Divider,
} from '@mui/material';

interface Diagnosis {
    id: number;
    summary: string;
    recommendations: string[];
    created_at: string;
}

const Diagnosis: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const diagnosis = location.state?.diagnosis as Diagnosis;

    if (!diagnosis) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography color="error">No diagnosis data available</Typography>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => navigate('/assessment')}
                    sx={{ mt: 2 }}
                >
                    Start Assessment
                </Button>
            </Box>
        );
    }

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            <Paper sx={{ p: 3 }}>
                <Typography variant="h4" gutterBottom>
                    Your Health Diagnosis
                </Typography>
                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                    Generated on {new Date(diagnosis.created_at).toLocaleDateString()}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom>
                    Summary
                </Typography>
                <Typography variant="body1" paragraph>
                    {diagnosis.summary}
                </Typography>
                <Typography variant="h6" gutterBottom>
                    Recommendations
                </Typography>
                <List>
                    {diagnosis.recommendations.map((recommendation, index) => (
                        <ListItem key={index}>
                            <ListItemText primary={recommendation} />
                        </ListItem>
                    ))}
                </List>
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => navigate('/assessment')}
                    >
                        Start New Assessment
                    </Button>
                    <Button
                        variant="outlined"
                        color="primary"
                        onClick={() => navigate('/dashboard')}
                    >
                        Back to Dashboard
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};

export default Diagnosis; 