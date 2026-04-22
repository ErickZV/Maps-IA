from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QGuiApplication

from UI.menu_lateral import MenuLateral

CUADRAS    = 10
TAM_CUADRA = 55
TAM_CALLE  = 14
FILAS      = list("ABCDEFGHIJ")
COLS       = list(range(1, 11))


class CeldaCuadra(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QWidget { background-color: #b04acb; border-radius: 6px; }")


class CeldaCalle(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._activa = False
        self._aplicar_estilo()

    def _aplicar_estilo(self):
        color = "#3b82f6" if self._activa else "#0d0d0d"
        self.setStyleSheet(f"QWidget {{ background-color: {color}; }}")

    def set_ruta(self, activa: bool):
        self._activa = activa
        self._aplicar_estilo()


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
            "ruta":       "QWidget { background-color: #3b82f6; border-radius: 7px; }",
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

    # ── Barra ────────────────────────────────────────────────

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

    # ── Mapa ─────────────────────────────────────────────────

    def _crear_mapa(self):
        contenedor = QWidget()
        contenedor.setObjectName("contenedorMapa")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        grid = QGridLayout(contenedor)
        grid.setSpacing(0)
        grid.setContentsMargins(20, 10, 20, 20)

        self.nodos   = {}
        self.cuadras = {}
        self.calles  = {}

        self._poblar_grid(grid)
        self._agregar_etiquetas(grid)
        self._configurar_tamanos(grid)

        self.layout_principal.addWidget(contenedor)

    def _poblar_grid(self, grid):
        N = CUADRAS
        for gf in range(2 * N + 1):
            for gc in range(2 * N + 1):
                self._agregar_celda(grid, gf, gc)

    def _agregar_celda(self, grid, gf, gc):
        es_fila_cuadra = (gf % 2 == 0)
        es_col_cuadra  = (gc % 2 == 0)
        wr = gf + 1
        wc = gc + 1

        if es_fila_cuadra and es_col_cuadra:
            self._agregar_cuadra(grid, gf, gc, wr, wc)
        elif not es_fila_cuadra and not es_col_cuadra:
            self._agregar_nodo(grid, gf, gc, wr, wc)
        else:
            self._agregar_calle(grid, gf, gc, wr, wc, es_fila_cuadra)

    def _agregar_cuadra(self, grid, gf, gc, wr, wc):
        w = CeldaCuadra()
        grid.addWidget(w, wr, wc)
        self.cuadras[(gf, gc)] = w

    def _agregar_nodo(self, grid, gf, gc, wr, wc):
        letra  = FILAS[gf // 2]
        numero = gc // 2 + 1
        clave  = f"{letra}{numero}"

        nodo = NodoInterseccion()
        self.nodos[clave] = nodo

        wrap = QWidget()
        wrap.setAttribute(Qt.WA_StyledBackground, True)
        wrap.setStyleSheet("QWidget { background-color: #0d0d0d; }")
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setAlignment(Qt.AlignCenter)
        wl.addWidget(nodo)
        grid.addWidget(wrap, wr, wc)

    def _agregar_calle(self, grid, gf, gc, wr, wc, es_fila_cuadra):
        celda = CeldaCalle()
        grid.addWidget(celda, wr, wc)

        if es_fila_cuadra:
            self._registrar_calle_vertical(celda, gf, gc)
        else:
            self._registrar_calle_horizontal(celda, gf, gc)

    def _registrar_calle_vertical(self, celda, gf, gc):
        ci = gc // 2
        c  = COLS[ci]
        fi = gf // 2 - 1
        if 0 <= fi and fi + 1 < CUADRAS:
            key = tuple(sorted([f"{FILAS[fi]}{c}", f"{FILAS[fi + 1]}{c}"]))
            self.calles[key] = celda

    def _registrar_calle_horizontal(self, celda, gf, gc):
        fi = gf // 2
        ci = gc // 2 - 1
        if 0 <= ci and ci + 1 < CUADRAS:
            key = tuple(sorted([f"{FILAS[fi]}{COLS[ci]}", f"{FILAS[fi]}{COLS[ci + 1]}"]))
            self.calles[key] = celda

    def _agregar_etiquetas(self, grid):
        for i in range(CUADRAS):
            gc = 2 * i + 1
            lbl = QLabel(str(i + 1))
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, gc + 1)

        for i in range(CUADRAS):
            gf = 2 * i + 1
            lbl = QLabel(FILAS[i])
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, gf + 1, 0)

    def _configurar_tamanos(self, grid):
        grid.setColumnMinimumWidth(0, 24)
        grid.setRowMinimumHeight(0, 24)

        for gf in range(2 * CUADRAS + 1):
            row = gf + 1
            if gf % 2 == 0:
                grid.setRowMinimumHeight(row, TAM_CUADRA)
                grid.setRowStretch(row, 2)
            else:
                grid.setRowMinimumHeight(row, TAM_CALLE)
                grid.setRowStretch(row, 0)

        for gc in range(2 * CUADRAS + 1):
            col = gc + 1
            if gc % 2 == 0:
                grid.setColumnMinimumWidth(col, TAM_CUADRA)
                grid.setColumnStretch(col, 2)
            else:
                grid.setColumnMinimumWidth(col, TAM_CALLE)
                grid.setColumnStretch(col, 0)    

    # ── Pintar ruta ──────────────────────────────────────────

    def pintar_ruta(self, camino: list):
        """
        Recibe la lista de nodos del camino (ej: ["A1","A2","B2"])
        y pinta de azul los nodos intermedios y las celdas de calle entre ellos.
        """
        for i, nodo in enumerate(camino):
            if i == 0:
                self.nodos[nodo].set_estado("inicio")
            elif i == len(camino) - 1:
                self.nodos[nodo].set_estado("destino")
            else:
                self.nodos[nodo].set_estado("ruta")

            # Pintar celda de calle entre nodo anterior y actual
            if i > 0:
                key = tuple(sorted([camino[i - 1], nodo]))
                if key in self.calles:
                    self.calles[key].set_ruta(True)

    def limpiar_ruta(self):
        for nodo in self.nodos.values():
            nodo.set_estado("normal")
        for calle in self.calles.values():
            calle.set_ruta(False)

    # ── Overlay ──────────────────────────────────────────────

    def _crear_overlay(self):
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,160);")
        self.overlay.hide()
        self.overlay.mousePressEvent = lambda e: self.ocultar_menu()

    # ── Menú ─────────────────────────────────────────────────

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

    # ── Estilos ──────────────────────────────────────────────

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