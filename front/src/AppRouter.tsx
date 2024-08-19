import React from 'react';
import {BrowserRouter as Router, Switch, Redirect, Route} from 'react-router-dom';
import LoginPage from './pages/login/LoginPage.tsx';
import ProjectPage from './pages/ProjectPage';
import ProjectsPage from "./pages/projects/ProjectsPage.tsx";
import LoginRoute from "./components/LoginRoute.tsx";

const AppRouter: React.FC = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/login" component={LoginPage} />
                <LoginRoute exact path="/projects" component={ProjectsPage} />
                <LoginRoute path="/project/*" component={ProjectPage} />
                <Redirect to="/" />
            </Switch>
        </Router>
    );
};

export default AppRouter;
