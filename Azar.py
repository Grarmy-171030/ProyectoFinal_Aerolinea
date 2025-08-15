import random  # Importamos random para generar datos aleatorios
from Pasajero import Pasajero  # Importamos la clase Pasajero
from Maleta import Maleta  # Importamos la clase Maleta
from Clase import Clase  # Importamos la clase Clase (Business o Turista)
class Azar:
    # Clase que genera datos aleatorios para simular pasajeros, maletas y reservas
    _pasaportes_generados = set()  # Conjunto para almacenar pasaportes únicos
    _nombres_generados = set()  # Conjunto para almacenar nombres completos únicos
    @staticmethod
    def generar_nombre():
        # Genera un nombre completo único con dos apellidos
        nombres = ["Ana", "Carlos", "David", "Elena", "Fernando", "Gabriela",
                   "Héctor", "Irene", "Juan", "Laura", "Miguel", "Nuria",
                   "Óscar", "Patricia", "Quique", "Rosa", "Sergio", "Teresa"]
        apellidos = ["García", "Rodríguez", "González", "Fernández", "López",
                     "Martínez", "Sánchez", "Pérez", "Gómez", "Ruiz", "Hernández",
                     "Díaz", "Moreno", "Álvarez", "Romero", "Navarro", "Torres"]

        while True:  # Genera hasta encontrar una combinación única
            nombre = f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"
            if nombre not in Azar._nombres_generados:
                Azar._nombres_generados.add(nombre)
                return nombre

    @staticmethod
    def generar_pasaporte():
        # Genera un pasaporte único (3 letras + 6 números)
        while True:
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            numeros = ''.join(random.choices('0123456789', k=6))
            pasaporte = f"{letras}{numeros}"

            if pasaporte not in Azar._pasaportes_generados:
                Azar._pasaportes_generados.add(pasaporte)
                return pasaporte

    @staticmethod
    def generar_telefono():
        # Devuelve un número de teléfono ficticio (9 dígitos, empieza con 6/7/8)
        return f"{random.choice(['6', '7', '8'])}{''.join(random.choices('0123456789', k=8))}"

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
            Azar.generar_nombre(),  # Nombre completo único
            Azar.generar_pasaporte(),  # Pasaporte único
            Azar.generar_telefono(),  # Teléfono
            Azar.generar_edad(),  # Edad
            Azar.generar_maleta()  # Maleta
        )

    @staticmethod
    def reiniciar_pasaportes():
        # Método auxiliar para limpiar los pasaportes generados
        Azar._pasaportes_generados.clear()
    @staticmethod
    def reiniciar_nombres():
        # Método auxiliar para limpiar los nombres generados
        Azar._nombres_generados.clear()
    @staticmethod
    def reiniciar_todo():
        # Limpia todos los registros de datos generados
        Azar.reiniciar_pasaportes()
        Azar.reiniciar_nombres()