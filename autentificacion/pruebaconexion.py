import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")
dsn = os.getenv("ORACLE_DSN")

try:
    conn = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )
    print("Conexión exitosa a Oracle")
    conn.close()
except Exception as e:
    print("Error de conexión:", e)
