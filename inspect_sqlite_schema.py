from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "database.db"


def inspect_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()

    print(f"SQLite database: {DB_PATH}")
    print("\nTables found:")
    for row in tables:
        table = row["name"]
        count = cur.execute(f"SELECT COUNT(*) FROM \"{table}\"").fetchone()[0]
        print(f"- {table}: {count} rows")

    print("\nDetailed schema:")
    for row in tables:
        table = row["name"]
        print(f"\nTable: {table}")
        cols = cur.execute(f"PRAGMA table_info(\"{table}\")").fetchall()
        for col in cols:
            cid, name, ctype, notnull, dflt_value, pk = col
            print(
                f"  - {name}: {ctype} | notnull={notnull} | pk={pk} | default={dflt_value}"
            )

    conn.close()


if __name__ == "__main__":
    inspect_db()
