const fs = require("fs");
const path = require("path");

const DATA_DIR = path.join(__dirname, "..", "..", "cache");
const DATA_FILE = path.join(DATA_DIR, "autoreply.json");

function ensureStore() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(DATA_FILE)) fs.writeFileSync(DATA_FILE, JSON.stringify({ threads: {} }, null, 2));
}
function readStore() {
  ensureStore();
  try { return JSON.parse(fs.readFileSync(DATA_FILE, "utf8")); }
  catch { return { threads: {} }; }
}
function writeStore(data) {
  ensureStore();
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

module.exports.config = {
  name: "autoreplyEvent",
  version: "1.0",
  author: "you + chatgpt",
  description: "Auto-reply incoming messages",
  eventType: ["message", "message_reply"]
};

module.exports.run = async function ({ api, event }) {
  // Ignore bot's own messages to avoid loops
  try {
    if (event.senderID == api.getCurrentUserID()) return;
  } catch { /* ignore */ }

  // Only respond in group threads
  if (!event.isGroup && typeof event.threadID === "string") {
    // Optional: return; // uncomment if you want group-only
  }

  const store = readStore();
  const threadID = event.threadID;
  const cfg = store.threads[threadID];

  if (!cfg || !cfg.enabled) return;

  const now = Date.now();
  const last = cfg.last || 0;
  const delayMs = (cfg.delay || 30) * 1000;

  if (now - last < delayMs) return; // rate-limit

  const text = cfg.text || "Hello 👋";
  // Reply and update last time
  api.sendMessage(text, threadID, () => {
    cfg.last = Date.now();
    store.threads[threadID] = cfg;
    writeStore(store);
  });
};
