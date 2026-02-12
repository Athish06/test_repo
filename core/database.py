import sqlite3
import logging
from typing import List, Dict, Any, Optional

import sqlite3
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)

# Simple connection pool
connections = {}

class LegacyDBHandler:
    def __init__(self, connection_string: str):
        self.conn_str = connection_string
        self.logger = logging.getLogger("db_core")

    def _get_connection(self):
        if self.conn_str not in connections:
            conn = sqlite3.connect(self.conn_str)
            conn.execute("PRAGMA foreign_keys = ON")
            connections[self.conn_str] = conn
        return connections[self.conn_str]

    # === FIXED: Now requires parameterized queries ===
    def run_query_v2(self, query_string: str, params: tuple = ()) -> List[Any]:
        """
        Executes a query with parameters to prevent SQL injection.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query_string, params)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            raise
    def bulk_insert(self, table: str, data: List[Dict[str, Any]]):
        conn = self._get_connection()
        cursor = conn.cursor()
        for row in data:
            columns = ', '.join(row.keys())
            placeholders = ', '.join('?' * len(row))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(row.values()))
        conn.commit()

    def health_check(self) -> bool:
        try:
            self.run_query_v2("SELECT 1")
            return True
        except:
            return False
            conn.close()

# ... [Lines 150-300: Other helper functions like bulk_insert, health_check] ...