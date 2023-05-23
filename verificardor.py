import sys


def comparar_archivos(archivo1, archivo2):
    with open(archivo1, "r", encoding="ISO-8859-1") as f1, open(
        archivo2, "r", encoding="ISO-8859-1"
    ) as f2:
        contenido1 = f1.read()
        contenido2 = f2.read()
        if contenido1 == contenido2:
            return "ok"
        else:
            return "nok"


filename = sys.argv[1]
filename_des = sys.argv[2]
print(comparar_archivos(filename, filename_des))