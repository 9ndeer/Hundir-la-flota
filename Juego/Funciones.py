import os
from Juego.Variables import TAMANO


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_modo():
    while True:
        print("\n1. Un jugador (contra la máquina)")
        print("2. Dos jugadores")
        print("3. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion in ("1", "2", "3"):
            return opcion
        print("Opción no válida.")


def pedir_nombre(texto):
    nombre = input(f"{texto}: ").strip()
    return nombre if nombre else texto


def pedir_coordenada():
    """Devuelve (fila, col), 'salir' o 'trampa'."""
    while True:
        texto = input("Coordenada fila,columna (0-9) | 'trampa' | 'salir': ").strip().lower()
        if texto in ("salir", "trampa"):
            return texto
        try:
            f, c = (int(x) for x in texto.replace(" ", "").split(","))
        except ValueError:
            print("Formato no válido. Ejemplo: 3,5")
            continue
        if 0 <= f < TAMANO and 0 <= c < TAMANO:
            return f, c
        print("Fuera del tablero.")

def pedir_dificultad():
    while True:
        print("\nDificultad:")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            return "facil"
        if opcion == "2":
            return "medio"
        if opcion == "3":
            return "dificil"
        print("Opción no válida.")

def texto_resultado(r, rival):
    if r == "hundido":
        return f"¡HUNDIDO! ({rival.ultimo_hundido})"
    return r.upper()


def jugar(j1, j2, vs_maquina, dificultad="facil"):
    """Si vs_maquina es True, j2 es la máquina."""
    atacante, defensor = j1, j2
    pausa = not vs_maquina  

    while True:
        if vs_maquina and atacante is j2:
            f, c, r = defensor.disparo_maquina(dificultad)
            print(f"La máquina dispara a {f},{c}: {texto_resultado(r, defensor)}")
        else:
            if pausa:
                limpiar()
                input(f"Turno de {atacante.id_jugador}. Pulsa Enter cuando estés listo...")
                pausa = False
            print(f"\n--- Turno de {atacante.id_jugador} ---")
            print("Tu tablero:")
            atacante.mostrar(atacante.tablero)
            print("Tus disparos al rival:")
            atacante.mostrar(defensor.disparos)

            coord = pedir_coordenada()
            if coord == "salir":
                print("Partida abandonada.")
                return
            if coord == "trampa":
                if not vs_maquina:
                    print("La trampa solo está en el modo un jugador.")
                else:
                    print("Tablero de la máquina:")
                    defensor.mostrar(defensor.tablero)
                continue

            r = defensor.disparar(*coord)
            if r == "repetido":
                print("Ya disparaste ahí.")
                continue
            print(texto_resultado(r, defensor))

        if defensor.vidas == 0:
            print(f"\n¡Gana {atacante.id_jugador}!")
            return

        if r == "agua":
            atacante, defensor = defensor, atacante
            pausa = not vs_maquina