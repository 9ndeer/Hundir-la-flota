from Juego.Tablero import Tablero
from Juego.Funciones import pedir_modo, pedir_nombre, pedir_dificultad, jugar


def main():
    print("\nBIENVENIDO A HUNDIR LA FLOTA")
    print("----------------------------")
    print("Dispara a una coordenada fila,columna. Si aciertas, repites turno.")
    print("Gana quien hunda todos los barcos del rival.")

    modo = pedir_modo()
    if modo == "3":
        print("¡Hasta la próxima!")
        return

    dificultad = "facil"
    if modo == "1":
        j1 = Tablero(pedir_nombre("Tu nombre"))
        j2 = Tablero("Máquina")
        dificultad = pedir_dificultad()
    else:
        j1 = Tablero(pedir_nombre("Nombre del jugador 1"))
        j2 = Tablero(pedir_nombre("Nombre del jugador 2"))

    j1.colocar_barcos()
    j2.colocar_barcos()
    jugar(j1, j2, vs_maquina=(modo == "1"), dificultad=dificultad)


if __name__ == "__main__":
    main()