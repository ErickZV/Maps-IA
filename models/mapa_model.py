from models.grafo_model import construir_grafo, dijkstra

FILAS = list("ABCDEFGHIJ")
COLS  = list(range(1, 11))


class MapaModel:

    def __init__(self):
        self.inicio      = None
        self.destino     = None
        self.incidencias = {}
        self.grafo       = construir_grafo()
        self.ruta        = []   # lista de nodos del camino actual

    def coordenada_valida(self, coord: str) -> bool:
        if len(coord) < 2:
            return False
        letra  = coord[0].upper()
        numero = coord[1:]
        return (
            letra in FILAS
            and numero.isdigit()
            and int(numero) in COLS
        )

    def normalizar(self, coord: str) -> str:
        return coord[0].upper() + coord[1:]

    def set_inicio(self, coord: str):
        self.inicio = self.normalizar(coord)

    def set_destino(self, coord: str):
        self.destino = self.normalizar(coord)

    def calcular_ruta(self) -> list | None:
        if not self.inicio or not self.destino:
            return None
        self.ruta = dijkstra(self.grafo, self.inicio, self.destino) or []
        return self.ruta if self.ruta else None

    def agregar_incidencia(self, coord: str, tipo: str, descripcion: str = ""):
        clave = self.normalizar(coord)
        self.incidencias[clave] = {"tipo": tipo, "descripcion": descripcion}

    def limpiar(self):
        self.inicio      = None
        self.destino     = None
        self.incidencias = {}
        self.ruta        = []