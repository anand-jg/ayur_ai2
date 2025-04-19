import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Typography,
    Button,
    Paper,
    Radio,
    RadioGroup,
    FormControlLabel,
    FormControl,
    CircularProgress,
} from '@mui/material';
import { decisions } from '../../services/api';

interface Question {
    id: number;
    text: string;
    category: string;
    answers: Answer[];
}

interface Answer {
    id: number;
    text: string;
    next_question: number | null;
}

const HealthAssessment: React.FC = () => {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
    const [sessionId, setSessionId] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const initializeAssessment = async () => {
            try {
                const data = await decisions.getQuestions();
                setQuestions(data);
                const rootQuestion = data.find((q: Question) => q.category === 'root');
                if (rootQuestion) {
                    setCurrentQuestion(rootQuestion);
                    setSessionId(Date.now().toString());
                }
            } catch (err: any) {
                setError(err.response?.data?.message || 'Failed to load questions');
            } finally {
                setLoading(false);
            }
        };

        initializeAssessment();
    }, []);

    const handleAnswerSelect = (answerId: number) => {
        setSelectedAnswer(answerId);
    };

    const handleSubmit = async () => {
        if (!currentQuestion || !selectedAnswer) return;

        try {
            await decisions.submitResponse({
                question: currentQuestion.id,
                answer: selectedAnswer,
                session_id: sessionId,
            });

            const answer = currentQuestion.answers.find(a => a.id === selectedAnswer);
            if (answer?.next_question) {
                const nextQuestion = questions.find(q => q.id === answer.next_question);
                if (nextQuestion) {
                    setCurrentQuestion(nextQuestion);
                    setSelectedAnswer(null);
                } else {
                    // No more questions, get diagnosis
                    const diagnosis = await decisions.getDiagnosis(sessionId);
                    navigate('/diagnosis', { state: { diagnosis } });
                }
            } else {
                // No more questions, get diagnosis
                const diagnosis = await decisions.getDiagnosis(sessionId);
                navigate('/diagnosis', { state: { diagnosis } });
            }
        } catch (err: any) {
            setError(err.response?.data?.message || 'Failed to submit answer');
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    if (!currentQuestion) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography>No questions available</Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            <Paper sx={{ p: 3 }}>
                <Typography variant="h5" gutterBottom>
                    Health Assessment
                </Typography>
                <Typography variant="body1" gutterBottom>
                    {currentQuestion.text}
                </Typography>
                <FormControl component="fieldset" sx={{ mt: 2 }}>
                    <RadioGroup
                        value={selectedAnswer}
                        onChange={(e) => handleAnswerSelect(Number(e.target.value))}
                    >
                        {currentQuestion.answers.map((answer) => (
                            <FormControlLabel
                                key={answer.id}
                                value={answer.id}
                                control={<Radio />}
                                label={answer.text}
                            />
                        ))}
                    </RadioGroup>
                </FormControl>
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleSubmit}
                        disabled={!selectedAnswer}
                    >
                        Next
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};

export default HealthAssessment; 