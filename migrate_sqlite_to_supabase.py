from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from supabase import create_client


USERS_SCHEMA_SQL = """
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS xp INTEGER DEFAULT 0;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS level INTEGER DEFAULT 1;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS streak INTEGER DEFAULT 0;
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS preparedness_level TEXT DEFAULT 'Beginner';
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS profile_photo TEXT;
"""


def build_payload_for_remote_columns(row: dict[str, Any], available_columns: set[str]) -> dict[str, Any]:
    """Return only the columns that are present in the remote Supabase table."""
    return {key: value for key, value in row.items() if key in available_columns}

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
DB_PATH = BASE_DIR / "database.db"


def load_env() -> tuple[str, str]:
    load_dotenv(dotenv_path=ENV_FILE, override=True)

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url:
        raise RuntimeError(f"SUPABASE_URL was not loaded from {ENV_FILE}")
    if not supabase_key:
        raise RuntimeError(f"SUPABASE_KEY was not loaded from {ENV_FILE}")

    return supabase_url, supabase_key


def get_sqlite_tables() -> list[dict[str, Any]]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()

    inventory: list[dict[str, Any]] = []
    for row in tables:
        table = row["name"]
        count = cur.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()

        inventory.append(
            {
                "name": table,
                "row_count": count,
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "notnull": col[3],
                        "default": col[4],
                        "pk": col[5],
                    }
                    for col in columns
                ],
            }
        )

    conn.close()
    return inventory


def print_sqlite_inventory(inventory: list[dict[str, Any]]) -> None:
    print("SQLite inspection summary")
    print("=" * 80)
    for entry in inventory:
        print(f"- {entry['name']}: {entry['row_count']} rows")

    print("\nSchema details:")
    for entry in inventory:
        print(f"\nTable: {entry['name']}")
        for col in entry["columns"]:
            print(
                "  - {name}: {type} | notnull={notnull} | pk={pk} | default={default}".format(
                    **col
                )
            )


def compare_with_supabase(supabase, inventory: list[dict[str, Any]]) -> bool:
    print("\nSupabase compatibility check")
    print("=" * 80)

    compatible = True
    for entry in inventory:
        table_name = entry["name"]
        print(f"Checking table: {table_name}")

        try:
            response = supabase.table(table_name).select("id").limit(1).execute()
            remote_rows = response.data or []
            print(f"  - Supabase table exists and is reachable: {table_name}")
            print(f"  - Sample rows returned: {len(remote_rows)}")
        except Exception as exc:
            error_text = str(exc).lower()

            if "permission denied" in error_text or "42501" in error_text:
                print(f"  - Table {table_name} exists, but the current Supabase role cannot read it.")
                print(f"  - Reason: {exc}")
                print("  - Grant SELECT permission to the current role before migration.")
            elif "not found" in error_text or "does not exist" in error_text or "404" in error_text:
                print(f"  - Table {table_name} does not exist in Supabase.")
                print(f"  - Reason: {exc}")
                print("  - This table must be created in Supabase before migration.")
            else:
                print(f"  - Table {table_name} is not reachable or does not exist in Supabase.")
                print(f"  - Reason: {exc}")
                print("  - This table must be created in Supabase before migration.")

            compatible = False

    return compatible


def get_remote_existing_ids(supabase, table_name: str) -> set[int]:
    try:
        response = supabase.table(table_name).select("id").execute()
        rows = response.data or []
        return {int(row["id"]) for row in rows if row.get("id") is not None}
    except Exception:
        return set()


def get_remote_columns(supabase, table_name: str, candidate_columns: list[str] | None = None) -> set[str]:
    """Probe the remote table for the columns that exist, without needing any rows first."""
    if candidate_columns is None:
        candidate_columns = ["id"]

    available_columns: set[str] = set()
    for column_name in candidate_columns:
        try:
            supabase.table(table_name).select(column_name).limit(1).execute()
            available_columns.add(column_name)
        except Exception as exc:
            error_text = str(exc).lower()
            if "does not exist" in error_text or "42703" in error_text or "pgrst204" in error_text:
                continue
            if "not found" in error_text or "404" in error_text:
                break

    return available_columns


def migrate_table(supabase, table_name: str, columns: list[dict[str, Any]], rows: list[dict[str, Any]]) -> int:
    if not rows:
        print(f"[{table_name}] 0 rows to migrate")
        return 0

    existing_ids = get_remote_existing_ids(supabase, table_name)
    candidate_columns = [col["name"] for col in columns]
    available_columns = get_remote_columns(supabase, table_name, candidate_columns)
    if not available_columns:
        available_columns = {col["name"] for col in columns}
        print(f"[{table_name}] remote column detection unavailable; using local column list")

    payload = []
    for row in rows:
        row_id = row.get("id")
        if row_id is not None and int(row_id) in existing_ids:
            continue
        filtered_row = build_payload_for_remote_columns(row, available_columns)
        if filtered_row:
            payload.append(filtered_row)

    if not payload:
        print(f"[{table_name}] duplicate-only rows detected; no new rows will be migrated")
        return 0

    print(f"[{table_name}] migrating {len(payload)} rows")
    try:
        response = supabase.table(table_name).upsert(payload, on_conflict="id").execute()
        migrated = len(response.data or [])
        print(f"[{table_name}] migrated {migrated} rows")
        return migrated
    except Exception as exc:
        print(f"[{table_name}] migration failed: {exc}")
        raise


def fetch_sqlite_rows(conn: sqlite3.Connection, table_name: str) -> list[dict[str, Any]]:
    cur = conn.cursor()
    columns = [row[1] for row in cur.execute(f'PRAGMA table_info("{table_name}")')]
    if not columns:
        return []

    select_sql = f'SELECT * FROM "{table_name}"'
    rows = cur.execute(select_sql).fetchall()
    return [dict(zip(columns, row)) for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely inspect and migrate SQLite data into Supabase.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually migrate data. Default is dry-run only.",
    )
    args = parser.parse_args()

    print("Loading environment from .env...")
    try:
        supabase_url, supabase_key = load_env()
    except Exception as exc:
        print(f"Environment load failed: {exc}")
        return 1

    print("SQLite inspection starting...")
    inventory = get_sqlite_tables()
    print_sqlite_inventory(inventory)

    if any(entry["name"] == "users" for entry in inventory):
        print("\nSupabase users schema migration SQL:")
        print("-" * 80)
        print(USERS_SCHEMA_SQL)
        print("-" * 80)

    print("Creating Supabase client...")
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as exc:
        print(f"Supabase client creation failed: {exc}")
        return 1

    if not compare_with_supabase(supabase, inventory):
        print("\nMigration stopped safely because one or more required Supabase tables are missing or incompatible.")
        return 2

    if not args.execute:
        print("\nDry-run mode: no data will be moved.")
        print("Use --execute only after confirming the Supabase tables exist and the network is reachable.")
        return 0

    conn = sqlite3.connect(DB_PATH)
    try:
        for entry in inventory:
            table_name = entry["name"]
            rows = fetch_sqlite_rows(conn, table_name)
            print(f"\nProcessing table: {table_name}")
            migrate_table(supabase, table_name, entry["columns"], rows)
    finally:
        conn.close()

    print("\nMigration complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
