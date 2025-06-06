def intercambio_sort(arr):  # Definir la función de ordenamiento por intercambio
    n = len(arr)  # Obtiene la longitud de la lista
    for i in range(n - 1):  # Recorre la lista desde el primer hasta el penúltimo elemento
        for j in range(i + 1, n):  # Compara el elemento actual con los siguientes elementos
            if arr[i] > arr[j]:  # Si el elemento actual es mayor que el siguiente
                arr[i], arr[j] = arr[j], arr[i]  # Intercambia los elementos

if __name__ == "__main__":  # Punto de entrada del script
    # Lista de ejemplo para ordenar
    lista = [34, 7, 23, 32, 5, 62]  # Define la lista de números a ordenar
    print("Lista original:", lista)  # Imprime la lista original
    intercambio_sort(lista)  # Llama a la función de ordenamiento
    print("Lista ordenada:", lista)  # Imprime la lista ya ordenada