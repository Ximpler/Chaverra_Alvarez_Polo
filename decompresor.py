import os
import sys
import numpy as np

def verify_path_exists(path_w):
    return os.path.exists(path_w)

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
filename = sys.argv[1]
#filename = "comprimido.elmejorprofesor"
code_dict, compressed_string = open_compressed_file(filename)
#pasar de binario a string el comprimido (01010 -> "01010")
compressed_string = combine_arrays(compressed_string)
compressed_string = BintoStr(compressed_string)
tamaño = len(compressed_string)
#decodificar el string binario
data = decompress_string(compressed_string, code_dict)
decoded_text = ArrayToString(data)
generate_DesCompressed_File("descomprimido-elmejorprofesor.txt", decoded_text)
    
descompressOk = np.datetime64("now")
time = descompressOk - startTime

print(
    time / np.timedelta64(1, "s")
)