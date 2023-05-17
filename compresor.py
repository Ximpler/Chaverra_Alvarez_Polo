import os
import sys
import numpy as np



class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right


def verify_path_exists(path_w):
    return os.path.exists(path_w)


def frequency_dict(text):
    freq_dict = {}
    for i in text:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    return freq_dict


def huffman_code(freq_dict):
    # Convertir el diccionario de frecuencias en una lista de tuplas
    freq_list = [(freq_dict[symbol], symbol) for symbol in freq_dict]
    # Ordenar la lista de frecuencias en orden ascendente
    freq_list.sort()

    # Convertir la lista de tuplas en una lista de nodos
    nodes = [
        HuffmanNode(freq_list[i][0], freq_list[i][1]) for i in range(len(freq_list))
    ]

    # Combinar los nodos hasta que haya solo un nodo
    while len(nodes) > 1:
        # Tomar los dos nodos con la frecuencia más baja
        right = nodes.pop(0)
        left = nodes.pop(0)
        # Crear un nuevo nodo con la suma de sus frecuencias y los dos nodos como hijos
        parent = HuffmanNode(
            left.freq + right.freq, left.freq + right.freq, left, right
        )
        # Agregar el nuevo nodo a la lista de nodos y ordenarla
        nodes.append(parent)
        nodes.sort(key=lambda x: x.freq)
        for i in range(len(nodes) - 1):
            if (
                nodes[i].freq == nodes[i + 1].freq
                and nodes[i + 1].freq == nodes[i + 1].symbol
            ):
                nodes[i], nodes[i + 1] = nodes[i + 1], nodes[i]

    # Construir el diccionario de códigos Huffman
    code_dict = {}

    def traverse_tree(node, code=""):
        if node.symbol != node.freq:
            code_dict[node.symbol] = code
        else:
            traverse_tree(node.left, code + "0")
            traverse_tree(node.right, code + "1")

    traverse_tree(nodes[0])
    # print(code_dict)
    return code_dict


def compress_file(filename, code_dict):
    try:
        with open(filename, "r", encoding="ISO-8859-1") as f:
            text = f.read()
        compressed_string = ""
        for char in text:
            compressed_string += code_dict[char]
        return compressed_string
    except FileNotFoundError:
        print("Archivo no encontrado")
    except ValueError:
        print("Error al comprimir el archivo")


def generate_Compressed_File(compressed_string, code_dict, interlineado):
    with open("comprimido.elmejorprofesor", "wb") as f:
        np.save(f, (code_dict, interlineado))
        f.write(StrToBin(compressed_string))
        f.close()


"""def StrToBin(bin_str):
    # binary_data = int(bin_str, 2).to_bytes(len(bin_str) // 8, byteorder='big')
    binary_data = bytes(int(bin_str[i : i + 8], 2) for i in range(0, len(bin_str), 8))
    return binary_data  # ;"""

def StrToBin(bin_str):
    bin_str_filtered = filter(lambda x: x != ' ', bin_str)
    binary_data = bytes(int(ch, 2) for ch in bin_str_filtered)
    return binary_data

def ver_interlineado(filename):
    with open(filename, "rb") as f:
        contenido = f.read()

        

    if b"\r\n" in contenido:
        return "\r\n"
    else:
        return "\n"


#print("<------ Bienvenidos al sistema de compresión PYTHON ------>")

startTime = np.datetime64("now")
filename = sys.argv[1]
if verify_path_exists(filename):
    with open(filename, "r", encoding="ISO-8859-1", newline="") as f:
        text = f.read()
    interlineado = ver_interlineado(filename)
    # Función para comprimir el archivo
    print(frequency_dict(text))
    code_dict = huffman_code(frequency_dict(text))
    print(code_dict)
    compressed_string = compress_file(filename, code_dict) 
    #funcion para generar el comprimido .elmejorprofesor
    generate_Compressed_File(compressed_string, code_dict, interlineado)  
    print("Se generó su archivo comprimido")
    #tiempo
    compressOk = np.datetime64("now")
    time = compressOk - startTime
    print(
        "Se demoró ",
        time / np.timedelta64(1, "s"),
        " segundos en comprimir el archivo: ",
        filename,
    )
