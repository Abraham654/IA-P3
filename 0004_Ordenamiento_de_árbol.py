class Node:  # Define la clase Node para los nodos del árbol binario
    def __init__(self, key):  # Inicializa un nodo con una clave
        self.key = key  # Asigna el valor de la clave al nodo
        self.left = None  # Inicializa el hijo izquierdo como None
        self.right = None  # Inicializa el hijo derecho como None

def insert(root, key):  # Inserta una clave en el árbol binario de búsqueda
    if root is None:  # Si el árbol está vacío
        return Node(key)  # Crea y retorna un nuevo nodo
    if key < root.key:  # Si la clave es menor que la clave del nodo actual
        root.left = insert(root.left, key)  # Inserta en el subárbol izquierdo
    else:  # Si la clave es mayor o igual
        root.right = insert(root.right, key)  # Inserta en el subárbol derecho
    return root  # Retorna la raíz actualizada

def inorder_traversal(root, result):  # Realiza un recorrido inorden del árbol
    if root:  # Si el nodo no es None
        inorder_traversal(root.left, result)  # Recorre el subárbol izquierdo
        result.append(root.key)  # Agrega la clave del nodo a la lista resultado
        inorder_traversal(root.right, result)  # Recorre el subárbol derecho

def tree_sort(arr):  # Ordena una lista usando ordenamiento de árbol
    root = None  # Inicializa la raíz del árbol como None
    for key in arr:  # Recorre cada elemento de la lista
        root = insert(root, key)  # Inserta el elemento en el árbol
    result = []  # Inicializa la lista para el resultado ordenado
    inorder_traversal(root, result)  # Realiza el recorrido inorden para ordenar
    return result  # Retorna la lista ordenada

# Ejemplo de uso    #Punto de entrada del script
if __name__ == "__main__":  # Verifica si el script se ejecuta directamente
    datos = [5, 3, 7, 2, 4, 6, 8]  # Lista de datos a ordenar
    print("Lista original:", datos)  # Imprime la lista original
    ordenada = tree_sort(datos)  # Ordena la lista usando tree_sort
    print("Lista ordenada:", ordenada)  # Imprime la lista ordenada