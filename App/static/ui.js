let editingId = null;

async function fetchExercises() {
  const res = await fetch('/exercises');
  const data = await res.json();
  const tbody = document.querySelector('#exerciseTable tbody');
  tbody.innerHTML = '';
  data.forEach(ex => {
    const tr = document.createElement('tr');
    const targets = `${ex.target_sets ?? '-'}×${ex.target_reps ?? '-'} @ ${ex.target_hold_sec ?? 0}s`;
    const schedule = (ex.schedule_dow || []).sort().join(', ');
    tr.innerHTML = `
      <td>${ex.id}</td>
      <td>${ex.name}</td>
      <td><span class="badge">${ex.side}</span></td>
      <td><span class="badge">${ex.category}</span></td>
      <td>${targets}</td>
      <td>${schedule}</td>
      <td>
        <button class="action-edit" onclick="editExercise(${ex.id})">Edit</button>
        <button class="action-del" onclick="deleteExercise(${ex.id})">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function deleteExercise(id) {
  const ok = confirm('Delete exercise #' + id + '?');
  if (!ok) return;
  const res = await fetch(`/exercises/${id}`, { method: 'DELETE' });
  if (res.status === 204) {
    if (editingId === id) cancelEdit();
    await fetchExercises();
  } else {
    alert('Failed to delete (status ' + res.status + ')');
  }
}

async function editExercise(id) {
  const res = await fetch(`/exercises/${id}`);
  if (!res.ok) { alert('Failed to load exercise #' + id); return; }
  const ex = await res.json();
  document.getElementById('name').value = ex.name;
  document.getElementById('side').value = ex.side;
  document.getElementById('category').value = ex.category;
  document.getElementById('target_sets').value = ex.target_sets ?? '';
  document.getElementById('target_reps').value = ex.target_reps ?? '';
  document.getElementById('target_hold_sec').value = ex.target_hold_sec ?? '';
  clearDOW(); setDOW(ex.schedule_dow || []);
  editingId = ex.id; setModeEdit(true); document.getElementById('name').focus();
}

function clearDOW() { for (const cb of document.querySelectorAll('input[name="dow"]')) cb.checked = false; }
function setDOW(arr) {
  const set = new Set(arr.map(Number));
  for (const cb of document.querySelectorAll('input[name="dow"]')) cb.checked = set.has(Number(cb.value));
}
function readCheckedDOW() {
  return Array.from(document.querySelectorAll('input[name="dow"]:checked'))
    .map(cb => Number(cb.value)).sort((a,b)=>a-b);
}
function toNullableInt(v) { const n = Number(v); return Number.isFinite(n) && v !== '' ? n : null; }

function payloadFromForm() {
  return {
    name: document.getElementById('name').value.trim(),
    side: document.getElementById('side').value,
    category: document.getElementById('category').value,
    target_sets: toNullableInt(document.getElementById('target_sets').value),
    target_reps: toNullableInt(document.getElementById('target_reps').value),
    target_hold_sec: toNullableInt(document.getElementById('target_hold_sec').value),
    schedule_dow: readCheckedDOW()
  };
}

async function submitExercise(ev) {
  ev.preventDefault();
  const payload = payloadFromForm();
  if (!payload.name) { showMsg('Name is required'); return false; }
  let res;
  if (editingId) {
    res = await fetch(`/exercises/${editingId}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } else {
    res = await fetch('/exercises', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }
  if (res.ok) {
    document.getElementById('exerciseForm').reset(); clearDOW();
    if (editingId) { showMsg('Updated ✓'); editingId = null; setModeEdit(false); }
    else { showMsg('Saved ✓'); }
    await fetchExercises();
  } else {
    showMsg('Error: ' + (await res.text()));
  }
  return false;
}

function cancelEdit() {
  document.getElementById('exerciseForm').reset(); clearDOW();
  editingId = null; setModeEdit(false); showMsg('Canceled');
}

function setModeEdit(on) {
  const saveBtn = document.getElementById('saveBtn');
  const cancelBtn = document.getElementById('cancelBtn');
  if (saveBtn) saveBtn.textContent = on ? 'Save Changes' : 'Add Exercise';
  if (cancelBtn) cancelBtn.classList.toggle('hidden', !on);
}

function showMsg(text) { const el = document.getElementById('msg'); if (el) el.textContent = text; }

window.addEventListener('DOMContentLoaded', fetchExercises);
