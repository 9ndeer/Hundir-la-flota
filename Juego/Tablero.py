import random
from Juego.Variables import TAMANO, BARCOS, AGUA, BARCO, IMPACTO, FALLO, ORIENTACIONES


class Tablero:
    def __init__(self, id_jugador):
        self.id_jugador = id_jugador
        self.tamano = TAMANO
        self.barcos = BARCOS
        self.tablero = [[AGUA] * TAMANO for valor in range(TAMANO)]   # barcos + impactos
        self.disparos = [[AGUA] * TAMANO for valor in range(TAMANO)]  # lo que ve el rival
        self.vidas = sum(eslora * cant for eslora, cant in BARCOS.values())
        self.flota = []            # lista de (nombre, set de casillas)
        self.ultimo_hundido = ""
        self.objetivos = []   # casillas a probar después de un impacto

    def mostrar(self, tablero):
        print("    ", end="")
        for numero_columna in range(TAMANO):
            print(numero_columna, end=" ")
        print()

        for numero_fila in range(TAMANO):
            print(numero_fila, end="   ")
            for casilla in tablero[numero_fila]:
                print(casilla, end=" ")
            print()

    def hay_barco_cerca(self, casillas):

        for f, c in casillas:
            for cambio_fila in (-1, 0, 1):
                for cambio_columna in (-1, 0, 1):
                    fila_vecina = f + cambio_fila
                    columna_vecina = c + cambio_columna
                    if 0 <= fila_vecina < TAMANO and 0 <= columna_vecina < TAMANO:
                        if self.tablero[fila_vecina][columna_vecina] == BARCO:
                            return True
        return False

    def colocar_barco(self, nombre, eslora):
        while True:
            fila = random.randint(0, self.tamano - 1)
            col = random.randint(0, self.tamano - 1)
            filaR, columnaR = ORIENTACIONES[random.choice(list(ORIENTACIONES))]
            casillas = [(fila + filaR * i, col + columnaR * i) for i in range(eslora)]

            if not all(0 <= f < self.tamano and 0 <= c < self.tamano for f, c in casillas):
                continue

            if self.hay_barco_cerca(casillas):
                continue

            for f, c in casillas:
                self.tablero[f][c] = BARCO
            self.flota.append((nombre, set(casillas)))
            return

    def colocar_barcos(self):
        for nombre, (eslora, cantidad) in self.barcos.items():
            for _ in range(cantidad):
                self.colocar_barco(nombre, eslora)

    def disparar(self, fila, col):
        """Devuelve 'repetido', 'agua', 'tocado' o 'hundido'."""
        if self.disparos[fila][col] != AGUA:
            return "repetido"

        if self.tablero[fila][col] == BARCO:
            self.tablero[fila][col] = IMPACTO
            self.disparos[fila][col] = IMPACTO
            self.vidas -= 1
            for nombre, casillas in self.flota:
                if (fila, col) in casillas:
                    casillas.remove((fila, col))
                    if not casillas:
                        self.ultimo_hundido = nombre
                        return "hundido"
                    break
            return "tocado"

        self.tablero[fila][col] = FALLO
        self.disparos[fila][col] = FALLO
        return "agua"

    def disparo_aleatorio(self, intentos=1):
        libres = []
        for f in range(TAMANO):
            for c in range(TAMANO):
                if self.disparos[f][c] == AGUA:
                    libres.append((f, c))

        candidatas = random.sample(libres, min(intentos, len(libres)))

        elegida = candidatas[0]

        for casilla in candidatas:
            if self.tablero[casilla[0]][casilla[1]] == BARCO:
                elegida = casilla
                break

        fila = elegida[0]
        columna = elegida[1]
        resultado = self.disparar(fila, columna)
        return fila, columna, resultado

    def disparo_inteligente(self):
        fila = -1
        columna = -1

        while len(self.objetivos) > 0 and fila == -1:
            casilla = self.objetivos.pop()
            if self.disparos[casilla[0]][casilla[1]] == AGUA:
                fila = casilla[0]
                columna = casilla[1]

        if fila == -1:
            libres = []
            for f in range(TAMANO):
                for c in range(TAMANO):
                    if self.disparos[f][c] == AGUA:
                        libres.append((f, c))
            casilla = random.choice(libres)
            fila = casilla[0]
            columna = casilla[1]

        resultado = self.disparar(fila, columna)

        if resultado == "tocado":
            for orientacion in ORIENTACIONES:
                cambio = ORIENTACIONES[orientacion]
                nueva_fila = fila + cambio[0]
                nueva_columna = columna + cambio[1]
                if nueva_fila >= 0 and nueva_fila < TAMANO and nueva_columna >= 0 and nueva_columna < TAMANO:
                    self.objetivos.append((nueva_fila, nueva_columna))

   
        if resultado == "hundido":
            self.objetivos = []

        return fila, columna, resultado

    def disparo_maquina(self, dificultad):
        if dificultad == "facil":
            return self.disparo_aleatorio(1)
        elif dificultad == "medio":
            return self.disparo_aleatorio(2)
        else:
            return self.disparo_inteligente()