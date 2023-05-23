import os
import sys
import numpy as np
from mpi4py import MPI


def combine_arrays(array_de_arrays):
    array_combinado = []
    for array in array_de_arrays:
        array_combinado.extend(array)

    return array_combinado

def open_compressed_file(archivo):
    try:
        with open(archivo, "rb") as f:
            data = np.load(f, allow_pickle=True)
            code_dict = data[0]
            compressed_string = data[1]
            f.close()
        return code_dict, compressed_string
    except FileNotFoundError:
        print("Archivo no encontrado")
    except ValueError:
        print("Error al descomprimir el archivo")


def BintoStr(binary_data):
    bin_str = "".join(format(byte, "b") for byte in binary_data)
    return bin_str

def ArrayToString(Array):
    # Usamos la función map para convertir cada valor del array en un string
    arr_str = list(map(str, Array))
    # Concatenamos todos los elementos del array en un solo string usando el método join
    string = ''.join(arr_str)
    return string

def generate_DesCompressed_File(file_name, decoded_text):
    with open(file_name, "w", encoding="ISO-8859-1") as f:
        f.write(decoded_text)
        f.close()


def decompress_string(compressed_string, code_dict):
    # Invertir el diccionario de códigos Huffman para buscar los símbolos por código
    inverse_dict = {code_dict[char]: char for char in code_dict}
    # Decodificar la cadena comprimida
    decoded_text = ""
    code = ""
    for bit in compressed_string:
        code += bit
        if code in inverse_dict:
            decoded_text += inverse_dict[code]
            code = ""
    return decoded_text


startTime = np.datetime64("now")
#filename = sys.argv[1]
filename = "comprimido.elmejorprofesor"
code_dict, compressed_string = open_compressed_file(filename)
#pasar de binario a string el comprimido (01010 -> "01010")

#compressed_string = [BintoStr(elemento) for elemento in compressed_string]
compressed_string = BintoStr(compressed_string)
compressed_string = remove_padding(compressed_string)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
bits_proceso = [None]*size
data = None
if(rank==0):
    tamaño = len(compressed_string)
    bits_por_proceso = tamaño // size
    resto = tamaño % size
    padding_bits = (size - resto) % size
    compressed_string += "0" * padding_bits
    # Calcular el rango de líneas asignadas a cada proceso
    for i in range(size):
        inicio = i * bits_por_proceso
        fin = inicio + bits_por_proceso
        # Ajustar el rango de líneas para el último proceso si hay un resto
        if i == size - 1:
            fin += resto
        # Dividir las líneas asignadas a cada proceso
        bits_proceso[i] = compressed_string[inicio:fin]
        # Aquí puedes realizar el procesamiento de los datos en cada proceso
        # ...
    # Calcular el número de bits adicionales necesarios
    
    data = bits_proceso
    #decodificar el string binario
    data0 = comm.scatter(data, root=0)
    data0 = [decompress_string(elemento, code_dict) for elemento in data0]
    decoded_text = comm.gather(data0,root=0)
    decoded_text = combine_arrays(decoded_text)
    decoded_text = ArrayToString(decoded_text)
    generate_DesCompressed_File("descomprimido-elmejorprofesor.txt", decoded_text)
else:
    data = comm.scatter(data, root=0)
    data = [decompress_string(elemento, code_dict) for elemento in data]
    comm.gather(data,root=0)

MPI.Finalize()
descompressOk = np.datetime64("now")
time = descompressOk - startTime

print(
    time / np.timedelta64(1, "s")
)
