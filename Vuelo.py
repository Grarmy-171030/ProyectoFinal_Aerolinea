from Clase import Clase  # Importamos Clase, que indica si un asiento es Business o Turista
class Vuelo:
    def __init__(self, origen, destino, fecha, avion):
        # Información básica del vuelo
        self.origen = origen      # Ciudad o país de origen
        self.destino = destino    # Ciudad o país de destino
        self.fecha = fecha        # Fecha del vuelo
        self.avion = avion        # Avión asignado al vuelo
        # Precios de los boletos por clase
        self.precio_business = 500  # Precio por asiento en clase Business
        self.precio_turista = 200   # Precio por asiento en clase Turista
        # Contadores de reservas por clase
        self.reservas_business = 0  # Número de reservas en Business
        self.reservas_turista = 0   # Número de reservas en Turista
    def agregar_reserva(self, clase, precio):
        # Aumenta el contador de reservas dependiendo de la clase
        if clase == Clase.BUSINESS:
            self.reservas_business += 1
        else:
            self.reservas_turista += 1
    def calcular_ingresos(self):
        # Devuelve el total de reservas por clase
        return (self.reservas_business, self.reservas_turista)
    def get_pais_origen(self):
        # Devuelve el país o ciudad de origen del vuelo
        return self.origen
    def get_pais_destino(self):
        # Devuelve el país o ciudad de destino del vuelo
        return self.destino
    def get_fecha(self):
        # Devuelve la fecha del vuelo
        return self.fecha
    def get_avion(self):
        # Devuelve el avión asignado al vuelo
        return self.avion
    def get_precio(self, clase):
        # Devuelve el precio dependiendo de la clase seleccionada
        return self.precio_business if clase == Clase.BUSINESS else self.precio_turista
    def __str__(self):
        # Representación del vuelo
        return f"{self.origen} → {self.destino} ({self.fecha}) - Business: ${self.precio_business} | Turista: ${self.precio_turista}"
