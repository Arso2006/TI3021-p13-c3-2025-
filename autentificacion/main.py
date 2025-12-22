# ============================
# IMPORTACIONES ORIGINALES
# ============================

import oracledb
import os
from dotenv import load_dotenv
import bcrypt
from typing import Optional
import requests
import datetime

# ============================
# CARGA DE VARIABLES DE ENTORNO
# ============================

load_dotenv()

username = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")
dsn = os.getenv("ORACLE_DSN")

# ============================
# CLASE DATABASE
# ============================

class Database:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn

    def get_connection(self):
        return oracledb.connect(
            user=self.username,
            password=self.password,
            dsn=self.dsn
        )

    def create_all_tables(self):
        pass

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    if sql.startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)


# ============================
# AUTENTICACIÓN
# ============================

class Auth:

    @staticmethod
    def register(db: Database, username: str, password: bytes):
        salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(password, salt)

        db.query(
            """
            INSERT INTO USERS (username, password_hash, rol)
            VALUES (:username, :password_hash, 'USER')
            """,
            {
                "username": username,
                "password_hash": hashed_password
            }
        )

    @staticmethod
    def login(db: Database, username: str, password: str):
        password = password.encode("UTF-8")

        resultado = db.query(
            sql= "SELECT * FROM USERS WHERE username = :username",
            parameters={"username":username}
        )

        if len(resultado) < 0:
            return print("No hay coincidencias")
        
        hashed_password = resultado[0][2]

        if bcrypt.checkpw(password, hashed_password):
            print("Logeado correctamente")
            return resultado[0]
        else:
            print("Contraseña incorrecta")
            return None

# ============================
# FINANZAS / INDICADORES
# ============================

class Finance:

    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url

    # MÉTODO ORIGINAL (NO SE ELIMINA)
    def gert_indicator(self, indicator: str = None, fecha: str = None):
        if not indicator:
            print("Indicator faltante")
            return

        if not fecha:
            today = datetime.datetime.now()
            fecha = f"{today.day}-{today.month}-{today.year}"

        url = f"{self.base_url}/{indicator}/{fecha}"
        data = requests.get(url).json()
        print(data["serie"][0]["valor"])

    # ============================
    # MÉTODO SEGURO AGREGADO
    # ============================

    def get_indicator_safe(self, indicator: str, fecha: str = None):
        try:
            if not fecha:
                today = datetime.datetime.now()
                fecha = f"{today.day}-{today.month}-{today.year}"

            url = f"{self.base_url}/{indicator}/{fecha}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            if "serie" not in data or len(data["serie"]) == 0:
                raise ValueError("No hay datos disponibles")

            valor = data["serie"][0]["valor"]
            print(f"{indicator.upper()} ({fecha}): {valor}")
            return valor, fecha

        except Exception as e:
            print("Error al obtener indicador:", e)
            return None, None

    # ============================
    # GUARDAR EN BASE DE DATOS
    # ============================

    def save_indicator_db(
        self,
        db: Database,
        nombre: str,
        fecha_valor: str,
        valor: float,
        id_usuario: int
    ):
        try:
            db.query(
                """
                INSERT INTO INDICADORES_ECONOMICOS
                (id, nombre_indicador, fecha_valor, valor, sitio_origen, id_usuario)
                VALUES
                (seq_indicadores.NEXTVAL,
                 :nombre,
                 TO_DATE(:fecha, 'DD-MM-YYYY'),
                 :valor,
                 'mindicador.cl',
                 :id_usuario)
                """,
                {
                    "nombre": nombre.upper(),
                    "fecha": fecha_valor,
                    "valor": valor,
                    "id_usuario": id_usuario
                }
            )
            print("Indicador guardado correctamente.")
        except Exception as e:
            print("Error al guardar indicador:", e)

# ============================
# FUNCIÓN AGREGADA (NO MODIFICA MENÚ)
# ============================

def consultar_y_guardar(finance, db, indicador, id_usuario):
    valor, fecha = finance.get_indicator_safe(indicador)
    if valor is not None:
        guardar = input("¿Desea guardar el indicador? (s/n): ").lower()
        if guardar == "s":
            finance.save_indicator_db(
                db=db,
                nombre=indicador,
                fecha_valor=fecha,
                valor=valor,
                id_usuario=id_usuario
            )

# ============================
# MENÚ PRINCIPAL (ORIGINAL)
# ============================

def menu_principal():
    db = Database(username, password, dsn)
    print(username, password, dsn)
    finance = Finance()

    while True:
        print("\n====== MENÚ PRINCIPAL ======")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Consultar indicador (sin guardar)")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            user = input("Ingrese usuario: ")
            pwd = input("Ingrese contraseña: ")
            Auth.register(db, user, pwd.encode())
            print("Usuario registrado.")

        elif opcion == "2":
            user = input("Usuario: ")
            pwd = input("Contraseña: ")

            user_id = Auth.login(db, user, pwd)
            if user_id:
                print("Sesión iniciada correctamente.")
                menu_usuario(finance, db, user_id)
            else:
                print("Credenciales incorrectas.")

        elif opcion == "3":
            indicador = input("Ingrese indicador (uf, ivp, ipc, utm, dolar, euro): ")
            finance.gert_indicator(indicador)

        elif opcion == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")

# ============================
# MENÚ USUARIO (EXTENDIDO)
# ============================

def menu_usuario(finance: Finance, db: Database, id_usuario: int):
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1. UF")
        print("2. Dólar")
        print("3. Euro")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            consultar_y_guardar(finance, db, "uf", id_usuario)
        elif opcion == "2":
            consultar_y_guardar(finance, db, "dolar", id_usuario)
        elif opcion == "3":
            consultar_y_guardar(finance, db, "euro", id_usuario)
        elif opcion == "4":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")

# ============================
# MAIN
# ============================

if __name__ == "__main__":
    menu_principal()
