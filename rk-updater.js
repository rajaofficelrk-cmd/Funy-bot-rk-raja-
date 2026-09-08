// rk-updater.js
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { execSync } = require("child_process");

// ===============================
// RK RAJA AUTO UPDATER
// ===============================

const CONFIG = {
    owner: "RK-Raja",
    repo: "YOUR-REPOSITORY",
    branch: "main",
    versionFile: "versions.json",
    backupDir: ".rk-backups"
};

const ROOT = process.cwd();

const VERSION_URL =
    `https://raw.githubusercontent.com/${CONFIG.owner}/${CONFIG.repo}/${CONFIG.branch}/${CONFIG.versionFile}`;

const FILE_URL =
    `https://raw.githubusercontent.com/${CONFIG.owner}/${CONFIG.repo}/${CONFIG.branch}/`;

function log(type, message) {
    console.log(`[RK-RAJA][${type}] ${message}`);
}

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function getLocalVersion() {
    const packageFile = path.join(ROOT, "package.json");

    if (!fs.existsSync(packageFile)) {
        throw new Error("package.json nahi mila.");
    }

    const pkg = JSON.parse(
        fs.readFileSync(packageFile, "utf8")
    );

    return pkg.version || "0.0.0";
}

function backupFile(file, backupDir) {
    const source = path.join(ROOT, file);
    const target = path.join(backupDir, file);

    if (!fs.existsSync(source)) return;

    ensureDir(path.dirname(target));
    fs.copyFileSync(source, target);
}

async function downloadFile(file) {
    const url = FILE_URL + file;

    const response = await axios.get(url, {
        responseType: "arraybuffer",
        timeout: 30000
    });

    const target = path.join(ROOT, file);

    ensureDir(path.dirname(target));

    fs.writeFileSync(target, Buffer.from(response.data));
}

async function checkUpdate() {
    log("INFO", "RK Raja updater start...");

    const currentVersion = getLocalVersion();

    log("INFO", `Current version: ${currentVersion}`);

    const response = await axios.get(VERSION_URL, {
        timeout: 15000
    });

    const versions = response.data;

    if (!Array.isArray(versions) || versions.length === 0) {
        throw new Error("versions.json ka format invalid hai.");
    }

    const index = versions.findIndex(
        v => v.version === currentVersion
    );

    if (index === -1) {
        log(
            "WARN",
            "Current version versions.json me nahi mili."
        );
        return;
    }

    const updates = versions.slice(index + 1);

    if (updates.length === 0) {
        log("OK", "Already latest version hai.");
        return;
    }

    const latest = updates[updates.length - 1];

    log(
        "UPDATE",
        `New version available: ${latest.version}`
    );

    const backupDir = path.join(
        ROOT,
        CONFIG.backupDir,
        Date.now().toString()
    );

    ensureDir(backupDir);

    for (const update of updates) {
        if (!update.files) continue;

        for (const file of Object.keys(update.files)) {
            try {
                backupFile(file, backupDir);

                log("DOWNLOAD", file);

                await downloadFile(file);

                log("OK", `${file} updated`);
            } catch (error) {
                log(
                    "ERROR",
                    `${file}: ${error.message}`
                );
            }
        }

        if (Array.isArray(update.deleteFiles)) {
            for (const file of update.deleteFiles) {
                const target = path.join(ROOT, file);

                if (fs.existsSync(target)) {
                    fs.rmSync(target, {
                        recursive: true,
                        force: true
                    });

                    log("DELETE", file);
                }
            }
        }
    }

    // Dependency reinstall
    const reinstall =
        updates.some(
            u => u.reinstallDependencies === true
        );

    if (reinstall) {
        log("NPM", "Installing dependencies...");

        execSync("npm install", {
            cwd: ROOT,
            stdio: "inherit"
        });
    }

    log(
        "SUCCESS",
        `RK Raja update complete: ${latest.version}`
    );

    log(
        "BACKUP",
        `Backup saved: ${backupDir}`
    );
}

checkUpdate().catch(error => {
    log("FATAL", error.message);
    process.exitCode = 1;
});
