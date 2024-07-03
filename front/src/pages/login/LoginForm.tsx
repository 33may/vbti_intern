import React, { useState } from 'react';
import { Box, TextField, IconButton, InputAdornment } from '@mui/material';
import CButton from "../../components/CButton";
import { Visibility, VisibilityOff } from "@mui/icons-material";

const LoginForm: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };

    const handleSubmit = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        console.log('Username:', username);
        console.log('Password:', password);

    };

    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
    };

    return (
        <div className="flex flex-col items-center w-full p-5 ">
            <div className="m-5 w-full">
                <TextField
                    id="username"
                    label="Username"
                    color="error"
                    variant="standard"
                    fullWidth
                    value={username}
                    onChange={handleUsernameChange}
                />
            </div>

            <div className="m-5 w-full">
                <TextField
                    id="password"
                    label="Password"
                    color="error"
                    variant="standard"
                    type={showPassword ? 'text' : 'password'}
                    fullWidth
                    value={password}
                    onChange={handlePasswordChange}
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                    onMouseDown={handleMouseDownPassword}
                                >
                                    {showPassword ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                            </InputAdornment>
                        )
                    }}
                />
            </div>

            <div className="mt-[40px] w-full">
                <CButton text="Login" variant="outlined" col="error" onAction={handleSubmit} />
            </div>
        </div>
    );
};

export default LoginForm;
