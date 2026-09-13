const LOGIN_STEPS = ['step-waiting', 'step-phone', 'step-code', 'step-nickname', 'step-ready'];
const REMEMBERED_STATE = 'ctf:last-known-state';

function rememberState(state) {
  try {
    window.localStorage.setItem(REMEMBERED_STATE, JSON.stringify(state));
  } catch (error) {
    // A browser refusing storage is not worth a word to the contestant.
  }
}

function rememberedState() {
  try {
    return JSON.parse(window.localStorage.getItem(REMEMBERED_STATE)) || null;
  } catch (error) {
    return null;
  }
}

function forgetState() {
  try {
    window.localStorage.removeItem(REMEMBERED_STATE);
  } catch (error) {
    // As above.
  }
}

const phoneInput = document.getElementById('phone');
const codeInput = document.getElementById('code');
const nicknameInput = document.getElementById('nickname');
const sendCodeButton = document.getElementById('send-code');
const verifyCodeButton = document.getElementById('verify-code');
const saveNicknameButton = document.getElementById('save-nickname');
const changePhoneButton = document.getElementById('change-phone');
const logoutButton = document.getElementById('logout');
const messageElement = document.getElementById('message');
const readyNicknameElement = document.getElementById('ready-nickname');
const readyUnsolvedElement = document.getElementById('ready-unsolved');
const countdownElement = document.getElementById('countdown');
const countdownWhenElement = document.getElementById('countdown-when');
const countdownUnits = {
  days: document.getElementById('cd-days'),
  hours: document.getElementById('cd-hours'),
  minutes: document.getElementById('cd-minutes'),
  seconds: document.getElementById('cd-seconds'),
};
const panelLeadElement = document.getElementById('panel-lead');
const panelAnswerElement = document.getElementById('panel-answer');
const panelCallElement = document.getElementById('panel-call');
const panelAsideElement = document.getElementById('panel-aside');

let countdownTimerId = 0;
let secondsLeft = 0;
const readySolvedElement = document.getElementById('ready-solved');
const PAGE_TITLE = document.title;

const FOX_CARD = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidXNlciJ9.GjAtC_t19ITzY7KeQqfufv8u64So1OI4G-esLFKKKAU';

function chosenLevelQuery() {
  try {
    const id = window.localStorage.getItem('ctf_level');
    if (!id) {
      return '';
    }
    const level = '?level=' + encodeURIComponent(id);
    return id === 'shahed' ? level + '&token=' + FOX_CARD : level;
  } catch (error) {
    return '';
  }
}

const DEFAULT_ICON = 'static/img/hero.jpg';

function showLevelIcon(picture) {
  const link = document.getElementById('favicon');
  if (!link) {
    return;
  }
  link.href = picture || DEFAULT_ICON;
}

const LEVEL_BACKGROUND_GROUND = '#0e1216';

function showLevelBackground(picture) {
  if (!picture) {
    document.body.style.removeProperty('background');
    return;
  }
  document.body.style.background =
    LEVEL_BACKGROUND_GROUND + ' url("' + picture + '") center / cover no-repeat fixed';
}

function showChosenLevel(level) {
  if (!level) {
    showLevelIcon(null);
    showLevelBackground(null);
    document.title = PAGE_TITLE;
    try {
      window.localStorage.removeItem('ctf_level');
    } catch (error) {
      void error;
    }
    return;
  }
  document.title = level.title + ' — ' + PAGE_TITLE;
  showLevelIcon(level.icon ?? null);
  showLevelBackground(level.background ?? null);
  try {
    window.localStorage.setItem('ctf_level', level.id);
  } catch (error) {
    void error;
  }
}

const charmElement = document.getElementById('charm');
const noteElement = document.getElementById('note');
const solvedLeadElement = document.getElementById('solved-lead');
const solvedAsideElement = document.getElementById('solved-aside');
const solvedBoardElement = document.getElementById('solved-board');
const readyProgressElement = document.getElementById('ready-progress');

let resendTimerId = 0;

function showLoginStep(id) {
  LOGIN_STEPS.forEach((step) => {
    document.getElementById(step).hidden = step !== id;
  });
  if (id !== 'step-waiting') {
    setHomeLink(id === 'step-ready');
  }
}

function showLoginMessage(text, isGood) {
  messageElement.textContent = text;
  messageElement.classList.toggle('ok', isGood === true);
}

function startResendCountdown(seconds) {
  window.clearInterval(resendTimerId);
  let remaining = seconds;
  sendCodeButton.disabled = true;
  resendTimerId = window.setInterval(() => {
    remaining -= 1;
    if (remaining <= 0) {
      window.clearInterval(resendTimerId);
      sendCodeButton.disabled = false;
      sendCodeButton.textContent = 'ارسال دوباره‌ی کد';
      return;
    }
    sendCodeButton.textContent = `ارسال دوباره تا ${remaining} ثانیه`;
  }, 1000);
}

async function requestCode() {
  showLoginMessage('');
  try {
    const payload = await api('api/otp/request', {phone: phoneInput.value});
    showLoginStep('step-code');
    codeInput.focus();
    startResendCountdown(payload.resend_after_seconds);
    showLoginMessage('کد فرستاده شد.', true);
  } catch (error) {
    showLoginMessage(error.message);
  }
}

async function verifyCode() {
  showLoginMessage('');
  try {
    const payload = await api('api/otp/verify', {phone: phoneInput.value, code: codeInput.value});
    window.clearInterval(resendTimerId);
    if (payload.needs_nickname) {
      showLoginStep('step-nickname');
      nicknameInput.focus();
      return;
    }
    await showReadyStep();
  } catch (error) {
    showLoginMessage(error.message);
  }
}

async function saveNickname() {
  showLoginMessage('');
  try {
    await api('api/nickname', {nickname: nicknameInput.value});
    await showReadyStep();
  } catch (error) {
    showLoginMessage(error.message);
  }
}

const COUNTDOWN_SEGMENTS = {
  0: 'ABCDEF', 1: 'BC', 2: 'ABGED', 3: 'ABGCD', 4: 'FBGC',
  5: 'AFGCD', 6: 'AFGEDC', 7: 'ABC', 8: 'ABCDEFG', 9: 'ABCDFG',
};

function digitRows(digit) {
  const segments = COUNTDOWN_SEGMENTS[digit];
  const has = (segment) => segments.includes(segment);
  const span = '─'.repeat(3);
  const bar = (present, left, right) => (present ? left + span + right : '     ');
  const middle = has('G')
    ? (has('F') && has('E') ? '├' : has('F') ? '╰' : has('E') ? '╭' : '─') + span +
      (has('B') && has('C') ? '┤' : has('B') ? '╯' : has('C') ? '╮' : '─')
    : (has('F') || has('E') ? '│' : ' ') + '   ' + (has('B') || has('C') ? '│' : ' ');
  return [
    bar(has('A'), has('F') ? '╭' : '─', has('B') ? '╮' : '─'),
    (has('F') ? '│' : ' ') + '   ' + (has('B') ? '│' : ' '),
    middle,
    (has('E') ? '│' : ' ') + '   ' + (has('C') ? '│' : ' '),
    bar(has('D'), has('E') ? '╰' : '─', has('C') ? '╯' : '─'),
  ];
}

function drawNumber(value) {
  const digits = String(value).padStart(2, '0').split('').map((digit) => digitRows(Number(digit)));
  return [0, 1, 2, 3, 4].map((row) => digits.map((glyph) => glyph[row]).join(' ')).join('\n');
}

function stopCountdown() {
  window.clearInterval(countdownTimerId);
  countdownTimerId = 0;
  countdownElement.hidden = true;
}

function startCountdown(seconds, opensAt) {
  secondsLeft = seconds;
  window.clearInterval(countdownTimerId);
  countdownElement.hidden = false;
  const when = new Intl.DateTimeFormat('fa-IR', {
    timeZone: 'Asia/Tehran',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).formatToParts(new Date(opensAt));
  const part = (name) => (when.find((piece) => piece.type === name) || {value: ''}).value;
  countdownWhenElement.textContent =
    `${part('day')} ${part('month')} ${part('year')} — ساعت ${part('hour')}:${part('minute')}`;
  const draw = () => {
    if (secondsLeft <= 0) {
      window.clearInterval(countdownTimerId);
      window.location.reload();
      return;
    }
    countdownUnits.days.textContent = drawNumber(Math.floor(secondsLeft / 86400));
    countdownUnits.hours.textContent = drawNumber(Math.floor((secondsLeft % 86400) / 3600));
    countdownUnits.minutes.textContent = drawNumber(Math.floor((secondsLeft % 3600) / 60));
    countdownUnits.seconds.textContent = drawNumber(secondsLeft % 60);
    secondsLeft -= 1;
  };
  draw();
  countdownTimerId = window.setInterval(draw, 1000);
}

async function renderReadyPanel() {
  const player = await api('api/me');
  readyNicknameElement.textContent = player.nickname;
  const status = await api('api/status' + chosenLevelQuery());
  rememberState({
    step: 'step-ready',
    nickname: player.nickname,
    started: status.started,
    opensAt: status.opens_at,
  });
  showChosenLevel(status.level);
  charmElement.textContent = status.charm ?? '';
  noteElement.textContent = status.note ?? '';
  if (!status.started) {
    startCountdown(status.seconds_left, status.opens_at);
    readyUnsolvedElement.hidden = true;
    readySolvedElement.hidden = true;
    return;
  }
  stopCountdown();
  panelLeadElement.textContent = status.panel.lead;
  panelAnswerElement.textContent = status.panel.answer;
  panelCallElement.textContent = status.panel.call;
  panelAsideElement.textContent = status.panel.aside;
  const hasSolvedSomething = player.solved.length > 0;
  readyUnsolvedElement.hidden = hasSolvedSomething;
  readySolvedElement.hidden = !hasSolvedSomething;
  if (!hasSolvedSomething || !status.solved) {
    return;
  }
  solvedLeadElement.textContent = status.solved.lead;
  readyProgressElement.textContent = status.solved.progress;
  solvedAsideElement.textContent = status.solved.aside;
  solvedBoardElement.textContent = status.solved.board;
}

async function showReadyStep() {
  await renderReadyPanel();
  showLoginStep('step-ready');
  showLoginMessage('وارد شدی.', true);
}

// drawRemembered puts the page back the way this browser last saw it, before the server is asked
// anything. Somebody reloading is almost always the same person as a moment ago, so painting the login
// form and taking it back is wrong far more often than it is right. Everything drawn here is provisional
// and the server's answer replaces it.
function drawRemembered() {
  const remembered = rememberedState();
  if (remembered === null || !LOGIN_STEPS.includes(remembered.step)) {
    return;
  }
  if (remembered.step === 'step-ready') {
    readyNicknameElement.textContent = remembered.nickname ?? '';
    if (remembered.started === false && remembered.opensAt) {
      const secondsLeft = Math.max(0, Math.floor((new Date(remembered.opensAt) - new Date()) / 1000));
      startCountdown(secondsLeft, remembered.opensAt);
    }
  }
  showLoginStep(remembered.step);
}

async function restoreSession() {
  try {
    const player = await api('api/me');
    if (player.nickname === '') {
      rememberState({step: 'step-nickname'});
      showLoginStep('step-nickname');
      return;
    }
    await renderReadyPanel();
    showLoginStep('step-ready');
  } catch (error) {
    forgetState();
    stopCountdown();
    showLoginStep('step-phone');
  }
}

sendCodeButton.addEventListener('click', requestCode);
verifyCodeButton.addEventListener('click', verifyCode);
saveNicknameButton.addEventListener('click', saveNickname);
changePhoneButton.addEventListener('click', () => {
  window.clearInterval(resendTimerId);
  sendCodeButton.disabled = false;
  sendCodeButton.textContent = 'ارسال کد';
  showLoginStep('step-phone');
  showLoginMessage('');
});
logoutButton.addEventListener('click', async () => {
  forgetState();
  await api('api/logout', {});
  stopCountdown();
  showLoginStep('step-phone');
  showLoginMessage('خارج شدی.', true);
});
phoneInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    requestCode();
  }
});
codeInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    verifyCode();
  }
});
nicknameInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    saveNickname();
  }
});
['ctf:solved', 'ctf:selected'].forEach((name) => {
  window.addEventListener(name, () => {
    renderReadyPanel().catch(() => {});
  });
});
drawRemembered();
restoreSession();
