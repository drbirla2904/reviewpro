/* ReviewPro — Global JS */
'use strict';

// ── CSRF ──────────────────────────────────────────────────────────────────────
function getCsrf() {
  return document.cookie.split(';').map(c => c.trim())
    .find(c => c.startsWith('csrftoken='))?.split('=')[1] ?? '';
}

// ── FETCH HELPERS ─────────────────────────────────────────────────────────────
async function api(url, method = 'GET', data = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
  };
  if (data) opts.body = JSON.stringify(data);
  const res = await fetch(url, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}
const apiGet  = url       => api(url, 'GET');
const apiPost = (url, d)  => api(url, 'POST', d);
const apiPatch= (url, d)  => api(url, 'PATCH', d);

// ── TOAST ─────────────────────────────────────────────────────────────────────
function toast(msg, type = 'success') {
  let container = document.getElementById('toast');
  if (!container) {
    container = Object.assign(document.createElement('div'), { id: 'toast' });
    document.body.appendChild(container);
  }
  const item = document.createElement('div');
  item.className = `toast-item ${type}`;
  item.innerHTML = `<span class="toast-dot"></span><span>${msg}</span>`;
  container.appendChild(item);
  requestAnimationFrame(() => { requestAnimationFrame(() => item.classList.add('show')); });
  setTimeout(() => {
    item.classList.remove('show');
    setTimeout(() => item.remove(), 350);
  }, 3200);
}

// ── MODAL ─────────────────────────────────────────────────────────────────────
function openModal(id)  { document.getElementById(id)?.classList.add('open'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) e.target.classList.remove('open');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
});

// ── BUTTON LOADING ────────────────────────────────────────────────────────────
function btnLoading(btn, loading) {
  if (loading) {
    btn._origHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>';
  } else {
    btn.disabled = false;
    btn.innerHTML = btn._origHTML || btn.innerHTML;
  }
}

// ── CONFIRM ───────────────────────────────────────────────────────────────────
function confirmAction(msg, fn) {
  if (window.confirm(msg)) fn();
}

// ── COPY ──────────────────────────────────────────────────────────────────────
function copyText(text, label) {
  navigator.clipboard.writeText(text).then(() => toast(`${label || 'Copied'}!`));
}
