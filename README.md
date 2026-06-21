# Defensa y Asalto de Base

Proyecto 2 - Introducción a la Programación (Live Learning)
Instituto Tecnológico de Costa Rica
Aarón Umaña, Daniel Solano

## Descripción

Juego de estrategia por turnos para dos jugadores, hecho en Python con Tkinter.
Un jugador asume el rol de **defensor** y construye muros y torres alrededor
de una base ubicada en el centro del tablero. El otro jugador asume el rol
de **atacante** y compra unidades que coloca en los bordes del mapa para
intentar abrirse paso y destruir la base. Gana la partida quien primero
consiga 3 victorias de ronda.

## Requisitos

- Python 
- Tkinter 

No se requieren librerías externas.

## Cómo ejecutar

```
python3 defensa_asalto_base.py
```

Al ejecutarlo se crea (o se reutiliza si ya existe) un archivo
`jugadores.json` en la misma carpeta, donde se guardan los usuarios
registrados y sus victorias.

## Estructura del código

Todo el proyecto está en un único archivo. Está organizado en tres bloques:

**Clases de datos** (`Jugador`, `Torre`, `Unidad`): representan a un jugador
registrado y a cada objeto que puede existir sobre el tablero. `Torre` y
`Unidad` se construyen a partir de los diccionarios `TORRES` y `UNIDADES`,
que funcionan como catálogo central con el costo, vida, daño, alcance (o
velocidad) y turnos necesarios para activar la habilidad especial de cada
tipo.

**Catálogos de datos** (`FACCIONES`, `TORRES`, `UNIDADES`): listas fijas que
definen las 3 facciones visuales (Medieval, Futurista, Naturaleza, cada una
con sus propios colores), los 3 tipos de torre (básica, pesada, mágica) y
los 3 tipos de unidad (soldado, tanque, rápida).

**Clase `Juego`**: contiene toda la lógica y la interfaz. Es la única clase
que controla la ventana, y se apoya en el método `limpiar()` para borrar
los widgets actuales y dibujar la siguiente pantalla cada vez que el juego
cambia de fase (menú → login → selección de facción → construcción →
ataque → combate → fin de ronda). El tablero se dibuja como una cuadrícula
de botones de Tkinter (no un Canvas), y cada botón se actualiza con
`actualizar_tablero()` para reflejar el color y el texto de lo que hay en
esa casilla.

## Flujo del juego

1. **Menú principal**: iniciar partida, ver el top de jugadores, o salir.
2. **Login**: ambos jugadores (defensor y atacante) registran o inician
   sesión en la misma pantalla, cada uno con su propio usuario y contraseña.
3. **Selección de facción**: cada jugador elige una facción distinta entre
   las 3 disponibles, solo afecta los colores del tablero.
4. **Fase de construcción** (defensor): hace clic en el tablero para colocar
   muros o alguna de las 3 torres, siempre que la casilla esté libre y tenga
   dinero suficiente. También puede borrar lo que colocó.
5. **Fase de ataque** (atacante): compra unidades y las coloca únicamente en
   los bordes del tablero (fila o columna 0, o la última fila/columna).
6. **Fase de combate**: se ejecuta turno por turno presionando el botón
   "Ejecutar turno". En cada turno: primero atacan las torres a la unidad
   más cercana dentro de su alcance, luego las unidades atacan (a la base si
   están junto a ella, si no a una torre o muro adyacente) o usan su
   habilidad especial si ya cumplieron sus turnos de espera, y por último
   las unidades que siguen vivas avanzan un paso hacia la base por el camino
   libre más corto.
7. La ronda termina cuando la base llega a 0 de vida (gana el atacante) o
   cuando ya no quedan unidades del atacante en el tablero (gana el
   defensor). La partida completa la gana quien llegue primero a 3 rondas
   ganadas.

## Habilidades especiales

| Tipo | Habilidad |
|---|---|
| Torre básica | Disparo doble (el daño se duplica ese turno) |
| Torre pesada | Daño en área a todas las unidades junto al objetivo |
| Torre mágica | Daña y congela a la unidad un turno |
| Soldado | Ataque doble |
| Tanque | Escudo temporal |
| Unidad rápida | Se cura 25 de vida antes de atacar |

Cada habilidad se activa automáticamente cuando el contador de turnos de esa
torre o unidad alcanza el valor de `turnos_habilidad` definido en su
catálogo; después el contador se reinicia.

## Sistema económico

Cada jugador inicia con `DINERO_INICIAL` (300) y recibe un bono de
`BONO_RONDA` (80) al comenzar cada ronda nueva. El defensor gana dinero por
cada unidad eliminada (la recompensa varía según el tipo de unidad) y el
atacante gana dinero por cada golpe que conecta contra una torre o la base.

## Persistencia de datos

Los usuarios, contraseñas y el conteo de victorias como defensor/atacante de
cada jugador se guardan en `jugadores.json`, en la misma carpeta del script.
El archivo se lee al iniciar el programa y se vuelve a escribir cada vez que
termina una partida.

## Posibles mejoras futuras

- Animar el combate en lugar de avanzar turno por turno con un botón.
- Agregar imágenes o sprites en vez de colores planos.
- Sonido con pygame.
- Guardar también el historial de partidas jugadas, no solo el total de
  victorias.

Complete con los integrantes del grupo.o con pygame, y la
documentacion tecnica / manual de usuario que pide la rubrica.
