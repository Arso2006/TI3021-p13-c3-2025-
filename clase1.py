class participantes:
    def _init_(self, rut: str, nombre: str, edad: int):
        self._rut: str = rut
        self._nombre: str = nombre
        self._edad: int = edad
    
    def presentarse(self):
        return f"hola mi nombre es {self._nombre} y mi edad es {self._edad}"