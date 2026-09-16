import sqlite3
import os
import pandas as pd
from app.config import settings, DATA_DIR, DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite database and loads datasets if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create investigations table for persisted analysis runs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            investigation_id TEXT PRIMARY KEY,
            component_id TEXT,
            machine_id TEXT,
            failure_type TEXT,
            severity TEXT,
            status TEXT,
            created_at TEXT,
            primary_root_cause TEXT,
            confidence REAL,
            result_json TEXT
        )
    """)
    conn.commit()

    # Check if CSV files exist, if not generate them
    logs_csv = DATA_DIR / "machine_logs.csv"
    if not logs_csv.exists():
        from data.generate_data import generate_all
        generate_all()

    # Load CSVs into SQLite tables for fast indexed querying
    tables_to_load = [
        ("machine_logs", DATA_DIR / "machine_logs.csv"),
        ("inspection_results", DATA_DIR / "inspection_results.csv"),
        ("maintenance_history", DATA_DIR / "maintenance_history.csv"),
        ("process_parameters", DATA_DIR / "process_parameters.csv"),
        ("historical_cases", DATA_DIR / "historical_cases.csv"),
    ]

    for table_name, csv_path in tables_to_load:
        if csv_path.exists():
            # Check if table already populated
            cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if cursor.fetchone()[0] == 0:
                df = pd.read_csv(csv_path)
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Loaded {len(df)} records into SQLite table '{table_name}'")

    # Create indices for fast lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_m_t ON machine_logs (machine_id, timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_insp_c_m ON inspection_results (component_id, machine_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_maint_m ON maintenance_history (machine_id)")
    conn.commit()
    conn.close()
