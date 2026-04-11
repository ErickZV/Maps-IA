from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QTextEdit, QPushButton, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AgregarIncidencias(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(420, 380)

        self.crearUI()
        self.crearEstilos()

    def crearUI(self):
        # Contenedor principal con fondo
        self.contenedor = QWidget(self)
        self.contenedor.setObjectName("contenedor")
        self.contenedor.setGeometry(0, 0, 420, 380)

        layout = QVBoxLayout(self.contenedor)
        layout.setContentsMargins(30, 25, 30, 30)
        layout.setSpacing(14)

        # ── título + botón X ──
        fila_titulo = QHBoxLayout()

        self.lbl_titulo = QLabel("Agrega una indicencia")
        self.lbl_titulo.setObjectName("titulo")

        self.btn_cerrar = QPushButton("X")
        self.btn_cerrar.setObjectName("btnCerrar")
        self.btn_cerrar.setFixedSize(32, 32)
        self.btn_cerrar.clicked.connect(self.reject)

        fila_titulo.addWidget(self.lbl_titulo)
        fila_titulo.addStretch()
        fila_titulo.addWidget(self.btn_cerrar)

        # ── Inputs ──
        self.input_ubicacion = QLineEdit()
        self.input_ubicacion.setPlaceholderText("Agrega la ubicacion del incidente")
        self.input_ubicacion.setFixedHeight(42)

        self.combo_tipo = QComboBox()
        self.combo_tipo.setPlaceholderText("Selecciona el tipo de incidente")
        self.combo_tipo.setFixedHeight(42)
        self.combo_tipo.addItems([
            "Accidente",
            "Obra vial",
            "Corte de calle",
            "Inundación",
            "Otro",
        ])

        self.input_descripcion = QTextEdit()
        self.input_descripcion.setPlaceholderText("Agrega una descripcion del incidente (opcional)")
        self.input_descripcion.setFixedHeight(80)

        # ── Botón agregar ──
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setObjectName("btnAgregar")
        self.btn_agregar.setFixedHeight(44)

        layout.addLayout(fila_titulo)
        layout.addSpacing(4)
        layout.addWidget(self.input_ubicacion)
        layout.addWidget(self.combo_tipo)
        layout.addWidget(self.input_descripcion)
        layout.addSpacing(4)
        layout.addWidget(self.btn_agregar)

    def crearEstilos(self):
        self.setStyleSheet("""
            QWidget#contenedor {
                background-color: #1a1a2e;
                border-radius: 16px;
                border: 1.5px solid #7d3cff;
            }

            QLabel#titulo {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }

            QPushButton#btnCerrar {
                background-color: #c0392b;
                color: white;
                border-radius: 16px;
                font-weight: bold;
                font-size: 13px;
            }

            QPushButton#btnCerrar:hover {
                background-color: #e74c3c;
            }

            QLineEdit, QComboBox, QTextEdit {
                background-color: transparent;
                color: white;
                border: 2px solid #c039d4;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 13px;
            }

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 2px solid #a855f7;
            }

            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #c039d4;
                width: 0;
                height: 0;
            }

            QComboBox QAbstractItemView {
                background-color: #1a1a2e;
                color: white;
                selection-background-color: #7d3cff;
                border: 1px solid #7d3cff;
            }

            QPushButton#btnAgregar {
                background-color: #c039d4;
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#btnAgregar:hover {
                background-color: #a855f7;
            }

            QPushButton#btnAgregar:pressed {
                background-color: #7d3cff;
            }
        """)

    # ── Getters para el controller ──
    def get_ubicacion(self) -> str:
        return self.input_ubicacion.text().strip()

    def get_tipo(self) -> str:
        return self.combo_tipo.currentText()

    def get_descripcion(self) -> str:
        return self.input_descripcion.toPlainText().strip()