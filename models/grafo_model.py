import heapq

FILAS = list("ABCDEFGHIJ")   # A=0 … J=9
COLS  = list(range(1, 11))   # 1 … 10

def _sentido_horizontal(numero: int) -> str:
    """
    Calles horizontales (letras):
    par → derecha, impar → izquierda
    """
    idx = FILAS.index(numero)
    return "derecha" if idx % 2 == 0 else "izquierda"


def _sentido_vertical(numero: int) -> str:
    """
    Calles verticales (números):
    impar → abajo, par → arriba
    """
    return "abajo" if numero % 2 != 0 else "arriba"


def construir_grafo() -> dict:
    """
    Retorna un dict: nodo → lista de (vecino, costo)
    Nodo = "A1", "B3", etc.
    Solo se añaden aristas en el sentido permitido de cada calle.
    """
    grafo = {f"{f}{c}": [] for f in FILAS for c in COLS}

    for f in FILAS:
        fi = FILAS.index(f)
        sentido = _sentido_horizontal(f)

        for ci in range(len(COLS)):
            c = COLS[ci]
            nodo_actual = f"{f}{c}"

            if sentido == "derecha" and ci + 1 < len(COLS):
                vecino = f"{f}{COLS[ci + 1]}"
                grafo[nodo_actual].append((vecino, 1))

            elif sentido == "izquierda" and ci - 1 >= 0:
                vecino = f"{f}{COLS[ci - 1]}"
                grafo[nodo_actual].append((vecino, 1))

    for c in COLS:
        sentido = _sentido_vertical(c)

        for fi in range(len(FILAS)):
            f = FILAS[fi]
            nodo_actual = f"{f}{c}"

            if sentido == "abajo" and fi + 1 < len(FILAS):
                vecino = f"{FILAS[fi + 1]}{c}"
                grafo[nodo_actual].append((vecino, 1))

            elif sentido == "arriba" and fi - 1 >= 0:
                vecino = f"{FILAS[fi - 1]}{c}"
                grafo[nodo_actual].append((vecino, 1))

    return grafo


def dijkstra(grafo: dict, inicio: str, destino: str) -> list | None:
    """
    Retorna la lista de nodos del camino más corto,
    o None si no existe ruta.
    """
    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[inicio] = 0
    previo = {nodo: None for nodo in grafo}

    heap = [(0, inicio)]

    while heap:
        costo_actual, nodo_actual = heapq.heappop(heap)

        if nodo_actual == destino:
            # Reconstruir camino
            camino = []
            n = destino
            while n is not None:
                camino.append(n)
                n = previo[n]
            camino.reverse()
            return camino

        if costo_actual > distancias[nodo_actual]:
            continue

        for vecino, costo in grafo[nodo_actual]:
            nueva_dist = costo_actual + costo
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                previo[vecino] = nodo_actual
                heapq.heappush(heap, (nueva_dist, vecino))

    return None  # Sin ruta posible