from Clase import Clase      # Importamos la Clase
from Asiento import Asiento  # Importamos la clase Asiento, que representa cada asiento del avión
class Avion:
    ASIENTOS_POR_FILA = 4  # Constante: cantidad de asientos por cada fila del avión
    def __init__(self, modelo, num_business, num_turista):
        # Guardamos el modelo del avión
        self.modelo = modelo
        # Creamos la matriz de asientos para la clase Business
        self.asientos_business = self._crear_asientos(num_business, Clase.BUSINESS)
        # Creamos la matriz de asientos para la clase Turista
        self.asientos_turista = self._crear_asientos(num_turista, Clase.TURISTA)
    def _crear_asientos(self, cantidad, clase):
        # Calcula cuántas filas son necesarias para la cantidad de asientos
        filas = cantidad // self.ASIENTOS_POR_FILA
        # Crea una matriz de asientos (lista de listas), inicializada con None
        return [[None for _ in range(self.ASIENTOS_POR_FILA)] for _ in range(filas)]
    def reservar_asiento(self, fila, butaca, clase, pasajero):
        # Determina la matriz de asientos según la clase elegida
        if clase == Clase.BUSINESS:
            matriz = self.asientos_business
        else:
            matriz = self.asientos_turista
        # Validamos que la fila y la butaca existan en la matriz
        if 1 <= fila <= len(matriz) and 1 <= butaca <= self.ASIENTOS_POR_FILA:
            # Si el asiento está libre, realizamos la reserva
            if matriz[fila - 1][butaca - 1] is None:
                asiento = Asiento(fila, butaca, pasajero)  # Creamos el objeto Asiento
                matriz[fila - 1][butaca - 1] = asiento     # Guardamos el asiento en la matriz
                return asiento                             # Retornamos el asiento reservado
        # Si no se pudo reservar, retornamos None
        return None
    def get_pasajero(self, fila, butaca, clase):
        # Determina en qué matriz buscar según la clase
        if clase == Clase.BUSINESS:
            matriz = self.asientos_business
        else:
            matriz = self.asientos_turista
        # Validamos que la fila y butaca sean correctas
        if 1 <= fila <= len(matriz) and 1 <= butaca <= self.ASIENTOS_POR_FILA:
            asiento = matriz[fila - 1][butaca - 1]  # Obtenemos el asiento correspondiente
            return asiento.get_pasajero() if asiento else None  # Retornamos el pasajero si existe
        return None
    def get_numero_filas(self, clase):
        # Devuelve el número de filas que tiene la clase solicitada
        return len(self.asientos_business) if clase == Clase.BUSINESS else len(self.asientos_turista)
    def get_butacas_por_fila(self):
        # Devuelve la cantidad de asientos por cada fila del avión
        return self.ASIENTOS_POR_FILA
    def mostrar_mapa_asientos(self):
        # Muestra en consola el estado de todos los asientos del avión
        print(f"\nMapa de asientos - Avión {self.modelo}")
        print("Business (Primeras filas):")
        self._mostrar_clase(self.asientos_business)  # Muestra la sección Business
        print("\nTurista (Últimas filas):")
        self._mostrar_clase(self.asientos_turista)   # Muestra la sección Turista
    def _mostrar_clase(self, asientos):
        # Recorre todas las filas y muestra un cuadrado lleno (■) si el asiento está ocupado
        # y un cuadrado vacío (□) si está libre
        for i, fila in enumerate(asientos, 1):
            print(f"Fila {i}:", end=" ")
            print(" ".join("■" if a else "□" for a in fila))
