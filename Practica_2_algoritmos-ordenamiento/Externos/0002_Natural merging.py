import os

def split_runs(input_file, temp1, temp2):
    with open(input_file, 'r') as infile, \
         open(temp1, 'w') as out1, \
         open(temp2, 'w') as out2:
        last = None
        toggle = True
        for line in infile:
            num = int(line.strip())
            if last is not None and num < last:
                toggle = not toggle
            if toggle:
                out1.write(f"{num}\n")
            else:
                out2.write(f"{num}\n")
            last = num

def merge_runs(temp1, temp2, output_file):
    with open(temp1, 'r') as in1, \
         open(temp2, 'r') as in2, \
         open(output_file, 'w') as out:
        def next_num(f):
            line = f.readline()
            return int(line.strip()) if line else None

        n1, n2 = next_num(in1), next_num(in2)
        last1, last2 = None, None
        while n1 is not None or n2 is not None:
            run1, run2 = True, True
            while run1 or run2:
                if (n1 is not None and (n2 is None or n1 <= n2)) and run1:
                    out.write(f"{n1}\n")
                    last1 = n1
                    n1 = next_num(in1)
                    if n1 is not None and last1 > n1:
                        run1 = False
                elif n2 is not None and run2:
                    out.write(f"{n2}\n")
                    last2 = n2
                    n2 = next_num(in2)
                    if n2 is not None and last2 > n2:
                        run2 = False
                else:
                    break

def is_sorted(input_file):
    with open(input_file, 'r') as f:
        last = None
        for line in f:
            num = int(line.strip())
            if last is not None and num < last:
                return False
            last = num
    return True

def natural_merge_sort(input_file, output_file):
    temp1 = 'temp1.txt'
    temp2 = 'temp2.txt'
    src = input_file
    dst = output_file
    while True:
        split_runs(src, temp1, temp2)
        merge_runs(temp1, temp2, dst)
        if is_sorted(dst):
            break
        src, dst = dst, src
    os.remove(temp1)
    os.remove(temp2)
    if dst != output_file:
        os.replace(dst, output_file)

# Ejemplo de uso:
# Crear un archivo de entrada con números desordenados, uno por línea.
# natural_merge_sort('entrada.txt', 'salida.txt')