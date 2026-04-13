class MapaModel:

    ESTILO_NORMAL     = "background-color: #b04acb; border-radius: 8px;"
    ESTILO_INICIO     = "background-color: white;   border-radius: 8px;"
    ESTILO_DESTINO    = "background-color: #27ae60;  border-radius: 8px;"
    ESTILO_INCIDENCIA = "background-color: #e74c3c;  border-radius: 8px;"

    FILAS = list("ABCDEFGHIJ")
    COLS  = list(range(1, 11))

    def __init__(self):
        self.inicio     = None
        self.destino    = None
        self.incidencias = {}   # clave -> tipo

    # ── Validación ──────────────────────────────────────────

    def coordenada_valida(self, coord: str) -> bool:
        if len(coord) < 2:
            return False
        letra = coord[0].upper()
        numero = coord[1:]
        return letra in self.FILAS and numero.isdigit() and int(numero) in self.COLS

    def normalizar(self, coord: str) -> str:
        return coord[0].upper() + coord[1:]

    # ── Setters ─────────────────────────────────────────────

    def set_inicio(self, coord: str):
        self.inicio = self.normalizar(coord)

    def set_destino(self, coord: str):
        self.destino = self.normalizar(coord)

    def agregar_incidencia(self, coord: str, tipo: str, descripcion: str = ""):
        clave = self.normalizar(coord)
        self.incidencias[clave] = {"tipo": tipo, "descripcion": descripcion}

    # ── Reset ────────────────────────────────────────────────

    def limpiar(self):
        self.inicio    = None
        self.destino   = None
        self.incidencias = {}