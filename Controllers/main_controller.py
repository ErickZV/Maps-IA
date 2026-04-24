from UI.agregar_incidencias import AgregarIncidencias
from models.mapa_model import MapaModel

class ControladorPrincipal:
    """
    Actúa como intermediario entre la vista (VentanaPrincipal)
    y el modelo (MapaModel), conectando los eventos de la UI
    con la lógica de negocio (Arquitectura MVC).
    """

    def __init__(self, vista):
        """
        Inicializa el controlador con la vista principal y crea
        una instancia del modelo. Luego conecta todos los eventos.

        Args:
            vista: Instancia de VentanaPrincipal.
        """
        self.vista  = vista
        self.modelo = MapaModel()
        self._conectar_eventos()

    def _conectar_eventos(self):
        """
        Conecta todos los botones y eventos de la UI con sus
        métodos correspondientes en el controlador.
        """
        # Botón hamburguesa — abre el menú lateral
        self.vista.boton_menu.clicked.connect(self.vista.mostrar_menu)

        # Botón cerrar del menú lateral — oculta el menú
        self.vista.menu_lateral.btn_cerrar.clicked.connect(self.vista.ocultar_menu)

        # Clic en el overlay oscuro — cierra el menú lateral
        self.vista.overlay.mousePressEvent = self._click_overlay

        # Botón calcular viaje — ejecuta el cálculo de ruta
        self.vista.menu_lateral.btn_calcular.clicked.connect(self.calcular_ruta)

        # Botón agregar incidencia — abre el diálogo de incidencias
        self.vista.menu_lateral.btn_incidencia.clicked.connect(self.abrir_agregar_incidencia)

    def _click_overlay(self, event):
        """
        Maneja el clic sobre el overlay oscuro que aparece
        cuando el menú lateral está abierto.

        Args:
            event: Evento de ratón de PySide6 (no se usa directamente).
        """
        self.vista.ocultar_menu()

    def calcular_ruta(self):
        """
        Orquesta el cálculo de la ruta óptima entre el inicio y el destino.

        Flujo:
            1. Lee y valida las coordenadas ingresadas por el usuario.
            2. Limpia el mapa y los resultados anteriores.
            3. Solicita al modelo el camino óptimo mediante Dijkstra.
            4. Pinta la ruta en el mapa y muestra distancia y tiempo en el menú.
        """
        # Leer coordenadas del menú lateral
        inicio  = self.vista.menu_lateral.input_inicio.text().strip()
        destino = self.vista.menu_lateral.input_destino.text().strip()

        # Validar que ambos campos estén llenos
        if not inicio or not destino:
            print("[ERROR] Ingresa el punto de partida y el destino.")
            return

        # Validar formato y existencia de la coordenada de inicio
        if not self.modelo.coordenada_valida(inicio):
            print(f"[ERROR] Coordenada de inicio inválida: {inicio}")
            return

        # Validar formato y existencia de la coordenada de destino
        if not self.modelo.coordenada_valida(destino):
            print(f"[ERROR] Coordenada de destino inválida: {destino}")
            return

        # Limpiar estado visual y resultados del cálculo anterior
        self.vista.limpiar_ruta()
        self.vista.menu_lateral.ocultar_resultados()

        # Actualizar el modelo con los nuevos puntos
        self.modelo.set_inicio(inicio)
        self.modelo.set_destino(destino)

        # Ejecutar Dijkstra a través del modelo
        camino = self.modelo.calcular_ruta()

        # Si no existe ruta válida respetando los sentidos de calle
        if camino is None:
            print(f"[SIN RUTA] No existe camino de {inicio} a {destino}.")
            return

        # Pintar la ruta en el mapa y mostrar resultados en el menú
        self.vista.pintar_ruta(camino)
        self.vista.menu_lateral.mostrar_resultados(
            self.modelo.distancia_texto(),
            self.modelo.tiempo_texto()
        )

        print(f"Ruta: {' → '.join(camino)}")
        print(f"Distancia: {self.modelo.distancia_texto()} | Tiempo: {self.modelo.tiempo_texto()}")

    def abrir_agregar_incidencia(self):
        """
        Abre el diálogo para registrar una nueva incidencia en el mapa.

        Flujo:
            1. Muestra el diálogo AgregarIncidencias.
            2. Si el usuario confirma, valida la coordenada ingresada.
            3. Registra la incidencia en el modelo y pinta el nodo en la vista.
        """
        dialogo = AgregarIncidencias(self.vista)

        # exec() retorna True si el usuario presionó 'Agregar'
        if dialogo.exec():
            ubicacion   = dialogo.get_ubicacion().strip()
            tipo        = dialogo.get_tipo()
            descripcion = dialogo.get_descripcion()

            # Validar que la coordenada ingresada exista en el mapa
            if not self.modelo.coordenada_valida(ubicacion):
                print(f"[ERROR] Coordenada inválida: {ubicacion}")
                return

            # Registrar en el modelo y actualizar el nodo en la vista
            self.modelo.agregar_incidencia(ubicacion, tipo, descripcion)
            clave = self.modelo.normalizar(ubicacion)
            self.vista.nodos[clave].set_estado("incidencia")

            print(f"Incidencia '{tipo}' en {clave}: {descripcion}")

    def salir(self):
        """
        Cierra la ventana principal y termina la aplicación.
        """
        self.vista.close()