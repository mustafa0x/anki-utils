import toml
import tempfile
import sqlite3
import re
from zipfile import ZipFile
from time import time

write_toml = lambda path, data: open(path, "w").write(toml.dumps(data))


def apply_repls(text, repls):
    for r in repls:
        text = re.sub(r[1], r[2], text) if r[0] else text.replace(r[1], r[2])
    return text


def generate_id():
    import string
    import random

    return "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits + "_")
        for _ in range(10)
    )


def clean_side(side):
    return apply_repls(
        side,
        [
            (0, "<br>", "\n"),
            (0, "<p>✽✽✽✽✽✽✽</p>", "\n✽✽✽✽✽✽✽\n"),
            (1, r"[  ]+", " "),
            (1, r"[\u200D\u200C]", ""),
            (1, r"</?(span|p|span class=\"indent\")>", ""),
        ],
    )


def export_apkg(apkg_path):
    tmpdir = tempfile.TemporaryDirectory()

    archive = ZipFile(apkg_path)
    collection_name = "collection.anki21"
    try:
        archive.getinfo(collection_name).filename
    except KeyError:
        collection_name = "collection.anki2"

    db_path = archive.extract(collection_name, tmpdir.name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cards = []
    for row in cursor.execute("SELECT guid, flds FROM notes"):
        cards.append((row[0], row[1].split("\x1F")))

    data = {
        "id": generate_id(),
        "meta": {
            "name": "",
            "desc": "",
            "created": round(time() * 1000),
        },
    }
    data["cards"] = [
        dict(id=card[0], front=clean_side(card[1][1]), back=clean_side(card[1][0]))
        for card in cards
    ]

    return data


if __name__ == "__main__":
    # python3 apkg_to_toml.py <apkg file> <path to write toml file to>
    import sys
    from pathlib import Path

    write_to = (
        f"{Path(sys.argv[1]).with_suffix('')}.toml"
        if len(sys.argv) < 3
        else sys.argv[2]
    )
    if Path(write_to).exists():
        print(write_to + " exists")
        sys.exit()

    write_toml(write_to, export_apkg(sys.argv[1]))
