import sqlite3

DATABASE = "database.db"


# ==========================================
# Create Database
# ==========================================

def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS inspections(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image_name TEXT,

            defect_name TEXT,

            confidence REAL,

            status TEXT,

            inspection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()


# ==========================================
# Insert Inspection
# ==========================================

def insert_inspection(image, defect, confidence, status):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO inspections
        (image_name, defect_name, confidence, status)

        VALUES (?, ?, ?, ?)

    """, (

        image,

        defect,

        confidence,

        status

    ))

    conn.commit()

    conn.close()


# ==========================================
# Get All Inspections
# ==========================================

def get_all_inspections():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *
        FROM inspections
        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================
# Dashboard Statistics
# ==========================================

def get_dashboard_stats():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # Total

    cursor.execute("""

        SELECT COUNT(*)
        FROM inspections

    """)

    total = cursor.fetchone()[0]

    # Passed

    cursor.execute("""

        SELECT COUNT(*)
        FROM inspections
        WHERE status='PASS'

    """)

    passed = cursor.fetchone()[0]

    # Failed

    cursor.execute("""

        SELECT COUNT(*)
        FROM inspections
        WHERE status='FAIL'

    """)

    failed = cursor.fetchone()[0]

    # Average Confidence

    cursor.execute("""

        SELECT AVG(confidence)
        FROM inspections

    """)

    avg = cursor.fetchone()[0]

    if avg is None:
        avg = 0

    avg = round(avg, 2)

    conn.close()

    return {

        "total": total,

        "passed": passed,

        "failed": failed,

        "average": avg

    }


# ==========================================
# Defect Distribution
# ==========================================

def get_defect_counts():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT defect_name,
               COUNT(*)

        FROM inspections

        GROUP BY defect_name

        ORDER BY COUNT(*) DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================
# Delete All History
# ==========================================

def clear_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM inspections

    """)

    conn.commit()

    conn.close()


# ==========================================
# Recent Inspections
# ==========================================

def get_recent_inspections(limit=10):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *
        FROM inspections

        ORDER BY id DESC

        LIMIT ?

    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================
# Search Inspection
# ==========================================


def search_inspections(keyword="", status="ALL"):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM inspections
    WHERE
    (
        image_name LIKE ?
        OR defect_name LIKE ?
        OR status LIKE ?
    )
    """

    params = [
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ]

    if status != "ALL":

        query += " AND status=?"

        params.append(status)

    query += " ORDER BY id DESC"

    cursor.execute(query, params)

    data = cursor.fetchall()

    conn.close()

    return data
# ==========================================
# Inspection Trend
# ==========================================

def get_inspection_trend():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(inspection_time), COUNT(*)
        FROM inspections
        GROUP BY DATE(inspection_time)
        ORDER BY DATE(inspection_time)
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================
# Top 5 Defects
# ==========================================

def get_top_defects():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT defect_name, COUNT(*)
        FROM inspections
        WHERE defect_name != 'None'
        GROUP BY defect_name
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================
# Highest Confidence
# ==========================================

def get_highest_confidence():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(confidence)
        FROM inspections
    """)

    value = cursor.fetchone()[0]

    conn.close()

    return value if value else 0


# ==========================================
# Most Common Defect
# ==========================================

def get_most_common_defect():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT defect_name, COUNT(*)
        FROM inspections
        WHERE defect_name != 'None'
        GROUP BY defect_name
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row:
        return row

    return ("None", 0)
def get_top_defects():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT defect_name,
               COUNT(*)

        FROM inspections

        WHERE defect_name != 'None'

        GROUP BY defect_name

        ORDER BY COUNT(*) DESC

        LIMIT 5

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
# ==========================================
# Database Test
# ==========================================

if __name__ == "__main__":

    create_database()

    print("Database Created Successfully!")