import random                    # Importamos random para generar datos aleatorios
from Pasajero import Pasajero     # Importamos la clase Pasajero
from Maleta import Maleta         # Importamos la clase Maleta
from Clase import Clase           # Importamos la clase Clase (Business o Turista)
class Azar:
    # Clase que genera datos aleatorios para simular pasajeros, maletas y reservas
    @staticmethod
    def generar_nombre():
        # Lista de posibles nombres
        nombres = ["Ana", "Carlos", "David", "Elena", "Fernando", "Gabriela",
                   "Héctor", "Irene", "Juan", "Laura", "Miguel", "Nuria"]
        # Lista de posibles apellidos
        apellidos = ["García", "Rodríguez", "González", "Fernández", "López",
                     "Martínez", "Sánchez", "Pérez", "Gómez", "Ruiz"]
        # Devuelve un nombre completo aleatorio con dos apellidos
        return f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"
    @staticmethod
    def generar_pasaporte():
        # Genera 3 letras aleatorias
        letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        # Genera 6 números aleatorios
        numeros = ''.join(random.choices('0123456789', k=6))
        # Devuelve un pasaporte
        return f"{letras}{numeros}"

    @staticmethod
    def generar_telefono():
        # Devuelve un número de teléfono ficticio que empieza con 6 y tiene 9 dígitos
        return f"6{''.join(random.choices('0123456789', k=8))}"

    @staticmethod
    def generar_edad():
        # Devuelve una edad aleatoria entre 1 y 80 años
        return random.randint(1, 80)
    @staticmethod
    def generar_maleta():
        # Genera un peso aleatorio entre 5 y 30 kg (con 2 decimales)
        peso = round(random.uniform(5, 30), 2)
        # Genera medidas aleatorias dentro de rangos realistas
        ancho = random.randint(30, 60)
        alto = random.randint(40, 80)
        fondo = random.randint(20, 40)
        # Devuelve un objeto Maleta con las medidas generadas
        return Maleta(peso, ancho, alto, fondo)
    @staticmethod
    def generar_pasajero():
        # Crea y devuelve un pasajero con datos completamente aleatorios
        return Pasajero(
            Azar.generar_nombre(),      # Nombre y apellidos
            Azar.generar_pasaporte(),   # Pasaporte
            Azar.generar_telefono(),    # Teléfono
            Azar.generar_edad(),        # Edad
            Azar.generar_maleta()       # Maleta
        )
