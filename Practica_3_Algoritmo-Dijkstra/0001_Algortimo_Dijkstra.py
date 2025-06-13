import heapq
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Optional, Any


def dijkstra_simulator(
    graph: Dict[Any, Dict[Any, int]],
    start_node: Any,
    end_node: Optional[Any] = None
):
    """
    Simula el Algoritmo de Dijkstra paso a paso.

    Args:
        graph (dict): Un diccionario que representa el grafo.
                      Las claves son nodos, y los valores son diccionarios
                      de nodos vecinos con sus pesos.
                      Ejemplo: {'A': {'B': 1, 'C': 4}, 'B': {'A': 1, 'D': 2}}
        start_node: El nodo de inicio para el algoritmo.
        end_node: El nodo final deseado (opcional). Si se especifica,
                  el algoritmo puede detenerse una vez que se encuentre la ruta
                  a este nodo.
    """
    distances: Dict[Any, float] = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    previous_nodes: Dict[Any, Optional[Any]] = {node: None for node in graph}
    priority_queue = [(0, start_node)]  # (distancia, nodo)

    print("\n--- Iniciando la simulación del Algoritmo de Dijkstra "
          f"desde el nodo: {start_node} ---\n")
    print(f"Distancias iniciales: {distances}")
    print(f"Nodos previos iniciales: {previous_nodes}\n")

    step = 0
    while priority_queue:
        step += 1
        current_distance, current_node = heapq.heappop(priority_queue)

        print(f"--- Paso {step} ---")
        print(f"Explorando nodo: '{current_node}' "
              f"(Distancia actual: {current_distance})")

        # Si ya hemos encontrado una ruta más corta a este nodo, lo ignoramos
        if current_distance > distances[current_node]:
            print(f"  (Ignorando: Ya se encontró una ruta más corta a "
                  f"'{current_node}')")
            continue

        # Si hemos llegado al nodo final y se especificó, podemos detenernos
        if end_node and current_node == end_node:
            print(f"\n¡Nodo final '{end_node}' alcanzado! "
                  "Terminando la búsqueda...\n")
            break

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            print(f"  Considerando vecino: '{neighbor}' con peso {weight} "
                  f"desde '{current_node}'")
            print(f"    Distancia calculada a '{neighbor}': {distance}")
            print(f"    Distancia actual conocida a '{neighbor}': "
                  f"{distances[neighbor]}")

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                print(f"    ¡Nueva ruta más corta encontrada a '{neighbor}'!")
                print(f"      Distancia actualizada a '{neighbor}': "
                      f"{distances[neighbor]}")
                print(f"      Nodo previo de '{neighbor}' actualizado a: "
                      f"'{current_node}'")
            else:
                print(f"    La ruta a '{neighbor}' a través de '{current_node}'"
                      " no es más corta. No se actualiza.")
        print(f"\nEstado actual de distancias: {distances}")
        print(f"Estado actual de nodos previos: {previous_nodes}\n")

    print("\n--- Simulación Finalizada ---\n")
    print(f"Distancias finales: {distances}")
    print(f"Nodos previos finales: {previous_nodes}\n")

    # Reconstruir la ruta si se especificó un nodo final
    path = []
    if end_node:
        current = end_node
        # Asegurarse de que current esté en previous_nodes y no sea None
        while current is not None and previous_nodes.get(current) is not None:
            path.insert(0, current)
            current = previous_nodes[current]
        # Agregar el nodo inicial si la ruta se construyó correctamente
        if current == start_node:
            path.insert(0, current)

        if path and path[0] == start_node and path[-1] == end_node:
            print(f"Ruta más corta de '{start_node}' a '{end_node}': "
                  f"{' -> '.join(path)}")
            print(f"Distancia total: {distances[end_node]}")
        else:
            print(f"No se encontró una ruta completa de '{start_node}' a "
                  f"'{end_node}'.")
    else:
        print("No se especificó un nodo final, mostrando todas las distancias"
              " desde el inicio.")


def visualize_graph(
    graph: Dict[Any, Dict[Any, int]],
    distances: Dict[Any, float],
    start_node: Any,
    end_node: Optional[Any] = None,
    previous_nodes: Optional[Dict[Any, Optional[Any]]] = None
):
    """
    Visualiza el grafo usando matplotlib y networkx.

    Args:
        graph (dict): El grafo.
        distances (dict): Las distancias calculadas por Dijkstra.
        start_node: El nodo de inicio.
        end_node: El nodo final (opcional).
        previous_nodes (dict): Los nodos previos para reconstruir la ruta
                               (opcional).
    """
    G = nx.DiGraph()  # Usamos un grafo dirigido para mayor claridad

    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)  # Para una disposición consistente

    plt.figure(figsize=(10, 8))
    plt.title("Simulador del Algoritmo de Dijkstra")

    # Dibujar nodos
    node_colors_list = []
    for node in G.nodes():
        if node == start_node:
            node_colors_list.append('lightgreen')
        elif end_node and node == end_node:
            node_colors_list.append('red')
        else:
            node_colors_list.append('lightblue')

    # Añadido un type: ignore para suprimir la advertencia de Pylance,
    # ya que sabemos que el tipo de node_color es una lista de str para networkx.
    


    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.7, edge_color='gray')

    # Añadir etiquetas de peso a las aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_color='darkgreen')

    # Añadir etiquetas de nodos (nombre del nodo y su distancia calculada)
    node_labels = {
        node: (
            f"{node}\n("
            f"{distances[node] if distances[node] != float('infinity') else '∞'})"
        )
        for node in G.nodes()
    }
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10,
                            font_weight='bold')

    # Dibujar la ruta más corta si se encontró y se proporcionaron previous_nodes
    if end_node and previous_nodes:
        path_edges = []
        path_nodes = []
        current = end_node
        # Reconstrucción de la ruta: asegurarse de que el nodo actual y su
        # predecesor no sean None
        while current is not None and previous_nodes.get(current) is not None:
            path_edges.append((previous_nodes[current], current))
            path_nodes.append(current)
            current = previous_nodes[current]

        # Añadir el nodo de inicio si la ruta se construyó correctamente
        if current == start_node:
            path_nodes.append(start_node)

        path_nodes.reverse()  # Para que esté en el orden correcto

        if start_node in path_nodes and end_node in path_nodes:
            # Resaltar la ruta
            nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                   edge_color='red', width=3)
            # Resaltar los nodos en la ruta
            nx.draw_networkx_nodes(G, pos, nodelist=path_nodes,
                                   node_color='purple', node_size=3500,
                                   alpha=0.7)

            # Re-dibujar etiquetas de la ruta para que sean visibles
            path_node_labels = {
                node: (
                    f"{node}\n("
                    f"{distances[node] if distances[node] != float('infinity') else '∞'})"
                )
                for node in path_nodes
            }
            nx.draw_networkx_labels(G, pos, labels=path_node_labels,
                                    font_size=10, font_weight='bold',
                                    font_color='white')

    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # Ejemplo de Grafo 1
    graph1 = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    start_node1 = 'A'
    end_node1 = 'D'

    # Ejemplo de Grafo 2 (más complejo)
    graph2 = {
        'S': {'A': 6, 'B': 2},
        'A': {'S': 6, 'C': 1},
        'B': {'S': 2, 'A': 3, 'C': 5},
        'C': {'A': 1, 'B': 5, 'D': 3},
        'D': {'C': 3, 'E': 4},
        'E': {'D': 4, 'F': 2},
        'F': {'E': 2}
    }
    start_node2 = 'S'
    end_node2 = 'F'

    # --- Ejecutar Simulación 1 ---
    print("\n\n############################################")
    print("### SIMULACIÓN 1: GRAFO PEQUEÑO (A -> D) ###")
    print("############################################")

    # Ejecutar la simulación con seguimiento paso a paso (en consola)
    dijkstra_simulator(graph1, start_node1, end_node1)

    # Para la visualización, necesitamos los resultados finales
    # (distances y previous_nodes)
    # Ejecutar Dijkstra completo para obtener los resultados finales
    distances_final1: Dict[Any, float] = {
        node: float('infinity') for node in graph1
    }
    distances_final1[start_node1] = 0
    previous_nodes_final1: Dict[Any, Optional[Any]] = {
        node: None for node in graph1
    }
    priority_queue_final1 = [(0, start_node1)]

    while priority_queue_final1:
        current_distance, current_node = heapq.heappop(priority_queue_final1)
        if current_distance > distances_final1[current_node]:
            continue
        for neighbor, weight in graph1[current_node].items():
            distance = current_distance + weight
            if distance < distances_final1[neighbor]:
                distances_final1[neighbor] = distance
                previous_nodes_final1[neighbor] = current_node
                heapq.heappush(priority_queue_final1, (distance, neighbor))

    print("\n--- Visualizando el Grafo 1 con los resultados finales ---")
    visualize_graph(graph1, distances_final1, start_node1,
                    end_node1, previous_nodes_final1)

    input("\nPresiona Enter para ejecutar la siguiente simulación...")

    # --- Ejecutar Simulación 2 ---
    print("\n\n################################################")
    print("### SIMULACIÓN 2: GRAFO MÁS GRANDE (S -> F) ###")
    print("################################################")

    # Ejecutar la simulación con seguimiento paso a paso (en consola)
    dijkstra_simulator(graph2, start_node2, end_node2)

    # Para la visualización, necesitamos los resultados finales
    # (distances y previous_nodes)
    # Ejecutar Dijkstra completo para obtener los resultados finales
    distances_final2: Dict[Any, float] = {
        node: float('infinity') for node in graph2
    }
    distances_final2[start_node2] = 0
    previous_nodes_final2: Dict[Any, Optional[Any]] = {
        node: None for node in graph2
    }
    priority_queue_final2 = [(0, start_node2)]

    while priority_queue_final2:
        current_distance, current_node = heapq.heappop(priority_queue_final2)
        if current_distance > distances_final2[current_node]:
            continue
        for neighbor, weight in graph2[current_node].items():
            distance = current_distance + weight
            if distance < distances_final2[neighbor]:
                distances_final2[neighbor] = distance
                previous_nodes_final2[neighbor] = current_node
                heapq.heappush(priority_queue_final2, (distance, neighbor))

    print("\n--- Visualizando el Grafo 2 con los resultados finales ---")
    visualize_graph(graph2, distances_final2, start_node2,
                    end_node2, previous_nodes_final2)