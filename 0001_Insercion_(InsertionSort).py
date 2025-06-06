def insertion_sort(arr):    #Definir la función de ordenamiento por inserción
    # Recorre el arreglo desde el segundo elemento hasta el final
    for i in range(1, len(arr)):
        key = arr[i]              # Guarda el valor actual a insertar
        j = i - 1                 # Inicializa j con el índice anterior a i
        # Desplaza los elementos mayores que key una posición adelante
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]   # Mueve el elemento una posición adelante
            j -= 1                # Decrementa j para comparar con el elemento anterior
        arr[j + 1] = key          # Inserta key en la posición correcta

# Ejemplo de uso
if __name__ == "__main__":
    lista = [5, 2, 9, 1, 5, 6]    # Lista de ejemplo a ordenar
    print("Lista original:", lista) # Muestra la lista antes de ordenar
    insertion_sort(lista)           # Llama a la función de ordenamiento
    print("Lista ordenada:", lista) # Muestra la lista ya ordenada