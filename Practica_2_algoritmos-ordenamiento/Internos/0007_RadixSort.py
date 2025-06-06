def counting_sort(arr, exp):    # Definir la función de ordenamiento por conteo para Radix Sort
    n = len(arr)    # Obtener la longitud del arreglo
    output = [0] * n    # Crear un arreglo de salida del mismo tamaño que arr
    count = [0] * 10    # Crear un arreglo de conteo para los dígitos (0-9)

    # Contar ocurrencias de dígitos en la posición actual (exp)
    for i in range(n):      # Recorre cada elemento del arreglo
        index = (arr[i] // exp) % 10    # Obtener el dígito en la posición exp
        count[index] += 1   # Incrementar el conteo de ese dígito

    # Cambiar count[i] para que contenga la posición real de este dígito en output[]
    for i in range(1, 10):      # Recorre el arreglo de conteo
        count[i] += count[i - 1]    # Acumular el conteo para posiciones

    # Construir el arreglo de salida
    i = n - 1   # Empezar desde el final del arreglo original
    while i >= 0:   # Mientras haya elementos por procesar
        index = (arr[i] // exp) % 10    # Obtener el dígito en la posición exp
        output[count[index] - 1] = arr[i]   # Colocar el elemento en la posición correcta en output
        count[index] -= 1   # Decrementar el conteo para ese dígito
        i -= 1  # Mover al siguiente elemento en arr

    # Copiar el arreglo de salida al arreglo original
    for i in range(n):  # Recorre el arreglo de salida
        arr[i] = output[i]  # Asigna los valores ordenados de output a arr

def radix_sort(arr):    # Definir la función de ordenamiento Radix Sort
    # Encontrar el número máximo para saber el número de dígitos  
    max_num = max(arr) if arr else 0    # Obtener el valor máximo del arreglo, o 0 si está vacío

    # Aplicar counting sort para cada dígito
    exp = 1 # Inicializar el exponente para el dígito actual (1, 10, 100, ...)
    while max_num // exp > 0:   # Mientras haya dígitos que procesar
        counting_sort(arr, exp) # Llamar a counting_sort para ordenar por el dígito actual
        exp *= 10   # Incrementar el exponente para el siguiente dígito

# Ejemplo de uso
if __name__ == "__main__":  # Punto de entrada del script
    arr = [170, 45, 75, 90, 802, 24, 2, 66] # Lista de ejemplo para ordenar
    print("Arreglo original:", arr) # Imprime el arreglo original
    radix_sort(arr) # Llama a la función de ordenamiento Radix Sort
    print("Arreglo ordenado:", arr) # Imprime el arreglo ya ordenado
# Este código implementa el algoritmo de ordenamiento Radix Sort utilizando Counting Sort como subrutina.
# Radix Sort es un algoritmo eficiente para ordenar números enteros, especialmente cuando los números tienen un rango limitado.