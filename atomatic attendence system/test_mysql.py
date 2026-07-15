import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",      # ✅ correct host
        port=3306,             # ✅ MySQL default port
        user="root",
        password="Sitaram620@",   # put your real password
        database="logface"
    )

    print("✅ MySQL Connected Successfully")
    conn.close()

except mysql.connector.Error as err:
    print("❌ Error:", err)
