import random

NORMAL = "abcdefghijklmnopqrstuvwxyz"

BOLD = "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"

ITALIC = "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧"

DOUBLE = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"

MONO = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"


def translate(text, style):

    result = []

    for char in text:

        lower = char.lower()

        if lower in NORMAL:

            index = NORMAL.index(lower)

            replacement = style[index]

            if char.isupper():
                replacement = replacement.upper()

            result.append(replacement)

        else:
            result.append(char)

    return "".join(result)


def stylish_text(text):

    style = random.choice([
        BOLD,
        ITALIC,
        DOUBLE,
        MONO
    ])

    return translate(
        text,
        style
    )
