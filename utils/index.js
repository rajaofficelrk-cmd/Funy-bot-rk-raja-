const assets = require('@miraipr0ject/assets');
const crypto = require('crypto');
const os = require('os');

module.exports.throwError = function (command, threadID, messageID) {
    const threadSetting =
        global.data.threadData.get(parseInt(threadID)) || {};

    return global.client.api.sendMessage(
        global.getText(
            'utils',
            'throwError',
            threadSetting.hasOwnProperty('PREFIX')
                ? threadSetting.PREFIX
                : global.config.PREFIX,
            command
        ),
        threadID,
        messageID
    );
};

module.exports.cleanAnilistHTML = function (text) {
    return text
        .replace('<br>', '\n')
        .replace(/<\/?(i|em)>/g, '*')
        .replace(/<\/?b>/g, '**')
        .replace(/~!|!~/g, '||')
        .replace('&amp;', '&')
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('&quot;', '"')
        .replace('&#039;', "'");
};

module.exports.downloadFile = async function (url, path) {
    const { createWriteStream } = require('fs');
    const axios = require('axios');

    const response = await axios({
        method: 'GET',
        responseType: 'stream',
        url
    });

    const writer = createWriteStream(path);
    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
        writer.on('finish', resolve);
        writer.on('error', reject);
    });
};

module.exports.getContent = async function (url) {
    try {
        const axios = require('axios');

        const response = await axios({
            method: 'GET',
            url
        });

        return response;
    } catch (e) {
        console.log(e);
        return null;
    }
};

module.exports.randomString = function (length) {
    let result = '';
    const characters =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

    for (let i = 0; i < length; i++) {
        result += characters.charAt(
            Math.floor(Math.random() * characters.length)
        );
    }

    return result;
};

module.exports.assets = {
    async font(name) {
        if (!assets.font.loaded) {
            await assets.font.load();
        }
        return assets.font.get(name);
    },

    async image(name) {
        if (!assets.image.loaded) {
            await assets.image.load();
        }
        return assets.image.get(name);
    },

    async data(name) {
        if (!assets.data.loaded) {
            await assets.data.load();
        }
        return assets.data.get(name);
    }
};

module.exports.AES = {
    encrypt(cryptKey, cryptIv, plainData) {
        const encipher = crypto.createCipheriv(
            'aes-256-cbc',
            Buffer.from(cryptKey),
            Buffer.from(cryptIv)
        );

        let encrypted = encipher.update(plainData);
        encrypted = Buffer.concat([
            encrypted,
            encipher.final()
        ]);

        return encrypted.toString('hex');
    },

    decrypt(cryptKey, cryptIv, encrypted) {
        encrypted = Buffer.from(encrypted, 'hex');

        const decipher = crypto.createDecipheriv(
            'aes-256-cbc',
            Buffer.from(cryptKey),
            Buffer.from(cryptIv, 'binary')
        );

        let decrypted = decipher.update(encrypted);
        decrypted = Buffer.concat([
            decrypted,
            decipher.final()
        ]);

        return String(decrypted);
    },

    makeIv() {
        return Buffer.from(
            crypto.randomBytes(16)
        ).toString('hex').slice(0, 16);
    }
};

module.exports.homeDir = function () {
    let returnHome;
    let typeSystem;

    const home = process.env.HOME;
    const user =
        process.env.LOGNAME ||
        process.env.USER ||
        process.env.LNAME ||
        process.env.USERNAME;

    switch (process.platform) {
        case 'win32':
            returnHome =
                process.env.USERPROFILE ||
                process.env.HOMEDRIVE + process.env.HOMEPATH ||
                home ||
                null;
            typeSystem = 'win32';
            break;

        case 'darwin':
            returnHome =
                home || (user ? '/Users/' + user : null);
            typeSystem = 'darwin';
            break;

        case 'linux':
            returnHome =
                home ||
                (process.getuid() === 0
                    ? '/root'
                    : user
                    ? '/home/' + user
                    : null);
            typeSystem = 'linux';
            break;

        default:
            returnHome = home || null;
            typeSystem = 'unknown';
    }

    return [
        typeof os.homedir === 'function'
            ? os.homedir()
            : returnHome,
        typeSystem
    ];
};

GitHub: "index.js"
Dependencies चाहिए हों तो कम-से-कम "axios" और "@miraipr0ject/assets" package भी project में होना चाहिए।
