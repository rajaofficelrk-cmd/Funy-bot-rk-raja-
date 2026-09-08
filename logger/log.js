const chalk = require("chalk");

const APP_NAME = "RK Raja";

function styledLog({
  prefix = "🔷",
  label = APP_NAME,
  suffix = "🔷",
  color = "#33ffc9",
  msg,
}) {
  const time = new Date().toLocaleTimeString();

  console.log(
    chalk.bold.hex(color)(
      `${prefix} [ ${label} ] [ ${time} ] » ${msg} ${suffix}`
    )
  );
}

function logger(msg, type = "info") {
  switch (String(type).toLowerCase()) {
    case "warn":
      styledLog({
        prefix: "⚠️",
        label: APP_NAME,
        suffix: "⚠️",
        color: "#FFD700",
        msg,
      });
      break;

    case "error":
      styledLog({
        prefix: "❌",
        label: APP_NAME,
        suffix: "❌",
        color: "#FF3333",
        msg,
      });
      break;

    case "success":
      styledLog({
        prefix: "✅",
        label: APP_NAME,
        suffix: "✅",
        color: "#00FF7F",
        msg,
      });
      break;

    case "load":
      styledLog({
        prefix: "🔄",
        label: `${APP_NAME} Loader`,
        suffix: "🔄",
        color: "#00CED1",
        msg,
      });
      break;

    case "ready":
      styledLog({
        prefix: "🟢",
        label: `${APP_NAME} Ready`,
        suffix: "🟢",
        color: "#00FF7F",
        msg,
      });
      break;

    case "debug":
      styledLog({
        prefix: "🐛",
        label: `${APP_NAME} Debug`,
        suffix: "🐛",
        color: "#9370DB",
        msg,
      });
      break;

    case "cmd":
    case "command":
      styledLog({
        prefix: "⚡",
        label: `${APP_NAME} CMD`,
        suffix: "⚡",
        color: "#FF8C00",
        msg,
      });
      break;

    case "db":
    case "database":
      styledLog({
        prefix: "🗄️",
        label: `${APP_NAME} DB`,
        suffix: "🗄️",
        color: "#00BFFF",
        msg,
      });
      break;

    default:
      styledLog({
        prefix: "ℹ️",
        label: APP_NAME,
        suffix: "ℹ️",
        color: "#00BFFF",
        msg,
      });
  }
}

module.exports = logger;

// Loader shortcut
module.exports.loader = (msg, type = "info") => {
  logger(msg, type);
};

// Extra shortcuts
module.exports.info = (msg) => logger(msg, "info");
module.exports.warn = (msg) => logger(msg, "warn");
module.exports.error = (msg) => logger(msg, "error");
module.exports.success = (msg) => logger(msg, "success");
module.exports.load = (msg) => logger(msg, "load");
module.exports.ready = (msg) => logger(msg, "ready");
module.exports.debug = (msg) => logger(msg, "debug");
module.exports.cmd = (msg) => logger(msg, "command");
module.exports.db = (msg) => logger(msg, "database");
