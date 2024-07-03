import React from 'react';
import Button from '@mui/material/Button';

interface ButtonUsageProps {
    text: string;
    variant?: 'text' | 'outlined' | 'contained';
    col?: "inherit" | "primary" | "secondary" | "success" | "error" | "info" | "warning";
    onAction?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const CButton: React.FC<ButtonUsageProps> = ({ text, variant = 'text', col = 'error', onAction }) => {
    return (
        <Button onClick={onAction} variant={variant} color={col} fullWidth>
            {text}
        </Button>
    );
};

export default CButton;
