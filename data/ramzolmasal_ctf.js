const TITLE_STYLE = 'color:#fed82a;font-weight:bold;font-size:14px';
const MUTED_STYLE = 'color:#8b949e';
const OK_STYLE = 'color:#3fb950;font-weight:bold';
const BAD_STYLE = 'color:#f85149;font-weight:bold';

const WORDMARK = ' YEK{256} ';
const WORDMARK_STYLE = 'background:#fed82a;color:#0d1117;font-weight:bold;font-size:20px;' +
  'padding:5px 12px;border-radius:6px;letter-spacing:0.12em';


// Anything a contestant copies is printed bare. ltr() and rtl() wrap text in bidi isolates so a mixed
// line reads correctly, and those characters come along when the text is selected — into a URL bar, a
// hashing tool, or select(). A path breaks visibly. A value hashes to the wrong thing silently. Only
// runs of prose keep their isolates; values stand alone on their line and need none.
function rememberLevel(id) {
  try {
    window.localStorage.setItem('ctf_level', id);
  } catch (error) {
    void error;
  }
}

function complain(error) {
  console.log('%c✖ ' + rtl(error.message), BAD_STYLE);
}

async function printChallenges() {
  const payload = await api('api/challenges');
  const rows = {};
  payload.challenges.forEach((challenge) => {
    rows[challenge.id] = {
      'عنوان': rtl(challenge.title),
      'حل شده': challenge.solved ? '✔' : '',
    };
  });
  console.table(rows);
  console.log('%c' + rtl('برای انتخاب یک سؤال: ' + ltr('select("id")')), MUTED_STYLE);
}

function describeChallenge(challenge) {
  console.log('%c' + rtl(challenge.title), TITLE_STYLE);
  console.log('%c' + rtl(challenge.prompt), '');
  (challenge.files ?? []).forEach((file) => {
    console.log('%c' + file.url, MUTED_STYLE);
  });
  if (challenge.solved) {
    console.log('%c✔ ' + rtl('این را ساعت ' + ltr(challenge.solved_at) + ' حل کرده‌ای.'), OK_STYLE);
  }
}

async function printChosenChallenge() {
  const status = await api('api/status');
  if (!status.level) {
    return;
  }
  const payload = await api('api/challenges');
  const challenge = payload.challenges.find((candidate) => candidate.id === status.level.id);
  if (challenge === undefined) {
    return;
  }
  describeChallenge(challenge);
  rememberLevel(challenge.id);
}

async function chooseChallenge(id) {
  const payload = await api('api/challenges');
  const challenge = payload.challenges.find((candidate) => candidate.id === id);
  if (challenge === undefined) {
    console.log('%c✖ ' + rtl('سؤالی با شناسه‌ی ' + ltr(id) + ' وجود ندارد.'), BAD_STYLE);
    return;
  }
  await api('api/select', {id});
  rememberLevel(id);
  // The card is showing whichever clues were open when it was drawn. Choosing changes which ones the
  // server will hand over, so the page has to ask again — otherwise the console says one thing and the
  // page in the other tab keeps saying another until it is reloaded.
  window.dispatchEvent(new CustomEvent('ctf:selected'));
  describeChallenge(challenge);
}

async function sendFlag(flag) {
  const payload = await api('api/submit', {flag: flag});
  if (!payload.correct) {
    console.log('%c✖ ' + rtl(payload.message), BAD_STYLE);
    return;
  }
  console.log('%c✔ ' + rtl(payload.message), OK_STYLE);
  window.dispatchEvent(new CustomEvent('ctf:solved'));
  if (payload.first_solve) {
    console.log('%c' + rtl('پیدایش کردی. از اینجا به بعد این‌ها را داری:'), TITLE_STYLE);
    printHelp();
  printRule().catch(() => {});
  }
}

async function printBoard() {
  const payload = await api('api/board');
  const rows = {};
  (payload.problems || []).forEach((problem) => {
    rows[auto(problem.title)] = {'حل کرده‌اند': problem.solved_count};
  });
  console.table(rows);
}

async function printRule() {
  const status = await api('api/status');
  if (status.rule) {
    console.log('%c' + rtl(status.rule), MUTED_STYLE);
  }
}

async function printMe() {
  const payload = await api('api/me');
  console.log('%c' + (payload.nickname === '' ? rtl('بی‌نام') : auto(payload.nickname)), TITLE_STYLE);
  console.log('%c' + rtl('شماره: ' + ltr(payload.masked_phone) +
    ' · حل‌شده: ' + payload.solved.length), MUTED_STYLE);
  console.log('%c' + rtl('شناسه‌ی تو:') + ' ' + payload.id, MUTED_STYLE);
}

function printHelp() {
  console.log('%c' + rtl('دستورهای مسابقه'), TITLE_STYLE);
  const commands = [
    ['puzzles()', 'فهرست سؤال‌ها'],
    ['select("id")', 'انتخاب یک سؤال؛ از آن به بعد سرنخ‌ها مال همان است'],
    ['submit("YEK{...}")', 'ارسال پرچم برای سؤالی که انتخاب کرده‌ای'],
    ['board()', 'جدول مرحله‌ها'],
    ['me()', 'وضعیت خودت'],
    ['help()', 'همین جدول'],
  ];
  const rows = {};
  commands.forEach(([command, description]) => {
    rows[command] = {'کار': rtl(description)};
  });
  console.table(rows);
  console.log('%c' + rtl('پاسخ هر دستور چند لحظه بعد، پایین‌تر چاپ می‌شود.'), MUTED_STYLE);
}

function printBanner() {
  console.log('%c' + WORDMARK, WORDMARK_STYLE);
  console.log('%c' + rtl('مسابقه‌ی روز برنامه‌نویس — یکتانت'), TITLE_STYLE);
  console.log('%c' + rtl('روز ۲۵۶ام سال. چون یک بایت همین‌قدر جا دارد.'), MUTED_STYLE);
}

function puzzles() {
  printChallenges().catch(complain);
  return rtl('در حال گرفتن فهرست سؤال‌ها…');
}

function select(id) {
  chooseChallenge(id).catch(complain);
  return rtl('در حال باز کردن سؤال…');
}

function submit(flag) {
  if (typeof flag !== 'string' || flag.trim() === '') {
    return rtl('پرچم را به صورت رشته بده: ' + ltr('submit("YEK{...}")'));
  }
  if (flag.includes('object Promise')) {
    return rtl('نتیجه هنوز آماده نشده. اول بگیرش، بعد بفرست.');
  }
  sendFlag(flag.trim()).catch(complain);
  return rtl('در حال ارسال…');
}

function board() {
  printBoard().catch(complain);
  return rtl('در حال گرفتن جدول…');
}

function me() {
  printMe().catch(complain);
  return rtl('در حال گرفتن وضعیت…');
}

function help() {
  printHelp();
  return rtl('راهنما بالا چاپ شد.');
}

async function hash(input) {
  const bytes = typeof input === 'string' ? new TextEncoder().encode(input) : Uint8Array.from(input);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  const hex = Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, '0'))
    .join('');
  console.log('%c' + hex, OK_STYLE);
  return hex;
}

async function khord(input) {
  const bytes = typeof input === 'string' ? new TextEncoder().encode(input) : Uint8Array.from(await input);
  const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  console.log('%c' + Array.from(digest).map((byte) => byte.toString(16).padStart(2, '0')).join(''), OK_STYLE);
  return digest;
}

async function setabr(input) {
  const value = await input;
  const bytes = typeof value === 'string' ? new TextEncoder().encode(value) : Uint8Array.from(value);
  const base64 = btoa(Array.from(bytes).map((byte) => String.fromCharCode(byte)).join(''));
  console.log('%c' + base64, OK_STYLE);
  return base64;
}

async function bytesOf(input) {
  const value = await input;
  if (typeof value === 'string') {
    return new TextEncoder().encode(value);
  }
  if (Object.prototype.toString.call(value) === '[object ArrayBuffer]') {
    return new Uint8Array(value);
  }
  if (ArrayBuffer.isView(value)) {
    return new Uint8Array(value.buffer, value.byteOffset, value.byteLength);
  }
  if (value && typeof value.arrayBuffer === 'function') {
    return new Uint8Array(await value.arrayBuffer());
  }
  return Uint8Array.from(value);
}

async function xor(first, second) {
  const [left, right] = await Promise.all([bytesOf(first), bytesOf(second)]);
  const joined = new Uint8Array(Math.min(left.length, right.length));
  for (let index = 0; index < joined.length; index++) {
    joined[index] = left[index] ^ right[index];
  }
  console.log('%c' + new TextDecoder().decode(joined), OK_STYLE);
  return joined;
}

window.ctf = {puzzles, select, submit, board, me, help, hash, khord, setabr, xor};
printBanner();
printChosenChallenge().catch(() => {});
