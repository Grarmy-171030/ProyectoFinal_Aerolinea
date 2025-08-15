class Asiento:
    # Este es el constructor, se llama automáticamente cuando creo un asiento.
    def __init__(self, fila, butaca, pasajero):
        self.fila = fila              # Guardo el número de la fila (por ejemplo: 3, 7, etc.)
        self.butaca = butaca          # Guardo el número de la butaca (por ejemplo: 1 para A, 2 para B...)
        self.pasajero = pasajero      # Aquí va el nombre o datos del pasajero que ocupa el asiento

    # Este método me permite obtener la fila del asiento
    def get_fila(self):
        return self.fila
    # Este me devuelve el número de butaca
    def get_butaca(self):
        return self.butaca
    # Este devuelve al pasajero que está sentado allí
    def get_pasajero(self):
        return self.pasajero

    # Este método sirve para mostrar el asiento en formato bonito, como 3A, 5B, etc.
    def __str__(self):
        letra = chr(64 + self.butaca)   # Convierto el número de butaca a letra: 1 es A, 2 es B, etc.
        return f"{self.fila}{letra}"    # Devuelvo el asiento en formato "filaLetra", por ejemplo "7C"