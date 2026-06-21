# Defensa y Asalto de Base

Juego de estrategia para dos jugadores (modo "hot-seat", en la misma
computadora) hecho en Python con Tkinter.

## Requisitos
- Python 3 (incluye tkinter en la mayoria de instalaciones; en Linux puede
  necesitar instalarse con `sudo apt install python3-tk`).
- No se necesitan librerias externas (no se usa pygame en esta version).

## Como ejecutar
Desde la carpeta del proyecto:

    python3 main.py

## Estructura del proyecto
- `main.py` - punto de entrada del programa.
- `app.py` - clase `Aplicacion` (ventana principal), maneja la navegacion
  entre pantallas y conecta la logica del juego con la interfaz.
- `pantallas.py` - todas las pantallas (Frames de Tkinter): inicio, login,
  seleccion de rol/faccion, construccion, ataque, combate, resultado final
  y top de jugadores.
- `partida.py` - clase `Partida`: estado de una partida (rondas, dinero,
  torres, muros, unidades) y la simulacion de la fase de combate.
- `models.py` - clases `Jugador`, `GestorJugadores` (maneja el archivo
  .json), `Torre`, `Unidad`, `Muro`, y los catalogos de facciones/torres/
  unidades.
- `data/jugadores.json` - archivo donde se guardan los usuarios, sus
  contrasenas y su cantidad de victorias como defensor/atacante.

## Notas
Este es un esqueleto funcional que cumple los requisitos minimos del
enunciado (registro/login, 3 facciones, mapa 10x10, 3 tipos de torre y de
unidad con habilidades, sistema de dinero, rondas al mejor de 5, ranking).
Quedan pendientes (a proposito, para que el grupo los agregue si quiere
subir nota): imagenes/sprites en lugar de colores, sonido con pygame, y la
documentacion tecnica / manual de usuario que pide la rubrica.
