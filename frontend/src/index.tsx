import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import reportWebVitals from './reportWebVitals';

import LoginPage from './routes/login/LoginPage';
import HomePage from './routes/home/HomePage';
import NetworkPage from './routes/network/NetworkPage';

import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import ProfilePage from './routes/profile/ProfilePage';
import PostPage from './routes/post/PostPage';
import PostCreationPage from './routes/post/PostCreationPage';
import { getUserId } from './utils/auth';
import SettingsPage from './routes/settings/SettingsPage';
import PostEditPage from './routes/post/PostEditPage';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" Component={LoginPage} />
      <Route path="/home" Component={HomePage} />
      <Route path="/network" Component={NetworkPage} />
      <Route path="/profile" element={<Navigate to={`/profile/${getUserId()}`} />} />
      <Route path="/profile/settings" Component={SettingsPage} />
      <Route path="/profile/:id" Component={ProfilePage} />
      <Route path="/profile/:author/posts/:post" Component={PostPage} />
      <Route path="/post" Component={PostCreationPage} />
      <Route path="/post/:id" Component={PostEditPage} />
    </Routes>
  </BrowserRouter>
);

reportWebVitals();
