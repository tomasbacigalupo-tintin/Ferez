import { useState } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState('');

  async function callFixAll() {
    const res = await fetch('http://localhost:8000/fix_all', { method: 'POST' });
    const data = await res.json();
    setOutput(JSON.stringify(data, null, 2));
  }

  async function callDiagnose() {
    const res = await fetch('http://localhost:8000/diagnose');
    const data = await res.json();
    setOutput(JSON.stringify(data, null, 2));
  }

  return (
    <div className="container">
      <h1>WiFi Fixer</h1>
      <div className="actions">
        <button onClick={callFixAll}>Arreglar todo</button>
        <button onClick={callDiagnose}>Diagnóstico</button>
      </div>
      <pre>{output}</pre>
    </div>
  );
}

export default App;
