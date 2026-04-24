from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QGuiApplication

from UI.menu_lateral import MenuLateral

# ── Constantes del mapa ──────────────────────────────────────
CUADRAS    = 10          # Número de cuadras por eje (10x10)
TAM_CUADRA = 55          # Tamaño en píxeles de cada cuadra en el grid
TAM_CALLE  = 14          # Tamaño en píxeles de cada calle (espacio entre cuadras)
FILAS      = list("ABCDEFGHIJ")   # Identificadores de filas (eje Y)
COLS       = list(range(1, 11))   # Identificadores de columnas (eje X)


class CeldaCuadra(QWidget):
    """
    Widget que representa una cuadra (bloque construido) en el mapa.
    Se pinta en color morado y ocupa las posiciones pares del grid.
    """

    def __init__(self):
        super().__init__()
        # WA_StyledBackground permite que el stylesheet se aplique
        # correctamente sin heredar el fondo del widget padre
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QWidget { background-color: #b04acb; border-radius: 6px; }")


class CeldaCalle(QWidget):
    """
    Widget que representa el espacio de una calle entre dos cuadras.
    Cambia de color cuando forma parte de la ruta calculada (azul).
    Ocupa las posiciones impares del grid junto a posiciones pares.
    """

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._activa = False   # True cuando la celda forma parte de la ruta
        self._aplicar_estilo()

    def _aplicar_estilo(self):
        """Pinta la celda de azul si es parte de la ruta, negro si no lo es."""
        color = "#3b82f6" if self._activa else "#0d0d0d"
        self.setStyleSheet(f"QWidget {{ background-color: {color}; }}")

    def set_ruta(self, activa: bool):
        """
        Activa o desactiva el color de ruta en esta celda.

        Args:
            activa: True para pintar de azul, False para restaurar a negro.
        """
        self._activa = activa
        self._aplicar_estilo()


class NodoInterseccion(QWidget):
    """
    Widget que representa la intersección entre dos calles.
    Es el punto donde el usuario puede colocar inicio, destino o incidencias.
    Ocupa las posiciones impares en ambos ejes del grid.

    Estados posibles:
        - normal:     Gris oscuro (intersección libre)
        - inicio:     Blanco (punto de partida)
        - destino:    Verde (punto de llegada)
        - incidencia: Rojo (incidencia registrada)
        - ruta:       Azul (nodo intermedio de la ruta calculada)
    """

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(14, 14)
        self._estado = "normal"
        self._aplicar_estilo()

    def _aplicar_estilo(self):
        """Aplica el stylesheet correspondiente al estado actual del nodo."""
        estilos = {
            "normal":     "QWidget { background-color: #555555; border-radius: 7px; }",
            "inicio":     "QWidget { background-color: white;   border-radius: 7px; }",
            "destino":    "QWidget { background-color: #27ae60; border-radius: 7px; }",
            "incidencia": "QWidget { background-color: #e74c3c; border-radius: 7px; }",
            "ruta":       "QWidget { background-color: #3b82f6; border-radius: 7px; }",
        }
        self.setStyleSheet(estilos.get(self._estado, estilos["normal"]))

    def set_estado(self, estado: str):
        """
        Cambia el estado visual del nodo y actualiza su apariencia.

        Args:
            estado: Uno de 'normal', 'inicio', 'destino', 'incidencia', 'ruta'.
        """
        self._estado = estado
        self._aplicar_estilo()

    def get_estado(self):
        """
        Retorna el estado visual actual del nodo.

        Returns:
            Cadena con el estado actual.
        """
        return self._estado


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal de la aplicación Maps IA.

    Contiene la barra superior, el mapa de cuadras e intersecciones,
    el overlay oscuro y el menú lateral deslizable. Expone los
    diccionarios de nodos y calles para que el controlador pueda
    actualizar el estado visual del mapa.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maps IA")
        self.resize(1200, 700)
        self._centrar()

        # Widget central obligatorio en QMainWindow
        self.widget_central = QWidget()
        self.widget_central.setObjectName("widgetCentral")
        self.setCentralWidget(self.widget_central)

        # Layout principal vertical sin márgenes ni espaciado
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        self._crear_barra()
        self._crear_mapa()
        self._crear_overlay()
        self._crear_menu()
        self._estilos()

    def _centrar(self):
        """Centra la ventana en la pantalla principal al iniciar."""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        geo = self.frameGeometry()
        geo.moveCenter(screen.center())
        self.move(geo.topLeft())

    # ── Barra superior ───────────────────────────────────────

    def _crear_barra(self):
        """
        Crea la barra superior de la ventana con el botón
        hamburguesa que abre el menú lateral.
        """
        barra = QWidget()
        barra.setObjectName("barraWidget")
        barra.setFixedHeight(56)

        layout = QHBoxLayout(barra)
        layout.setContentsMargins(10, 8, 10, 8)

        # Botón hamburguesa ☰ — conectado en el controlador
        self.boton_menu = QPushButton("☰")
        self.boton_menu.setObjectName("botonMenu")
        self.boton_menu.setFixedSize(40, 40)

        layout.addWidget(self.boton_menu)
        layout.addStretch()
        self.layout_principal.addWidget(barra)

    # ── Mapa ─────────────────────────────────────────────────

    def _crear_mapa(self):
        """
        Crea el contenedor del mapa y delega la construcción
        del grid, las etiquetas y los tamaños a métodos auxiliares.

        Diccionarios que expone:
            self.nodos:   {clave: NodoInterseccion}  — intersecciones seleccionables
            self.cuadras: {(gf, gc): CeldaCuadra}    — bloques del mapa
            self.calles:  {(nodoA, nodoB): CeldaCalle} — segmentos de calle
        """
        contenedor = QWidget()
        contenedor.setObjectName("contenedorMapa")
        contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        grid = QGridLayout(contenedor)
        grid.setSpacing(0)
        grid.setContentsMargins(20, 10, 20, 20)

        # Diccionarios de acceso rápido a los widgets del mapa
        self.nodos   = {}   # "A1" → NodoInterseccion
        self.cuadras = {}   # (gf, gc) → CeldaCuadra
        self.calles  = {}   # (nodoA, nodoB) ordenado → CeldaCalle

        self._poblar_grid(grid)
        self._agregar_etiquetas(grid)
        self._configurar_tamanos(grid)

        self.layout_principal.addWidget(contenedor)

    def _poblar_grid(self, grid):
        """
        Itera sobre todas las posiciones del grid (2N+1 x 2N+1)
        y delega la creación de cada celda a _agregar_celda.

        Args:
            grid: QGridLayout del contenedor del mapa.
        """
        N = CUADRAS
        for gf in range(2 * N + 1):
            for gc in range(2 * N + 1):
                self._agregar_celda(grid, gf, gc)

    def _agregar_celda(self, grid, gf, gc):
        """
        Determina el tipo de celda según la paridad de sus índices
        y llama al método de creación correspondiente.

        Regla de paridad:
            par  + par   → cuadra
            impar+ impar → nodo de intersección
            otro         → segmento de calle

        Args:
            grid: QGridLayout destino.
            gf:   Índice de fila en el grid lógico (0 a 2N).
            gc:   Índice de columna en el grid lógico (0 a 2N).
        """
        es_fila_cuadra = (gf % 2 == 0)
        es_col_cuadra  = (gc % 2 == 0)

        # +1 en ambos ejes porque la fila/col 0 está reservada para etiquetas
        wr = gf + 1
        wc = gc + 1

        if es_fila_cuadra and es_col_cuadra:
            self._agregar_cuadra(grid, gf, gc, wr, wc)
        elif not es_fila_cuadra and not es_col_cuadra:
            self._agregar_nodo(grid, gf, gc, wr, wc)
        else:
            self._agregar_calle(grid, gf, gc, wr, wc, es_fila_cuadra)

    def _agregar_cuadra(self, grid, gf, gc, wr, wc):
        """
        Crea una CeldaCuadra, la añade al grid y la registra
        en el diccionario de cuadras.

        Args:
            grid: QGridLayout destino.
            gf, gc: Índices lógicos de la posición.
            wr, wc: Índices reales en el grid (con offset de etiquetas).
        """
        w = CeldaCuadra()
        grid.addWidget(w, wr, wc)
        self.cuadras[(gf, gc)] = w

    def _agregar_nodo(self, grid, gf, gc, wr, wc):
        """
        Crea un NodoInterseccion, lo envuelve en un contenedor centrado,
        lo añade al grid y lo registra en el diccionario de nodos.

        La clave del nodo se forma con la letra de la fila y el número
        de columna correspondiente (ej. gf=1, gc=1 → 'A1').

        Args:
            grid: QGridLayout destino.
            gf, gc: Índices lógicos de la posición.
            wr, wc: Índices reales en el grid.
        """
        letra  = FILAS[gf // 2]   # gf=1→A, gf=3→B, gf=5→C ...
        numero = gc // 2 + 1      # gc=1→1, gc=3→2, gc=5→3 ...
        clave  = f"{letra}{numero}"

        nodo = NodoInterseccion()
        self.nodos[clave] = nodo

        # Contenedor negro centrado para que el nodo no se estire con el grid
        wrap = QWidget()
        wrap.setAttribute(Qt.WA_StyledBackground, True)
        wrap.setStyleSheet("QWidget { background-color: #0d0d0d; }")
        wl = QHBoxLayout(wrap)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.setAlignment(Qt.AlignCenter)
        wl.addWidget(nodo)
        grid.addWidget(wrap, wr, wc)

    def _agregar_calle(self, grid, gf, gc, wr, wc, es_fila_cuadra):
        """
        Crea una CeldaCalle, la añade al grid y la registra en el
        diccionario de calles con la clave de los dos nodos que conecta.

        Args:
            grid: QGridLayout destino.
            gf, gc: Índices lógicos de la posición.
            wr, wc: Índices reales en el grid.
            es_fila_cuadra: True si gf es par (calle entre filas de cuadras).
        """
        celda = CeldaCalle()
        grid.addWidget(celda, wr, wc)

        # Delegar el registro según orientación de la calle
        if es_fila_cuadra:
            self._registrar_calle_vertical(celda, gf, gc)
        else:
            self._registrar_calle_horizontal(celda, gf, gc)

    def _registrar_calle_vertical(self, celda, gf, gc):
        """
        Registra una celda de calle vertical (entre dos nodos de
        la misma columna, filas consecutivas).

        Args:
            celda: CeldaCalle a registrar.
            gf:    Índice de fila par (entre dos filas de nodos).
            gc:    Índice de columna impar (columna de nodos).
        """
        ci = gc // 2          # índice de columna lógica
        c  = COLS[ci]
        fi = gf // 2 - 1      # fila lógica superior del segmento

        if 0 <= fi and fi + 1 < CUADRAS:
            key = tuple(sorted([f"{FILAS[fi]}{c}", f"{FILAS[fi + 1]}{c}"]))
            self.calles[key] = celda

    def _registrar_calle_horizontal(self, celda, gf, gc):
        """
        Registra una celda de calle horizontal (entre dos nodos de
        la misma fila, columnas consecutivas).

        Args:
            celda: CeldaCalle a registrar.
            gf:    Índice de fila impar (fila de nodos).
            gc:    Índice de columna par (entre dos columnas de nodos).
        """
        fi = gf // 2          # índice de fila lógica
        ci = gc // 2 - 1      # índice de columna lógica izquierda del segmento

        if 0 <= ci and ci + 1 < CUADRAS:
            key = tuple(sorted([f"{FILAS[fi]}{COLS[ci]}", f"{FILAS[fi]}{COLS[ci + 1]}"]))
            self.calles[key] = celda

    def _agregar_etiquetas(self, grid):
        """
        Agrega las etiquetas de números (fila 0) y letras (columna 0)
        alineadas sobre las calles del mapa para identificar cada eje.

        Args:
            grid: QGridLayout del mapa.
        """
        # Números 1-10 sobre cada columna de intersecciones
        for i in range(CUADRAS):
            gc = 2 * i + 1   # columna impar = columna de nodos
            lbl = QLabel(str(i + 1))
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, gc + 1)

        # Letras A-J a la izquierda de cada fila de intersecciones
        for i in range(CUADRAS):
            gf = 2 * i + 1   # fila impar = fila de nodos
            lbl = QLabel(FILAS[i])
            lbl.setObjectName("etiquetaMapa")
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, gf + 1, 0)

    def _configurar_tamanos(self, grid):
        """
        Asigna tamaños mínimos y factores de estiramiento a todas
        las filas y columnas del grid para diferenciar cuadras de calles.

        - Cuadras (índice par):  TAM_CUADRA px, stretch 2
        - Calles  (índice impar): TAM_CALLE px, stretch 0 (tamaño fijo)
        - Fila/col 0 (etiquetas): 24 px, sin stretch

        Args:
            grid: QGridLayout del mapa.
        """
        # Columna y fila 0 reservadas para etiquetas
        grid.setColumnMinimumWidth(0, 24)
        grid.setRowMinimumHeight(0, 24)

        for gf in range(2 * CUADRAS + 1):
            row = gf + 1
            if gf % 2 == 0:   # fila de cuadras
                grid.setRowMinimumHeight(row, TAM_CUADRA)
                grid.setRowStretch(row, 2)
            else:              # fila de calles
                grid.setRowMinimumHeight(row, TAM_CALLE)
                grid.setRowStretch(row, 0)

        for gc in range(2 * CUADRAS + 1):
            col = gc + 1
            if gc % 2 == 0:   # columna de cuadras
                grid.setColumnMinimumWidth(col, TAM_CUADRA)
                grid.setColumnStretch(col, 2)
            else:              # columna de calles
                grid.setColumnMinimumWidth(col, TAM_CALLE)
                grid.setColumnStretch(col, 0)

    # ── Pintar / limpiar ruta ────────────────────────────────

    def pintar_ruta(self, camino: list):
        """
        Pinta visualmente la ruta en el mapa coloreando los nodos
        y las celdas de calle que forman el camino calculado.

        - Primer nodo  → estado 'inicio'  (blanco)
        - Último nodo  → estado 'destino' (verde)
        - Nodos medios → estado 'ruta'    (azul)
        - Calles entre nodos consecutivos → azul

        Args:
            camino: Lista ordenada de claves de nodos (ej. ['A1', 'A2', 'B2']).
        """
        for i, nodo in enumerate(camino):
            if i == 0:
                self.nodos[nodo].set_estado("inicio")
            elif i == len(camino) - 1:
                self.nodos[nodo].set_estado("destino")
            else:
                self.nodos[nodo].set_estado("ruta")

            # Pintar el segmento de calle entre el nodo anterior y el actual
            if i > 0:
                key = tuple(sorted([camino[i - 1], nodo]))
                if key in self.calles:
                    self.calles[key].set_ruta(True)

    def limpiar_ruta(self):
        """
        Restaura todos los nodos y celdas de calle a su estado
        visual original, eliminando cualquier ruta pintada.
        """
        for nodo in self.nodos.values():
            nodo.set_estado("normal")
        for calle in self.calles.values():
            calle.set_ruta(False)

    # ── Overlay ──────────────────────────────────────────────

    def _crear_overlay(self):
        """
        Crea el widget semitransparente oscuro que cubre el mapa
        cuando el menú lateral está abierto. Al hacer clic sobre
        él, se cierra el menú.
        """
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,160);")
        self.overlay.hide()
        # Cerrar el menú al hacer clic fuera de él
        self.overlay.mousePressEvent = lambda e: self.ocultar_menu()

    # ── Menú lateral ─────────────────────────────────────────

    def _crear_menu(self):
        """
        Instancia el MenuLateral y lo posiciona fuera de la pantalla
        (x = -300) para que la animación de entrada lo deslice desde la izquierda.
        """
        self.menu_lateral = MenuLateral(self)
        self.menu_lateral.btn_cerrar.clicked.connect(self.ocultar_menu)
        self.menu_lateral.setGeometry(-300, 0, 300, self.height())

    def resizeEvent(self, event):
        """
        Ajusta el tamaño del overlay y la posición del menú lateral
        cada vez que la ventana cambia de tamaño.
        """
        self.overlay.setGeometry(self.rect())
        x = self.menu_lateral.geometry().x()
        self.menu_lateral.setGeometry(x, 0, 300, self.height())
        super().resizeEvent(event)

    def mostrar_menu(self):
        """
        Muestra el overlay y desliza el menú lateral hacia adentro
        con una animación de 300 ms con easing OutCubic.
        """
        self.overlay.setGeometry(self.rect())
        self.overlay.show()

        # El overlay debe quedar detrás del menú lateral
        self.overlay.lower()
        self.menu_lateral.raise_()

        self.anim = QPropertyAnimation(self.menu_lateral, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(QRect(-300, 0, 300, self.height()))
        self.anim.setEndValue(QRect(0, 0, 300, self.height()))
        self.anim.start()

    def ocultar_menu(self):
        """
        Desliza el menú lateral hacia afuera con una animación de
        300 ms con easing InCubic y oculta el overlay al terminar.
        """
        self.anim = QPropertyAnimation(self.menu_lateral, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setStartValue(QRect(0, 0, 300, self.height()))
        self.anim.setEndValue(QRect(-300, 0, 300, self.height()))
        self.anim.start()
        self.overlay.hide()

    # ── Estilos globales ─────────────────────────────────────

    def _estilos(self):
        """
        Aplica el stylesheet global de la ventana principal.
        Solo afecta a widgets identificados por objectName para
        no interferir con los estilos propios de los subwidgets.
        """
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