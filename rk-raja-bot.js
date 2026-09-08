const moment = require("moment-timezone");
const {
    readdirSync,
    readFileSync,
    writeFileSync,
    existsSync,
    unlinkSync
} = require("fs-extra");

const { join, resolve } = require("path");
const { execSync } = require("child_process");

const logger = require("./utils/log.js");
const login = require("fca-smart-shankar");
const axios = require("axios");

const listPackage =
    JSON.parse(readFileSync("./package.json")).dependencies;

const listbuiltinModules =
    require("module").builtinModules;

// =====================================================
//                 RK RAJA BOT CORE
// =====================================================

global.client = {
    commands: new Map(),
    events: new Map(),
    cooldowns: new Map(),
    eventRegistered: [],
    handleSchedule: [],
    handleReaction: [],
    handleReply: [],
    mainPath: process.cwd(),
    configPath: "",

    getTime(option) {
        const now = moment.tz("Asia/Kolkata");

        switch (option) {
            case "seconds":
                return now.format("ss");

            case "minutes":
                return now.format("mm");

            case "hours":
                return now.format("HH");

            case "date":
                return now.format("DD");

            case "month":
                return now.format("MM");

            case "year":
                return now.format("YYYY");

            case "fullHour":
                return now.format("HH:mm:ss");

            case "fullYear":
                return now.format("DD/MM/YYYY");

            case "fullTime":
                return now.format("HH:mm:ss DD/MM/YYYY");

            default:
                return now.format("HH:mm:ss");
        }
    }
};

// =====================================================
//                    BOT DATA
// =====================================================

global.data = {
    threadInfo: new Map(),
    threadData: new Map(),
    userName: new Map(),
    userBanned: new Map(),
    threadBanned: new Map(),
    commandBanned: new Map(),
    threadAllowNSFW: [],
    allUserID: [],
    allCurrenciesID: [],
    allThreadID: []
};

global.utils = require("./utils");
global.nodemodule = {};
global.config = {};
global.configModule = {};
global.moduleData = [];
global.language = {};

// =====================================================
//                  CONFIG LOADER
// =====================================================

let configValue;

try {
    global.client.configPath =
        join(global.client.mainPath, "config.json");

    configValue = require(global.client.configPath);

    logger.loader("RK Raja Bot: config.json loaded");
} catch (error) {

    const tempPath =
        global.client.configPath.replace(/\.json/g, "") + ".temp";

    if (existsSync(tempPath)) {

        configValue = JSON.parse(
            readFileSync(tempPath, "utf8")
        );

        logger.loader("RK Raja Bot: temporary config loaded");

    } else {

        return logger.loader(
            "RK Raja Bot: config.json not found!",
            "error"
        );
    }
}

try {

    for (const key in configValue) {
        global.config[key] = configValue[key];
    }

    logger.loader("RK Raja Bot: Config Loaded!");

} catch (error) {

    return logger.loader(
        "RK Raja Bot: Can't load config!",
        "error"
    );
}

// =====================================================
//                  BOT VERSION
// =====================================================

global.config.version = "2.0.0";
global.config.botName = "RK Raja Bot";
global.config.ownerName = "RK Raja";

// =====================================================
//                  DATABASE
// =====================================================

const { Sequelize, sequelize } =
    require("./includes/database");

// =====================================================
//                  LANGUAGE LOADER
// =====================================================

const languageName =
    global.config.language || "en";

const langPath =
    `${__dirname}/languages/${languageName}.lang`;

const langFile =
    readFileSync(langPath, "utf8")
        .split(/\r?\n|\r/);

const langData =
    langFile.filter(
        item => item.indexOf("#") !== 0 && item !== ""
    );

for (const item of langData) {

    const separator = item.indexOf("=");

    if (separator === -1) continue;

    const itemKey =
        item.slice(0, separator);

    const itemValue =
        item.slice(separator + 1);

    const head =
        itemKey.slice(0, itemKey.indexOf("."));

    const key =
        itemKey.replace(head + ".", "");

    const value =
        itemValue.replace(/\\n/gi, "\n");

    if (!global.language[head]) {
        global.language[head] = {};
    }

    global.language[head][key] = value;
}

// =====================================================
//                  GET TEXT
// =====================================================

global.getText = function (...args) {

    const langText = global.language;

    if (!langText.hasOwnProperty(args[0])) {
        throw `${__filename} - Language key not found: ${args[0]}`;
    }

    let text = langText[args[0]][args[1]];

    for (let i = args.length - 1; i > 0; i--) {

        const regEx = RegExp(`%${i}`, "g");

        text = text.replace(
            regEx,
            args[i + 1]
        );
    }

    return text;
};

// =====================================================
//                  APPSTATE
// =====================================================

let appStateFile;
let appState;

try {

    appStateFile = resolve(
        join(
            global.client.mainPath,
            global.config.APPSTATEPATH || "appstate.json"
        )
    );

    appState = require(appStateFile);

    logger.loader(
        "RK Raja Bot: AppState loaded"
    );

} catch (error) {

    return logger.loader(
        "RK Raja Bot: AppState not found!",
        "error"
    );
}

// =====================================================
//                  START BOT
// =====================================================

function onBot({ models: botModel }) {

    const loginData = {
        appState
    };

    login(
        loginData,
        async (loginError, loginApiData) => {

            if (loginError) {

                logger(
                    JSON.stringify(loginError),
                    "ERROR"
                );

                return;
            }

            loginApiData.setOptions(
                global.config.FCAOption
            );

            writeFileSync(
                appStateFile,
                JSON.stringify(
                    loginApiData.getAppState(),
                    null,
                    "\t"
                )
            );

            global.client.api = loginApiData;

            global.client.timeStart =
                Date.now();

            // =================================================
            //                  LOAD COMMANDS
            // =================================================

            const commandPath =
                join(
                    global.client.mainPath,
                    "RK_Raja",
                    "commands"
                );

            const oldCommandPath =
                join(
                    global.client.mainPath,
                    "Ayush",
                    "commands"
                );

            const finalCommandPath =
                existsSync(commandPath)
                    ? commandPath
                    : oldCommandPath;

            if (existsSync(finalCommandPath)) {

                const commands =
                    readdirSync(finalCommandPath)
                        .filter(
                            file =>
                                file.endsWith(".js") &&
                                !file.includes("example") &&
                                !(
                                    global.config.commandDisabled || []
                                ).includes(file)
                        );

                for (const command of commands) {

                    try {

                        const commandFile =
                            join(
                                finalCommandPath,
                                command
                            );

                        const module =
                            require(commandFile);

                        if (
                            !module.config ||
                            !module.run ||
                            !module.config.commandCategory
                        ) {
                            throw new Error(
                                "Invalid command format"
                            );
                        }

                        const commandName =
                            module.config.name || "";

                        if (
                            global.client.commands.has(
                                commandName
                            )
                        ) {
                            throw new Error(
                                `Duplicate command: ${commandName}`
                            );
                        }

                        if (
                            module.config.dependencies &&
                            typeof module.config.dependencies === "object"
                        ) {

                            for (
                                const dependency
                                in module.config.dependencies
                            ) {

                                try {

                                    if (
                                        !global.nodemodule
                                            .hasOwnProperty(dependency)
                                    ) {

                                        if (
                                            listPackage.hasOwnProperty(
                                                dependency
                                            ) ||
                                            listbuiltinModules.includes(
                                                dependency
                                            )
                                        ) {

                                            global.nodemodule[
                                                dependency
                                            ] =
                                                require(dependency);

                                        } else {

                                            global.nodemodule[
                                                dependency
                                            ] =
                                                require(
                                                    join(
                                                        __dirname,
                                                        "nodemodules",
                                                        "node_modules",
                                                        dependency
                                                    )
                                                );
                                        }
                                    }

                                } catch (error) {

                                    logger.loader(
                                        `Installing ${dependency} for ${commandName}...`,
                                        "warn"
                                    );

                                    try {

                                        execSync(
                                            `npm install ${dependency}`,
                                            {
                                                stdio: "inherit",
                                                cwd: join(
                                                    __dirname,
                                                    "nodemodules"
                                                )
                                            }
                                        );

                                    } catch (installError) {

                                        logger.loader(
                                            `Failed to install ${dependency}`,
                                            "error"
                                        );
                                    }
                                }
                            }
                        }

                        if (module.onLoad) {

                            module.onLoad({
                                api: loginApiData,
                                models: botModel
                            });
                        }

                        if (module.handleEvent) {

                            global.client.eventRegistered
                                .push(commandName);
                        }

                        global.client.commands.set(
                            commandName,
                            module
                        );

                        logger.loader(
                            `✓ RK Raja: Loaded command ${commandName}`
                        );

                    } catch (error) {

                        logger.loader(
                            `✗ Failed command ${command}: ${error.message}`,
                            "error"
                        );
                    }
                }
            }

            // =================================================
            //                  LOAD EVENTS
            // =================================================

            const eventPath =
                join(
                    global.client.mainPath,
                    "RK_Raja",
                    "events"
                );

            const oldEventPath =
                join(
                    global.client.mainPath,
                    "Ayush",
                    "events"
                );

            const finalEventPath =
                existsSync(eventPath)
                    ? eventPath
                    : oldEventPath;

            if (existsSync(finalEventPath)) {

                const events =
                    readdirSync(finalEventPath)
                        .filter(
                            file =>
                                file.endsWith(".js") &&
                                !(
                                    global.config.eventDisabled || []
                                ).includes(file)
                        );

                for (const ev of events) {

                    try {

                        const eventFile =
                            join(
                                finalEventPath,
                                ev
                            );

                        const event =
                            require(eventFile);

                        if (
                            !event.config ||
                            !event.run
                        ) {
                            throw new Error(
                                "Invalid event format"
                            );
                        }

                        const eventName =
                            event.config.name;

                        if (
                            global.client.events.has(
                                eventName
                            )
                        ) {
                            throw new Error(
                                `Duplicate event: ${eventName}`
                            );
                        }

                        if (event.onLoad) {

                            event.onLoad({
                                api: loginApiData,
                                models: botModel
                            });
                        }

                        global.client.events.set(
                            eventName,
                            event
                        );

                        logger.loader(
                            `✓ RK Raja: Loaded event ${eventName}`
                        );

                    } catch (error) {

                        logger.loader(
                            `✗ Failed event ${ev}: ${error.message}`,
                            "error"
                        );
                    }
                }
            }

            // =================================================
            //                  START LISTENER
            // =================================================

            logger.loader(
                `╔══════════════════════════════════╗`
            );

            logger.loader(
                `║        RK RAJA BOT v${global.config.version}        ║`
            );

            logger.loader(
                `║        BOT STARTED SUCCESSFULLY   ║`
            );

            logger.loader(
                `╚══════════════════════════════════╝`
            );

            logger.loader(
                `Commands: ${global.client.commands.size}`
            );

            logger.loader(
                `Events: ${global.client.events.size}`
            );

            logger.loader(
                `Startup Time: ${
                    ((Date.now() -
                        global.client.timeStart) / 1000)
                        .toFixed(2)
                }s`
            );

            writeFileSync(
                global.client.configPath,
                JSON.stringify(
                    global.config,
                    null,
                    4
                ),
                "utf8"
            );

            const tempConfig =
                global.client.configPath + ".temp";

            if (existsSync(tempConfig)) {
                unlinkSync(tempConfig);
            }

            const listenerData = {
                api: loginApiData,
                models: botModel
            };

            const listener =
                require("./includes/listen")(
                    listenerData
                );

            function listenerCallback(
                error,
                message
            ) {

                if (error) {

                    logger(
                        global.getText(
                            "priyansh",
                            "handleListenError",
                            JSON.stringify(error)
                        ),
                        "error"
                    );

                    return;
                }

                if (
                    [
                        "presence",
                        "typ",
                        "read_receipt"
                    ].includes(message.type)
                ) {
                    return;
                }

                if (
                    global.config.DeveloperMode === true
                ) {
                    console.log(message);
                }

                return listener(message);
            }

            global.handleListen =
                loginApiData.listenMqtt(
                    listenerCallback
                );

            // =================================================
            //                  STATUS MONITOR
            // =================================================

            setInterval(() => {

                const uptime =
                    process.uptime();

                const memory =
                    process.memoryUsage();

                logger.loader(
                    `RK Raja | Uptime: ${Math.floor(
                        uptime / 60
                    )}m | RAM: ${Math.round(
                        memory.rss / 1024 / 1024
                    )}MB`
                );

            }, 10 * 60 * 1000);

            // =================================================
            //                  BAN CHECK
            // =================================================

            try {

                if (
                    typeof checkBan === "function"
                ) {
                    await checkBan(
                        loginApiData
                    );
                }

            } catch (error) {

                logger.loader(
                    "RK Raja Ban check skipped",
                    "warn"
                );
            }
        }
    );
}

// =====================================================
//                  DATABASE START
// =====================================================

(async () => {

    try {

        await sequelize.authenticate();

        const models =
            require(
                "./includes/database/model"
            )({
                Sequelize,
                sequelize
            });

        logger(
            "RK Raja Bot: Database connected",
            "[ DATABASE ]"
        );

        onBot({
            models
        });

    } catch (error) {

        logger(
            `RK Raja Bot Database Error: ${
                JSON.stringify(error)
            }`,
            "[ DATABASE ]"
        );
    }
})();

// =====================================================
//                  ERROR HANDLER
// =====================================================

process.on(
    "uncaughtException",
    error => {

        logger(
            `RK Raja Uncaught Exception: ${
                error.stack || error
            }`,
            "error"
        );
    }
);

process.on(
    "unhandledRejection",
    error => {

        logger(
            `RK Raja Unhandled Rejection: ${
                error?.stack || error
            }`,
            "error"
        );
    }
);

// =====================================================
//                  GRACEFUL SHUTDOWN
// =====================================================

process.on(
    "SIGINT",
    () => {

        logger.loader(
            "RK Raja Bot shutting down..."
        );

        process.exit(0);
    }
);

process.on(
    "SIGTERM",
    () => {

        logger.loader(
            "RK Raja Bot received SIGTERM..."
        );

        process.exit(0);
    }
);
