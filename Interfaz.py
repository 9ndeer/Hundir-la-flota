import tkinter as tk
from Juego.Tablero import Tablero
from Juego.Variables import TAMANO, AGUA, BARCO, IMPACTO, FALLO

COLORES = {AGUA: "#4da6ff", BARCO: "#555555", IMPACTO: "#e63946", FALLO: "#d0e8ff"}


class App:
    def __init__(self, root):
        self.root = root
        root.title("Hundir la flota")
        root.geometry("800x560")
        root.resizable(False, False)
        self.marco = None
        self.en_partida = False
        self.menu()

    def nueva_pantalla(self):
        if self.marco:
            self.marco.destroy()
        self.marco = tk.Frame(self.root, padx=15, pady=15)
        self.marco.place(relx=0.5, rely=0.5, anchor="center")

    def menu(self):
        self.nueva_pantalla()
        self.en_partida = False
        tk.Label(self.marco, text="HUNDIR LA FLOTA", font=("Arial", 20)).pack(pady=15)
        tk.Button(self.marco, text="Un jugador - Fácil", width=25,
                  command=lambda: self.empezar(False, "facil")).pack(pady=3)
        tk.Button(self.marco, text="Un jugador - Medio", width=25,
                  command=lambda: self.empezar(False, "medio")).pack(pady=3)
        tk.Button(self.marco, text="Un jugador - Difícil", width=25,
                  command=lambda: self.empezar(False, "dificil")).pack(pady=3)
        tk.Button(self.marco, text="Dos jugadores", width=25,
                  command=lambda: self.empezar(True)).pack(pady=(12, 3))
        tk.Button(self.marco, text="Salir", width=25, command=self.root.destroy).pack(pady=3)

    def empezar(self, dos, dificultad="facil"):
        self.dos = dos
        self.dificultad = dificultad
        self.en_partida = True
        self.jugadores = [Tablero("Jugador 1"), Tablero("Jugador 2" if dos else "Máquina")]
        for j in self.jugadores:
            j.colocar_barcos()
        self.actual = 0
        self.trampa = False
        if dos:
            self.pantalla_paso()
        else:
            self.pantalla_juego()

    def pantalla_paso(self):
        if not self.en_partida:
            return
        self.nueva_pantalla()
        nombre = self.jugadores[self.actual].id_jugador
        tk.Label(self.marco, text=f"Turno de {nombre}\n(que el otro no mire)",
                 font=("Arial", 16)).pack(pady=20)
        tk.Button(self.marco, text="Listo", width=15, command=self.pantalla_juego).pack()
        tk.Button(self.marco, text="Salir al menú", width=15, command=self.menu).pack(pady=10)

    def pantalla_juego(self):
        self.nueva_pantalla()
        self.yo = self.jugadores[self.actual]
        self.rival = self.jugadores[1 - self.actual]
        self.bloqueado = False

        self.mensaje = tk.Label(self.marco, text=f"Turno de {self.yo.id_jugador}", font=("Arial", 14))
        self.mensaje.grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(self.marco, text="Tablero enemigo").grid(row=1, column=0)
        tk.Label(self.marco, text="Tu tablero").grid(row=1, column=1)
        self.cuadrado_rival = self.crear_cuadrado(0, clicable=True)
        self.cuadrado_propia = self.crear_cuadrado(1, clicable=False)

        if not self.dos:
            tk.Button(self.marco, text="Ver/ocultar barcos enemigos",
                      command=self.alternar_trampa).grid(row=3, column=0, columnspan=2)

        # botón de salir (al acabar la partida cambia a "Volver al menú")
        self.boton_salir = tk.Button(self.marco, text="Salir al menú", command=self.menu)
        self.boton_salir.grid(row=4, column=0, columnspan=2, pady=5)

        self.pintar()

    def alternar_trampa(self):
        self.trampa = not self.trampa
        self.pintar()

    def crear_cuadrado(self, columna, clicable):
        cuadro = tk.Frame(self.marco, padx=10, pady=10)
        cuadro.grid(row=2, column=columna)
        cuadrado = []
        for f in range(TAMANO):
            fila = []
            for c in range(TAMANO):
                casilla = tk.Label(cuadro, width=3, height=1, relief="raised", bd=2)
                casilla.grid(row=f, column=c)
                if clicable:
                    casilla.bind("<Button-1>", lambda e, f=f, c=c: self.clic(f, c))
                fila.append(casilla)
            cuadrado.append(fila)
        return cuadrado

    def pintar(self):
        origen = self.rival.tablero if self.trampa else self.rival.disparos
        for f in range(TAMANO):
            for c in range(TAMANO):
                self.cuadrado_rival[f][c].config(bg=COLORES[origen[f][c]])
                self.cuadrado_propia[f][c].config(bg=COLORES[self.yo.tablero[f][c]])

    def clic(self, f, c):
        if self.bloqueado:
            return
        r = self.rival.disparar(f, c)
        if r == "repetido":
            return
        self.pintar()

        if self.rival.vidas == 0:
            self.fin(f"¡Gana {self.yo.id_jugador}!")
        elif r == "hundido":
            self.mensaje.config(text=f"¡HUNDIDO! ({self.rival.ultimo_hundido}) Dispara otra vez")
        elif r == "tocado":
            self.mensaje.config(text="¡Tocado! Dispara otra vez")
        else:
            self.bloqueado = True
            self.mensaje.config(text="Agua...")
            if self.dos:
                self.actual = 1 - self.actual
                self.root.after(900, self.pantalla_paso)
            else:
                self.root.after(700, self.turno_maquina)

    def turno_maquina(self):
        if not self.en_partida:
            return
        humano = self.jugadores[0]
        f, c, r = humano.disparo_maquina(self.dificultad)
        self.pintar()

        if humano.vidas == 0:
            self.fin("Ha ganado la máquina")
        elif r == "hundido":
            self.mensaje.config(text=f"La máquina ha hundido tu {humano.ultimo_hundido}")
            self.root.after(900, self.turno_maquina)
        elif r == "tocado":
            self.mensaje.config(text="La máquina te ha tocado...")
            self.root.after(700, self.turno_maquina)
        else:
            self.bloqueado = False
            self.mensaje.config(text="Tu turno")

    def fin(self, texto):
        self.bloqueado = True
        self.mensaje.config(text=texto)
        self.boton_salir.config(text="Volver al menú")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()