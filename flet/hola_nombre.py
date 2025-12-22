#
#
#
#

#
import flet as ft 

#
class app:
    def _init_ (self, page: ft.page):
        self.page = page
        self.page.tittle = "hola nombre"

        self.input_nombre = ft.TextField( hint_text = "ingresa tu nombre" )
        self.button_saludar = ft.button(text="saludar", on_click=self.handle_saludo )
        self.text_saludo = ft.text( value="")

        self.build()

    def build(self):
        self.page.add(
            self.input_nombre,
            self.button_saludar,
            self.text_saludo
        )
        self.page.update()
    def handle_saludo(self, e):
        nombre = (self.input_nombre.value or "").strip()
        if nombre:
            self.text_saludo.value = f"hola, {nombre}"
        else:
            self.text_saludo.value = "ingrese un nombre"
        self.page.update    


#
if __name__ == "__main__":
    ft.app(target=app)