// src/components/LoginForm.tsx
import React, { useState } from 'react';
import { TextField, IconButton, InputAdornment } from '@mui/material';
import CButton from '../../components/CButton';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import useAuthStore from "../../util/storage/authStore.ts";
import {UserAdd} from "../../util/interfaces/IUser.ts";
import {loginUser} from "../../util/api/APIUser.ts";
import {Redirect} from "react-router-dom";

const LoginForm: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [showPassword, setShowPassword] = useState(false);
    const { isAuthenticated, setToken } = useAuthStore();

    const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };

    const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();

        const user: UserAdd = { email: username, password };

        try{
            const response = await loginUser(user);
            setToken(response.access_token);
        }
        catch (error) {
            setError((error as Error).message);
            setPassword("");

        }
    };

    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
    };

    if (isAuthenticated) {
        return <Redirect to={{ pathname: "/projects" }} />;
    }

    return (
        <div className="flex flex-col items-center w-full p-5">
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
                        ),
                    }}
                />
            </div>

            <div className="mt-[40px] w-full">
                <CButton text="Login" variant="outlined" col="error" onAction={handleSubmit} />
            </div>

            {error && <div className="text-red-500">{error}</div>}
        </div>
    );
};

export default LoginForm;
