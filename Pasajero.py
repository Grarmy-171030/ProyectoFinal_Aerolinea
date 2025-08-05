class Pasajero:
    def __init__(self, nombre, pasaporte, telefono, edad, maleta):
        # Datos básicos del pasajero
        self.nombre = nombre       # Nombre del pasajero
        self.pasaporte = pasaporte # Número de pasaporte
        self.telefono = telefono   # Teléfono de contacto
        self.edad = edad           # Edad del pasajero
        self.maleta = maleta       # Información de la maleta
    def get_nombre(self):
        # Devuelve el nombre del pasajero
        return self.nombre
    def get_pasaporte(self):
        # Devuelve el número de pasaporte
        return self.pasaporte
    def get_telefono(self):
        # Devuelve el teléfono del pasajero
        return self.telefono
    def get_edad(self):
        # Devuelve la edad del pasajero
        return self.edad
    def get_maleta(self):
        # Devuelve la información de la maleta
        return self.maleta
