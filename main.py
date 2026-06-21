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


# ------------------------------------------------------------
# APLICACION PRINCIPAL
# ------------------------------------------------------------

class Juego:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Defensa y Asalto de Base")
        self.ventana.geometry("1100x720")
        self.ventana.resizable(False, False)

        self.jugadores = self.cargar_jugadores()
        self.defensor = None
        self.atacante = None

        self.faccion_defensor = None
        self.faccion_atacante = None

        self.ronda = 1
        self.victorias_defensor = 0
        self.victorias_atacante = 0

        self.dinero_defensor = DINERO_INICIAL
        self.dinero_atacante = DINERO_INICIAL

        self.matriz = []
        self.botones = []
        self.torres = []
        self.unidades = []
        self.muros = {}
        self.base_vida = 350
        self.base_vida_max = 350

        self.herramienta_defensor = "muro"
        self.herramienta_atacante = "soldado"
        self.fase = "menu"

        self.menu()

    # --------------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------------

    def limpiar(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def cargar_jugadores(self):
        if not os.path.exists(ARCHIVO_JUGADORES):
            return {}

        try:
            with open(ARCHIVO_JUGADORES, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except:
            return {}

        jugadores = {}
        for usuario in datos:
            info = datos[usuario]
            jugadores[usuario] = Jugador(
                info["usuario"],
                info["contrasena"],
                info.get("victorias_defensor", 0),
                info.get("victorias_atacante", 0)
            )
        return jugadores

    def guardar_jugadores(self):
        datos = {}
        for usuario in self.jugadores:
            datos[usuario] = self.jugadores[usuario].convertir_diccionario()

        with open(ARCHIVO_JUGADORES, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def crear_matriz(self):
        self.matriz = []
        self.torres = []
        self.unidades = []
        self.muros = {}
        self.base_vida = self.base_vida_max

        for f in range(FILAS):
            fila = []
            for c in range(COLUMNAS):
                fila.append("libre")
            self.matriz.append(fila)

        self.matriz[BASE_FILA][BASE_COLUMNA] = "base"

    def distancia(self, f1, c1, f2, c2):
        return abs(f1 - f2) + abs(c1 - c2)

    def objeto_torre(self, fila, columna):
        for torre in self.torres:
            if torre.fila == fila and torre.columna == columna:
                return torre
        return None

    def objeto_unidad(self, fila, columna):
        for unidad in self.unidades:
            if unidad.fila == fila and unidad.columna == columna:
                return unidad
        return None

    # --------------------------------------------------------
    # MENU, LOGIN Y TOP
    # --------------------------------------------------------

    def menu(self):
        self.limpiar()
        self.fase = "menu"

        tk.Label(
            self.ventana,
            text="DEFENSA Y ASALTO DE BASE",
            font=("Arial", 32, "bold")
        ).pack(pady=40)

        tk.Button(
            self.ventana,
            text="Iniciar partida",
            font=("Arial", 18),
            width=25,
            command=self.pantalla_login
        ).pack(pady=15)

        tk.Button(
            self.ventana,
            text="Top de jugadores",
            font=("Arial", 18),
            width=25,
            command=self.mostrar_top
        ).pack(pady=15)

        tk.Button(
            self.ventana,
            text="Salir",
            font=("Arial", 18),
            width=25,
            command=self.ventana.destroy
        ).pack(pady=15)

    def pantalla_login(self):
        self.limpiar()

        tk.Label(
            self.ventana,
            text="Registro / inicio de sesión",
            font=("Arial", 26, "bold")
        ).pack(pady=20)

        marco = tk.Frame(self.ventana)
        marco.pack(pady=10)

        tk.Label(marco, text="Defensor", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(marco, text="Usuario:").grid(row=1, column=0)
        tk.Label(marco, text="Contraseña:").grid(row=2, column=0)

        self.entry_def_user = tk.Entry(marco)
        self.entry_def_pass = tk.Entry(marco, show="*")
        self.entry_def_user.grid(row=1, column=1, padx=10)
        self.entry_def_pass.grid(row=2, column=1, padx=10)

        tk.Label(marco, text="Atacante", font=("Arial", 18, "bold")).grid(row=0, column=3, columnspan=2, pady=10)
        tk.Label(marco, text="Usuario:").grid(row=1, column=3)
        tk.Label(marco, text="Contraseña:").grid(row=2, column=3)

        self.entry_atq_user = tk.Entry(marco)
        self.entry_atq_pass = tk.Entry(marco, show="*")
        self.entry_atq_user.grid(row=1, column=4, padx=10)
        self.entry_atq_pass.grid(row=2, column=4, padx=10)

        tk.Button(
            self.ventana,
            text="Registrar jugadores nuevos",
            font=("Arial", 15),
            command=self.registrar_jugadores
        ).pack(pady=10)

        tk.Button(
            self.ventana,
            text="Iniciar sesión",
            font=("Arial", 15),
            command=self.iniciar_sesion
        ).pack(pady=10)

        tk.Button(
            self.ventana,
            text="Volver",
            font=("Arial", 15),
            command=self.menu
        ).pack(pady=10)

    def registrar_jugadores(self):
        datos = [
            (self.entry_def_user.get().strip(), self.entry_def_pass.get().strip()),
            (self.entry_atq_user.get().strip(), self.entry_atq_pass.get().strip())
        ]

        if datos[0][0] == "" or datos[0][1] == "" or datos[1][0] == "" or datos[1][1] == "":
            messagebox.showerror("Error", "Debe llenar todos los espacios.")
            return

        if datos[0][0] == datos[1][0]:
            messagebox.showerror("Error", "Los dos jugadores no pueden ser el mismo usuario.")
            return

        for usuario, contrasena in datos:
            if usuario in self.jugadores:
                messagebox.showerror("Error", f"El usuario {usuario} ya existe.")
                return

        for usuario, contrasena in datos:
            self.jugadores[usuario] = Jugador(usuario, contrasena)

        self.guardar_jugadores()
        messagebox.showinfo("Listo", "Jugadores registrados. Ahora presione iniciar sesión.")

    def iniciar_sesion(self):
        du = self.entry_def_user.get().strip()
        dp = self.entry_def_pass.get().strip()
        au = self.entry_atq_user.get().strip()
        ap = self.entry_atq_pass.get().strip()

        if du == au:
            messagebox.showerror("Error", "Los jugadores deben ser diferentes.")
            return

        if du not in self.jugadores or au not in self.jugadores:
            messagebox.showerror("Error", "Uno de los usuarios no existe.")
            return

        if self.jugadores[du].contrasena != dp or self.jugadores[au].contrasena != ap:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return

        self.defensor = self.jugadores[du]
        self.atacante = self.jugadores[au]
        self.pantalla_facciones()

    def mostrar_top(self):
        self.limpiar()

        tk.Label(self.ventana, text="TOP DE JUGADORES", font=("Arial", 28, "bold")).pack(pady=20)

        marco = tk.Frame(self.ventana)
        marco.pack(pady=20)

        defensores = list(self.jugadores.values())
        defensores.sort(key=lambda j: j.victorias_defensor, reverse=True)

        atacantes = list(self.jugadores.values())
        atacantes.sort(key=lambda j: j.victorias_atacante, reverse=True)

        tk.Label(marco, text="Top defensor", font=("Arial", 18, "bold")).grid(row=0, column=0, padx=80)
        tk.Label(marco, text="Top atacante", font=("Arial", 18, "bold")).grid(row=0, column=1, padx=80)

        for i in range(5):
            if i < len(defensores):
                texto_def = f"{i + 1}. {defensores[i].usuario}: {defensores[i].victorias_defensor}"
            else:
                texto_def = f"{i + 1}. ---"

            if i < len(atacantes):
                texto_atq = f"{i + 1}. {atacantes[i].usuario}: {atacantes[i].victorias_atacante}"
            else:
                texto_atq = f"{i + 1}. ---"

            tk.Label(marco, text=texto_def, font=("Arial", 14)).grid(row=i + 1, column=0, pady=8)
            tk.Label(marco, text=texto_atq, font=("Arial", 14)).grid(row=i + 1, column=1, pady=8)

        tk.Button(self.ventana, text="Volver", font=("Arial", 16), command=self.menu).pack(pady=20)


    # --------------------------------------------------------
    # FACCIONES
    # --------------------------------------------------------

    def pantalla_facciones(self):
        self.limpiar()

        tk.Label(self.ventana, text="Selección de facciones", font=("Arial", 28, "bold")).pack(pady=20)

        self.var_faccion_def = tk.StringVar(value="Medieval")
        self.var_faccion_atq = tk.StringVar(value="Futurista")

        marco = tk.Frame(self.ventana)
        marco.pack(pady=20)

        tk.Label(marco, text=f"Defensor: {self.defensor.usuario}", font=("Arial", 17, "bold")).grid(row=0, column=0, padx=80)
        tk.Label(marco, text=f"Atacante: {self.atacante.usuario}", font=("Arial", 17, "bold")).grid(row=0, column=1, padx=80)

        for faccion in FACCIONES:
            tk.Radiobutton(
                marco,
                text=faccion,
                variable=self.var_faccion_def,
                value=faccion,
                font=("Arial", 14)
            ).grid(sticky="w", row=list(FACCIONES.keys()).index(faccion) + 1, column=0)

            tk.Radiobutton(
                marco,
                text=faccion,
                variable=self.var_faccion_atq,
                value=faccion,
                font=("Arial", 14)
            ).grid(sticky="w", row=list(FACCIONES.keys()).index(faccion) + 1, column=1)

        tk.Button(
            self.ventana,
            text="Empezar partida",
            font=("Arial", 16),
            command=self.iniciar_partida
        ).pack(pady=25)

    def iniciar_partida(self):
        if self.var_faccion_def.get() == self.var_faccion_atq.get():
            messagebox.showerror("Error", "El atacante y el defensor no pueden usar la misma facción.")
            return

        self.faccion_defensor = self.var_faccion_def.get()
        self.faccion_atacante = self.var_faccion_atq.get()

        self.ronda = 1
        self.victorias_defensor = 0
        self.victorias_atacante = 0

        self.dinero_defensor = DINERO_INICIAL
        self.dinero_atacante = DINERO_INICIAL

        self.nueva_ronda()

# --------------------------------------------------------
    # RONDAS
    # --------------------------------------------------------

    def nueva_ronda(self):
        self.crear_matriz()

        self.dinero_defensor += BONO_RONDA
        self.dinero_atacante += BONO_RONDA

        self.fase_construccion()

    def fase_construccion(self):
        self.limpiar()
        self.fase = "defensor"
        self.crear_interfaz_juego("Fase de construcción del defensor")

        marco = tk.Frame(self.ventana)
        marco.place(x=700, y=120)

        tk.Label(marco, text="Herramientas del defensor", font=("Arial", 16, "bold")).pack(pady=5)

        opciones = [
            ("Muro ($30)", "muro"),
            ("Torre básica ($60)", "basica"),
            ("Torre pesada ($100)", "pesada"),
            ("Torre mágica ($90)", "magica"),
            ("Borrar", "borrar")
        ]

        for texto, valor in opciones:
            tk.Button(
                marco,
                text=texto,
                width=22,
                command=lambda v=valor: self.seleccionar_defensor(v)
            ).pack(pady=4)

        tk.Button(
            marco,
            text="Terminar construcción",
            font=("Arial", 13, "bold"),
            command=self.fase_ataque
        ).pack(pady=20)

        self.actualizar_tablero()

    def fase_ataque(self):
        self.fase = "atacante"
        self.limpiar()
        self.crear_interfaz_juego("Fase de compra y colocación del atacante")

        marco = tk.Frame(self.ventana)
        marco.place(x=700, y=120)

        tk.Label(marco, text="Unidades del atacante", font=("Arial", 16, "bold")).pack(pady=5)

        opciones = [
            ("Soldado ($50)", "soldado"),
            ("Tanque ($110)", "tanque"),
            ("Unidad rápida ($70)", "rapida"),
            ("Borrar unidad", "borrar_unidad")
        ]

        for texto, valor in opciones:
            tk.Button(
                marco,
                text=texto,
                width=22,
                command=lambda v=valor: self.seleccionar_atacante(v)
            ).pack(pady=4)

        tk.Label(
            marco,
            text="Coloque unidades en los bordes del mapa.",
            wraplength=260
        ).pack(pady=10)

        tk.Button(
            marco,
            text="Iniciar combate",
            font=("Arial", 13, "bold"),
            command=self.iniciar_combate
        ).pack(pady=20)

        self.actualizar_tablero()

    def crear_interfaz_juego(self, titulo):
        tk.Label(self.ventana, text=titulo, font=("Arial", 21, "bold")).place(x=30, y=10)

        self.label_info = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 13),
            justify="left"
        )
        self.label_info.place(x=700, y=20)

        self.marco_tablero = tk.Frame(self.ventana)
        self.marco_tablero.place(x=30, y=70)

        self.botones = []

        for f in range(FILAS):
            fila_botones = []
            for c in range(COLUMNAS):
                b = tk.Button(
                    self.marco_tablero,
                    width=6,
                    height=3,
                    command=lambda fi=f, co=c: self.click_casilla(fi, co)
                )
                b.grid(row=f, column=c)
                fila_botones.append(b)
            self.botones.append(fila_botones)

        tk.Button(
            self.ventana,
            text="Menú",
            command=self.menu
        ).place(x=1000, y=660)

        self.actualizar_info()

    def actualizar_info(self):
        texto = (
            f"Ronda: {self.ronda}\n"
            f"Defensor: {self.defensor.usuario} | Victorias: {self.victorias_defensor} | Dinero: ${self.dinero_defensor}\n"
            f"Atacante: {self.atacante.usuario} | Victorias: {self.victorias_atacante} | Dinero: ${self.dinero_atacante}\n"
            f"Vida base: {self.base_vida}/{self.base_vida_max}"
        )
        self.label_info.config(text=texto)

    def seleccionar_defensor(self, herramienta):
        self.herramienta_defensor = herramienta

    def seleccionar_atacante(self, herramienta):
        self.herramienta_atacante = herramienta

    def click_casilla(self, fila, columna):
        if self.fase == "defensor":
            self.click_defensor(fila, columna)
        elif self.fase == "atacante":
            self.click_atacante(fila, columna)

    def click_defensor(self, fila, columna):
        if self.herramienta_defensor == "borrar":
            if self.matriz[fila][columna] == "muro":
                self.matriz[fila][columna] = "libre"
                self.muros.pop((fila, columna), None)
            elif self.matriz[fila][columna] == "torre":
                torre = self.objeto_torre(fila, columna)
                if torre:
                    self.torres.remove(torre)
                self.matriz[fila][columna] = "libre"
            self.actualizar_tablero()
            return

        if self.matriz[fila][columna] != "libre":
            messagebox.showerror("Error", "Esa casilla no está libre.")
            return

        if self.herramienta_defensor == "muro":
            costo = 30
            if self.dinero_defensor < costo:
                messagebox.showerror("Error", "No tiene suficiente dinero.")
                return
            self.dinero_defensor -= costo
            self.matriz[fila][columna] = "muro"
            self.muros[(fila, columna)] = 80

        else:
            tipo = self.herramienta_defensor
            costo = TORRES[tipo]["costo"]
            if self.dinero_defensor < costo:
                messagebox.showerror("Error", "No tiene suficiente dinero.")
                return
            self.dinero_defensor -= costo
            self.matriz[fila][columna] = "torre"
            self.torres.append(Torre(tipo, fila, columna))

        self.actualizar_tablero()

    def click_atacante(self, fila, columna):
        if self.herramienta_atacante == "borrar_unidad":
            if self.matriz[fila][columna] == "unidad":
                unidad = self.objeto_unidad(fila, columna)
                if unidad:
                    self.unidades.remove(unidad)
                self.matriz[fila][columna] = "libre"
            self.actualizar_tablero()
            return

        if fila not in [0, FILAS - 1] and columna not in [0, COLUMNAS - 1]:
            messagebox.showerror("Error", "Las unidades solo se colocan en los bordes.")
            return

        if self.matriz[fila][columna] != "libre":
            messagebox.showerror("Error", "Esa casilla no está libre.")
            return

        tipo = self.herramienta_atacante
        costo = UNIDADES[tipo]["costo"]

        if self.dinero_atacante < costo:
            messagebox.showerror("Error", "No tiene suficiente dinero.")
            return

        self.dinero_atacante -= costo
        self.matriz[fila][columna] = "unidad"
        self.unidades.append(Unidad(tipo, fila, columna))
        self.actualizar_tablero()

    def actualizar_tablero(self):
        color_def = FACCIONES[self.faccion_defensor]
        color_atq = FACCIONES[self.faccion_atacante]

        for f in range(FILAS):
            for c in range(COLUMNAS):
                valor = self.matriz[f][c]
                texto = ""
                color = "white"

                if valor == "libre":
                    texto = ""
                    color = "#EEEEEE"
                elif valor == "base":
                    texto = "BASE\n" + str(self.base_vida)
                    color = color_def["base"]
                elif valor == "muro":
                    texto = "MURO\n" + str(self.muros.get((f, c), 0))
                    color = color_def["muro"]
                elif valor == "torre":
                    torre = self.objeto_torre(f, c)
                    if torre:
                        texto = torre.nombre.replace("Torre ", "T.") + "\n" + str(torre.vida)
                    color = color_def["torre"]
                elif valor == "unidad":
                    unidad = self.objeto_unidad(f, c)
                    if unidad:
                        texto = unidad.nombre + "\n" + str(unidad.vida)
                    color = color_atq["unidad"]

                self.botones[f][c].config(text=texto, bg=color)

        self.actualizar_info()
