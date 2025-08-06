import sqlite3

def list_regions():
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Region")
    rows = cursor.fetchall()
    conn.close()

    print("RegionID | RegionName")
    print("---------------------")
    for row in rows:
        print(f"{row[0]:<8} | {row[1]}")

if __name__ == "__main__":
    list_regions()
