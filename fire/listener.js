#!/usr/bin/env node
/**
 * Seventh River: FIRE listener
 *
 * Listens on localhost:9999 for simple spike messages (e.g. "fire\n").
 * Designed to be triggered by udev rules on Linux/NixOS:
 *   echo fire | nc localhost 9999
 *
 * Behavior on receiving a line:
 * - prints an ANSI-highlighted line to stdout
 * - appends a timestamped entry to the current daily memory file (if present)
 *
 * No network calls, no external side effects beyond local file append.
 */

const net = require('net');
const fs = require('fs');
const path = require('path');

const HOST = process.env.FIRE_HOST || '127.0.0.1';
const PORT = Number(process.env.FIRE_PORT || 9999);

const workspace = process.env.OPENCLAW_WORKSPACE || path.resolve(process.cwd());
const memoryDir = path.join(workspace, 'memory');

function isoLocal(d = new Date()) {
  // human-friendly local timestamp
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function todayFile() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const name = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}.md`;
  return path.join(memoryDir, name);
}

function ensureFireSection(filePath) {
  if (!fs.existsSync(filePath)) return false;
  const txt = fs.readFileSync(filePath, 'utf8');
  if (txt.includes('## Fire spikes')) return true;
  fs.appendFileSync(filePath, `\n## Fire spikes\n\n`, 'utf8');
  return true;
}

function appendFire(msg) {
  try {
    if (!fs.existsSync(memoryDir)) return;
    const file = todayFile();
    if (!fs.existsSync(file)) return;
    ensureFireSection(file);
    fs.appendFileSync(file, `- ${isoLocal()} — ${msg}\n`, 'utf8');
  } catch (e) {
    // swallow to keep listener alive
  }
}

function color(s, code) { return `\x1b[${code}m${s}\x1b[0m`; }

const server = net.createServer((socket) => {
  socket.setEncoding('utf8');
  let buf = '';

  socket.on('data', (chunk) => {
    buf += chunk;
    let idx;
    while ((idx = buf.indexOf('\n')) >= 0) {
      const line = buf.slice(0, idx).trim();
      buf = buf.slice(idx + 1);
      if (!line) continue;

      const stamp = isoLocal();
      const isFire = line.toLowerCase() === 'fire';
      const label = isFire ? color('FIRE', '38;2;40;240;255') : color('SIGNAL', '38;2;65;105;225');

      process.stdout.write(`${color(stamp, '2')}  ${label}  ${line}\n`);

      if (isFire) appendFire('fire');
      else appendFire(line);
    }
  });

  socket.on('error', () => {});
});

server.on('error', (err) => {
  console.error(`Listener error: ${err.message}`);
  process.exitCode = 1;
});

server.listen(PORT, HOST, () => {
  console.log(`Seventh River FIRE listener: listening on ${HOST}:${PORT}`);
  console.log(`Workspace: ${workspace}`);
  console.log(`Daily log (if present): ${todayFile()}`);
});
