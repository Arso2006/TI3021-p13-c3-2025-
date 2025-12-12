#conectarnos a la base de datos
import oracledb
import os
from dotenv import load_dotenv
import bcrypt
#implementar hasheo de contraseña
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")


class database:
   def _init_(self, username,password, dsn):
      self.username = username
      self.password = password
      self.dsn = dsn
      def get_connection(self):
         return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
      def create_all_tables(self):
         pass
      def query(self, sentence: str, parameters: Optional [dict] = None):
         pass

class auth:
    @staticmethod
    def register():
        pass
    @staticmethod
    def login():
        pass

"""
unidad de fomento (UF)
indice de valor promedio (IVP)
indice de precio al consumidor (IPC)
unidad tributaria mensual (UTM)
Dolar-> CLP
Euro -> CLP
"""

class finance:
    @staticmethod
    def get_uf():
