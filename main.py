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

# ------------------------------------------------------------
# DATOS DEL JUEGO
# ------------------------------------------------------------

FACCIONES = {
    "Medieval": {
        "base": "#8B4513", "muro": "#A0522D", "torre": "#708090", "unidad": "#DC143C"
    },
    "Futurista": {
        "base": "#00BFFF", "muro": "#1E90FF", "torre": "#9400D3", "unidad": "#FF1493"
    },
    "Naturaleza": {
        "base": "#228B22", "muro": "#8FBC8F", "torre": "#006400", "unidad": "#DAA520"
    }
}

TORRES = {
    "basica": {
        "nombre": "Torre básica",
        "costo": 60,
        "vida": 100,
        "dano": 25,
        "alcance": 3,
        "turnos_habilidad": 3
    },
    "pesada": {
        "nombre": "Torre pesada",
        "costo": 100,
        "vida": 180,
        "dano": 40,
        "alcance": 2,
        "turnos_habilidad": 4
    },
    "magica": {
        "nombre": "Torre mágica",
        "costo": 90,
        "vida": 90,
        "dano": 15,
        "alcance": 4,
        "turnos_habilidad": 3
    }
}

UNIDADES = {
    "soldado": {
        "nombre": "Soldado",
        "costo": 50,
        "vida": 90,
        "dano": 25,
        "velocidad": 1,
        "recompensa": 25,
        "turnos_habilidad": 3
    },
    "tanque": {
        "nombre": "Tanque",
        "costo": 110,
        "vida": 220,
        "dano": 45,
        "velocidad": 1,
        "recompensa": 55,
        "turnos_habilidad": 4
    },
    "rapida": {
        "nombre": "Unidad rápida",
        "costo": 70,
        "vida": 70,
        "dano": 18,
        "velocidad": 2,
        "recompensa": 35,
        "turnos_habilidad": 3
    }
}

