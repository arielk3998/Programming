import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Dashboard from './components/Dashboard';
import Editor from './components/Editor';
import Glossary from './components/Glossary';
import ProjectTracker from './components/ProjectTracker';
import StyleGuide from './components/StyleGuide';
import TemplatesLibrary from './components/TemplatesLibrary';
import Tutorials from './components/Tutorials';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/login" component={Login} />
                <Route path="/register" component={Register} />
                <Route path="/profile" component={Profile} />
                <Route path="/dashboard" component={Dashboard} />
                <Route path="/editor" component={Editor} />
                <Route path="/glossary" component={Glossary} />
                <Route path="/project-tracker" component={ProjectTracker} />
                <Route path="/style-guide" component={StyleGuide} />
                <Route path="/templates-library" component={TemplatesLibrary} />
                <Route path="/tutorials" component={Tutorials} />
            </Switch>
        </Router>
    );
};

export default App;