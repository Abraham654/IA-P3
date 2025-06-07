import collections

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
        self.adj = collections.defaultdict(list) # For easier representation if needed

    def add_edge(self, u, v, weight):
        """Adds an edge to the graph."""
        self.graph.append([u, v, weight])
        # self.adj[u].append((v, weight))
        # self.adj[v].append((u, weight))

class DisjointSet:
    """A simple Disjoint Set (Union-Find) data structure."""
    def __init__(self, vertices):
        self.parent = list(range(vertices))
        self.rank = [0] * vertices

    def find(self, i):
        """Finds the representative of the set containing element i."""
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]

    def union(self, i, j):
        """Unites the sets containing elements i and j."""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True # Union was successful
        return False # Elements already in the same set

def kruskal_mst_simulator(graph_obj, mode="min"):
    """
    Simulates Kruskal's algorithm to find a Minimum or Maximum Spanning Tree.
    Shows steps in the console.

    Args:
        graph_obj (Graph): The graph object.
        mode (str): "min" for Minimum Spanning Tree, "max" for Maximum Spanning Tree.
    """
    print(f"\n--- Kruskal's Algorithm for {mode.upper()} Cost Spanning Tree ---")
    mst = []
    cost = 0
    ds = DisjointSet(graph_obj.V)

    # Sort edges based on mode
    if mode == "min":
        # Sort edges in ascending order of weight for MST
        edges = sorted(graph_obj.graph, key=lambda item: item[2])
        print("Step 1: Sort all edges in ascending order of their weights.")
    elif mode == "max":
        # Sort edges in descending order of weight for MaxST
        edges = sorted(graph_obj.graph, key=lambda item: item[2], reverse=True)
        print("Step 1: Sort all edges in descending order of their weights.")
    else:
        print("Invalid mode. Please choose 'min' or 'max'.")
        return

    print("Sorted Edges (u, v, weight):")
    for u, v, weight in edges:
        print(f"  ({chr(65+u)}, {chr(65+v)}, {weight})") # Convert to A, B, C... for readability

    edge_count = 0
    step = 2
    for u, v, weight in edges:
        print(f"\n--- Step {step}: Considering edge ({chr(65+u)}, {chr(65+v)}) with weight {weight} ---")

        # Check if adding this edge forms a cycle
        if ds.find(u) != ds.find(v):
            print(f"  Nodes {chr(65+u)} and {chr(65+v)} are in different sets.")
            print(f"  Adding edge ({chr(65+u)}, {chr(65+v)}) to MST.")
            ds.union(u, v)
            mst.append((u, v, weight))
            cost += weight
            edge_count += 1
        else:
            print(f"  Nodes {chr(65+u)} and {chr(65+v)} are already in the same set.")
            print(f"  Adding edge ({chr(65+u)}, {chr(65+v)}) would form a cycle. Skipping.")

        # Stop when V-1 edges are included
        if edge_count == graph_obj.V - 1:
            break
        step += 1

    print("\n--- Kruskal's Algorithm Simulation Complete ---")
    print(f"Final {mode.upper()} Spanning Tree Edges:")
    for u, v, weight in mst:
        print(f"  ({chr(65+u)}, {chr(65+v)}, {weight})")
    print(f"Total {mode.upper()} Spanning Tree Cost: {cost}")

    # Optional: For graphical visualization, you would typically use matplotlib
    # and NetworkX. This is just a placeholder to explain:
    #
    # import networkx as nx
    # import matplotlib.pyplot as plt
    #
    # G_draw = nx.Graph()
    # for i in range(graph_obj.V):
    #     G_draw.add_node(chr(65+i))
    # for u, v, weight in graph_obj.graph:
    #     G_draw.add_edge(chr(65+u), chr(65+v), weight=weight)
    #
    # pos = nx.spring_layout(G_draw) # You might need to adjust layout
    # nx.draw(G_draw, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10)
    # edge_labels = nx.get_edge_attributes(G_draw, 'weight')
    # nx.draw_networkx_edge_labels(G_draw, pos, edge_labels=edge_labels)
    #
    # # Highlight MST edges
    # mst_edges_to_draw = [(chr(65+u), chr(65+v)) for u, v, _ in mst]
    # nx.draw_networkx_edges(G_draw, pos, edgelist=mst_edges_to_draw, edge_color='red', width=2)
    #
    # plt.title(f"{mode.upper()} Spanning Tree")
    # plt.show()


# --- Example Usage ---
if __name__ == "__main__":
    # Example Graph 1 (from common Kruskal's examples)
    # Vertices are 0, 1, 2, 3, 4, 5, 6, 7, 8 (representing A, B, C...)
    g1 = Graph(9)
    g1.add_edge(0, 1, 4) # A-B
    g1.add_edge(0, 7, 8) # A-H
    g1.add_edge(1, 2, 8) # B-C
    g1.add_edge(1, 7, 11) # B-H
    g1.add_edge(2, 3, 7) # C-D
    g1.add_edge(2, 8, 2) # C-I
    g1.add_edge(2, 5, 4) # C-F
    g1.add_edge(3, 4, 9) # D-E
    g1.add_edge(3, 5, 14) # D-F
    g1.add_edge(4, 5, 10) # E-F
    g1.add_edge(5, 6, 2) # F-G
    g1.add_edge(6, 7, 1) # G-H
    g1.add_edge(6, 8, 6) # G-I
    g1.add_edge(7, 8, 7) # H-I

    # Run for Minimum Spanning Tree
    kruskal_mst_simulator(g1, mode="min")

    # Run for Maximum Spanning Tree
    kruskal_mst_simulator(g1, mode="max")

    print("\n" + "="*50 + "\n")

    # Example Graph 2 (smaller example)
    g2 = Graph(4)
    g2.add_edge(0, 1, 10) # A-B
    g2.add_edge(0, 2, 6)  # A-C
    g2.add_edge(0, 3, 5)  # A-D
    g2.add_edge(1, 3, 15) # B-D
    g2.add_edge(2, 3, 4)  # C-D

    kruskal_mst_simulator(g2, mode="min")
    kruskal_mst_simulator(g2, mode="max")