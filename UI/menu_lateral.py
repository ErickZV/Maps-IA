from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class MenuLateral(QWidget):
    """
    Panel lateral deslizable que contiene los controles principales
    de la aplicación: campos de inicio y destino, botón de incidencias,
    panel de resultados y botones de acción.

    Se muestra y oculta mediante animación desde VentanaPrincipal.
    """

    def __init__(self, parent=None):
        """
        Inicializa el menú lateral con fondo sólido forzado mediante
        QPalette, evitando que el stylesheet del padre lo sobreescriba.

        Args:
            parent: Widget padre, normalmente la VentanaPrincipal.
        """
        super().__init__(parent)
        self.setObjectName("menuLateral")
        self.setFixedWidth(300)

        # Necesario para que el stylesheet propio del widget se aplique
        # correctamente cuando es hijo de otro widget con estilo global
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        # Forzar fondo sólido mediante paleta para evitar transparencias
        paleta = self.palette()
        paleta.setColor(QPalette.Window, QColor("#1e1e2e"))
        self.setPalette(paleta)

        self.crearUI()
        self.crearEstilos()

    def crearUI(self):
        """
        Construye y organiza todos los widgets del menú lateral:
        título, campos de texto, botones y panel de resultados.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 20)
        layout.setSpacing(15)

        # ── Título de la aplicación ──
        self.titulo = QLabel("MAPS - IA")

        # ── Campo: coordenada del punto de partida ──
        self.input_inicio = QLineEdit()
        self.input_inicio.setPlaceholderText("Ingresa el punto de partida")
        self.input_inicio.setFixedHeight(40)

        # ── Campo: coordenada del punto de destino ──
        self.input_destino = QLineEdit()
        self.input_destino.setPlaceholderText("Ingresa el punto de destino")
        self.input_destino.setFixedHeight(40)

        # ── Botón: abre el diálogo para registrar incidencias ──
        self.btn_incidencia = QPushButton("Agregar incidencias")

        # ── Panel de resultados ──
        # Se mantiene oculto hasta que se calcula una ruta exitosa
        self.panel_resultados = QFrame()
        self.panel_resultados.setObjectName("panelResultados")
        self.panel_resultados.hide()

        panel_layout = QVBoxLayout(self.panel_resultados)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(8)

        # Título interno del panel de resultados
        lbl_titulo_panel = QLabel("Resultado")
        lbl_titulo_panel.setObjectName("tituloPanel")

        # Etiqueta que muestra la distancia total de la ruta
        self.lbl_distancia = QLabel("Distancia: —")
        self.lbl_distancia.setObjectName("datoPanel")

        # Etiqueta que muestra el tiempo estimado del recorrido
        self.lbl_tiempo = QLabel("Tiempo estimado: —")
        self.lbl_tiempo.setObjectName("datoPanel")

        panel_layout.addWidget(lbl_titulo_panel)
        panel_layout.addWidget(self.lbl_distancia)
        panel_layout.addWidget(self.lbl_tiempo)

        # ── Botón: ejecuta el cálculo de ruta ──
        self.btn_calcular = QPushButton("Calcular viaje")

        # ── Botón: cierra el menú lateral sin realizar acciones ──
        self.btn_cerrar = QPushButton("Cerrar")

        # Altura uniforme para todos los botones
        for b in [self.btn_incidencia, self.btn_calcular, self.btn_cerrar]:
            b.setFixedHeight(40)

        # ── Ensamblar layout vertical ──
        layout.addWidget(self.titulo)
        layout.addSpacing(20)
        layout.addWidget(self.input_inicio)
        layout.addWidget(self.input_destino)
        layout.addSpacing(10)
        layout.addWidget(self.btn_incidencia)
        layout.addWidget(self.panel_resultados)   # aparece entre incidencias y calcular
        layout.addStretch()                        # empuja los botones de acción al fondo
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.btn_cerrar)

    def mostrar_resultados(self, distancia: str, tiempo: str):
        """
        Actualiza las etiquetas del panel de resultados y lo hace visible.
        Se llama desde el controlador tras un cálculo de ruta exitoso.

        Args:
            distancia: Cadena con la distancia formateada (ej. '350 m').
            tiempo:    Cadena con el tiempo formateado (ej. '2 min 30 seg').
        """
        self.lbl_distancia.setText(f"Distancia: {distancia}")
        self.lbl_tiempo.setText(f"Tiempo estimado: {tiempo}")
        self.panel_resultados.show()

    def ocultar_resultados(self):
        """
        Oculta el panel de resultados.
        Se llama antes de cada nuevo cálculo para limpiar el estado visual.
        """
        self.panel_resultados.hide()

    def crearEstilos(self):
        """
        Aplica los estilos CSS al menú lateral y todos sus widgets hijos.
        """
        self.setStyleSheet("""
            QWidget#menuLateral {
                background-color: #1e1e2e;
                border-right: 2px solid #7d3cff;
            }
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2a2a3e;
                color: white;
                border: 2px solid #7d3cff;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #a855f7;
            }
            QPushButton {
                background-color: #7d3cff;
                color: white;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #9b59b6; }
            QPushButton:pressed { background-color: #5b21b6; }

            QFrame#panelResultados {
                background-color: #2a2a3e;
                border: 1.5px solid #7d3cff;
                border-radius: 10px;
            }
            QLabel#tituloPanel {
                color: #a855f7;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#datoPanel {
                color: white;
                font-size: 12px;
                font-weight: normal;
            }
        """)