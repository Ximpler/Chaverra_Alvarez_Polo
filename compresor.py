import os
import sys
import numpy as np
import re


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


def compress_file(text, code_dict):
    compressed_string = ""
    for char in text:
        compressed_string += code_dict[char]
    return compressed_string

def generate_Compressed_File(compressed_string, code_dict):
    with open("comprimido.elmejorprofesor", "wb") as f:
        np.save(f, (code_dict, compressed_string))
        #f.write(StrToBin(compressed_string))
        f.close()


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

startTime = np.datetime64("now")
filename = sys.argv[1]
if verify_path_exists(filename):
    with open(filename, "r", encoding="ISO-8859-1", newline="") as f:
        text = f.read()
    text_lineas = re.split(r'(\r\n|\r|\n)', text)
    num_lineas = len(text_lineas)
    print(frequency_dict(text))
    code_dict = huffman_code(frequency_dict(text))
    print(code_dict)
    compressed_string = [compress_file(elemento, code_dict) for elemento in text_lineas]
    compressed_string = [StrToBin(elemento) for elemento in compressed_string]
    #funcion para generar el comprimido .elmejorprofesor
    generate_Compressed_File(compressed_string, code_dict)  
    #tiempo
    compressOk = np.datetime64("now")
    time = compressOk - startTime
    print(
        time / np.timedelta64(1, "s"),
    )
