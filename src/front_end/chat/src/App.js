import React from "react";
import { Container } from '@material-ui/core'
import { BrowserRouter, Switch, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Home from "./components/Home/Home";
import './App.css'

// Main App Code
const App = () => {
    // Main Website Return
    return (
        <BrowserRouter>
            <Container maxWidth='lg' className="mainContainer">
                <Navbar />
                <Switch>
                    <Route path="/" exact component={Home}/>
                </Switch>
            </Container>
        </BrowserRouter>
    )
}

export default App;
