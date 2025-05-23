async function callFixAll() {
  const res = await fetch('http://localhost:8000/fix_all', { method: 'POST' });
  const data = await res.json();
  document.getElementById('output').textContent = JSON.stringify(data, null, 2);
}

async function callDiagnose() {
  const res = await fetch('http://localhost:8000/diagnose');
  const data = await res.json();
  document.getElementById('output').textContent = JSON.stringify(data, null, 2);
}
