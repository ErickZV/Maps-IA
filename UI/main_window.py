from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QGuiApplication

from UI.menu_lateral import MenuLateral


class CeldaMapa(QLabel):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(40, 20)
        self.setStyleSheet("""
            background-color: #b04acb;
            border-radius: 8px;
        """)


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maps IA")
        self.resize(1200, 700)
        self._centrar()

        self.widget_central = QWidget()
        self.widget_central.setObjectName("widgetCentral")
        self.setCentralWidget(self.widget_central)

        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        self._crear_barra()
        self._crear_mapa()
        self._crear_overlay()
        self._crear_menu()
        self._estilos()

    # ---------------- CENTRAR ----------------
    def _centrar(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        geo = self.frameGeometry()
        geo.moveCenter(screen.center())
        self.move(geo.topLeft())

    # ---------------- BARRA ----------------
    def _crear_barra(self):
        barra_widget = QWidget()
        barra_widget.setObjectName("barraWidget")
        barra_widget.setFixedHeight(56)

        layout = QHBoxLayout(barra_widget)
        layout.setContentsMargins(10, 8, 10, 8)

        self.boton_menu = QPushButton("☰")
        self.boton_menu.setObjectName("botonMenu")
        self.boton_menu.setFixedSize(40, 40)
        self.boton_menu.clicked.connect(self.mostrar_menu)

        layout.addWidget(self.boton_menu)
        layout.addStretch()

        self.layout_principal.addWidget(barra_widget)

    # ---------------- MAPA ----------------
    def _crear_mapa(self):
        contenedor = QWidget()
        contenedor.setObjectName("contenedorMapa")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        grid = QGridLayout(contenedor)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(14)
        grid.setContentsMargins(20, 10, 20, 20)

        self.celdas = {}
        COLS = 10
        FILAS = 10

        # Números encima
        for col in range(COLS):
            lbl = QLabel(str(col + 1))
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, col + 1)

        # Letras + celdas
        for fila in range(FILAS):
            letra = QLabel(chr(65 + fila))
            letra.setObjectName("etiquetaMapa")
            letra.setAlignment(Qt.AlignCenter)
            grid.addWidget(letra, fila + 1, 0)

            for col in range(COLS):
                celda = CeldaMapa()
                grid.addWidget(celda, fila + 1, col + 1)
                clave = f"{chr(65 + fila)}{col + 1}"
                self.celdas[clave] = celda

        # Stretch para que el grid llene la pantalla
        grid.setColumnStretch(0, 0)
        for c in range(1, COLS + 1):
            grid.setColumnStretch(c, 1)

        grid.setRowStretch(0, 0)
        for f in range(1, FILAS + 1):
            grid.setRowStretch(f, 1)

        self.layout_principal.addWidget(contenedor)

    # ---------------- OVERLAY ----------------
    def _crear_overlay(self):
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,160);")
        self.overlay.hide()
        self.overlay.mousePressEvent = lambda e: self.ocultar_menu()

    # ---------------- MENÚ ----------------
    def _crear_menu(self):
        self.menu_lateral = MenuLateral(self)
        self.menu_lateral.btn_cerrar.clicked.connect(self.ocultar_menu)
        self.menu_lateral.setGeometry(-300, 0, 300, self.height())

    # ---------------- RESPONSIVE ----------------
    def resizeEvent(self, event):
        self.overlay.setGeometry(self.rect())
        x = self.menu_lateral.geometry().x()
        self.menu_lateral.setGeometry(x, 0, 300, self.height())
        super().resizeEvent(event)

    # ---------------- ANIMACIÓN ----------------
    def mostrar_menu(self):
        self.overlay.setGeometry(self.rect())
        self.overlay.show()
        self.overlay.lower()
        self.menu_lateral.raise_()

        self.anim = QPropertyAnimation(self.menu_lateral, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(QRect(-300, 0, 300, self.height()))
        self.anim.setEndValue(QRect(0, 0, 300, self.height()))
        self.anim.start()

    def ocultar_menu(self):
        self.anim = QPropertyAnimation(self.menu_lateral, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setStartValue(QRect(0, 0, 300, self.height()))
        self.anim.setEndValue(QRect(-300, 0, 300, self.height()))
        self.anim.start()
        self.overlay.hide()

    # ---------------- ESTILOS ----------------
    def _estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d0d0d;
            }

            QWidget#widgetCentral,
            QWidget#contenedorMapa,
            QWidget#barraWidget {
                background-color: #0d0d0d;
            }

            QPushButton#botonMenu {
                background-color: #7d3cff;
                color: white;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton#botonMenu:hover {
                background-color: #9b59b6;
            }

            QLabel#etiquetaMapa {
                color: white;
                font-size: 15px;
                font-weight: 700;
                background-color: transparent;
            }
        """)