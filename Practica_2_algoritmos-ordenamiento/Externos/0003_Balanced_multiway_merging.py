import os
import heapq

def balanced_multiway_merge_sort(input_file_path, output_file_path, num_ways=4, chunk_size=10000):
    
    print(f"Iniciando Balanced Multiway Merging para '{input_file_path}'...")
    print(f"Número de caminos (num_ways): {num_ways}")
    print(f"Tamaño del chunk (chunk_size): {chunk_size}")

    # --- Fase 1: Creación de "runs" iniciales (archivos intermedios ordenados) ---
    print("\nFase 1: Creando runs iniciales...")
    temp_run_files = []
    try:
        with open(input_file_path, 'r') as infile:
            chunk = []
            run_count = 0
            for line in infile:
                try:
                    num = int(line.strip())
                    chunk.append(num)
                except ValueError:
                    print(f"Advertencia: Saltando línea no numérica: '{line.strip()}'")
                    continue

                if len(chunk) >= chunk_size:
                    chunk.sort()  # Ordenamiento interno del chunk
                    temp_run_file_path = f"temp_run_{run_count}.txt"
                    with open(temp_run_file_path, 'w') as temp_file:
                        for item in chunk:
                            temp_file.write(f"{item}\n")
                    temp_run_files.append(temp_run_file_path)
                    chunk = []
                    run_count += 1
                    print(f"Creado run inicial: {temp_run_file_path}")

            # Escribir el último chunk si no está vacío
            if chunk:
                chunk.sort()
                temp_run_file_path = f"temp_run_{run_count}.txt"
                with open(temp_run_file_path, 'w') as temp_file:
                    for item in chunk:
                        temp_file.write(f"{item}\n")
                temp_run_files.append(temp_run_file_path)
                print(f"Creado run inicial: {temp_run_file_path}")

    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_file_path}' no fue encontrado.")
        return
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la Fase 1: {e}")
        # Limpiar archivos temporales en caso de error
        for f in temp_run_files:
            if os.path.exists(f):
                os.remove(f)
        return

    if not temp_run_files:
        print("El archivo de entrada está vacío o no contiene números válidos. No hay nada que ordenar.")
        # Crear un archivo de salida vacío si no hay datos.
        open(output_file_path, 'w').close()
        return

    # --- Fase 2: Fusión de runs (pasadas múltiples) ---
    print("\nFase 2: Fusionando runs...")
    current_files = temp_run_files
    pass_num = 0

    while len(current_files) > 1:
        pass_num += 1
        print(f"\nIniciando pasada de fusión #{pass_num} con {len(current_files)} archivos...")
        next_pass_files = []

        for i in range(0, len(current_files), num_ways):
            files_to_merge = current_files[i : i + num_ways]
            if not files_to_merge:
                continue

            output_temp_file_path = f"temp_merge_pass_{pass_num}_part_{i // num_ways}.txt"
            print(f"  Fusionando: {files_to_merge} -> {output_temp_file_path}")

            try:
                # Abrir archivos de entrada para la fusión
                input_file_handlers = []
                for f_path in files_to_merge:
                    input_file_handlers.append(open(f_path, 'r'))

                # Usar un min-heap para la fusión K-way
                # Cada elemento en el heap es una tupla: (valor, índice_del_archivo, línea_completa)
                min_heap = []
                for idx, fh in enumerate(input_file_handlers):
                    line = fh.readline()
                    if line:
                        try:
                            value = int(line.strip())
                            heapq.heappush(min_heap, (value, idx, line))
                        except ValueError:
                            print(f"Advertencia: Saltando línea no numérica en archivo intermedio: '{line.strip()}'")


                with open(output_temp_file_path, 'w') as outfile:
                    while min_heap:
                        min_val, source_idx, original_line = heapq.heappop(min_heap)
                        outfile.write(original_line) # Escribimos la línea original para mantener formato

                        # Leer el siguiente elemento del archivo del que sacamos el mínimo
                        next_line = input_file_handlers[source_idx].readline()
                        if next_line:
                            try:
                                next_val = int(next_line.strip())
                                heapq.heappush(min_heap, (next_val, source_idx, next_line))
                            except ValueError:
                                print(f"Advertencia: Saltando línea no numérica en archivo intermedio: '{next_line.strip()}'")

                next_pass_files.append(output_temp_file_path)

            except Exception as e:
                print(f"Ocurrió un error inesperado durante la fusión en la pasada {pass_num}: {e}")
                # Cerrar todos los manejadores de archivos y limpiar
                for fh in input_file_handlers:
                    fh.close()
                for f in current_files + next_pass_files:
                    if os.path.exists(f):
                        os.remove(f)
                return
            finally:
                # Asegurarse de cerrar todos los manejadores de archivos abiertos
                for fh in input_file_handlers:
                    fh.close()

        # Eliminar los archivos de la pasada anterior
        print(f"  Eliminando archivos temporales de la pasada anterior ({len(current_files)} archivos)...")
        for f in current_files:
            if os.path.exists(f):
                os.remove(f)
        current_files = next_pass_files

    # --- Fase 3: Renombrar el archivo final y limpiar ---
    if current_files:
        final_sorted_file = current_files[0]
        try:
            os.rename(final_sorted_file, output_file_path)
            print(f"\nOrdenamiento completado. Resultado guardado en '{output_file_path}'")
        except OSError as e:
            print(f"Error al renombrar el archivo final de '{final_sorted_file}' a '{output_file_path}': {e}")
            print(f"El archivo ordenado final se encuentra en: '{final_sorted_file}'")
    else:
        print("\n¡Algo salió mal! No se generó ningún archivo de salida final.")


def create_large_test_file(filename="large_numbers.txt", num_elements=1000000, max_value=10000000):
    """
    Crea un archivo de texto grande con números enteros aleatorios para pruebas.
    """
    import random
    print(f"Creando archivo de prueba: '{filename}' con {num_elements} números...")
    with open(filename, 'w') as f:
        for _ in range(num_elements):
            f.write(f"{random.randint(1, max_value)}\n")
    print("Archivo de prueba creado exitosamente.")

def verify_sorted_file(filepath):
    """
    Verifica si un archivo de números está ordenado de forma ascendente.
    """
    print(f"\nVerificando archivo: '{filepath}'...")
    try:
        with open(filepath, 'r') as f:
            prev_num = float('-inf')
            for line_num, line in enumerate(f, 1):
                try:
                    current_num = int(line.strip())
                    if current_num < prev_num:
                        print(f"¡Error de ordenamiento en la línea {line_num}! {current_num} < {prev_num}")
                        return False
                    prev_num = current_num
                except ValueError:
                    print(f"Advertencia: Línea no numérica en el archivo de verificación: '{line.strip()}'")
                    continue
        print("El archivo está correctamente ordenado.")
        return True
    except FileNotFoundError:
        print(f"Error: El archivo '{filepath}' no fue encontrado para verificación.")
        return False
    except Exception as e:
        print(f"Ocurrió un error durante la verificación del archivo: {e}")
        return False

if __name__ == "__main__":
    # --- Configuración para pruebas ---
    input_file = "unsorted_numbers.txt"
    output_file = "sorted_numbers.txt"
    test_num_elements = 500000 # Un buen tamaño para probar sin que sea excesivamente lento
    test_max_value = 1000000

    # Crear un archivo de prueba grande
    create_large_test_file(input_file, test_num_elements, test_max_value)

    # Ejecutar el algoritmo de ordenamiento
    balanced_multiway_merge_sort(input_file, output_file, num_ways=8, chunk_size=50000)

    # Verificar el archivo de salida
    verify_sorted_file(output_file)

    # --- Limpiar archivos de prueba ---
    print("\nLimpiando archivos de prueba...")
    if os.path.exists(input_file):
        os.remove(input_file)
    if os.path.exists(output_file):
        os.remove(output_file)
    print("Archivos de prueba limpiados.")