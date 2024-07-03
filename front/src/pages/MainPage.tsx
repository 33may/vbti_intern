import React from "react";
import ButtonUsage from "../components/ButtonUsage.tsx";

const MainPage: React.FC = () => {
    return (
        <div className="container flex min-h-screen mx-auto bg-gray-300 ">
            <h1>Main Page</h1>
            <ButtonUsage/>
        </div>
    );
}

export default MainPage;