import math
import os
import tkinter as tk
from enum import Enum
from tkinter import filedialog, messagebox, ttk


class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class Empleado:

    def __init__(self, nombre: str, apellidos: str, cargo: TipoCargo,
                 genero: TipoGenero, salario_dia: float, dias_trabajados: int,
                 otros_ingresos: float, pagos_salud: float, aporte_pensiones: float):
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__cargo = cargo
        self.__genero = genero
        self.__salario_dia = salario_dia
        self.__dias_trabajados = dias_trabajados
        self.__otros_ingresos = otros_ingresos
        self.__pagos_salud = pagos_salud
        self.__aporte_pensiones = aporte_pensiones

    def get_nombre(self) -> str:
        return self.__nombre

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_cargo(self) -> TipoCargo:
        return self.__cargo

    def get_genero(self) -> TipoGenero:
        return self.__genero

    def get_salario_dia(self) -> float:
        return self.__salario_dia

    def get_dias_trabajados(self) -> int:
        return self.__dias_trabajados

    def get_otros_ingresos(self) -> float:
        return self.__otros_ingresos

    def get_pagos_salud(self) -> float:
        return self.__pagos_salud

    def get_aporte_pensiones(self) -> float:
        return self.__aporte_pensiones

    def calcular_nomina(self) -> float:
        return ((self.__salario_dia * self.__dias_trabajados) + self.__otros_ingresos
                - self.__pagos_salud - self.__aporte_pensiones)


class ListaEmpleados:

    NOMBRE_ARCHIVO = "Nómina.txt"

    def __init__(self):
        self.__lista = []
        self.__total_nomina = 0.0

    def agregar_empleado(self, empleado: Empleado) -> None:
        self.__lista.append(empleado)

    def get_cantidad(self) -> int:
        return len(self.__lista)

    def calcular_total_nomina(self) -> float:
        self.__total_nomina = 0.0
        for empleado in self.__lista:
            self.__total_nomina += empleado.calcular_nomina()
        return self.__total_nomina

    def obtener_matriz(self) -> list:
        datos = []
        for empleado in self.__lista:
            datos.append((empleado.get_nombre(), empleado.get_apellidos(),
                          f"{empleado.calcular_nomina():,.2f}"))
        return datos

    def convertir_texto(self) -> str:
        texto = ""
        for empleado in self.__lista:
            texto += (f"Nombre = {empleado.get_nombre()}\n"
                      f"Apellidos = {empleado.get_apellidos()}\n"
                      f"Cargo = {empleado.get_cargo().value}\n"
                      f"Género = {empleado.get_genero().value}\n"
                      f"Salario por día = ${empleado.get_salario_dia():,.2f}\n"
                      f"Días trabajados = {empleado.get_dias_trabajados()}\n"
                      f"Otros ingresos = ${empleado.get_otros_ingresos():,.2f}\n"
                      f"Pagos por salud = ${empleado.get_pagos_salud():,.2f}\n"
                      f"Aporte pensiones = ${empleado.get_aporte_pensiones():,.2f}\n"
                      f"Salario mensual = ${empleado.calcular_nomina():,.2f}\n"
                      "---------\n")
        texto += f"Total nómina = ${self.calcular_total_nomina():,.2f}\n"
        return texto

    def guardar_archivo(self, carpeta: str) -> str:
        ruta = os.path.join(carpeta, ListaEmpleados.NOMBRE_ARCHIVO)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(self.convertir_texto())
        return ruta


def aplicar_estilo(ventana: tk.Misc) -> None:
    estilo = ttk.Style(ventana)
    if estilo.theme_use() == "default":
        estilo.theme_use("clam")


def ubicar_respecto_a(ventana: tk.Toplevel, padre: tk.Misc) -> None:
    ventana.update_idletasks()
    x = padre.winfo_x() + 40
    y = padre.winfo_y() + 40
    ventana.geometry(f"+{x}+{y}")


class VentanaAgregarEmpleado(tk.Toplevel):

    def __init__(self, padre: tk.Misc, lista: ListaEmpleados):
        super().__init__(padre)
        self.__lista = lista
        self.__campo_nombre = None
        self.__campo_apellidos = None
        self.__campo_cargo = None
        self.__genero = tk.StringVar(self, value=TipoGenero.MASCULINO.value)
        self.__campo_salario_dia = None
        self.__campo_dias = None
        self.__campo_otros_ingresos = None
        self.__campo_pagos_salud = None
        self.__campo_aporte_pensiones = None
        self.__inicio()
        self.title("Agregar empleado")
        self.resizable(False, False)
        ubicar_respecto_a(self, padre)
        self.transient(padre)
        self.grab_set()
        self.__campo_nombre.focus_set()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()
        self.__campo_nombre = self.__crear_campo(contenedor, "Nombre:", 0)
        self.__campo_apellidos = self.__crear_campo(contenedor, "Apellidos:", 1)

        ttk.Label(contenedor, text="Cargo:").grid(row=2, column=0, sticky="w", pady=4)
        self.__campo_cargo = ttk.Combobox(contenedor, state="readonly", width=17,
                                          values=[cargo.value for cargo in TipoCargo])
        self.__campo_cargo.current(0)
        self.__campo_cargo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=4)

        ttk.Label(contenedor, text="Género:").grid(row=3, column=0, sticky="nw", pady=4)
        generos = ttk.Frame(contenedor)
        generos.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=4)
        for genero in TipoGenero:
            ttk.Radiobutton(generos, text=genero.value, value=genero.value,
                            variable=self.__genero).pack(anchor="w")

        self.__campo_salario_dia = self.__crear_campo(contenedor, "Salario por día:", 4)
        ttk.Label(contenedor, text="Días trabajados al mes:").grid(
            row=5, column=0, sticky="w", pady=4)
        self.__campo_dias = ttk.Spinbox(contenedor, from_=1, to=31, width=6)
        self.__campo_dias.set(30)
        self.__campo_dias.grid(row=5, column=1, sticky="w", padx=(10, 0), pady=4)
        self.__campo_otros_ingresos = self.__crear_campo(contenedor, "Otros ingresos:", 6)
        self.__campo_pagos_salud = self.__crear_campo(contenedor, "Pagos por salud:", 7)
        self.__campo_aporte_pensiones = self.__crear_campo(contenedor, "Aporte pensiones:", 8)

        botones = ttk.Frame(contenedor)
        botones.grid(row=9, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(botones, text="Agregar", command=self.__al_agregar).grid(
            row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Borrar", command=self.limpiar_campos).grid(row=0, column=1)

    @staticmethod
    def __crear_campo(padre: ttk.Frame, texto: str, fila: int) -> ttk.Entry:
        ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=4)
        campo = ttk.Entry(padre, width=20)
        campo.grid(row=fila, column=1, sticky="w", padx=(10, 0), pady=4)
        return campo

    @staticmethod
    def leer_texto(nombre: str, texto: str) -> str:
        texto = texto.strip()
        if texto == "":
            raise ValueError(f"Campo nulo: ingrese el valor de «{nombre}».")
        return texto

    @staticmethod
    def leer_numero(nombre: str, texto: str) -> float:
        texto = VentanaAgregarEmpleado.leer_texto(nombre, texto).replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            raise ValueError(f"Error en formato de número en «{nombre}».") from None
        if not math.isfinite(valor) or valor < 0:
            raise ValueError(f"«{nombre}» debe ser un número mayor o igual a cero.")
        return valor

    @staticmethod
    def leer_dias(texto: str) -> int:
        try:
            dias = int(texto.strip())
        except ValueError:
            raise ValueError("Los días trabajados deben ser un número entero.") from None
        if dias < 1 or dias > 31:
            raise ValueError("Los días trabajados deben estar entre 1 y 31.")
        return dias

    def __al_agregar(self) -> None:
        try:
            empleado = Empleado(
                self.leer_texto("Nombre", self.__campo_nombre.get()),
                self.leer_texto("Apellidos", self.__campo_apellidos.get()),
                TipoCargo(self.__campo_cargo.get()),
                TipoGenero(self.__genero.get()),
                self.leer_numero("Salario por día", self.__campo_salario_dia.get()),
                self.leer_dias(self.__campo_dias.get()),
                self.leer_numero("Otros ingresos", self.__campo_otros_ingresos.get()),
                self.leer_numero("Pagos por salud", self.__campo_pagos_salud.get()),
                self.leer_numero("Aporte pensiones", self.__campo_aporte_pensiones.get()))
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self)
            return
        self.__lista.agregar_empleado(empleado)
        messagebox.showinfo("Mensaje", "El empleado ha sido agregado", parent=self)
        self.limpiar_campos()

    def limpiar_campos(self) -> None:
        for campo in (self.__campo_nombre, self.__campo_apellidos, self.__campo_salario_dia,
                      self.__campo_otros_ingresos, self.__campo_pagos_salud,
                      self.__campo_aporte_pensiones):
            campo.delete(0, tk.END)
        self.__campo_cargo.current(0)
        self.__genero.set(TipoGenero.MASCULINO.value)
        self.__campo_dias.set(30)
        self.__campo_nombre.focus_set()


class VentanaNomina(tk.Toplevel):

    def __init__(self, padre: tk.Misc, lista: ListaEmpleados):
        super().__init__(padre)
        self.__lista = lista
        self.__tabla = None
        self.__etiqueta_total = None
        self.__inicio()
        self.title("Nómina de empleados")
        self.resizable(False, False)
        ubicar_respecto_a(self, padre)

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()
        ttk.Label(contenedor, text="Lista de empleados:").grid(
            row=0, column=0, sticky="w", pady=(0, 6))

        columnas = (("nombre", "NOMBRE", 120, "w"),
                    ("apellidos", "APELLIDOS", 140, "w"),
                    ("sueldo", "SUELDO", 130, "e"))
        self.__tabla = ttk.Treeview(contenedor, columns=[c[0] for c in columnas],
                                    show="headings", height=6)
        for clave, titulo, ancho, alineacion in columnas:
            self.__tabla.heading(clave, text=titulo)
            self.__tabla.column(clave, width=ancho, anchor=alineacion)
        for fila in self.__lista.obtener_matriz():
            self.__tabla.insert("", tk.END, values=fila)
        self.__tabla.grid(row=1, column=0)
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=self.__tabla.yview)
        self.__tabla.configure(yscrollcommand=barra.set)
        barra.grid(row=1, column=1, sticky="ns")

        total = self.__lista.calcular_total_nomina()
        self.__etiqueta_total = ttk.Label(
            contenedor, text=f"Total nómina mensual = $ {total:,.2f}")
        self.__etiqueta_total.grid(row=2, column=0, sticky="w", pady=(10, 0))


class VentanaPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.__empleados = ListaEmpleados()
        self.__etiqueta_cantidad = None
        self.__inicio()
        self.title("Nómina")
        self.resizable(False, False)
        self.__centrar_en_pantalla()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Agregar empleado", command=self.__al_agregar)
        menu_opciones.add_command(label="Calcular nómina", command=self.__al_calcular)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Guardar archivo", command=self.__al_guardar)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Nómina de empleados",
                  font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(contenedor, text="Use el menú para agregar empleados,\n"
                                   "calcular la nómina o guardar el archivo.").pack(
            anchor="w", pady=(6, 0))
        self.__etiqueta_cantidad = ttk.Label(contenedor)
        self.__etiqueta_cantidad.pack(anchor="w", pady=(10, 0))
        self.__actualizar_cantidad()

    def __centrar_en_pantalla(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 3
        self.geometry(f"+{x}+{y}")

    def __actualizar_cantidad(self) -> None:
        self.__etiqueta_cantidad.config(
            text=f"Empleados registrados: {self.__empleados.get_cantidad()}")

    def __al_agregar(self) -> None:
        ventana_agregar = VentanaAgregarEmpleado(self, self.__empleados)
        self.wait_window(ventana_agregar)
        self.__actualizar_cantidad()

    def __al_calcular(self) -> None:
        VentanaNomina(self, self.__empleados)

    def __al_guardar(self) -> None:
        if self.__empleados.get_cantidad() == 0:
            messagebox.showwarning("Mensaje", "No hay empleados registrados para guardar.",
                                   parent=self)
            return
        carpeta = filedialog.askdirectory(parent=self, title="Seleccione una carpeta")
        if not carpeta:
            return
        try:
            self.__empleados.guardar_archivo(carpeta)
        except OSError:
            messagebox.showerror("Error", "No se pudo crear el archivo.", parent=self)
            return
        messagebox.showinfo("Mensaje", f"El archivo de la nómina {ListaEmpleados.NOMBRE_ARCHIVO} "
                                       f"se ha creado en {carpeta}", parent=self)


class Principal:

    @staticmethod
    def main() -> None:
        mi_ventana_principal = VentanaPrincipal()
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()
