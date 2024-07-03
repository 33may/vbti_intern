import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const NewProjectCard: React.FC = () => {
    return (
        <Card sx={{ width: 300, height: 200, display: 'flex', justifyContent: 'center', alignItems: 'center', margin: 2 }}>
            <CardContent sx={{ textAlign: 'center' }}>
                <AddIcon sx={{ fontSize: 50 }} />
                <Typography variant="body2" color="text.secondary">
                    Add New Project
                </Typography>
            </CardContent>
        </Card>
    );
};

export default NewProjectCard;
