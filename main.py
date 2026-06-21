# Defensa y Asalto de Base
# Proyecto 2 - Introducción a la Programación
# Basado en una matriz 10x10 y una interfaz Tkinter.
# Autor: complete con los integrantes del grupo.

import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

ARCHIVO_JUGADORES = "jugadores.json"

FILAS = 10
COLUMNAS = 10
TAM = 55

BASE_FILA = 4
BASE_COLUMNA = 4

DINERO_INICIAL = 300
BONO_RONDA = 80

# ------------------------------------------------------------
# CLASES
# ------------------------------------------------------------

class Jugador:
    def __init__(self, usuario, contrasena, victorias_defensor=0, victorias_atacante=0):
        self.usuario = usuario
        self.contrasena = contrasena
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante

    def convertir_diccionario(self):
        return {
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante
        }


class Torre:
    def __init__(self, tipo, fila, columna):
        datos = TORRES[tipo]
        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.costo = datos["costo"]
        self.vida = datos["vida"]
        self.vida_max = datos["vida"]
        self.dano = datos["dano"]
        self.alcance = datos["alcance"]
        self.turnos_habilidad = datos["turnos_habilidad"]
        self.contador = 0
        self.fila = fila
        self.columna = columna

    def lista_texto(self):
        return f"{self.nombre} | Vida {self.vida} | Daño {self.dano}"


class Unidad:
    def __init__(self, tipo, fila, columna):
        datos = UNIDADES[tipo]
        self.tipo = tipo
        self.nombre = datos["nombre"]
        self.costo = datos["costo"]
        self.vida = datos["vida"]
        self.vida_max = datos["vida"]
        self.dano = datos["dano"]
        self.velocidad = datos["velocidad"]
        self.recompensa = datos["recompensa"]
        self.turnos_habilidad = datos["turnos_habilidad"]
        self.contador = 0
        self.fila = fila
        self.columna = columna
        self.congelada = 0
        self.escudo = 0

    def lista_texto(self):
        return f"{self.nombre} | Vida {self.vida} | Daño {self.dano}"

