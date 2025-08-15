class Maleta:
    def __init__(self, peso, ancho, alto, fondo):
        # Se guardan las características físicas de la maleta
        self.peso = peso      # Peso en kilogramos
        self.ancho = ancho    # Ancho en centímetros
        self.alto = alto      # Alto en centímetros
        self.fondo = fondo    # Fondo  en centímetros
        # Restricciones
        self.PESO_MAXIMO = 23     # Peso máximo permitido (kg)
        self.MEDIDA_MAXIMA = 158  # Suma máxima de dimensiones (cm)
    def excede_peso(self):
        # Devuelve True si el peso de la maleta supera el máximo permitido
        return self.peso > self.PESO_MAXIMO
    def excede_medidas(self):
        # Devuelve True si la suma de las dimensiones supera el límite permitido
        return (self.ancho + self.alto + self.fondo) > self.MEDIDA_MAXIMA
