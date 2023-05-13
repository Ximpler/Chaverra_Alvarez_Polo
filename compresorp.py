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


def compress_file(filename, code_dict):
    try:
        with open(filename, "r", encoding="ISO-8859-1") as f:
            text = f.read()
        text += " prueba" # <----nota importante
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

    data = None
    Condicion = True
    if rank == 0:
        with open(filename, "r", encoding="ISO-8859-1", newline="") as r:
            text = r.read()
        interlineado = ver_interlineado(filename)
        data = list(text.split(interlineado))
        array_lineas = data
        while len(array_lineas) > 0:
            lineas = []
            for i in range(size):
                try:
                    if len(array_lineas) >= 10:
                        lineas.append(''.join(str(x) for x in array_lineas[:10]))
                        del array_lineas[:10]
                    else:
                        lineas.append(''.join(str(x) for x in array_lineas[:]))
                        del array_lineas[:]
                except:
                    lineas.append(None)
            data = lineas
            data = comm.scatter(data, root=0)
            # Aquí puedes realizar el procesamiento de los datos en cada proceso
            # ...
        freq_dict2 = comm.gather(None, root=0)
        print(freq_dict2)
        code_dict = huffman_code(freq_dict2)
        print(huffman_code)
    else:
        freq_dict2={}
        #primero dividimos y damos a cada quien un pedazo de texto para que vaya sacando el diccionario
        while Condicion:
            data = comm.scatter(None, root=0)
            if data is None:
                Condicion = False
            else:
                freq_dict=frequency_dict(data)
                #sumamos los dos diccionarios
                freq_dict2=frequency_dict([freq_dict,freq_dict2])
        comm.gather(freq_dict2, root=0)
        code_dict= comm.scatter(None, root=0)
        
        #dividimos y damos a cada quien un pedazo de texto, esta vez para que todos vayan sacando el string comprimido
        """Condicion = True;
        while Condicion:
            data = comm.scatter(None, root=0)
            if data is None:
                Condicion = False
            else:
                compressed_string = compress_file(data, code_dict) 
        comm.gather(freq_dict2, root=0)
        
        #funcion para generar el comprimido .elmejorprofesor
        generate_Compressed_File(compressed_string, code_dict, interlineado)  
        print("Se generó su archivo comprimido")"""
    
    #tiempo
    compressOk = np.datetime64("now")
    time = compressOk - startTime
    print(
        "Se demoró ",
        time / np.timedelta64(1, "s"),
        " segundos en comprimir el archivo: ",
        filename,
    )
