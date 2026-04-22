import heapq

FILAS = list("ABCDEFGHIJ")
COLS  = list(range(1, 11))

DIST_HORIZONTAL = 100   # metros entre nodos en el eje horizontal
DIST_VERTICAL   = 50    # metros entre nodos en el eje vertical
VELOCIDAD_KMH   = 40    # velcoidad promedio a la que se movera el usuario
VELOCIDAD_MS    = VELOCIDAD_KMH * 1000 / 3600


def _sentido_horizontal(letra: str) -> str:
    """
    Determina el sentido de circulación de una calle horizontal.

    Las calles con índice par (A, C, E...) van hacia la derecha,
    las de índice impar (B, D, F...) van hacia la izquierda.

    Args:
        letra: Letra de la calle horizontal (ej. 'A', 'B').

    Returns:
        'derecha' o 'izquierda'.
    """
    return "derecha" if FILAS.index(letra) % 2 == 0 else "izquierda"


def _sentido_vertical(numero: int) -> str:
    """
    Determina el sentido de circulación de una calle vertical.

    Las calles con número impar (1, 3, 5...) van hacia abajo,
    las de número par (2, 4, 6...) van hacia arriba.

    Args:
        numero: Número de la calle vertical (ej. 1, 2).

    Returns:
        'abajo' o 'arriba'.
    """
    return "abajo" if numero % 2 != 0 else "arriba"


def _agregar_aristas_horizontales(grafo: dict) -> None:
    """
    Agrega al grafo las aristas correspondientes a las calles horizontales,
    respetando el sentido de circulación de cada una.

    Args:
        grafo: Diccionario del grafo a modificar en lugar.
    """
    for f in FILAS:
        sentido = _sentido_horizontal(f)
        for ci, c in enumerate(COLS):
            nodo = f"{f}{c}"
            if sentido == "derecha" and ci + 1 < len(COLS):
                grafo[nodo].append((f"{f}{COLS[ci + 1]}", DIST_HORIZONTAL))
            elif sentido == "izquierda" and ci - 1 >= 0:
                grafo[nodo].append((f"{f}{COLS[ci - 1]}", DIST_HORIZONTAL))


def _agregar_aristas_verticales(grafo: dict) -> None:
    """
    Agrega al grafo las aristas correspondientes a las calles verticales,
    respetando el sentido de circulación de cada una.

    Args:
        grafo: Diccionario del grafo a modificar en lugar.
    """
    for c in COLS:
        sentido = _sentido_vertical(c)
        for fi, f in enumerate(FILAS):
            nodo = f"{f}{c}"
            if sentido == "abajo" and fi + 1 < len(FILAS):
                grafo[nodo].append((f"{FILAS[fi + 1]}{c}", DIST_VERTICAL))
            elif sentido == "arriba" and fi - 1 >= 0:
                grafo[nodo].append((f"{FILAS[fi - 1]}{c}", DIST_VERTICAL))


def construir_grafo() -> dict:
    """
    Construye el grafo dirigido de la ciudad con todos los nodos
    e intersecciones, respetando los sentidos de cada calle.

    Cada nodo tiene el formato 'LetraNumero' (ej. 'A1', 'B3').
    Las aristas tienen un peso en metros según su orientación:
    - Horizontal: 100 m
    - Vertical:    50 m

    Returns:
        Diccionario {nodo: [(vecino, costo_metros), ...]}.
    """
    # S7519: usar dict.fromkeys en lugar de comprensión 
    grafo = dict.fromkeys(
        [f"{f}{c}" for f in FILAS for c in COLS], None
    )
    # fromkeys asigna el mismo objeto a todas las claves,
    # por lo que inicializamos cada lista de forma independiente
    grafo = {nodo: [] for nodo in grafo}

    _agregar_aristas_horizontales(grafo)
    _agregar_aristas_verticales(grafo)

    return grafo


def _reconstruir_camino(previo: dict, destino: str) -> list:
    """
    Reconstruye el camino desde el nodo destino hasta el inicio
    siguiendo el diccionario de predecesores.

    Args:
        previo:  Diccionario {nodo: nodo_anterior}.
        destino: Nodo final de la ruta.

    Returns:
        Lista de nodos en orden desde inicio hasta destino.
    """
    camino = []
    n = destino
    while n is not None:
        camino.append(n)
        n = previo[n]
    camino.reverse()
    return camino


def dijkstra(grafo: dict, inicio: str, destino: str) -> tuple[list, float] | tuple[None, None]:
    """
    Ejecuta el algoritmo de Dijkstra sobre el grafo para encontrar
    la ruta más corta (en metros) entre dos nodos.

    Args:
        grafo:   Grafo dirigido construido con construir_grafo().
        inicio:  Nodo de partida (ej. 'A1').
        destino: Nodo de llegada (ej. 'J10').

    Returns:
        Tupla (camino, distancia_metros) si existe ruta,
        o (None, None) si no hay camino posible.
    """
    # Inicializar distancias con infinito para todos los nodos
    distancias = dict.fromkeys(grafo, float("inf"))
    distancias[inicio] = 0

    # Predecesor de cada nodo para reconstruir el camino
    previo = dict.fromkeys(grafo, None)

    # Min-heap: (costo_acumulado, nodo)
    heap = [(0, inicio)]

    while heap:
        costo_actual, nodo_actual = heapq.heappop(heap)

        # Llegamos al destino — reconstruir y retornar
        if nodo_actual == destino:
            return _reconstruir_camino(previo, destino), costo_actual

        # Ignorar entradas obsoletas del heap
        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, costo in grafo[nodo_actual]:
            nueva_dist = costo_actual + costo
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                previo[vecino]     = nodo_actual
                heapq.heappush(heap, (nueva_dist, vecino))

    # No existe ruta entre inicio y destino
    return None, None