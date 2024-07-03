import React from 'react';
import { Route, Switch, useRouteMatch } from 'react-router-dom';
import UploadPage from './UploadPage';


const ProjectPage: React.FC = () => {
    const { path } = useRouteMatch();

    return (
        <div>
            <h1>Project Page</h1>
            <Switch>
                <Route exact path={`${path}/upload`} component={UploadPage} />
            </Switch>
        </div>
    );
};

export default ProjectPage;