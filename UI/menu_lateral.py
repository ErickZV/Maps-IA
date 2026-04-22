from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class MenuLateral(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("menuLateral")
        self.setFixedWidth(300)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        paleta = self.palette()
        paleta.setColor(QPalette.Window, QColor("#1e1e2e"))
        self.setPalette(paleta)

        self.crearUI()
        self.crearEstilos()

    def crearUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 20)
        layout.setSpacing(15)

        self.titulo = QLabel("MAPS - IA")

        self.input_inicio = QLineEdit()
        self.input_inicio.setPlaceholderText("Ingresa el punto de partida")
        self.input_inicio.setFixedHeight(40)

        self.input_destino = QLineEdit()
        self.input_destino.setPlaceholderText("Ingresa el punto de destino")
        self.input_destino.setFixedHeight(40)

        self.btn_incidencia = QPushButton("Agregar incidencias")

        # ── Panel de resultados ──
        self.panel_resultados = QFrame()
        self.panel_resultados.setObjectName("panelResultados")
        self.panel_resultados.hide()

        panel_layout = QVBoxLayout(self.panel_resultados)
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(8)

        lbl_titulo_panel = QLabel("Resultado")
        lbl_titulo_panel.setObjectName("tituloPanel")

        self.lbl_distancia = QLabel("Distancia: —")
        self.lbl_distancia.setObjectName("datoPanel")

        self.lbl_tiempo = QLabel("Tiempo estimado: —")
        self.lbl_tiempo.setObjectName("datoPanel")

        panel_layout.addWidget(lbl_titulo_panel)
        panel_layout.addWidget(self.lbl_distancia)
        panel_layout.addWidget(self.lbl_tiempo)

        self.btn_calcular = QPushButton("Calcular viaje")
        self.btn_cerrar   = QPushButton("Cerrar")

        for b in [self.btn_incidencia, self.btn_calcular, self.btn_cerrar]:
            b.setFixedHeight(40)

        layout.addWidget(self.titulo)
        layout.addSpacing(20)
        layout.addWidget(self.input_inicio)
        layout.addWidget(self.input_destino)
        layout.addSpacing(10)
        layout.addWidget(self.btn_incidencia)
        layout.addWidget(self.panel_resultados)   # ← entre incidencias y calcular
        layout.addStretch()
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.btn_cerrar)

    def mostrar_resultados(self, distancia: str, tiempo: str):
        self.lbl_distancia.setText(f"Distancia: {distancia}")
        self.lbl_tiempo.setText(f"Tiempo estimado: {tiempo}")
        self.panel_resultados.show()

    def ocultar_resultados(self):
        self.panel_resultados.hide()

    def crearEstilos(self):
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