import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from "react-router-dom";

import reportWebVitals from './reportWebVitals';

import LoginPage from './routes/login/LoginPage';
import HomePage from './routes/home/HomePage';
import NetworkPage from './routes/network/NetworkPage';

import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import ProfilePage from './routes/profile/ProfilePage';
import PostCreationPage from './routes/post/PostCreationPage';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" Component={LoginPage} />
      <Route path="/home" Component={HomePage} />
      <Route path="/network" Component={NetworkPage} />
      <Route path="/profile/:id" Component={ProfilePage} />
      <Route path="/post" Component={PostCreationPage} />
    </Routes>
  </BrowserRouter>
);

reportWebVitals();
