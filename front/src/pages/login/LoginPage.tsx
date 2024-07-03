import React from "react";
import HeaderLogin from "./HeaderLogin.tsx";
import LoginForm from "./LoginForm.tsx";

const LoginPage: React.FC = () => {
    return (
        <>
            <HeaderLogin/>
            <div className="w-[30vw] h-[30vh] mt-[20vh] flex mx-auto ">
                <LoginForm/>
            </div>
            {/*<FooterLogin/>*/}
        </>
    );
}

export default LoginPage;