def quicksort(arr): # Implementa el algoritmo de ordenamiento QuickSort de manera recursiva.
    """Ordena una lista usando el algoritmo QuickSort."""
    # Si la lista tiene 0 o 1 elementos, ya está ordenada.
    # Si la lista está vacía o tiene un solo elemento, retorna la lista tal cual.
    # Selecciona un pivote y divide la lista en tres partes: menores, iguales y mayores que el pivote.
    # Si la lista tiene un solo elemento o está vacía, retorna la lista sin cambios.
    if len(arr) <= 1:   # Verifica si la lista tiene un solo elemento o está vacía.
        return arr  # Retorna la lista tal cual si tiene 0 o 1 elementos.
    # Selecciona el pivote como el elemento del medio de la lista.
    # Selecciona el elemento del medio como pivote.
    pivot = arr[len(arr) // 2]  # Selecciona el pivote como el elemento del medio de la lista.
    # Divide la lista en tres partes: menores, iguales y mayores que el pivote.
    # Crea una lista de elementos menores que el pivote.
    # Crea una lista de elementos iguales al pivote.
    # Crea una lista de elementos mayores que el pivote.
    # Divide la lista en tres partes: menores, iguales y mayores que el pivote.
    left = [x for x in arr if x < pivot]    # Crea una lista de elementos menores que el pivote.
    middle = [x for x in arr if x == pivot] # Crea una lista de elementos iguales al pivote.
    right = [x for x in arr if x > pivot]   # Crea una lista de elementos mayores que el pivote.
    return quicksort(left) + middle + quicksort(right)  # Retorna la lista ordenada concatenando las listas menores, iguales y mayores que el pivote.

if __name__ == "__main__":  # Punto de entrada del script
    datos = [33, 10, 55, 71, 29, 3, 18, 42] # Lista de datos a ordenar
    print("Lista original:", datos) # Imprime la lista original
    ordenada = quicksort(datos) # Ordena la lista usando quicksort
    print("Lista ordenada:", ordenada)  # Imprime la lista ordenada
# Este código implementa el algoritmo de ordenamiento QuickSort de manera recursiva.
# El algoritmo selecciona un pivote y divide la lista en tres partes: menores, iguales y mayores que el pivote.
# Luego, ordena recursivamente las listas menores y mayores, y finalmente concatena las listas para obtener la lista ordenada.
# Este código implementa el algoritmo de ordenamiento QuickSort de manera recursiva.
# El algoritmo selecciona un pivote y divide la lista en tres partes: menores, iguales y mayores que el pivote.
# Luego, ordena recursivamente las listas menores y mayores, y finalmente concatena las listas para obtener la lista ordenada.
# Este código implementa el algoritmo de ordenamiento QuickSort de manera recursiva.