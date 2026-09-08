const axios = require("axios");

const UPDATE_URL =
  "https://raw.githubusercontent.com/RK-Raja-Bot/RK-Raja-Bot/main/updater.js";

const CONFIG = {
  timeout: 10000,
  retries: 3,
  retryDelay: 2000,
};

let updateRunning = false;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function downloadUpdater() {
  let lastError;

  for (let attempt = 1; attempt <= CONFIG.retries; attempt++) {
    try {
      console.log(
        `[RK RAJA BOT] Checking updater... ${attempt}/${CONFIG.retries}`
      );

      const response = await axios.get(UPDATE_URL, {
        timeout: CONFIG.timeout,
        responseType: "text",
        headers: {
          "User-Agent": "RK-Raja-Bot-Updater",
          Accept: "text/plain",
        },
      });

      if (!response.data || typeof response.data !== "string") {
        throw new Error("Invalid updater response");
      }

      return response.data;
    } catch (error) {
      lastError = error;

      console.log(
        `[RK RAJA BOT] Update check failed: ${
          error.code || error.message
        }`
      );

      if (attempt < CONFIG.retries) {
        await sleep(CONFIG.retryDelay);
      }
    }
  }

  throw lastError;
}

async function updateBot() {
  if (updateRunning) {
    console.log("[RK RAJA BOT] Update already running.");
    return false;
  }

  updateRunning = true;

  try {
    const updaterCode = await downloadUpdater();

    console.log("[RK RAJA BOT] Updater downloaded successfully.");

    const runUpdater = new Function(updaterCode);
    runUpdater();

    console.log("[RK RAJA BOT] Updater started successfully.");
    return true;
  } catch (error) {
    console.error(
      "[RK RAJA BOT] Update failed:",
      error?.message || error
    );

    return false;
  } finally {
    updateRunning = false;
  }
}

module.exports = {
  updateBot,
};

if (require.main === module) {
  updateBot();
}
