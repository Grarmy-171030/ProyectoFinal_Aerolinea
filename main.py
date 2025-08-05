from interfaz import VentanaAerolinea
from tkinter import Tk
if __name__ == "__main__":
    root = Tk()
    root.title("Sistema de Aerolínea")
    try:
        root.iconbitmap("Icono.ico")
    except:
        pass
    app = VentanaAerolinea(master=root)
    root.mainloop()