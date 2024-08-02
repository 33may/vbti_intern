import React from "react";
import HeaderLogin from "./HeaderLogin.tsx";
import LoginForm from "./LoginForm.tsx";
import useAuthStore from "../../util/storage/authStore.ts";
import {Redirect} from "react-router-dom";

const LoginPage: React.FC = () => {

    const { isAuthenticated } = useAuthStore();

    return (
        <>
            {!isAuthenticated} ? (
            <HeaderLogin/>
            <div className="w-[30vw] h-[30vh] mt-[20vh] flex mx-auto min-w-[500px]">
                <LoginForm/>
            </div>
            {/*<FooterLogin/>*/}
            ) :
            (
                <Redirect to={{ pathname: '/projects' }}/>
            )
        </>
    );
}

export default LoginPage;