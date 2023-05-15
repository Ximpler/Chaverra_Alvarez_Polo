import os
import sys
import numpy as np


def verify_path_exists(path_w):
    return os.path.exists(path_w)


def StrToIntArray(str):
    mi_array = [int(digito) for digito in str]
    print(mi_array)
    return mi_array


def open_compressed_file(archivo):
    try:
        with open(archivo, "rb") as f:
            data = np.load(f, allow_pickle=True)
            code_dict = data[0]
            interlineado = data[1]
            compressed_string = f.read()
            f.close()
        return code_dict, interlineado, compressed_string
    except FileNotFoundError:
        print("Archivo no encontrado")
    except ValueError:
        print("Error al descomprimir el archivo")


def BintoStr(binary_data):
    bin_str = "".join(format(byte, "08b") for byte in binary_data)
    return bin_str

#notaaaaaaaaaaaaaaaaaa
def generate_DesCompressed_File(file_name, decoded_text, interlineado):
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
print("<------ Bienvenidos al sistema de descompresión PYTHON ------>")
filename = "comprimido.elmejorprofesor"
if verify_path_exists(filename):
    code_dict, interlineado, compressed_string = open_compressed_file(filename)
    #pasar de binario a string el comprimido (01010 -> "01010")
    compressed_string = BintoStr(compressed_string)
    #decodificar el string binario
    decoded_text = decompress_string(compressed_string, code_dict)
    #muerto en el closet
    #posicion_ultimo_espacio = decoded_text.rfind(" ")
    #nueva_cadena = decoded_text[:posicion_ultimo_espacio]
    generate_DesCompressed_File("descomprimido-elmejorprofesor.txt", decoded_text, interlineado)
    print("Se generó su archivo descomprimido")
else:
    print("Error: La ruta especificada NO existe")
descompressOk = np.datetime64("now")
time = descompressOk - startTime
print(
    "Se demoró ", time / np.timedelta64(1, "s"), " segundos en descomprimir el archivo"
)
