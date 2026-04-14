from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QGuiApplication, QPalette, QColor

from UI.menu_lateral import MenuLateral

CUADRAS   = 10
TAM_CUADRA = 55
TAM_CALLE  = 14


class CeldaCuadra(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget {
                background-color: #b04acb;
                border-radius: 6px;
            }
        """)


class CeldaCalle(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QWidget { background-color: #0d0d0d; }")


class NodoInterseccion(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(14, 14)
        self._estado = "normal"
        self._aplicar_estilo()

    def _aplicar_estilo(self):
        estilos = {
            "normal":     "QWidget { background-color: #555555; border-radius: 7px; }",
            "inicio":     "QWidget { background-color: white;   border-radius: 7px; }",
            "destino":    "QWidget { background-color: #27ae60; border-radius: 7px; }",
            "incidencia": "QWidget { background-color: #e74c3c; border-radius: 7px; }",
        }
        self.setStyleSheet(estilos.get(self._estado, estilos["normal"]))

    def set_estado(self, estado: str):
        self._estado = estado
        self._aplicar_estilo()

    def get_estado(self):
        return self._estado


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

    def _centrar(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        geo = self.frameGeometry()
        geo.moveCenter(screen.center())
        self.move(geo.topLeft())

    def _crear_barra(self):
        barra = QWidget()
        barra.setObjectName("barraWidget")
        barra.setFixedHeight(56)

        layout = QHBoxLayout(barra)
        layout.setContentsMargins(10, 8, 10, 8)

        self.boton_menu = QPushButton("☰")
        self.boton_menu.setObjectName("botonMenu")
        self.boton_menu.setFixedSize(40, 40)

        layout.addWidget(self.boton_menu)
        layout.addStretch()

        self.layout_principal.addWidget(barra)

    def _crear_mapa(self):
        contenedor = QWidget()
        contenedor.setObjectName("contenedorMapa")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        from PySide6.QtWidgets import QGridLayout
        grid = QGridLayout(contenedor)
        grid.setSpacing(0)
        grid.setContentsMargins(20, 10, 20, 20)

        self.nodos   = {}
        self.cuadras = {}
        N = CUADRAS

        for gf in range(2 * N + 1):
            for gc in range(2 * N + 1):
                es_fila_cuadra = (gf % 2 == 0)
                es_col_cuadra  = (gc % 2 == 0)
                widget_row = gf + 1
                widget_col = gc + 1

                if es_fila_cuadra and es_col_cuadra:
                    w = CeldaCuadra()
                    grid.addWidget(w, widget_row, widget_col)
                    self.cuadras[(gf, gc)] = w

                elif not es_fila_cuadra and not es_col_cuadra:
                    nodo = NodoInterseccion()
                    letra  = chr(65 + gf // 2)
                    numero = gc // 2 + 1
                    clave  = f"{letra}{numero}"
                    self.nodos[clave] = nodo

                    # Contenedor centrado para el nodo
                    wrap = QWidget()
                    wrap.setAttribute(Qt.WA_StyledBackground, True)
                    wrap.setStyleSheet("QWidget { background-color: #0d0d0d; }")
                    wlayout = QHBoxLayout(wrap)
                    wlayout.setContentsMargins(0, 0, 0, 0)
                    wlayout.setAlignment(Qt.AlignCenter)
                    wlayout.addWidget(nodo)
                    grid.addWidget(wrap, widget_row, widget_col)

                else:
                    w = CeldaCalle()
                    grid.addWidget(w, widget_row, widget_col)

        # Etiquetas numéricas (fila 0)
        for i in range(N):
            gc = 2 * i + 1
            lbl = QLabel(str(i + 1))
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, gc + 1)

        # Etiquetas de letras (col 0)
        for i in range(N):
            gf = 2 * i + 1
            lbl = QLabel(chr(65 + i))
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, gf + 1, 0)

        # Tamaños
        grid.setColumnMinimumWidth(0, 24)
        grid.setRowMinimumHeight(0, 24)

        for gf in range(2 * N + 1):
            row = gf + 1
            if gf % 2 == 0:
                grid.setRowMinimumHeight(row, TAM_CUADRA)
                grid.setRowStretch(row, 2)
            else:
                grid.setRowMinimumHeight(row, TAM_CALLE)
                grid.setRowStretch(row, 0)

        for gc in range(2 * N + 1):
            col = gc + 1
            if gc % 2 == 0:
                grid.setColumnMinimumWidth(col, TAM_CUADRA)
                grid.setColumnStretch(col, 2)
            else:
                grid.setColumnMinimumWidth(col, TAM_CALLE)
                grid.setColumnStretch(col, 0)

        self.layout_principal.addWidget(contenedor)

    def _crear_overlay(self):
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,160);")
        self.overlay.hide()
        self.overlay.mousePressEvent = lambda e: self.ocultar_menu()

    def _crear_menu(self):
        self.menu_lateral = MenuLateral(self)
        self.menu_lateral.btn_cerrar.clicked.connect(self.ocultar_menu)
        self.menu_lateral.setGeometry(-300, 0, 300, self.height())

    def resizeEvent(self, event):
        self.overlay.setGeometry(self.rect())
        x = self.menu_lateral.geometry().x()
        self.menu_lateral.setGeometry(x, 0, 300, self.height())
        super().resizeEvent(event)

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
                font-size: 13px;
                font-weight: 700;
                background-color: transparent;
            }
        """)