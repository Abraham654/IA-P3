import heapq
import matplotlib.pyplot as plt
import networkx as nx
import math

class PrimMST:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = [[] for _ in range(num_vertices)]
        self.pos = {} # Para almacenar las posiciones de los nodos para la gráfica

    def add_edge(self, u, v, weight):
        """Añade una arista al grafo."""
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight)) # Para grafo no dirigido

    def set_node_positions(self, pos_dict):
        """Establece las posiciones de los nodos para la visualización."""
        self.pos = pos_dict

    def visualize_graph(self, title="Grafo Original", mst_edges=None, current_edge=None, step_info=""):
        """
        Visualiza el grafo usando matplotlib y networkx.
        Muestra el grafo original, el MST en construcción o el MST final.
        """
        G = nx.Graph()
        for u in range(self.num_vertices):
            for v, weight in self.graph[u]:
                if u < v:  # Evitar aristas duplicadas en la visualización
                    G.add_edge(u, v, weight=weight)

        if not self.pos:
            self.pos = nx.spring_layout(G) # Generar posiciones si no están dadas

        plt.figure(figsize=(10, 7))
        plt.title(f"{title}\n{step_info}")

        # Dibujar nodos y etiquetas
        nx.draw_networkx_nodes(G, self.pos, node_size=700, node_color='skyblue', alpha=0.9)
        nx.draw_networkx_labels(G, self.pos, font_size=10, font_weight='bold')

        # Dibujar todas las aristas con color gris claro por defecto
        all_edges = [(u, v) for u, v, d in G.edges(data=True)]
        nx.draw_networkx_edges(G, self.pos, edgelist=all_edges, edge_color='lightgray', width=1)

        # Dibujar pesos de las aristas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, font_color='red')

        # Resaltar aristas del MST
        if mst_edges:
            nx.draw_networkx_edges(G, self.pos, edgelist=mst_edges, edge_color='blue', width=2)
            # Dibujar los pesos de las aristas del MST con un color diferente si es necesario
            mst_edge_weights = {(u,v): G[u][v]['weight'] for u,v in mst_edges}
            nx.draw_networkx_edge_labels(G, self.pos, edge_labels=mst_edge_weights, font_color='darkblue', bbox={"alpha":0})


        # Resaltar la arista actual en consideración (para el paso a paso)
        if current_edge:
            u, v, weight = current_edge
            nx.draw_networkx_edges(G, self.pos, edgelist=[(u,v)], edge_color='green', width=3)
            # Añadir etiqueta para la arista actual
            mid_x = (self.pos[u][0] + self.pos[v][0]) / 2
            mid_y = (self.pos[u][1] + self.pos[v][1]) / 2
            plt.text(mid_x, mid_y, f"({weight})", color='green', fontsize=12, ha='center', va='center',
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='green', boxstyle='round,pad=0.3'))


        plt.show(block=False) # Permite que la ventana no bloquee el código
        plt.pause(2) # Pausa para ver la gráfica
        plt.close()

    def prim_mst(self, start_node=0):
        """
        Implementa el algoritmo de Prim para encontrar el Árbol de Expansión Mínimo (MST).
        Muestra el proceso paso a paso en consola y gráficamente.
        """
        min_heap = [(0, start_node, -1)]  # (peso, vértice_actual, vértice_origen)
        visited = [False] * self.num_vertices
        mst_edges = []
        total_weight = 0

        print("\n--- INICIO del Algoritmo de Prim ---")
        print(f"Comenzando desde el nodo: {start_node}")

        self.visualize_graph(title="Paso Inicial: Grafo Original", step_info=f"Nodo inicial: {start_node}")

        while min_heap:
            weight, u, parent = heapq.heappop(min_heap)

            if visited[u]:
                print(f"\nIgnorando arista ({parent}-{u}) con peso {weight} (el nodo {u} ya está en el MST).")
                continue

            visited[u] = True
            if parent != -1: # No añadir la arista ficticia inicial
                mst_edges.append((parent, u))
                total_weight += weight
                print(f"\nPASO: Se añade la arista ({parent}-{u}) con peso {weight} al MST.")
                print(f"MST actual: {mst_edges}")
                print(f"Peso total del MST hasta ahora: {total_weight}")
                self.visualize_graph(title="Construyendo MST", mst_edges=mst_edges,
                                     current_edge=(parent, u, weight),
                                     step_info=f"Se añadió la arista ({parent}-{u}) peso {weight}")
            else:
                print(f"\nPASO: Se selecciona el nodo inicial {u}.")
                self.visualize_graph(title="Construyendo MST", step_info=f"Nodo inicial seleccionado: {u}")


            print(f"\nExplorando vecinos del nodo {u}:")
            for v, edge_weight in self.graph[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (edge_weight, v, u))
                    print(f"  - Añadiendo arista ({u}-{v}) con peso {edge_weight} a la cola de prioridad.")
                else:
                    print(f"  - Ignorando arista ({u}-{v}) con peso {edge_weight} (el nodo {v} ya está visitado).")

        print("\n--- FIN del Algoritmo de Prim ---")
        print(f"\nEl Árbol de Expansión Mínimo (MST) está compuesto por las aristas: {mst_edges}")
        print(f"El peso total del MST es: {total_weight}")

        self.visualize_graph(title="Árbol de Expansión Mínimo (MST) Final", mst_edges=mst_edges,
                             step_info=f"Peso total del MST: {total_weight}")
        return mst_edges, total_weight

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # Crear un grafo de ejemplo
    num_nodes = 5
    prim_simulator = PrimMST(num_nodes)

    # Añadir aristas (u, v, peso)
    prim_simulator.add_edge(0, 1, 2)
    prim_simulator.add_edge(0, 3, 6)
    prim_simulator.add_edge(1, 2, 3)
    prim_simulator.add_edge(1, 3, 8)
    prim_simulator.add_edge(1, 4, 5)
    prim_simulator.add_edge(2, 4, 7)
    prim_simulator.add_edge(3, 4, 9)

    # Opcional: Definir posiciones para los nodos para una mejor visualización
    # Si no se definen, networkx intentará generarlas automáticamente.
    # Estas son solo sugerencias, puedes ajustarlas o dejarlas para layout automático
    node_positions = {
        0: (0, 0),
        1: (1, 1),
        2: (2, 0),
        3: (0, -1),
        4: (1, -2)
    }
    prim_simulator.set_node_positions(node_positions)

    # Ejecutar el algoritmo de Prim
    mst_edges, total_weight = prim_simulator.prim_mst(start_node=0)

    # Otro ejemplo con un grafo diferente
    print("\n\n--- Ejecutando otro ejemplo ---")
    num_nodes_2 = 7
    prim_simulator_2 = PrimMST(num_nodes_2)
    prim_simulator_2.add_edge(0, 1, 4)
    prim_simulator_2.add_edge(0, 2, 3)
    prim_simulator_2.add_edge(1, 2, 1)
    prim_simulator_2.add_edge(1, 3, 2)
    prim_simulator_2.add_edge(2, 3, 4)
    prim_simulator_2.add_edge(3, 4, 2)
    prim_simulator_2.add_edge(4, 5, 6)
    prim_simulator_2.add_edge(4, 6, 1)
    prim_simulator_2.add_edge(5, 6, 3)

    mst_edges_2, total_weight_2 = prim_simulator_2.prim_mst(start_node=0)