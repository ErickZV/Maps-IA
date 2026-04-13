from UI.agregar_incidencias import AgregarIncidencias
from models.mapa_model import MapaModel


class ControladorPrincipal:

    def __init__(self, vista):
        self.vista  = vista
        self.modelo = MapaModel()
        self._conectar_eventos()

    # ── Conexión de eventos ──────────────────────────────────

    def _conectar_eventos(self):
        self.vista.boton_menu.clicked.connect(self.vista.mostrar_menu)
        self.vista.menu_lateral.btn_cerrar.clicked.connect(self.vista.ocultar_menu)
        self.vista.overlay.mousePressEvent = self._click_overlay

        self.vista.menu_lateral.btn_calcular.clicked.connect(self.calcular_ruta)
        self.vista.menu_lateral.btn_incidencia.clicked.connect(self.abrir_agregar_incidencia)

    def _click_overlay(self, event):
        self.vista.ocultar_menu()

    # ── Marcar inicio y destino ──────────────────────────────

    def calcular_ruta(self):
        inicio  = self.vista.menu_lateral.input_inicio.text().strip()
        destino = self.vista.menu_lateral.input_destino.text().strip()

        if not inicio or not destino:
            self._mostrar_error("Ingresa el punto de partida y el destino.")
            return

        if not self.modelo.coordenada_valida(inicio):
            self._mostrar_error(f"Coordenada de inicio inválida: {inicio}")
            return

        if not self.modelo.coordenada_valida(destino):
            self._mostrar_error(f"Coordenada de destino inválida: {destino}")
            return

        # Limpiar mapa antes de pintar
        self.limpiar_mapa()

        # Guardar en modelo
        self.modelo.set_inicio(inicio)
        self.modelo.set_destino(destino)

        # Pintar en vista
        self.vista.celdas[self.modelo.inicio].setStyleSheet(MapaModel.ESTILO_INICIO)
        self.vista.celdas[self.modelo.destino].setStyleSheet(MapaModel.ESTILO_DESTINO)

        # Volver a pintar incidencias (limpiar_mapa las borra visualmente)
        self._repintar_incidencias()

        print(f"Inicio: {self.modelo.inicio} | Destino: {self.modelo.destino}")

    # ── Agregar incidencia ───────────────────────────────────

    def abrir_agregar_incidencia(self):
        dialogo = AgregarIncidencias(self.vista)

        if dialogo.exec():
            ubicacion   = dialogo.get_ubicacion().strip()
            tipo        = dialogo.get_tipo()
            descripcion = dialogo.get_descripcion()

            if not self.modelo.coordenada_valida(ubicacion):
                self._mostrar_error(f"Coordenada inválida: {ubicacion}")
                return

            self.modelo.agregar_incidencia(ubicacion, tipo, descripcion)

            clave = self.modelo.normalizar(ubicacion)
            self.vista.celdas[clave].setStyleSheet(MapaModel.ESTILO_INCIDENCIA)

            print(f"Incidencia '{tipo}' en {clave}: {descripcion}")

    # ── Limpiar mapa ─────────────────────────────────────────

    def limpiar_mapa(self):
        for celda in self.vista.celdas.values():
            celda.setStyleSheet(MapaModel.ESTILO_NORMAL)
        self.modelo.limpiar()

    def _repintar_incidencias(self):
        for clave in self.modelo.incidencias:
            if clave in self.vista.celdas:
                self.vista.celdas[clave].setStyleSheet(MapaModel.ESTILO_INCIDENCIA)

    # ── Utilidades ───────────────────────────────────────────

    def _mostrar_error(self, mensaje: str):
        print(f"[ERROR] {mensaje}")

    def salir(self):
        self.vista.close()