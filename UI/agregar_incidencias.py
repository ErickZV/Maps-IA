from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QTextEdit, QPushButton, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt

class AgregarIncidencias(QDialog):
    """
    Permite al usuario ingresar la ubicación (coordenada), el tipo
    de incidencia y una descripción opcional. Al confirmar, el
    controlador recupera los datos mediante los métodos getter.
    """

    def __init__(self, parent=None):
        """
        Inicializa el diálogo sin bordes nativos y con fondo transparente
        para que el contenedor con border-radius se vea correctamente.

        Args:
            parent: Widget padre, osea la VentanaPrincipal.
        """
        super().__init__(parent)

        # Sin barra de título nativa — usamos nuestro propio encabezado
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        # Fondo transparente para que el border-radius del contenedor sea visible
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(420, 380)

        self.crearUI()
        self.crearEstilos()

    def crearUI(self):
        """
        Construye y organiza todos los widgets del diálogo:
        título, botón de cierre, campos de entrada y botón de confirmación.
        """
        # Contenedor principal — recibe el fondo y el borde redondeado via CSS
        self.contenedor = QWidget(self)
        self.contenedor.setObjectName("contenedor")
        self.contenedor.setGeometry(0, 0, 420, 380)

        layout = QVBoxLayout(self.contenedor)
        layout.setContentsMargins(30, 25, 30, 30)
        layout.setSpacing(14)

        # ── Fila superior: título + botón X ──
        fila_titulo = QHBoxLayout()

        self.lbl_titulo = QLabel("Agrega una incidencia")
        self.lbl_titulo.setObjectName("titulo")

        # Botón X — cierra el diálogo sin guardar (reject)
        self.btn_cerrar = QPushButton("X")
        self.btn_cerrar.setObjectName("btnCerrar")
        self.btn_cerrar.setFixedSize(32, 32)
        self.btn_cerrar.clicked.connect(self.reject)

        fila_titulo.addWidget(self.lbl_titulo)
        fila_titulo.addStretch()
        fila_titulo.addWidget(self.btn_cerrar)

        # ── Campo: coordenada de la incidencia (ej. 'A1', 'C5') ──
        self.input_ubicacion = QLineEdit()
        self.input_ubicacion.setPlaceholderText("Agrega la ubicacion del incidente")
        self.input_ubicacion.setFixedHeight(42)

        # ── Combo: tipo de incidencia ──
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

        # ── Campo: descripción opcional del incidente ──
        self.input_descripcion = QTextEdit()
        self.input_descripcion.setPlaceholderText("Agrega una descripcion del incidente (opcional)")
        self.input_descripcion.setFixedHeight(80)

        # ── Botón confirmar — acepta el diálogo y devuelve los datos ──
        self.btn_agregar = QPushButton("Agregar")
        self.btn_agregar.setObjectName("btnAgregar")
        self.btn_agregar.setFixedHeight(44)
        self.btn_agregar.clicked.connect(self.accept)

        # Ensamblar layout
        layout.addLayout(fila_titulo)
        layout.addSpacing(4)
        layout.addWidget(self.input_ubicacion)
        layout.addWidget(self.combo_tipo)
        layout.addWidget(self.input_descripcion)
        layout.addSpacing(4)
        layout.addWidget(self.btn_agregar)

    def crearEstilos(self):
        """
        Aplica los estilos CSS al diálogo y todos sus widgets hijos.
        """
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

    # ── Getters — usados por el controlador tras cerrar el diálogo ──

    def get_ubicacion(self) -> str:
        """
        Retorna la coordenada ingresada por el usuario, sin espacios.

        Returns:
            Cadena con la coordenada (ej. 'A1').
        """
        return self.input_ubicacion.text().strip()

    def get_tipo(self) -> str:
        """
        Retorna el tipo de incidencia seleccionado en el combo.

        Returns:
            Cadena con el tipo seleccionado (ej. 'Accidente').
        """
        return self.combo_tipo.currentText()

    def get_descripcion(self) -> str:
        """
        Retorna la descripción opcional ingresada por el usuario, sin espacios.

        Returns:
            Cadena con la descripción, o vacío si no se ingresó ninguna.
        """
        return self.input_descripcion.toPlainText().strip()