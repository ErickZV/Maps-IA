from UI.agregar_incidencias import AgregarIncidencias


class ControladorPrincipal:

    def __init__(self, vista):
        self.vista = vista
        self._conectar_eventos()

    def _conectar_eventos(self):

        # -------- MENÚ LATERAL --------
        self.vista.boton_menu.clicked.connect(self.vista.mostrar_menu)
        self.vista.menu_lateral.btn_cerrar.clicked.connect(self.vista.ocultar_menu)
        self.vista.overlay.mousePressEvent = self._click_overlay

        # -------- BOTONES DEL MENÚ --------
        self.vista.menu_lateral.btn_calcular.clicked.connect(self.calcular_ruta)
        self.vista.menu_lateral.btn_incidencia.clicked.connect(self.agregar_incidencia)

    # -------- EVENTOS UI --------

    def _click_overlay(self, event):
        self.vista.ocultar_menu()

    # -------- LÓGICA --------

    def calcular_ruta(self):
        inicio = self.vista.menu_lateral.input_inicio.text().strip().upper()
        destino = self.vista.menu_lateral.input_destino.text().strip().upper()

        if not inicio or not destino:
            print("Faltan datos")
            return

        if inicio not in self.vista.celdas or destino not in self.vista.celdas:
            print("Puntos inválidos")
            return

        print(f"Calculando ruta de {inicio} a {destino}")
        self.limpiar_mapa()

        self.vista.celdas[inicio].setStyleSheet("background-color: white; border-radius: 8px;")
        self.vista.celdas[destino].setStyleSheet("background-color: green; border-radius: 8px;")

    def agregar_incidencia(self):
        """
        Abre el diálogo, y si el usuario confirma,
        marca la celda ingresada como incidencia.
        """
        dialogo = AgregarIncidencias(self.vista)

        if dialogo.exec():
            ubicacion = dialogo.get_ubicacion().upper()
            tipo = dialogo.get_tipo()
            descripcion = dialogo.get_descripcion()

            if ubicacion not in self.vista.celdas:
                print(f"Ubicación inválida: {ubicacion}")
                return

            self.vista.celdas[ubicacion].setStyleSheet(
                "background-color: red; border-radius: 8px;"
            )
            print(f"Incidencia '{tipo}' agregada en {ubicacion}: {descripcion}")

    def limpiar_mapa(self):
        for celda in self.vista.celdas.values():
            celda.setStyleSheet("background-color: #b04acb; border-radius: 8px;")
        print("Mapa limpiado")

    def salir(self):
        self.vista.close()