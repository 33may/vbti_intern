import React, { ComponentType } from 'react';
import {Redirect, Route, RouteProps} from 'react-router-dom';
import useAuthStore from '../util/storage/authStore';

interface AdminRouteProps extends RouteProps {
    component: ComponentType<RouteProps>;
}

const AdminRoute: React.FC<AdminRouteProps> = ({ component: Component, ...rest }) => {
    const { isAuthenticated, user } = useAuthStore();

    return (
        <Route
            {...rest}
            render={(props) =>
                isAuthenticated && user && user.account_type === 'admin' ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/login',
                            state: { from: props.location },
                        }}
                    />
                )
            }
        />
    );
};

export default AdminRoute;
