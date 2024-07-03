import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

interface ProjectCardProps {
    title: string;
    description: string;
    id: number;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ title, description, id }) => {
    return (
        <a href={`/project/${id}`}>
            <Card sx={{width: 300, height: 200, margin: 2}}>
                <CardContent>
                    <Typography variant="h5" component="div">
                        {title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {description}
                    </Typography>
                </CardContent>
            </Card>
        </a>
    );
};

export default ProjectCard;
