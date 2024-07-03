import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import LoginPage from './pages/login/LoginPage.tsx';
import ProjectPage from './pages/ProjectPage';
import ProjectsPage from "./pages/projects/ProjectsPage.tsx";

const AppRouter: React.FC = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/login" component={LoginPage} />
                <Route exact path="/projects" component={ProjectsPage} />
                <Route path="/project/*" component={ProjectPage} />
                <Redirect to="/" />
            </Switch>
        </Router>
    );
};

export default AppRouter;
