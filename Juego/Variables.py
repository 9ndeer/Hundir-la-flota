TAMANO = 10

# nombre: (eslora, cantidad)
BARCOS = {
    "lancha": (1, 4),
    "crucero": (2, 3),
    "acorazado": (3, 2),
    "portaaviones": (4, 1),
}

AGUA = " "
BARCO = "O"
IMPACTO = "X"
FALLO = "-"

# orientación: (cambio en fila, cambio en columna)
ORIENTACIONES = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}