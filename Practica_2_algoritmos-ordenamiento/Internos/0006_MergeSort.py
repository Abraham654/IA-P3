def merge_sort(arr): # Definir la función de ordenamiento por mezcla (Merge Sort)
    
    if len(arr) > 1:    # Verifica si el arreglo tiene más de un elemento
        mid = len(arr) // 2 # Encuentra el punto medio del arreglo
        left_half = arr[:mid]   # Divide el arreglo en dos mitades
        right_half = arr[mid:]      # Divide el arreglo en dos mitades

        # Recursively sort both halves  #   Ordena recursivamente ambas mitades
        merge_sort(left_half)   # Ordena la mitad izquierda
        merge_sort(right_half)  # Ordena la mitad derecha

        # Merge the sorted halves   # Combina las dos mitades ordenadas
        i = j = k = 0   # Inicializa los índices para las mitades y el arreglo original

        # Copy data to temp arrays left_half[] and right_half[]
        while i < len(left_half) and j < len(right_half):   # Mientras haya elementos en ambas mitades
            if left_half[i] < right_half[j]:    # Compara los elementos de ambas mitades
                arr[k] = left_half[i]   # Si el elemento de la mitad izquierda es menor
                i += 1  # Incrementa el índice de la mitad izquierda
            else:   # Si el elemento de la mitad derecha es menor o igual
                arr[k] = right_half[j]  # Asigna el elemento de la mitad derecha al arreglo original
                j += 1  # Incrementa el índice de la mitad derecha
            k += 1  # Incrementa el índice del arreglo original

        # Checking if any element was left  # Verifica si quedan elementos en alguna de las mitades
        while i < len(left_half):   # Si quedan elementos en la mitad izquierda
            arr[k] = left_half[i]   # Asigna el elemento restante al arreglo original
            i += 1  # Incrementa el índice de la mitad izquierda
            k += 1  # Incrementa el índice del arreglo original

        while j < len(right_half):  # Si quedan elementos en la mitad derecha
            arr[k] = right_half[j]  # Asigna el elemento restante al arreglo original
            j += 1  # Incrementa el índice de la mitad derecha
            k += 1  # Incrementa el índice del arreglo original

if __name__ == "__main__":  # Punto de entrada del script
    arr = [38, 27, 43, 3, 9, 82, 10]    # Lista de ejemplo para ordenar
    print("Original array:", arr)   # Imprime el arreglo original
    merge_sort(arr) # Llama a la función de ordenamiento por mezcla
    print("Sorted array:", arr) # Imprime el arreglo ya ordenado