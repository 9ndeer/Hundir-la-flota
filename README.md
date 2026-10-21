# Hundir la flota

Se puede jugar contra la máquina (con tres niveles de dificultad) o dos jugadores, y tiene dos versiones: por consola y con ventana gráfica.

## Requisitos

Python 3. La versión gráfica usa `tkinter`, que viene incluido con Python. No hay que instalar nada más.

## Cómo se ejecuta

Desde la carpeta del proyecto:

```
python Main.py        # versión consola
python Interfaz.py    # versión gráfica
```

## Reglas del juego

- Tablero de **10 x 10** para cada jugador.
- Los barcos se colocan **de forma aleatoria** y **nunca pueden quedar pegados** (ni en horizontal, vertical o diagonal):
  - 4 lanchas (1 casilla)
  - 3 cruceros (2 casillas)
  - 2 acorazados (3 casillas)
  - 1 portaaviones (4 casillas)
- Cada turno se dispara a una casilla del tablero rival.
- **Si aciertas, repites turno.** Si fallas, le toca al otro.
- Empieza el jugador 1.
- Gana quien hunda todos los barcos del rival.

## Modos de juego

1. **Un jugador**: contra la máquina, con tres niveles de dificultad:
   - **Fácil**: la máquina dispara a una casilla al azar.
   - **Medio**: la máquina elige dos casillas al azar y dispara a la que tenga barco, si hay alguna.
   - **Difícil**: la máquina dispara al azar, pero cuando acierta prueba las casillas de alrededor hasta hundir el barco.
2. **Dos jugadores**: en el mismo ordenador. Entre turno y turno aparece una pantalla de paso para que el otro jugador no vea tu tablero.

## Cómo jugar en consola

Al arrancar, el menú pide elegir el modo de juego. Si eliges **un jugador**, hay que elegir también la **dificultad**:

| Escribes | Dificultad |
|----------|------------|
| `1` | Fácil |
| `2` | Medio |
| `3` | Difícil |

Las coordenadas se escriben como `fila,columna`, con números del 0 al 9. Por ejemplo: `3,5`.

Otras opciones en tu turno:

| Escribes | Qué hace |
|----------|----------|
| `trampa` | Muestra el tablero de la máquina (solo en un jugador) |
| `salir`  | Abandona la partida |

Símbolos del tablero:

| Símbolo | Significado |
|---------|-------------|
| ` ` (espacio) | Agua sin disparar |
| `O` | Barco |
| `X` | Barco tocado |
| `-` | Disparo al agua |

El juego avisa con **HUNDIDO** cuando se hunde un barco entero.

## Cómo jugar en la versión gráfica

- En el menú eliges el modo de juego (un jugador con su dificultad, o dos jugadores).
- Haz clic en una casilla del **tablero enemigo** (izquierda) para disparar.
- A la derecha está **tu tablero**.
- Colores: azul = agua, gris = barco, rojo = tocado, azul claro = fallo.
- En un jugador hay un botón para ver u ocultar los barcos enemigos (demo).
- El botón **Salir al menú** abandona la partida en cualquier momento. Cuando la partida termina, pasa a llamarse **Volver al menú**.

## Estructura del proyecto

```
.
├── Main.py            # ejecutable: versión consola
├── Interfaz.py        # ejecutable: versión gráfica
├── README.md
├── .gitignore
└── Juego/
    ├── __init__.py
    ├── Variables.py   # constantes (tamaño, barcos, símbolos)
    ├── Tablero.py     # clase Tablero
    └── Funciones.py   # bucle de turnos y entrada de datos (consola)
```

## Cómo funciona por dentro

La clase `Tablero` guarda para cada jugador:

- `tablero`: lista de listas con los barcos, impactos y fallos (lo que ve su dueño).
- `disparos`: lista de listas solo con los disparos recibidos, sin barcos (lo que ve el rival).
- `vidas`: casillas de barco que quedan. Cuando llega a 0, ese jugador pierde.
- `flota`: lista de barcos con las casillas que les quedan sin tocar, para saber cuándo se hunde uno.
- `objetivos`: casillas que la máquina probará después de un impacto (nivel difícil).

Métodos principales:

- `colocar_barcos()`: coloca los barcos al azar, comprobando con `hay_barco_cerca()` que no se salgan del tablero ni queden pegados.
- `disparar(fila, columna)`: devuelve `repetido`, `agua`, `tocado` o `hundido`.
- `disparo_maquina(dificultad)`: elige cómo dispara la máquina según el nivel (`disparo_aleatorio()` en fácil y medio, `disparo_inteligente()` en difícil).
- `mostrar(tablero)`: imprime un tablero por consola.
