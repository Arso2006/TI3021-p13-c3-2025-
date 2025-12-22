from ecotech import auth, database, finance 
from dotenv import load_dotenv
import flet as ft
import os

class app:
    def __init__(self, page: ft.page):
        self.page = page
        self.page.tittle="ecotech solutions"
        self.db = database (
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )
      
    def page_register(self):
        self.page.controls.clear()
        #
    self.input_id = ft.TextField(
        label = "ID del usuario",
        hint_text="ingresa un numero para el ID del usuario"
    )
self.input_password =ft.TextField(
    label="contraseña"
    hint_Text="ingresa una contraseña",
    password=
)    
    