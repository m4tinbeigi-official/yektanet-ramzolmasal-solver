const RTL_ISOLATE = '\u2067';
const LTR_ISOLATE = '\u2066';
const AUTO_ISOLATE = '\u2068';
const POP_ISOLATE = '\u2069';

function rtl(text) {
  return RTL_ISOLATE + text + POP_ISOLATE;
}

function ltr(text) {
  return LTR_ISOLATE + text + POP_ISOLATE;
}

function auto(text) {
  return AUTO_ISOLATE + text + POP_ISOLATE;
}

function setHomeLink(signedIn) {
  const link = document.getElementById('nav-home');
  if (link === null) {
    return;
  }
  link.textContent = signedIn ? 'مسابقه' : 'ورود';
}

async function labelHomeLink() {
  try {
    const player = await api('api/me');
    setHomeLink(player.nickname !== '');
  } catch (error) {
    setHomeLink(false);
  }
}

async function api(path, body) {
  const response = await fetch(path, {
    method: body === undefined ? 'GET' : 'POST',
    headers: {'Content-Type': 'application/json'},
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error ?? rtl(`خطای ${response.status}`));
  }
  return payload;
}

