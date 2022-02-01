import sqlite3
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
import toml


def create_db(path, schema):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(schema)

    def close_db():
        conn.commit()
        conn.close()

    return cur, close_db


def create_apkg(deck, write_to):
    with ZipFile(write_to, "w") as zip, NamedTemporaryFile() as tmp_file:
        cursor, close_db = create_db(tmp_file.name, open("./anki_schema.sql").read())
        insert_data(deck, cursor)
        close_db()

        zip.write(tmp_file.name, "collection.anki21")


def insert_data(deck, cursor):
    cursor.executemany(
        "INSERT INTO notes(guid, flds) VALUES (?, ?);",
        (
            (card["id"], "\x1F".join([card["back"], card["front"]]))
            for card in deck["cards"]
        ),
    )


if __name__ == "__main__":
    # python3 toml_to_apkg.py <toml deck> <path to write apkg file to>
    import sys
    from pathlib import Path

    write_to = (
        Path(sys.argv[1]).with_suffix("") + ".toml"
        if len(sys.argv) < 3
        else sys.argv[2]
    )
    if Path(write_to).exists():
        print(write_to + " exists")
        sys.exit()
    deck = toml.load(open(sys.argv[1]))
    create_apkg(deck, write_to)
