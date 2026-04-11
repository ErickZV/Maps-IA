from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
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

        self._ui()
        self._estilos()

    def _ui(self):
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
        self.btn_calcular = QPushButton("Calcular viaje")
        self.btn_cerrar = QPushButton("Cerrar")

        for b in [self.btn_incidencia, self.btn_calcular, self.btn_cerrar]:
            b.setFixedHeight(40)

        layout.addWidget(self.titulo)
        layout.addSpacing(20)
        layout.addWidget(self.input_inicio)
        layout.addWidget(self.input_destino)
        layout.addSpacing(10)
        layout.addWidget(self.btn_incidencia)
        layout.addStretch()
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.btn_cerrar)

    def _estilos(self):
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

            QPushButton:hover {
                background-color: #9b59b6;
            }

            QPushButton:pressed {
                background-color: #5b21b6;
            }
        """)