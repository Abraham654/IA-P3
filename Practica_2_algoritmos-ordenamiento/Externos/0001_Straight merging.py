import os

def split_file(input_file, temp1, temp2, run_size):
    with open(input_file, 'r') as infile, \
         open(temp1, 'w') as out1, \
         open(temp2, 'w') as out2:
        toggle = True
        while True:
            lines = []
            for _ in range(run_size):
                line = infile.readline()
                if not line:
                    break
                lines.append(line)
            if not lines:
                break
            if toggle:
                out1.writelines(lines)
            else:
                out2.writelines(lines)
            toggle = not toggle

def merge_files(temp1, temp2, output_file, run_size):
    with open(temp1, 'r') as in1, \
         open(temp2, 'r') as in2, \
         open(output_file, 'w') as out:
        while True:
            run1 = []
            run2 = []
            for _ in range(run_size):
                line = in1.readline()
                if not line:
                    break
                run1.append(int(line.strip()))
            for _ in range(run_size):
                line = in2.readline()
                if not line:
                    break
                run2.append(int(line.strip()))
            if not run1 and not run2:
                break
            i = j = 0
            while i < len(run1) and j < len(run2):
                if run1[i] <= run2[j]:
                    out.write(f"{run1[i]}\n")
                    i += 1
                else:
                    out.write(f"{run2[j]}\n")
                    j += 1
            while i < len(run1):
                out.write(f"{run1[i]}\n")
                i += 1
            while j < len(run2):
                out.write(f"{run2[j]}\n")
                j += 1

def straight_merge_sort(input_file, output_file):
    n = sum(1 for _ in open(input_file))
    run_size = 1
    temp1 = 'temp1.txt'
    temp2 = 'temp2.txt'
    while run_size < n:
        split_file(input_file, temp1, temp2, run_size)
        merge_files(temp1, temp2, output_file, run_size)
        input_file, output_file = output_file, input_file
        run_size *= 2
    if input_file != output_file:
        os.replace(input_file, output_file)
    os.remove(temp1)
    os.remove(temp2)

# Ejemplo de uso:
# Supón que tienes un archivo 'datos.txt' con un número por línea.
# straight_merge_sort('datos.txt', 'ordenado.txt')