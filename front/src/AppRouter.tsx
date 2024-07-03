import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import MainPage from './pages/MainPage';
import ProjectPage from './pages/ProjectPage';

const AppRouter: React.FC = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component={MainPage} />
                <Route path="/project/:proj_name" component={ProjectPage} />
                <Redirect to="/" />
            </Switch>
        </Router>
    );
};

export default AppRouter;
