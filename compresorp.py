import os
import sys
import numpy as np
from mpi4py import MPI


class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right


def verify_path_exists(path_w):
    return os.path.exists(path_w)


def frequency_dict(dato):
    if type(dato)==str:
        freq_dict = {}
        for i in dato:
            if i in freq_dict:
                freq_dict[i] += 1
            else:
                freq_dict[i] = 1
        return freq_dict
    else:
        freq_dict = {}
        for freq_dict_temp in dato:
            for symbol in freq_dict_temp:
                if symbol in freq_dict:
                    freq_dict[symbol] += freq_dict_temp[symbol]
                else:
                    freq_dict[symbol] = freq_dict_temp[symbol]
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
    #text += " prueba" # <----nota importante
    compressed_string = ""
    for char in text:
        compressed_string += code_dict[char]
    return compressed_string


def generate_Compressed_File(compressed_string, code_dict, interlineado):
    with open("comprimido.elmejorprofesor", "wb") as f:
        if code_dict != None:
            np.save(f, (code_dict, interlineado))
        f.write(StrToBin(compressed_string))
        f.close()


def StrToBin(bin_str):
    # binary_data = int(bin_str, 2).to_bytes(len(bin_str) // 8, byteorder='big')
    binary_data = bytes(int(bin_str[i : i + 8], 2) for i in range(0, len(bin_str), 8))
    return binary_data  # ;

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
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    lineas_proceso = []
    data = None
    Condicion = True
    if rank == 0:
        with open(filename, "r", encoding="ISO-8859-1", newline="") as r:
            text = r.read()
        interlineado = ver_interlineado(filename)
        #texto dividido en lineas
        text_lineas = list(text.split(interlineado))
        for i in text_lineas:
            i = i+interlineado
        num_lineas = len(text_lineas)
        # Calcular el número de líneas por proceso
        lineas_por_proceso = num_lineas // size-1
        resto = num_lineas % size
        # Calcular el rango de líneas asignadas a cada proceso
        for i in range(size-1):
            inicio = (i+1) * lineas_por_proceso
            fin = inicio + lineas_por_proceso
            # Ajustar el rango de líneas para el último proceso si hay un resto
            if i+1 == size -1:
                fin += resto
            # Dividir las líneas asignadas a cada proceso
            lineas_proceso[i+1] = text_lineas[inicio:fin]
            # Aquí puedes realizar el procesamiento de los datos en cada proceso
            # ...
        lineas_proceso[0] = None;
        data = lineas_proceso
        data = comm.scatter(data, root=0)
        freq_dict = comm.gather(None, root=0)
        freq_dict = frequency_dict(freq_dict)
        print(freq_dict)
    else:
        data = comm.scatter(None, root=0)
        freq_dict = frequency_dict(data);
        comm.gather(freq_dict, root=0)
    
    MPI.Finalize()
    
    #tiempo
    compressOk = np.datetime64("now")
    time = compressOk - startTime
    print(
        "Se demoró ",
        time / np.timedelta64(1, "s"),
        " segundos en comprimir el archivo: ",
        filename,
    )
