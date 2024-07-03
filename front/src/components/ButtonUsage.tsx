import React from 'react';
import Button from '@mui/material/Button';

interface ButtonUsageProps {
  variant?: 'text' | 'outlined' | 'contained';
}

const ButtonUsage: React.FC<ButtonUsageProps> = ({ variant = 'contained' }) => {
  return (
      <div className="w-full h-full">
        <Button variant={variant}>Hello world</Button>
      </div>
  );
};

export default ButtonUsage;
