import React from 'react';
import './App.css';
import LoginPage from './components/LoginPage';
import Footer from './components/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="App">
      <div className="site_container">
        <LoginPage/>
        <Footer/>
      </div>
    </div>
  );
}

export default App;