def selection_sort(arr):# Definir la función de ordenamiento por selección
    n = len(arr)  # Obtiene la longitud del arreglo
    for i in range(n):  # Recorre cada elemento del arreglo
        min_idx = i  # Supone que el elemento actual es el mínimo
        for j in range(i+1, n):  # Busca el elemento más pequeño en el resto del arreglo
            if arr[j] < arr[min_idx]:  # Si encuentra un elemento menor
                min_idx = j  # Actualiza el índice del mínimo
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # Intercambia el elemento actual con el mínimo encontrado

if __name__ == "__main__":  # Punto de entrada del script
    # Lista de ejemplo para ordenar
    lista = [64, 25, 12, 22, 11]  # Lista de ejemplo a ordenar
    print("Lista original:", lista)  # Imprime la lista original
    selection_sort(lista)  # Llama a la función de ordenamiento por selección
    print("Lista ordenada:", lista)  # Imprime la lista ya ordenada