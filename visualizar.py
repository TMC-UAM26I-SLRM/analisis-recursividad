from __future__ import annotations
import matplotlib.pyplot as plt
from typing import Any


Nodo = dict[str, Any]


def crear_nodo(etiqueta: str) -> Nodo:
    """
    Crea un nodo del árbol de llamadas.

    Cada nodo se representa con un diccionario que contiene:
    - 'etiqueta': texto descriptivo de la llamada actual.
    - 'hijos': lista con los nodos hijos generados por llamadas recursivas.

    Args:
        etiqueta: Texto que identifica la llamada actual.

    Returns:
        Un diccionario que representa un nodo del árbol.
    """
    return {
        "etiqueta": etiqueta,
        "hijos": []
    }


def imprimir_arbol(nodo: Nodo, prefijo: str = "", es_ultimo: bool = True) -> None:
    """
    Imprime un árbol con formato jerárquico.

    La función imprime primero el nodo actual y después recorre
    recursivamente cada uno de sus hijos.

    Args:
        nodo: Nodo actual que se desea imprimir.
        prefijo: Cadena auxiliar para conservar la forma visual del árbol.
        es_ultimo: Indica si el nodo actual es el último hijo de su nivel.

    Returns:
        None.
    """
    if es_ultimo:
        conector = "└── "
        nuevo_prefijo = prefijo + "    "
    else:
        conector = "├── "
        nuevo_prefijo = prefijo + "│   "

    print(prefijo + conector + nodo["etiqueta"])

    cantidad_hijos = len(nodo["hijos"])

    for indice, hijo in enumerate(nodo["hijos"]):
        hijo_es_ultimo = indice == cantidad_hijos - 1
        imprimir_arbol(hijo, nuevo_prefijo, hijo_es_ultimo)


def fibonacci_recursivo(n: int) -> tuple[int, Nodo, int]:
    """
    Calcula Fibonacci de forma recursiva y construye el árbol de llamadas.

    La función regresa tres valores:
    1. El resultado numérico de fib(n).
    2. El nodo raíz del subárbol correspondiente a la llamada actual.
    3. El total de llamadas realizadas dentro de este subproblema.

    Args:
        n: Valor de entrada para Fibonacci.

    Returns:
        Una tupla con:
        - resultado de Fibonacci
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    nodo_actual = crear_nodo(f"fib({n})")

    if n <= 1:
        resultado = n
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    resultado_izquierdo, hijo_izquierdo, llamadas_izquierdas = fibonacci_recursivo(n - 1)
    resultado_derecho, hijo_derecho, llamadas_derechas = fibonacci_recursivo(n - 2)

    nodo_actual["hijos"].append(hijo_izquierdo)
    nodo_actual["hijos"].append(hijo_derecho)

    resultado = resultado_izquierdo + resultado_derecho
    total_llamadas = 1 + llamadas_izquierdas + llamadas_derechas

    return resultado, nodo_actual, total_llamadas


def fibonacci_recursivo_memoria(
    n: int,
    memo: dict[int, int] | None = None
) -> tuple[int, Nodo, int]:
    """
    Calcula Fibonacci con memoria dinámica y construye el árbol de llamadas.

    Si un valor ya fue calculado, no se vuelve a expandir su subárbol.
    En ese caso, el nodo se marca con la leyenda '[memo=valor]'.

    Args:
        n: Valor de entrada para Fibonacci.
        memo: Diccionario que almacena resultados ya calculados.

    Returns:
        Una tupla con:
        - resultado de Fibonacci
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    if memo is None:
        memo = {}

    if n in memo:
        nodo_actual = crear_nodo(f"fib({n}) [memo={memo[n]}]")
        resultado = memo[n]
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    nodo_actual = crear_nodo(f"fib({n})")

    if n <= 1:
        memo[n] = n
        resultado = n
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    resultado_izquierdo, hijo_izquierdo, llamadas_izquierdas = fibonacci_recursivo_memoria(
        n - 1,
        memo
    )
    resultado_derecho, hijo_derecho, llamadas_derechas = fibonacci_recursivo_memoria(
        n - 2,
        memo
    )

    nodo_actual["hijos"].append(hijo_izquierdo)
    nodo_actual["hijos"].append(hijo_derecho)

    resultado = resultado_izquierdo + resultado_derecho
    memo[n] = resultado
    total_llamadas = 1 + llamadas_izquierdas + llamadas_derechas

    return resultado, nodo_actual, total_llamadas


def busqueda_binaria_arbol(
    arreglo: list[int],
    objetivo: int,
    izquierda: int,
    derecha: int
) -> tuple[int, Nodo, int]:
    """
    Realiza búsqueda binaria recursiva y construye el árbol de llamadas.

    Cada llamada genera un nodo con el segmento actual del arreglo que
    está siendo analizado.

    Args:
        arreglo: Lista ordenada en la que se desea buscar.
        objetivo: Valor que se desea encontrar.
        izquierda: Índice izquierdo del rango de búsqueda actual.
        derecha: Índice derecho del rango de búsqueda actual.

    Returns:
        Una tupla con:
        - índice encontrado, o -1 si no existe
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    segmento_actual = arreglo[izquierda:derecha + 1]
    etiqueta = "buscar(" + str(segmento_actual) + ")"
    nodo_actual = crear_nodo(etiqueta)

    total_llamadas = 1

    if izquierda > derecha:
        nodo_actual["etiqueta"] += " -> no encontrado"
        return -1, nodo_actual, total_llamadas

    medio = (izquierda + derecha) // 2

    if arreglo[medio] == objetivo:
        nodo_actual["etiqueta"] += " -> encontrado en indice " + str(medio)
        return medio, nodo_actual, total_llamadas

    if objetivo < arreglo[medio]:
        resultado, hijo, llamadas = busqueda_binaria_arbol(
            arreglo,
            objetivo,
            izquierda,
            medio - 1
        )
        nodo_actual["hijos"].append(hijo)
        total_llamadas = total_llamadas + llamadas
        return resultado, nodo_actual, total_llamadas

    resultado, hijo, llamadas = busqueda_binaria_arbol(
        arreglo,
        objetivo,
        medio + 1,
        derecha
    )
    nodo_actual["hijos"].append(hijo)
    total_llamadas = total_llamadas + llamadas

    return resultado, nodo_actual, total_llamadas


def ejecutar_fibonacci(n: int) -> None:
    """
    Ejecuta y muestra dos versiones de Fibonacci:
    - recursiva simple
    - recursiva con memoria dinámica

    Args:
        n: Valor que se utilizará en la demostración.

    Returns:
        None.
    """
    print("=" * 70)
    print("FIBONACCI SIN MEMORIA DINAMICA")
    print("=" * 70)

    resultado, raiz, total_llamadas = fibonacci_recursivo(n)

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz)

    print("\nResumen:")
    print(f"Resultado: {resultado}")
    print(f"Total de llamadas: {total_llamadas}")

    print("\n" + "=" * 70)
    print("FIBONACCI CON MEMORIA DINAMICA")
    print("=" * 70)

    resultado_memo, raiz_memo, total_llamadas_memo = fibonacci_recursivo_memoria(n)

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz_memo)

    print("\nResumen:")
    print(f"Resultado: {resultado_memo}")
    print(f"Total de llamadas: {total_llamadas_memo}")


def ejecutar_busqueda(arreglo: list[int], objetivo: int) -> None:
    """
    Ejecuta la búsqueda binaria recursiva y muestra su árbol de llamadas.

    Args:
        arreglo: Lista ordenada en la que se realizará la búsqueda.
        objetivo: Valor que se desea localizar.

    Returns:
        None.
    """
    print("=" * 70)
    print("BUSQUEDA BINARIA")
    print("=" * 70)

    resultado, raiz, total_llamadas = busqueda_binaria_arbol(
        arreglo,
        objetivo,
        0,
        len(arreglo) - 1
    )

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz)

    print("\nResumen:")
    print(f"Indice encontrado: {resultado}")
    print(f"Total de llamadas: {total_llamadas}")



import matplotlib.pyplot as plt

if __name__ == "__main__":

    # LISTAS PARA la GRAFICA

    valores_n = []
    llamadas_normal = []
    llamadas_memoria = []
    llamadas_busqueda = []

    for n in range(1, 20):

        print(f"\n===== n = {n} =====")

        # Fibonacci normal
        _, _, total_llamadas = fibonacci_recursivo(n)

        # Fibonacci memoización
        _, _, total_llamadas_mem = fibonacci_recursivo_memoria(n, {})

        # Búsqueda binaria
        arreglo = list(range(1, n + 1))
        objetivo = -1 

        _, _, total_llamadas_busq = busqueda_binaria_arbol(
            arreglo,
            objetivo,
            0,
            len(arreglo) - 1
        )

        # guardar los puntos
        valores_n.append(n)
        llamadas_normal.append(total_llamadas)
        llamadas_memoria.append(total_llamadas_mem)
        llamadas_busqueda.append(total_llamadas_busq)

    # GRAFICA

    plt.figure()

    plt.plot(valores_n, llamadas_normal,
             marker='o', label="Fibonacci Recursivo")

    plt.plot(valores_n, llamadas_memoria,
             marker='s', label="Fibonacci Memoización")

    plt.plot(valores_n, llamadas_busqueda,
             marker='^', label="Búsqueda Binaria")

    plt.xlabel("n")
    plt.ylabel("Número de llamadas")
    plt.title("Comparación de Complejidad de Algoritmos")

    plt.legend()
    plt.grid(True)

    plt.show()

    print("\n" + "#" * 70 + "\n")

    # EJECUCION NORMAL

    arreglo_prueba = [
        1,2,3,4,5,6,7,8,9,10,
        11,12,13,14,15,16,17,18,19,20
    ]

    objetivo_prueba = 6
    ejecutar_busqueda(arreglo_prueba, objetivo_prueba)