import sys
from PySide6.QtWidgets import QApplication  

# Importacion de la vista y el controlador
from UI.main_window import VentanaPrincipal
from Controllers.main_controller import ControladorPrincipal


def main():
    #Inicializacion de la app y el controlador main
    app = QApplication(sys.argv)

    # Creamos la vista (UI)
    vista = VentanaPrincipal()

    # Creamos el controlador y le pasamos la vista como parametro
    controlador = ControladorPrincipal(vista)

    # Mostramos la ventana principal
    vista.show()

    # Ejecutamos la aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()