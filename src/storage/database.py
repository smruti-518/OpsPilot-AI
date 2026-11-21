import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "incidents.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                detected_at TEXT NOT NULL,
                severity TEXT,
                severity_score INTEGER,
                impact_area TEXT,
                total_logs INTEGER,
                total_errors INTEGER,
                total_warnings INTEGER,
                report TEXT
            )
        """)
        connection.commit()


def save_incident(incident_data, analysis, report):
    with get_connection() as connection:
        connection.execute("""
            INSERT OR REPLACE INTO incidents (
                incident_id,
                detected_at,
                severity,
                severity_score,
                impact_area,
                total_logs,
                total_errors,
                total_warnings,
                report
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis["incident_id"],
            analysis["detected_at"],
            analysis["severity"],
            analysis["severity_score"],
            analysis["impact_area"],
            incident_data["total_logs"],
            incident_data["total_errors"],
            incident_data["total_warnings"],
            report
        ))
        connection.commit()


def get_incident_history():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT
                incident_id,
                detected_at,
                severity,
                severity_score,
                impact_area,
                total_logs,
                total_errors,
                total_warnings
            FROM incidents
            ORDER BY detected_at DESC
        """).fetchall()

    return [dict(row) for row in rows]


def get_incident_report(incident_id):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT report
            FROM incidents
            WHERE incident_id = ?
        """, (incident_id,)).fetchone()

    return row["report"] if row else None