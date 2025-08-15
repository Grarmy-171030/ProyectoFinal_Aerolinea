from tkinter import *
from tkinter import ttk, messagebox
from Gestion_Aerolinea import Aerolinea
from Clase import Clase
from Pasajero import Pasajero
from Maleta import Maleta
import os
import sys
import subprocess
from datetime import datetime


class VentanaAerolinea(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=900, height=650)
        self.master = master
        self.aerolinea = Aerolinea()
        self.sistema_inicializado = False
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frame para botones de opciones
        frame_botones = Frame(self, bg="#bfdaff")
        frame_botones.place(x=0, y=0, width=180, height=650)

        # Botones de opciones
        Button(frame_botones, text="Inicializar Sistema", command=self.inicializar_sistema,
               bg="#4a7abc", fg="white", font=('Arial', 10, 'bold')).place(x=10, y=30, width=160, height=40)

        # Sección de precios visible
        Label(frame_botones, text="Precios por clase:", bg="#bfdaff", font=('Arial', 9, 'bold')).place(x=10, y=90)

        frame_precios = Frame(frame_botones, bg="#e6f2ff", bd=2, relief=GROOVE)
        frame_precios.place(x=10, y=120, width=160, height=80)

        Label(frame_precios, text="Business:", bg="#e6f2ff", font=('Arial', 9)).place(x=10, y=10)
        Label(frame_precios, text="$500", bg="#e6f2ff", font=('Arial', 9, 'bold'), fg="green").place(x=100, y=10)

        Label(frame_precios, text="Turista:", bg="#e6f2ff", font=('Arial', 9)).place(x=10, y=40)
        Label(frame_precios, text="$200", bg="#e6f2ff", font=('Arial', 9, 'bold'), fg="green").place(x=100, y=40)

        # Botones de funciones
        self.btnReservar = Button(frame_botones, text="Reservar Asiento", command=self.mostrar_reserva,
                                  bg="#4a7abc", fg="white", state=DISABLED, font=('Arial', 10))
        self.btnReservar.place(x=10, y=220, width=160, height=40)

        self.btnMapa = Button(frame_botones, text="Mostrar Mapa", command=self.mostrar_mapa,
                              bg="#4a7abc", fg="white", state=DISABLED, font=('Arial', 10))
        self.btnMapa.place(x=10, y=270, width=160, height=40)

        self.btnListar = Button(frame_botones, text="Listar Pasajeros", command=self.listar_pasajeros,
                                bg="#4a7abc", fg="white", state=DISABLED, font=('Arial', 10))
        self.btnListar.place(x=10, y=320, width=160, height=40)

        self.btnMenores = Button(frame_botones, text="Mostrar Menores", command=self.mostrar_menores,
                                 bg="#4a7abc", fg="white", state=DISABLED, font=('Arial', 10))
        self.btnMenores.place(x=10, y=370, width=160, height=40)

        self.btnIngresos = Button(frame_botones, text="Reporte Ingresos", command=self.mostrar_ingresos,
                                  bg="#2e8b57", fg="white", state=DISABLED, font=('Arial', 10, 'bold'))
        self.btnIngresos.place(x=10, y=420, width=160, height=40)

        Button(frame_botones, text="Salir", command=self.salir,
               bg="#d9534f", fg="white", font=('Arial', 10, 'bold')).place(x=10, y=480, width=160, height=40)

        # Frame para contenido principal
        frame_datos = Frame(self, bg="#d3dde3")
        frame_datos.place(x=180, y=0, width=720, height=650)

        # Lista de vuelos
        frame_vuelos = Frame(frame_datos, bg="#d3dde3")
        frame_vuelos.place(x=10, y=10, width=700, height=120)

        Label(frame_vuelos, text="Vuelos disponibles:", bg="#d3dde3", font=('Arial', 10, 'bold')).pack(anchor=W)

        scroll_vuelos = Scrollbar(frame_vuelos)
        self.lista_vuelos = Listbox(frame_vuelos, yscrollcommand=scroll_vuelos.set, font=('Arial', 10), height=5)
        self.lista_vuelos.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_vuelos.pack(side=RIGHT, fill=Y)
        scroll_vuelos.config(command=self.lista_vuelos.yview)

        # Frame para reserva de asientos
        self.frame_reserva = Frame(frame_datos, bg="#e3e3e3", bd=2, relief=GROOVE)
        self.frame_reserva.place(x=10, y=140, width=700, height=220)

        # Datos del pasajero
        Label(self.frame_reserva, text="Datos del Pasajero", bg="#e3e3e3",
              font=('Arial', 10, 'bold')).place(x=10, y=10)

        Label(self.frame_reserva, text="Nombre:").place(x=20, y=40)
        self.txtNombre = Entry(self.frame_reserva, font=('Arial', 10))
        self.txtNombre.place(x=100, y=40, width=200)

        # Campo de pasaporte con validación
        Label(self.frame_reserva, text="Pasaporte:").place(x=20, y=70)

        def validar_pasaporte(input_text):
            if len(input_text) > 9:
                return False
            if len(input_text) <= 3:
                return input_text.isalpha()
            return input_text[:3].isalpha() and input_text[3:].isdigit()

        vcmd_pasaporte = (self.register(validar_pasaporte), '%P')
        self.pasaporte_var = StringVar()

        self.txtPasaporte = Entry(
            self.frame_reserva,
            font=('Arial', 10),
            validate="key",
            validatecommand=vcmd_pasaporte,
            textvariable=self.pasaporte_var
        )
        self.txtPasaporte.place(x=100, y=70, width=200)

        def convertir_a_mayusculas(*args):
            current_pos = self.txtPasaporte.index(INSERT)
            self.pasaporte_var.set(self.pasaporte_var.get().upper())
            self.txtPasaporte.icursor(current_pos)

        self.pasaporte_var.trace_add('write', convertir_a_mayusculas)

        # Campo de teléfono con validación
        Label(self.frame_reserva, text="Teléfono:").place(x=20, y=100)

        def validar_telefono(input_text):
            return input_text.isdigit() and len(input_text) <= 10

        vcmd_telefono = (self.register(validar_telefono), '%P')
        self.txtTelefono = Entry(
            self.frame_reserva,
            font=('Arial', 10),
            validate="key",
            validatecommand=vcmd_telefono
        )
        self.txtTelefono.place(x=100, y=100, width=200)

        Label(self.frame_reserva, text="Edad:").place(x=20, y=130)
        self.txtEdad = Entry(self.frame_reserva, font=('Arial', 10), width=5)
        self.txtEdad.place(x=100, y=130)

        # Datos del equipaje
        Label(self.frame_reserva, text="Datos del Equipaje", bg="#e3e3e3",
              font=('Arial', 10, 'bold')).place(x=350, y=10)

        Label(self.frame_reserva, text="Peso (kg):").place(x=360, y=40)
        self.txtPeso = Entry(self.frame_reserva, font=('Arial', 10), width=8)
        self.txtPeso.place(x=450, y=40)

        Label(self.frame_reserva, text="Ancho (cm):").place(x=360, y=70)
        self.txtAncho = Entry(self.frame_reserva, font=('Arial', 10), width=8)
        self.txtAncho.place(x=450, y=70)

        Label(self.frame_reserva, text="Alto (cm):").place(x=360, y=100)
        self.txtAlto = Entry(self.frame_reserva, font=('Arial', 10), width=8)
        self.txtAlto.place(x=450, y=100)

        Label(self.frame_reserva, text="Fondo (cm):").place(x=360, y=130)
        self.txtFondo = Entry(self.frame_reserva, font=('Arial', 10), width=8)
        self.txtFondo.place(x=450, y=130)

        # Selección de asiento
        Label(self.frame_reserva, text="Selección de Asiento", bg="#e3e3e3",
              font=('Arial', 10, 'bold')).place(x=20, y=160)

        Label(self.frame_reserva, text="Clase:").place(x=30, y=190)
        self.clase_var = StringVar(value="TURISTA")
        OptionMenu(self.frame_reserva, self.clase_var, "BUSINESS", "TURISTA").place(x=80, y=185)

        Label(self.frame_reserva, text="Fila:").place(x=200, y=190)
        self.txtFila = Entry(self.frame_reserva, font=('Arial', 10), width=5)
        self.txtFila.place(x=240, y=190)

        Label(self.frame_reserva, text="Butaca:").place(x=300, y=190)
        self.txtButaca = Entry(self.frame_reserva, font=('Arial', 10), width=5)
        self.txtButaca.place(x=360, y=190)

        Button(self.frame_reserva, text="Reservar", command=self.guardar_reserva,
               bg="#5cb85c", fg="white", font=('Arial', 10)).place(x=450, y=185, width=100)
        Button(self.frame_reserva, text="Cancelar", command=self.ocultar_reserva,
               bg="#f0ad4e", fg="white", font=('Arial', 10)).place(x=560, y=185, width=100)

        # Área de resultados
        frame_resultados = Frame(frame_datos, bg="#d3dde3")
        frame_resultados.place(x=10, y=370, width=700, height=270)

        Label(frame_resultados, text="Resultados:", bg="#d3dde3",
              font=('Arial', 10, 'bold')).pack(anchor=W)

        scroll_resultados = Scrollbar(frame_resultados)
        self.text_resultados = Text(frame_resultados, wrap=WORD, yscrollcommand=scroll_resultados.set,
                                    font=('Arial', 10), height=12, width=85)
        self.text_resultados.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_resultados.pack(side=RIGHT, fill=Y)
        scroll_resultados.config(command=self.text_resultados.yview)

        # Ocultar frame de reserva inicialmente
        self.frame_reserva.place_forget()

    def inicializar_sistema(self):
        try:
            self.aerolinea.inicializar_sistema()
            self.sistema_inicializado = True
            self.btnReservar.config(state=NORMAL)
            self.btnMapa.config(state=NORMAL)
            self.btnListar.config(state=NORMAL)
            self.btnMenores.config(state=NORMAL)
            self.btnIngresos.config(state=NORMAL)

            # Actualizar lista de vuelos
            self.lista_vuelos.delete(0, END)
            for vuelo in self.aerolinea.vuelos:
                self.lista_vuelos.insert(END, f"{vuelo.origen} → {vuelo.destino} ({vuelo.fecha})")

            self.mostrar_resultado("Sistema inicializado correctamente con 2 vuelos\n" +
                                   "Business: $500 | Turista: $200")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo inicializar el sistema: {str(e)}")

    def mostrar_reserva(self):
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        if not self.lista_vuelos.curselection():
            messagebox.showwarning("Error", "Seleccione un vuelo primero")
            return

        # Limpiar campos
        self.txtNombre.delete(0, END)
        self.txtPasaporte.delete(0, END)
        self.txtTelefono.delete(0, END)
        self.txtEdad.delete(0, END)
        self.txtPeso.delete(0, END)
        self.txtAncho.delete(0, END)
        self.txtAlto.delete(0, END)
        self.txtFondo.delete(0, END)
        self.txtFila.delete(0, END)
        self.txtButaca.delete(0, END)
        self.clase_var.set("TURISTA")

        # Mostrar frame de reserva
        self.frame_reserva.place(x=10, y=140, width=700, height=220)

    def ocultar_reserva(self):
        self.frame_reserva.place_forget()

    def guardar_reserva(self):
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        if not self.lista_vuelos.curselection():
            messagebox.showwarning("Error", "Seleccione un vuelo primero")
            return

        # Validar campos obligatorios
        campos = [self.txtNombre.get(), self.txtPasaporte.get(), self.txtTelefono.get(),
                  self.txtEdad.get(), self.txtPeso.get(), self.txtAncho.get(),
                  self.txtAlto.get(), self.txtFondo.get(), self.txtFila.get(),
                  self.txtButaca.get()]

        if not all(campos):
            messagebox.showwarning("Error", "Complete todos los campos obligatorios")
            return

        # Validar formato de pasaporte (3 letras + 6 números)
        pasaporte = self.txtPasaporte.get()
        if len(pasaporte) != 9 or not (pasaporte[:3].isalpha() and pasaporte[3:].isdigit()):
            messagebox.showwarning("Error", "Pasaporte inválido. Debe ser 3 letras + 6 números (ej: ABC123456)")
            return

        # Validar teléfono (10 dígitos)
        telefono = self.txtTelefono.get()
        if len(telefono) != 10 or not telefono.isdigit():
            messagebox.showwarning("Error", "Teléfono debe tener exactamente 10 dígitos")
            return

        try:
            # Obtener datos del pasajero
            nombre = self.txtNombre.get()
            edad = int(self.txtEdad.get())

            # Validar edad
            if edad <= 0 or edad > 120:
                messagebox.showwarning("Error", "Edad no válida (debe ser 1-120)")
                return

            # Obtener datos del equipaje
            peso = float(self.txtPeso.get())
            ancho = int(self.txtAncho.get())
            alto = int(self.txtAlto.get())
            fondo = int(self.txtFondo.get())

            # Obtener datos del asiento
            fila = int(self.txtFila.get())
            butaca = int(self.txtButaca.get())
            clase = Clase.BUSINESS if self.clase_var.get() == "BUSINESS" else Clase.TURISTA

            # Obtener vuelo seleccionado
            vuelo = self.aerolinea.vuelos[self.lista_vuelos.curselection()[0]]
            avion = vuelo.get_avion()

            # Validar fila y butaca
            filas_disponibles = avion.get_numero_filas(clase)
            butacas_disponibles = avion.get_butacas_por_fila()

            if fila < 1 or fila > filas_disponibles:
                messagebox.showwarning("Error", f"Fila debe estar entre 1 y {filas_disponibles}")
                return

            if butaca < 1 or butaca > butacas_disponibles:
                messagebox.showwarning("Error", f"Butaca debe estar entre 1 y {butacas_disponibles}")
                return

            # Verificar si el asiento está ocupado
            if avion.get_pasajero(fila, butaca, clase) is not None:
                messagebox.showwarning("Error", "El asiento seleccionado ya está ocupado")
                return

            # Crear objetos necesarios
            maleta = Maleta(peso, ancho, alto, fondo)
            pasajero = Pasajero(nombre, pasaporte, telefono, edad, maleta)

            # Hacer la reserva
            avion.reservar_asiento(fila, butaca, clase, pasajero)
            precio = vuelo.get_precio(clase)
            vuelo.agregar_reserva(clase, precio)

            # Mostrar resultado
            letra = chr(64 + butaca)
            mensaje = f"¡Reserva exitosa!\n\n" \
                      f"Vuelo: {vuelo.origen} → {vuelo.destino}\n" \
                      f"Asiento: {fila}{letra} ({self.clase_var.get()})\n" \
                      f"Pasajero: {nombre}\n" \
                      f"Precio: ${precio}\n"

            # Advertencias por equipaje
            if maleta.excede_peso():
                mensaje += "\nADVERTENCIA: Equipaje excede peso máximo (23kg)"
            if maleta.excede_medidas():
                mensaje += "\nADVERTENCIA: Equipaje excede medidas (158cm)"

            self.mostrar_resultado(mensaje)
            self.ocultar_reserva()

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")

    def mostrar_mapa(self):
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        if not self.lista_vuelos.curselection():
            messagebox.showwarning("Error", "Seleccione un vuelo primero")
            return

        vuelo = self.aerolinea.vuelos[self.lista_vuelos.curselection()[0]]
        avion = vuelo.get_avion()

        self.text_resultados.config(state=NORMAL)
        self.text_resultados.delete(1.0, END)
        self.text_resultados.insert(END, f"Mapa de asientos - Vuelo {vuelo.origen} → {vuelo.destino}\n\n")

        # Mostrar mapa de asientos Business
        self.text_resultados.insert(END, "Clase Business ($500):\n")
        filas_business = avion.get_numero_filas(Clase.BUSINESS)
        butacas = avion.get_butacas_por_fila()

        for fila in range(1, filas_business + 1):
            self.text_resultados.insert(END, f"Fila {fila}: ")
            for butaca in range(1, butacas + 1):
                if avion.get_pasajero(fila, butaca, Clase.BUSINESS):
                    self.text_resultados.insert(END, "■ ")
                else:
                    self.text_resultados.insert(END, "□ ")
            self.text_resultados.insert(END, "\n")

        # Mostrar mapa de asientos Turista
        self.text_resultados.insert(END, "\nClase Turista ($200):\n")
        filas_turista = avion.get_numero_filas(Clase.TURISTA)

        for fila in range(1, filas_turista + 1):
            self.text_resultados.insert(END, f"Fila {fila}: ")
            for butaca in range(1, butacas + 1):
                if avion.get_pasajero(fila, butaca, Clase.TURISTA):
                    self.text_resultados.insert(END, "■ ")
                else:
                    self.text_resultados.insert(END, "□ ")
            self.text_resultados.insert(END, "\n")

        self.text_resultados.config(state=DISABLED)

    def listar_pasajeros(self):
    #Genera un PDF con la lista completa de pasajeros
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        if not self.lista_vuelos.curselection():
            messagebox.showwarning("Error", "Seleccione un vuelo primero")
            return

        vuelo = self.aerolinea.vuelos[self.lista_vuelos.curselection()[0]]

        # Recolectar datos de todos los pasajeros
        pasajeros_data = []
        for clase in [Clase.BUSINESS, Clase.TURISTA]:
            filas = vuelo.avion.get_numero_filas(clase)
            butacas = vuelo.avion.get_butacas_por_fila()

            for fila in range(1, filas + 1):
                for butaca in range(1, butacas + 1):
                    pasajero = vuelo.avion.get_pasajero(fila, butaca, clase)
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
        pdf_path = self.aerolinea.generar_reporte_pasajeros_pdf(
            titulo="LISTADO COMPLETO DE PASAJEROS",
            pasajeros_data=pasajeros_data
        )

        if pdf_path:
            self.mostrar_resultado(
                f"=== LISTA DE PASAJEROS GENERADA ===\n\n"
                f"Se ha creado el documento PDF con todos los pasajeros:\n\n"
                f"Archivo: {os.path.basename(pdf_path)}\n"
                f"Ubicación: {os.path.dirname(os.path.abspath(pdf_path))}\n\n"
                "El documento se abrirá automáticamente."
            )

            try:
                if os.name == 'nt':
                    os.startfile(pdf_path)
                elif os.name == 'posix':
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, pdf_path])
            except Exception as e:
                messagebox.showinfo("PDF Generado", f"El reporte se guardó en:\n{pdf_path}")

    def mostrar_menores(self):
        """Genera un PDF solo con los pasajeros menores de 15 años"""
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        if not self.lista_vuelos.curselection():
            messagebox.showwarning("Error", "Seleccione un vuelo primero")
            return

        vuelo = self.aerolinea.vuelos[self.lista_vuelos.curselection()[0]]

        # Recolectar datos de pasajeros menores
        menores_data = []
        for clase in [Clase.BUSINESS, Clase.TURISTA]:
            filas = vuelo.avion.get_numero_filas(clase)
            butacas = vuelo.avion.get_butacas_por_fila()

            for fila in range(1, filas + 1):
                for butaca in range(1, butacas + 1):
                    pasajero = vuelo.avion.get_pasajero(fila, butaca, clase)
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
            pdf_path = self.aerolinea.generar_reporte_pasajeros_pdf(
                titulo="PASAJEROS MENORES DE 15 AÑOS",
                pasajeros_data=menores_data
            )

            if pdf_path:
                self.mostrar_resultado(
                    f"=== LISTA DE PASAJEROS MENORES DE EDAD ===\n\n"
                    f"Se ha creado el documento PDF con pasajeros menores:\n\n"
                    f"Archivo: {os.path.basename(pdf_path)}\n"
                    f"Ubicación: {os.path.dirname(os.path.abspath(pdf_path))}\n\n"
                    "El documento se abrirá automáticamente."
                )

                try:
                    if os.name == 'nt':
                        os.startfile(pdf_path)
                    elif os.name == 'posix':
                        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                        subprocess.call([opener, pdf_path])
                except Exception as e:
                    messagebox.showinfo("PDF Generado", f"El reporte se guardó en:\n{pdf_path}")
        else:
            messagebox.showinfo("Información", "No hay pasajeros menores de 15 años en este vuelo")

    def mostrar_ingresos(self):
        #Muestra el reporte de ingresos y genera PDF automáticamente
        if not self.sistema_inicializado:
            messagebox.showwarning("Error", "Primero debe inicializar el sistema")
            return

        # Generar el PDF
        pdf_path = self.aerolinea.generar_reporte_ingresos_pdf()

        if pdf_path:
            # Mostrar confirmación en el área de texto
            self.text_resultados.config(state=NORMAL)
            self.text_resultados.delete(1.0, END)
            self.text_resultados.insert(END,
                                        "=== REPORTE DE INGRESOS GENERADO ===\n\n"
                                        f"Documento PDF creado exitosamente:\n\n"
                                        f"Archivo: {os.path.basename(pdf_path)}\n"
                                        f"Ubicación: {os.path.abspath(os.path.dirname(pdf_path))}\n\n"
                                        "El PDF se abrirá automáticamente."
                                        )
            self.text_resultados.config(state=DISABLED)

            # Intentar abrir el PDF automáticamente
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path)
                elif os.name == 'posix':  # macOS/Linux
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, pdf_path])
            except Exception as e:
                print(f"No se pudo abrir el PDF automáticamente: {str(e)}")
                messagebox.showinfo(
                    "PDF Generado",
                    f"El reporte se guardó en:\n{os.path.abspath(pdf_path)}"
                )
        else:
            messagebox.showerror("Error", "No se pudo generar el reporte PDF")

    def mostrar_resultado(self, mensaje):
        #Muestra un mensaje en el área de resultados
        self.text_resultados.config(state=NORMAL)
        self.text_resultados.delete(1.0, END)
        self.text_resultados.insert(END, mensaje)
        self.text_resultados.config(state=DISABLED)

    def salir(self):
        #Cierra la aplicación después de confirmación
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir del sistema?"):
            self.master.destroy()