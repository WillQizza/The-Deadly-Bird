import React from 'react';
import './App.css';
import LoginPage from './components/LoginPage';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="App">

      <div className="site_container">
        <LoginPage/>
      </div>
    </div>
  );
}

export default App;