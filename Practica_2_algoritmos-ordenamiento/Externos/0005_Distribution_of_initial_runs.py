import os
import heapq
import math
from typing import List, IO

class ExternalSort:
    def __init__(self, input_file: str, output_file: str, temp_dir: str = "temp_sort", 
                 block_size: int = 1000, num_tapes: int = 3):
        """
        Inicializa el ordenador externo
        
        Args:
            input_file: Archivo de entrada con los datos a ordenar
            output_file: Archivo de salida para los datos ordenados
            temp_dir: Directorio para archivos temporales
            block_size: Número de elementos que caben en memoria
            num_tapes: Número de "cintas" (archivos) a usar para la distribución
        """
        self.input_file = input_file
        self.output_file = output_file
        self.temp_dir = temp_dir
        self.block_size = block_size
        self.num_tapes = num_tapes
        self.runs = []

    def sort(self):
        """Ejecuta el proceso completo de ordenamiento externo"""
        try:
            self._prepare_temp_dir()
            self._generate_initial_runs()
            self._distribute_runs()
            self._merge_runs()
        finally:
            self._cleanup()

    def _prepare_temp_dir(self):
        """Prepara el directorio temporal"""
        if os.path.exists(self.temp_dir):
            for f in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, f))
        else:
            os.makedirs(self.temp_dir, exist_ok=True)

    def _generate_initial_runs(self):
        """
        Genera las corridas iniciales mediante ordenamiento interno.
        Cada corrida es del tamaño de block_size elementos.
        """
        with open(self.input_file, 'r') as infile:
            run_buffer = []
            run_count = 0
            
            for line in infile:
                num = line.strip()
                if num:
                    try:
                        run_buffer.append(int(num))
                        if len(run_buffer) >= self.block_size:
                            self._save_run(run_buffer, run_count)
                            run_count += 1
                            run_buffer = []
                    except ValueError:
                        continue
            
            if run_buffer:
                self._save_run(run_buffer, run_count)

    def _save_run(self, data: List[int], run_id: int):
        """Guarda una corrida ordenada en un archivo temporal"""
        data.sort()
        run_file = os.path.join(self.temp_dir, f"run_{run_id}.txt")
        with open(run_file, 'w') as f:
            f.writelines(f"{num}\n" for num in data)
        self.runs.append(run_file)

    def _distribute_runs(self):
        """
        Distribuye las corridas iniciales entre las cintas disponibles
        usando un algoritmo de distribución balanceada.
        """
        if not self.runs:
            raise ValueError("No hay corridas para distribuir")
        
        # Crear las cintas (archivos temporales)
        self.tapes = [os.path.join(self.temp_dir, f"tape_{i}.txt") for i in range(self.num_tapes)]
        
        # Distribuir corridas entre las cintas de forma balanceada
        for i, run_file in enumerate(self.runs):
            tape_idx = i % self.num_tapes
            with open(run_file, 'r') as src, open(self.tapes[tape_idx], 'a') as dest:
                dest.writelines(src.readlines())
            
            # Eliminar el archivo de corrida individual
            os.remove(run_file)
        
        self.runs = []  # Las corridas ahora están en las cintas

    def _merge_runs(self):
        """Fusiona las corridas de las cintas hasta obtener un solo archivo ordenado"""
        while True:
            # Determinar qué cintas tienen datos
            active_tapes = [tape for tape in self.tapes if os.path.exists(tape) and os.path.getsize(tape) > 0]
            
            if len(active_tapes) <= 1:
                break  # Solo queda una cinta con datos
            
            # Crear un nuevo conjunto de cintas para la siguiente fase
            new_tapes = [os.path.join(self.temp_dir, f"merge_{i}.txt") for i in range(self.num_tapes)]
            output_tape_idx = 0
            
            # Procesar en grupos de (num_tapes-1) cintas
            for i in range(0, len(active_tapes), self.num_tapes-1):
                input_tapes = active_tapes[i:i+self.num_tapes-1]
                if not input_tapes:
                    continue
                
                # Fusionar el grupo actual
                self._merge_to_tape(input_tapes, new_tapes[output_tape_idx])
                output_tape_idx = (output_tape_idx + 1) % self.num_tapes
            
            # Eliminar las cintas antiguas y actualizar a las nuevas
            for tape in self.tapes:
                if os.path.exists(tape):
                    os.remove(tape)
            
            self.tapes = new_tapes
        
        # El resultado final está en la primera cinta con datos
        final_tape = next(tape for tape in self.tapes if os.path.exists(tape) and os.path.getsize(tape) > 0)
        os.rename(final_tape, self.output_file)

    def _merge_to_tape(self, input_files: List[str], output_file: str):
        """
        Fusiona múltiples archivos de entrada en un solo archivo de salida
        usando un min-heap para la fusión multiway.
        """
        file_handles = [open(f, 'r') for f in input_files]
        heap = []
        
        # Inicializar el heap con el primer elemento de cada archivo
        for i, fh in enumerate(file_handles):
            line = fh.readline()
            if line:
                try:
                    heapq.heappush(heap, (int(line.strip()), i))
                except ValueError:
                    pass
        
        with open(output_file, 'w') as outfile:
            while heap:
                val, tape_idx = heapq.heappop(heap)
                outfile.write(f"{val}\n")
                
                # Leer el siguiente elemento del archivo correspondiente
                line = file_handles[tape_idx].readline()
                if line:
                    try:
                        heapq.heappush(heap, (int(line.strip()), tape_idx))
                    except ValueError:
                        pass
        
        # Cerrar todos los archivos
        for fh in file_handles:
            fh.close()

    def _cleanup(self):
        """Limpia archivos temporales"""
        if os.path.exists(self.temp_dir):
            for f in os.listdir(self.temp_dir):
                try:
                    os.remove(os.path.join(self.temp_dir, f))
                except:
                    pass
            try:
                os.rmdir(self.temp_dir)
            except:
                pass


if __name__ == "__main__":
    # Ejemplo de uso
    input_file = "input.txt"
    output_file = "sorted_output.txt"
    
    # Generar datos de prueba si no existen
    if not os.path.exists(input_file):
        import random
        print("Generando archivo de entrada con datos aleatorios...")
        with open(input_file, 'w') as f:
            for _ in range(100000):  # 100,000 números aleatorios
                f.write(f"{random.randint(1, 1000000)}\n")
    
    print("Iniciando ordenamiento externo...")
    sorter = ExternalSort(
        input_file=input_file,
        output_file=output_file,
        block_size=5000,  # Tamaño de bloque (elementos en memoria)
        num_tapes=3       # Número de cintas para distribución
    )
    sorter.sort()
    
    print(f"Ordenamiento completado. Resultado guardado en {output_file}")