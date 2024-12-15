import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ApiManager from './components/ApiManager'
import Intro from './Intro';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Define routes */}
        <Route path="/" element={<Intro />} />
        <Route path="/api-manager" element={<ApiManager />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

reportWebVitals();
