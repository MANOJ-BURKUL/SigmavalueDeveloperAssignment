import React from 'react';
import ChatInterface from './components/ChatInterface';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <div className="App bg-light" style={{ minHeight: '100vh', paddingTop: '20px' }}>
      <ChatInterface />
    </div>
  );
}

export default App;
