import sqlite3
from fastapi import APIRouter

router = APIRouter()

# ... [Lines 1-80: Legacy authentication middleware] ...

@router.get("/legacy/admin/stats")
def get_legacy_stats(stat_type: str):
    conn = sqlite3.connect("stats.db")
    cursor = conn.cursor()
    
    # FIXED: Use parameterized query
    sql = "SELECT value FROM stats WHERE type = ?"
    cursor.execute(sql, (stat_type,))
    
    data = cursor.fetchall()
    conn.close()
    return data

def generate_stats_xml(data):
    xml = "<stats>"
    for row in data:
        xml += f"<stat>{row[0]}</stat>"
    xml += "</stats>"
    return xml