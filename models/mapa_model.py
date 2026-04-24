from models.grafo_model import construir_grafo, dijkstra

# Filas del mapa representadas por letras (A-J)
FILAS = list("ABCDEFGHIJ")

# Columnas del mapa representadas por números (1-10)
COLS = list(range(1, 11))

# Velocidad promedio de circulación urbana
VELOCIDAD_KMH = 40
VELOCIDAD_MS  = VELOCIDAD_KMH * 1000 / 3600   # conversión a metros/segundo


class MapaModel:
    """
    Gestiona el estado de la aplicación: puntos de inicio y destino,
    incidencias registradas, y los resultados del cálculo de ruta
    (camino, distancia y tiempo estimado).
    """

    def __init__(self):
        self.inicio      = None   # Nodo de partida (ej. 'A1')
        self.destino     = None   # Nodo de llegada (ej. 'J10')
        self.incidencias = {}     # {clave: {tipo, descripcion}}
        self.grafo       = construir_grafo()   # Grafo dirigido de la ciudad
        self.ruta        = []     # Lista de nodos que forman el camino óptimo
        self.distancia_m = 0      # Distancia total de la ruta en metros
        self.tiempo_s    = 0      # Tiempo estimado de la ruta en segundos

    def coordenada_valida(self, coord: str) -> bool:
        """
        Verifica que una coordenada tenga el formato correcto (LetraNumero)
        y que exista dentro de los límites del mapa.

        Args:
            coord: Coordenada a validar (ej. 'A1', 'J10').

        Returns:
            True si la coordenada es válida, False en caso contrario.
        """
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
        """
        Convierte una coordenada a su forma canónica:
        primera letra en mayúscula seguida del número.

        Args:
            coord: Coordenada a normalizar (ej. 'a1', 'b3').

        Returns:
            Coordenada normalizada (ej. 'A1', 'B3').
        """
        return coord[0].upper() + coord[1:]

    def set_inicio(self, coord: str):
        """
        Establece el nodo de partida normalizando la coordenada.

        Args:
            coord: Coordenada del punto de inicio.
        """
        self.inicio = self.normalizar(coord)

    def set_destino(self, coord: str):
        """
        Establece el nodo de destino normalizando la coordenada.

        Args:
            coord: Coordenada del punto de destino.
        """
        self.destino = self.normalizar(coord)

    def calcular_ruta(self) -> list | None:
        """
        Ejecuta Dijkstra entre el inicio y el destino actuales,
        y almacena el camino, la distancia y el tiempo resultantes.

        Returns:
            Lista de nodos del camino óptimo, o None si no hay ruta posible
            o si falta alguno de los dos puntos.
        """
        # No calcular si falta alguno de los dos puntos
        if not self.inicio or not self.destino:
            return None

        camino, distancia = dijkstra(self.grafo, self.inicio, self.destino)

        # Si Dijkstra no encontró ruta, resetear resultados
        if camino is None:
            self.ruta        = []
            self.distancia_m = 0
            self.tiempo_s    = 0
            return None

        # Guardar resultados del cálculo
        self.ruta        = camino
        self.distancia_m = distancia
        self.tiempo_s    = distancia / VELOCIDAD_MS
        return camino

    def distancia_texto(self) -> str:
        """
        Formatea la distancia total para mostrarse en la UI.
        Usa kilómetros si supera los 1000 metros, metros en caso contrario.

        Returns:
            Cadena legible con la distancia (ej. '350 m' o '1.50 km').
        """
        if self.distancia_m >= 1000:
            return f"{self.distancia_m / 1000:.2f} km"
        return f"{int(self.distancia_m)} m"

    def tiempo_texto(self) -> str:
        """
        Formatea el tiempo estimado para mostrarse en la UI.
        Omite minutos o segundos si alguno es cero.

        Returns:
            Cadena legible con el tiempo (ej. '45 seg', '3 min', '2 min 30 seg').
        """
        minutos  = int(self.tiempo_s // 60)
        segundos = int(self.tiempo_s % 60)

        if minutos == 0:
            return f"{segundos} seg"
        if segundos == 0:
            return f"{minutos} min"
        return f"{minutos} min {segundos} seg"

    def agregar_incidencia(self, coord: str, tipo: str, descripcion: str = ""):
        """
        Registra una incidencia en el mapa en la coordenada indicada.

        Args:
            coord:       Coordenada donde ocurre la incidencia (ej. 'C5').
            tipo:        Tipo de incidencia (ej. 'Accidente', 'Obra vial').
            descripcion: Detalle opcional de la incidencia.
        """
        clave = self.normalizar(coord)
        self.incidencias[clave] = {"tipo": tipo, "descripcion": descripcion}

    def limpiar(self):
        """
        Reinicia todos los valores del modelo a su estado inicial.
        Se llama cuando el usuario solicita un nuevo cálculo de ruta.
        """
        self.inicio      = None
        self.destino     = None
        self.incidencias = {}
        self.ruta        = []
        self.distancia_m = 0
        self.tiempo_s    = 0