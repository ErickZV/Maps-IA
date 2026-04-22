from models.grafo_model import construir_grafo, dijkstra

FILAS            = list("ABCDEFGHIJ")
COLS             = list(range(1, 11))
VELOCIDAD_KMH    = 40
VELOCIDAD_MS     = VELOCIDAD_KMH * 1000 / 3600   # metros/segundo


class MapaModel:

    def __init__(self):
        self.inicio      = None
        self.destino     = None
        self.incidencias = {}
        self.grafo       = construir_grafo()
        self.ruta        = []
        self.distancia_m = 0      # metros
        self.tiempo_s    = 0      # segundos

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

        camino, distancia = dijkstra(self.grafo, self.inicio, self.destino)

        if camino is None:
            self.ruta        = []
            self.distancia_m = 0
            self.tiempo_s    = 0
            return None

        self.ruta        = camino
        self.distancia_m = distancia
        self.tiempo_s    = distancia / VELOCIDAD_MS
        return camino

    def distancia_texto(self) -> str:
        if self.distancia_m >= 1000:
            return f"{self.distancia_m / 1000:.2f} km"
        return f"{int(self.distancia_m)} m"

    def tiempo_texto(self) -> str:
        minutos = int(self.tiempo_s // 60)
        segundos = int(self.tiempo_s % 60)
        if minutos == 0:
            return f"{segundos} seg"
        if segundos == 0:
            return f"{minutos} min"
        return f"{minutos} min {segundos} seg"

    def agregar_incidencia(self, coord: str, tipo: str, descripcion: str = ""):
        clave = self.normalizar(coord)
        self.incidencias[clave] = {"tipo": tipo, "descripcion": descripcion}

    def limpiar(self):
        """
            Metodo para reiniciar los valores del sistema
            se llama cuando el usuario le de clic al boton de
            calcular
        """
        self.inicio      = None
        self.destino     = None
        self.incidencias = {}
        self.ruta        = []
        self.distancia_m = 0
        self.tiempo_s    = 0