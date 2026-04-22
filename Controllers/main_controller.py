from UI.agregar_incidencias import AgregarIncidencias
from models.mapa_model import MapaModel


class ControladorPrincipal:

    def __init__(self, vista):
        self.vista  = vista
        self.modelo = MapaModel()
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.vista.boton_menu.clicked.connect(self.vista.mostrar_menu)
        self.vista.menu_lateral.btn_cerrar.clicked.connect(self.vista.ocultar_menu)
        self.vista.overlay.mousePressEvent = self._click_overlay
        self.vista.menu_lateral.btn_calcular.clicked.connect(self.calcular_ruta)
        self.vista.menu_lateral.btn_incidencia.clicked.connect(self.abrir_agregar_incidencia)

    def _click_overlay(self, event):
        self.vista.ocultar_menu()

    def calcular_ruta(self):
        inicio  = self.vista.menu_lateral.input_inicio.text().strip()
        destino = self.vista.menu_lateral.input_destino.text().strip()

        if not inicio or not destino:
            print("[ERROR] Ingresa el punto de partida y el destino.")
            return

        if not self.modelo.coordenada_valida(inicio):
            print(f"[ERROR] Coordenada de inicio inválida: {inicio}")
            return

        if not self.modelo.coordenada_valida(destino):
            print(f"[ERROR] Coordenada de destino inválida: {destino}")
            return

        self.vista.limpiar_ruta()
        self.vista.menu_lateral.ocultar_resultados()
        self.modelo.set_inicio(inicio)
        self.modelo.set_destino(destino)

        camino = self.modelo.calcular_ruta()

        if camino is None:
            print(f"[SIN RUTA] No existe camino de {inicio} a {destino}.")
            return

        self.vista.pintar_ruta(camino)
        self.vista.menu_lateral.mostrar_resultados(
            self.modelo.distancia_texto(),
            self.modelo.tiempo_texto()
        )
        print(f"Ruta: {' → '.join(camino)}")
        print(f"Distancia: {self.modelo.distancia_texto()} | Tiempo: {self.modelo.tiempo_texto()}")

    def abrir_agregar_incidencia(self):
        dialogo = AgregarIncidencias(self.vista)

        if dialogo.exec():
            ubicacion   = dialogo.get_ubicacion().strip()
            tipo        = dialogo.get_tipo()
            descripcion = dialogo.get_descripcion()

            if not self.modelo.coordenada_valida(ubicacion):
                print(f"[ERROR] Coordenada inválida: {ubicacion}")
                return

            self.modelo.agregar_incidencia(ubicacion, tipo, descripcion)
            clave = self.modelo.normalizar(ubicacion)
            self.vista.nodos[clave].set_estado("incidencia")
            print(f"Incidencia '{tipo}' en {clave}: {descripcion}")

    def salir(self):
        self.vista.close()