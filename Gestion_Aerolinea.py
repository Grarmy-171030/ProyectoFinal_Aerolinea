from Clase import Clase
from Vuelo import Vuelo
from Avion import Avion
from Azar import Azar
import random
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

class Aerolinea:
    def __init__(self):
        # Inicializa la aerolínea sin vuelos ni aviones
        self.vuelos = []         # Lista de vuelos
        self.aviones = []        # Lista de aviones
        self.inicializado = False  # Bandera para saber si el sistema ya se inicializó

    def mostrar_menu(self):
        # Muestra el menú principal de la aplicación
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Inicializar sistema")
            print("2. Reservar asiento")
            print("3. Mostrar mapa de asientos")
            print("4. Listar pasajeros")
            print("5. Mostrar pasajeros menores")
            print("6. Reporte de ingresos")
            print("7. Salir")
            opcion = input("Seleccione una opción: ")
            # Dependiendo de la opción, ejecuta el método correspondiente
            if opcion == "1":
                self.inicializar_sistema()
            elif opcion == "2":
                self.reservar_asiento()
            elif opcion == "3":
                self.mostrar_mapa()
            elif opcion == "4":
                self.listar_pasajeros()
            elif opcion == "5":
                self.mostrar_menores()
            elif opcion == "6":
                self.reporte_ingresos()
            elif opcion == "7":
                print("\nFin de la ejecución")
                sys.exit()  # Sale del programa
            else:
                print("Opción no válida. Intente nuevamente.")

    def inicializar_sistema(self):
        # Crea aviones, vuelos y reservas automáticas
        if self.inicializado:
            print("El sistema ya fue inicializado")
            return
        # Crear aviones con cantidad de asientos para cada clase
        avion1 = Avion("Boeing 737-800", 16, 48)  # 4 filas Business, 12 filas Turista
        avion2 = Avion("Airbus A320", 12, 60)     # 3 filas Business, 15 filas Turista
        self.aviones.extend([avion1, avion2])
        # Crear vuelos asignados a los aviones
        self.vuelos.append(Vuelo("Madrid", "Barcelona", "1/8/2025", avion1))
        self.vuelos.append(Vuelo("Madrid", "París", "29/07/2025", avion2))
        # Crear reservas automáticas para simular ocupación inicial
        for vuelo in self.vuelos:
            for _ in range(3):  # 3 reservas Business
                self._hacer_reserva_automatica(vuelo, Clase.BUSINESS)
            for _ in range(5):  # 5 reservas Turista
                self._hacer_reserva_automatica(vuelo, Clase.TURISTA)
        self.inicializado = True
        print("\nAviones y vuelos inicializados")

    def _hacer_reserva_automatica(self, vuelo, clase):
        # Intenta reservar automáticamente un asiento para un pasajero aleatorio
        avion = vuelo.get_avion()
        filas = avion.get_numero_filas(clase)
        butacas = avion.get_butacas_por_fila()

        for _ in range(10):  # Hasta 10 intentos para encontrar un asiento libre
            fila = random.randint(1, filas)
            butaca = random.randint(1, butacas)
            if avion.get_pasajero(fila, butaca, clase) is None:
                pasajero = Azar.generar_pasajero()
                avion.reservar_asiento(fila, butaca, clase, pasajero)
                precio = vuelo.get_precio(clase)
                vuelo.agregar_reserva(clase, precio)
                return True
        return False

    def seleccionar_vuelo(self):
        # Muestra los vuelos disponibles y permite seleccionar uno
        print("\nVuelos disponibles:")
        for i, vuelo in enumerate(self.vuelos, 1):
            print(f"{i}.")
            print(vuelo)
            print("------")
        # Validar selección
        while True:
            try:
                opcion = int(input("Seleccione vuelo (número): ")) - 1
                if 0 <= opcion < len(self.vuelos):
                    return self.vuelos[opcion]
                print("Número de vuelo no válido")
            except ValueError:
                print("Ingrese un número válido")

    def reservar_asiento(self):
        # Permite reservar manualmente un asiento para un pasajero
        if not self.inicializado:
            print("Primero debe inicializar el sistema (Opción 1)")
            return

        vuelo = self.seleccionar_vuelo()
        avion = vuelo.get_avion()

        # Mostrar precios de cada clase
        print("\nTipos de clase y precios:")
        print(f"1. Business (${vuelo.get_precio(Clase.BUSINESS)})")
        print(f"2. Turista (${vuelo.get_precio(Clase.TURISTA)})")

        # Selección de clase
        while True:
            clase_op = input("Seleccione clase (1-2): ")
            if clase_op in ("1", "2"):
                clase = Clase.BUSINESS if clase_op == "1" else Clase.TURISTA
                break
            print("Opción no válida")

        # Mostrar mapa de asientos
        avion.mostrar_mapa_asientos()

        # Selección de asiento
        filas = avion.get_numero_filas(clase)
        butacas = avion.get_butacas_por_fila()
        print(f"\nSeleccione asiento (Filas: 1-{filas}, Butacas: 1-{butacas} -> A-D)")

        while True:
            try:
                fila = int(input(f"Fila (1-{filas}): "))
                butaca = int(input(f"Butaca (1-{butacas}): "))

                # Validación de asiento
                if 1 <= fila <= filas and 1 <= butaca <= butacas:
                    if avion.get_pasajero(fila, butaca, clase) is None:
                        pasajero = self.ingresar_datos_pasajero()
                        if pasajero:
                            avion.reservar_asiento(fila, butaca, clase, pasajero)
                            letra = chr(64 + butaca)  # Convierte número en letra A-D
                            precio = vuelo.get_precio(clase)
                            vuelo.agregar_reserva(clase, precio)
                            print(f"\n¡Reserva exitosa! Asiento: {fila}{letra} - {pasajero.get_nombre()}")
                            print(f"Precio del boleto: ${precio}")
                            return
                        else:
                            print("Reserva cancelada")
                            return
                    else:
                        print("Asiento ya ocupado")
                else:
                    print("Ubicación no válida")
            except ValueError:
                print("Ingrese números válidos")

    def ingresar_datos_pasajero(self):
        # Solicita los datos del pasajero y crea un objeto Pasajero
        print("\nIngrese datos del pasajero:")
        nombre = input("Nombre completo: ")
        pasaporte = input("Pasaporte: ")
        telefono = input("Teléfono: ")

        # Validación de edad
        while True:
            try:
                edad = int(input("Edad: "))
                if 0 < edad < 120:
                    break
                print("Edad no válida")
            except ValueError:
                print("Ingrese un número válido")

        # Datos de la maleta
        print("\nDatos de equipaje:")
        while True:
            try:
                peso = float(input("Peso (kg): "))
                ancho = int(input("Ancho (cm): "))
                alto = int(input("Alto (cm): "))
                fondo = int(input("Fondo (cm): "))
                break
            except ValueError:
                print("Ingrese valores numéricos válidos")

        maleta = Maleta(peso, ancho, alto, fondo)
        return Pasajero(nombre, pasaporte, telefono, edad, maleta)

    def mostrar_mapa(self):
        # Muestra el mapa de asientos de un vuelo seleccionado
        if not self.inicializado:
            print("Primero debe inicializar el sistema (Opción 1)")
            return

        vuelo = self.seleccionar_vuelo()
        vuelo.get_avion().mostrar_mapa_asientos()

    def listar_pasajeros(self):
        # Lista todos los pasajeros de un vuelo
        if not self.inicializado:
            print("Primero debe inicializar el sistema (Opción 1)")
            return

        vuelo = self.seleccionar_vuelo()
        avion = vuelo.get_avion()

        # Recolectar datos para PDF
        pasajeros_data = []
        for clase in [Clase.BUSINESS, Clase.TURISTA]:
            filas = avion.get_numero_filas(clase)
            butacas = avion.get_butacas_por_fila()

            for fila in range(1, filas + 1):
                for butaca in range(1, butacas + 1):
                    pasajero = avion.get_pasajero(fila, butaca, clase)
                    if pasajero:
                        letra = chr(64 + butaca)
                        pasajeros_data.append({
                            'nombre': pasajero.get_nombre(),
                            'pasaporte': pasajero.get_pasaporte(),
                            'telefono': pasajero.get_telefono(),
                            'edad': pasajero.get_edad(),
                            'asiento': f"{fila}{letra}",
                            'clase': "Business" if clase == Clase.BUSINESS else "Turista"
                        })

        # Generar PDF
        self.generar_reporte_pasajeros_pdf(
            titulo="LISTADO COMPLETO DE PASAJEROS",
            pasajeros_data=pasajeros_data
        )

    def _listar_pasajeros_clase(self, avion, clase):
        # Lista los pasajeros por clase
        filas = avion.get_numero_filas(clase)
        butacas = avion.get_butacas_por_fila()

        for fila in range(1, filas + 1):
            for butaca in range(1, butacas + 1):
                pasajero = avion.get_pasajero(fila, butaca, clase)
                if pasajero:
                    letra = chr(64 + butaca)
                    print(f"Fila {fila}{letra}: {pasajero.get_nombre()} ({pasajero.get_edad()} años) - {pasajero.get_pasaporte()}")

    def mostrar_menores(self):
        # Muestra solo los pasajeros menores de 15 años
        if not self.inicializado:
            print("Primero debe inicializar el sistema (Opción 1)")
            return

        vuelo = self.seleccionar_vuelo()
        avion = vuelo.get_avion()

        # Recolectar datos para PDF
        menores_data = []
        for clase in [Clase.BUSINESS, Clase.TURISTA]:
            filas = avion.get_numero_filas(clase)
            butacas = avion.get_butacas_por_fila()

            for fila in range(1, filas + 1):
                for butaca in range(1, butacas + 1):
                    pasajero = avion.get_pasajero(fila, butaca, clase)
                    if pasajero and pasajero.get_edad() < 15:
                        letra = chr(64 + butaca)
                        menores_data.append({
                            'nombre': pasajero.get_nombre(),
                            'pasaporte': pasajero.get_pasaporte(),
                            'telefono': pasajero.get_telefono(),
                            'edad': pasajero.get_edad(),
                            'asiento': f"{fila}{letra}",
                            'clase': "Business" if clase == Clase.BUSINESS else "Turista"
                        })

        # Generar PDF si hay menores
        if menores_data:
            self.generar_reporte_pasajeros_pdf(
                titulo="PASAJEROS_MENORES_DE_15_AÑOS",
                pasajeros_data=menores_data
            )
        else:
            print("\nNo hay pasajeros menores de 15 años en este vuelo.")

    def _mostrar_menores_clase(self, avion, clase):
        # Lista pasajeros menores de 15 años por clase
        filas = avion.get_numero_filas(clase)
        butacas = avion.get_butacas_por_fila()
        encontrados = False

        for fila in range(1, filas + 1):
            for butaca in range(1, butacas + 1):
                pasajero = avion.get_pasajero(fila, butaca, clase)
                if pasajero and pasajero.get_edad() < 15:
                    letra = chr(64 + butaca)
                    print(f"Fila {fila}{letra}: {pasajero.get_nombre()} ({pasajero.get_edad()} años)")
                    encontrados = True

        if not encontrados:
            print("No hay pasajeros menores en esta clase")

    def reporte_ingresos(self):
        # Genera un reporte de ingresos por vuelo y total general
        if not self.inicializado:
            print("Primero debe inicializar el sistema (Opción 1)")
            return

        print("\n=== REPORTE DE INGRESOS ===")
        total_general = 0

        for vuelo in self.vuelos:
            ingresos = vuelo.calcular_ingresos()
            print(f"\nVuelo {vuelo.origen} → {vuelo.destino}:")
            print(f"  Business: {ingresos[0]} pasajeros → ${ingresos[0] * vuelo.precio_business}")
            print(f"  Turista: {ingresos[1]} pasajeros → ${ingresos[1] * vuelo.precio_turista}")
            total_vuelo = (ingresos[0] * vuelo.precio_business) + (ingresos[1] * vuelo.precio_turista)
            print(f"  TOTAL: ${total_vuelo}")
            total_general += total_vuelo

        print("\n" + "=" * 40)
        print(f"INGRESOS TOTALES: ${total_general}")
        print("=" * 40)

    def generar_reporte_ingresos_pdf(self):
        #Genera un PDF con el detalle de ingresos por pasajero
        try:
            # Crear directorio para reportes si no existe
            os.makedirs('reportes', exist_ok=True)

            # Nombre de archivo único con fecha/hora
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join('reportes', f'Ingresos_{fecha_hora}.pdf')

            # Configurar documento PDF
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                leftMargin=40,
                rightMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            elements = []
            styles = getSampleStyleSheet()

            # Título del reporte
            title = Paragraph(
                "<b>REPORTE DE INGRESOS  DEL SISTEMA DE GESTIÓN DE AEROLÍNEA</b>",
                styles['Title']
            )
            elements.append(title)
            elements.append(Spacer(1, 20))

            # Información de generación
            gen_info = Paragraph(
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles['Normal']
            )
            elements.append(gen_info)
            elements.append(Spacer(1, 30))

            # Procesar cada vuelo
            total_general = 0

            for vuelo in self.vuelos:
                # Encabezado del vuelo
                vuelo_title = Paragraph(
                    f"<b>Vuelo:</b> {vuelo.origen} → {vuelo.destino} | "
                    f"<b>Fecha:</b> {vuelo.fecha} | "
                    f"<b>Avión:</b> {vuelo.avion.modelo}",
                    styles['Heading2']
                )
                elements.append(vuelo_title)
                elements.append(Spacer(1, 15))

                # Datos de la tabla
                table_data = [
                    ['Pasajero', 'Clase', 'Asiento', 'Monto']
                ]

                total_vuelo = 0

                # Procesar asientos Business
                for fila_num, fila in enumerate(vuelo.avion.asientos_business, 1):
                    for asiento_num, asiento in enumerate(fila, 1):
                        if asiento is not None:
                            pasajero = asiento.get_pasajero()
                            letra = chr(64 + asiento_num)  # 1=A, 2=B, etc.
                            monto = vuelo.precio_business

                            table_data.append([
                                pasajero.get_nombre(),
                                'Business',
                                f"{fila_num}{letra}",
                                f"${monto:,.2f}"
                            ])
                            total_vuelo += monto

                # Procesar asientos Turista
                for fila_num, fila in enumerate(vuelo.avion.asientos_turista, 1):
                    for asiento_num, asiento in enumerate(fila, 1):
                        if asiento is not None:
                            pasajero = asiento.get_pasajero()
                            letra = chr(64 + asiento_num)
                            monto = vuelo.precio_turista

                            table_data.append([
                                pasajero.get_nombre(),
                                'Turista',
                                f"{fila_num}{letra}",
                                f"${monto:,.2f}"
                            ])
                            total_vuelo += monto

                # Crear tabla
                table = Table(
                    table_data,
                    colWidths=[180, 80, 60, 80],
                    repeatRows=1
                )

                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A7ABC')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E6F2FF')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BFDAFF')),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT')
                ]))

                elements.append(table)
                elements.append(Spacer(1, 15))

                # Total del vuelo
                total_text = Paragraph(
                    f"<b>Total del vuelo:</b> ${total_vuelo:,.2f}",
                    styles['BodyText']
                )
                elements.append(total_text)
                elements.append(Spacer(1, 30))

                total_general += total_vuelo

            # Total general
            grand_total = Paragraph(
                f"<b>TOTAL GENERAL:</b> ${total_general:,.2f}",
                styles['Heading1']
            )
            elements.append(grand_total)
            elements.append(Spacer(1, 30))

            # Pie de página
            footer = Paragraph(
                "Sistema de Gestión de Aerolínea - Documento generado automáticamente",
                styles['Italic']
            )
            elements.append(footer)

            # Generar PDF
            doc.build(elements)

            return pdf_path

        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return None

    def generar_reporte_pasajeros_pdf(self, titulo, pasajeros_data):
        #Genera un PDF con la lista de pasajeros
        try:
            os.makedirs('reportes', exist_ok=True)
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join('reportes', f'{titulo}_{fecha_hora}.pdf')

            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                leftMargin=40,
                rightMargin=40,
                topMargin=40,
                bottomMargin=40
            )

            elements = []
            styles = getSampleStyleSheet()

            # Título del reporte
            title = Paragraph(f"<b>{titulo}</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))

            # Información de generación
            gen_info = Paragraph(
                f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles['Normal']
            )
            elements.append(gen_info)
            elements.append(Spacer(1, 30))

            # Datos de la tabla
            table_data = [
                ['Nombre', 'Pasaporte', 'Teléfono', 'Edad', 'Asiento', 'Clase']
            ]

            for pasajero_info in pasajeros_data:
                table_data.append([
                    pasajero_info['nombre'],
                    pasajero_info['pasaporte'],
                    pasajero_info['telefono'],
                    str(pasajero_info['edad']),
                    pasajero_info['asiento'],
                    pasajero_info['clase']
                ])

            # Crear tabla
            table = Table(
                table_data,
                colWidths=[120, 100, 80, 40, 60, 60],
                repeatRows=1
            )

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A7ABC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E6F2FF')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BFDAFF')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 0), (0, -1), 'LEFT')
            ]))

            elements.append(table)
            elements.append(Spacer(1, 30))

            # Pie de página
            footer = Paragraph(
                "Sistema de Gestión de Aerolínea - Documento generado automáticamente",
                styles['Italic']
            )
            elements.append(footer)

            # Generar PDF
            doc.build(elements)
            print(f"\nReporte generado en: {pdf_path}")
            return pdf_path

        except Exception as e:
            print(f"Error al generar PDF: {str(e)}")
            return None