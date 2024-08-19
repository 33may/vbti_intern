import React, { ComponentType } from 'react';
import { Redirect, Route, RouteProps } from 'react-router-dom';
import useAuthStore from '../util/storage/authStore';

interface LoginRouteProps extends RouteProps {
    component: ComponentType<RouteProps>;
}

const LoginRoute: React.FC<LoginRouteProps> = ({ component: Component, ...rest }) => {
    const { isAuthenticated } = useAuthStore();

    return (
        <Route
            {...rest}
            render={(props) =>
                isAuthenticated ? (
                    <Component {...props} />
                ) : (
                    <Redirect to={{ pathname: "/login" }} />
                )
            }
        />
    );
};

export default LoginRoute;
