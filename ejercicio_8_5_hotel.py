import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, simpledialog, ttk


class Huesped:

    def __init__(self, nombres: str, apellidos: str, documento_identidad: int):
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__documento_identidad = documento_identidad
        self.__fecha_ingreso = None
        self.__fecha_salida = None

    def get_nombres(self) -> str:
        return self.__nombres

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_documento_identidad(self) -> int:
        return self.__documento_identidad

    def get_fecha_ingreso(self) -> date:
        return self.__fecha_ingreso

    def get_fecha_salida(self) -> date:
        return self.__fecha_salida

    def set_fecha_ingreso(self, fecha: date) -> None:
        self.__fecha_ingreso = fecha

    def set_fecha_salida(self, fecha: date) -> None:
        self.__fecha_salida = fecha

    def obtener_dias_alojamiento(self) -> int:
        return (self.__fecha_salida - self.__fecha_ingreso).days


class Habitacion:

    def __init__(self, numero_habitacion: int, disponible: bool, precio_dia: float):
        self.__numero_habitacion = numero_habitacion
        self.__disponible = disponible
        self.__precio_dia = precio_dia
        self.__huesped = None

    def get_numero_habitacion(self) -> int:
        return self.__numero_habitacion

    def get_disponible(self) -> bool:
        return self.__disponible

    def get_precio_dia(self) -> float:
        return self.__precio_dia

    def get_huesped(self) -> Huesped:
        return self.__huesped

    def set_huesped(self, huesped: Huesped) -> None:
        self.__huesped = huesped

    def set_disponible(self, disponible: bool) -> None:
        self.__disponible = disponible


class Hotel:

    CANTIDAD_HABITACIONES = 10
    PRECIO_HABITACIONES_1_A_5 = 120000
    PRECIO_HABITACIONES_6_A_10 = 160000
    FORMATO_FECHA = "%Y-%m-%d"

    def __init__(self):
        self.__lista_habitaciones = []
        for numero in range(1, Hotel.CANTIDAD_HABITACIONES + 1):
            if numero <= 5:
                precio = Hotel.PRECIO_HABITACIONES_1_A_5
            else:
                precio = Hotel.PRECIO_HABITACIONES_6_A_10
            self.__lista_habitaciones.append(Habitacion(numero, True, precio))

    def get_lista_habitaciones(self) -> list:
        return list(self.__lista_habitaciones)

    def buscar_habitacion(self, numero: int) -> Habitacion:
        for habitacion in self.__lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero:
                return habitacion
        return None

    def buscar_fecha_ingreso_habitacion(self, numero: int) -> str:
        habitacion = self.buscar_habitacion(numero)
        if habitacion is None or habitacion.get_huesped() is None:
            return ""
        return habitacion.get_huesped().get_fecha_ingreso().strftime(Hotel.FORMATO_FECHA)

    def buscar_habitacion_ocupada(self, numero: int) -> bool:
        habitacion = self.buscar_habitacion(numero)
        return habitacion is not None and not habitacion.get_disponible()

    def registrar_ingreso(self, numero: int, huesped: Huesped, fecha_ingreso: date) -> None:
        habitacion = self.buscar_habitacion(numero)
        if habitacion is None or not habitacion.get_disponible():
            raise ValueError("La habitación está ocupada.")
        huesped.set_fecha_ingreso(fecha_ingreso)
        habitacion.set_huesped(huesped)
        habitacion.set_disponible(False)

    def registrar_salida(self, numero: int) -> None:
        habitacion = self.buscar_habitacion(numero)
        habitacion.set_huesped(None)
        habitacion.set_disponible(True)

    @staticmethod
    def convertir_fecha(texto: str) -> date:
        return datetime.strptime(texto.strip(), Hotel.FORMATO_FECHA).date()


def aplicar_estilo(ventana: tk.Misc) -> None:
    estilo = ttk.Style(ventana)
    if estilo.theme_use() == "default":
        estilo.theme_use("clam")


def ubicar_respecto_a(ventana: tk.Toplevel, padre: tk.Misc) -> None:
    ventana.update_idletasks()
    x = padre.winfo_x() + 40
    y = padre.winfo_y() + 40
    ventana.geometry(f"+{x}+{y}")


class VentanaHabitaciones(tk.Toplevel):

    COLOR_DISPONIBLE = "dark green"
    COLOR_NO_DISPONIBLE = "firebrick"

    def __init__(self, padre: tk.Misc, hotel: Hotel):
        super().__init__(padre)
        self.__hotel = hotel
        self.__campo_habitacion = None
        self.__inicio()
        self.title("Habitaciones")
        self.resizable(False, False)
        ubicar_respecto_a(self, padre)

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()
        for indice, habitacion in enumerate(self.__hotel.get_lista_habitaciones()):
            fila, columna = divmod(indice, 5)
            marco = ttk.LabelFrame(contenedor, padding=8,
                                   text=f"Habitación {habitacion.get_numero_habitacion()}")
            marco.grid(row=fila, column=columna, padx=4, pady=4, sticky="nsew")
            precio = f"$ {habitacion.get_precio_dia():,.0f} por día"
            ttk.Label(marco, text=precio).pack(anchor="w")
            if habitacion.get_disponible():
                estado, color = "Disponible", VentanaHabitaciones.COLOR_DISPONIBLE
            else:
                estado, color = "No disponible", VentanaHabitaciones.COLOR_NO_DISPONIBLE
            ttk.Label(marco, text=estado, foreground=color).pack(anchor="w", pady=(4, 0))

        seleccion = ttk.Frame(contenedor)
        seleccion.grid(row=2, column=0, columnspan=5, pady=(12, 0))
        ttk.Label(seleccion, text="Habitación a reservar:").grid(row=0, column=0)
        self.__campo_habitacion = ttk.Spinbox(seleccion, from_=1,
                                              to=Hotel.CANTIDAD_HABITACIONES, width=5)
        self.__campo_habitacion.set(1)
        self.__campo_habitacion.configure(state="readonly")
        self.__campo_habitacion.grid(row=0, column=1, padx=8)
        ttk.Button(seleccion, text="Aceptar", command=self.__al_aceptar).grid(row=0, column=2)

    def __al_aceptar(self) -> None:
        numero = int(self.__campo_habitacion.get())
        if self.__hotel.buscar_habitacion_ocupada(numero):
            messagebox.showwarning("Mensaje", "La habitación está ocupada.", parent=self)
            return
        padre = self.master
        self.destroy()
        VentanaIngreso(padre, self.__hotel, numero)


class VentanaIngreso(tk.Toplevel):

    def __init__(self, padre: tk.Misc, hotel: Hotel, numero_habitacion_reservada: int):
        super().__init__(padre)
        self.__hotel = hotel
        self.__numero_habitacion_reservada = numero_habitacion_reservada
        self.__campo_fecha_ingreso = None
        self.__campo_nombre = None
        self.__campo_apellidos = None
        self.__campo_documento_identidad = None
        self.__inicio()
        self.title("Ingreso")
        self.resizable(False, False)
        ubicar_respecto_a(self, padre)
        self.__campo_fecha_ingreso.focus_set()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()
        ttk.Label(contenedor, text=f"Habitación: {self.__numero_habitacion_reservada}",
                  font=("TkDefaultFont", 10, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        self.__campo_fecha_ingreso = self.__crear_campo(contenedor, "Fecha (aaaa-mm-dd):", 1)
        ttk.Label(contenedor, text="Huésped", font=("TkDefaultFont", 10, "bold")).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(10, 2))
        self.__campo_nombre = self.__crear_campo(contenedor, "Nombre:", 3)
        self.__campo_apellidos = self.__crear_campo(contenedor, "Apellidos:", 4)
        self.__campo_documento_identidad = self.__crear_campo(contenedor, "Doc. identidad:", 5)

        botones = ttk.Frame(contenedor)
        botones.grid(row=6, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(botones, text="Aceptar", command=self.__al_aceptar).grid(
            row=0, column=0, padx=(0, 8))
        ttk.Button(botones, text="Cancelar", command=self.destroy).grid(row=0, column=1)

    @staticmethod
    def __crear_campo(padre: ttk.Frame, texto: str, fila: int) -> ttk.Entry:
        ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=3)
        campo = ttk.Entry(padre, width=22)
        campo.grid(row=fila, column=1, sticky="ew", padx=(10, 0), pady=3)
        return campo

    def __al_aceptar(self) -> None:
        textos = [campo.get().strip() for campo in (
            self.__campo_fecha_ingreso, self.__campo_nombre,
            self.__campo_apellidos, self.__campo_documento_identidad)]
        if "" in textos:
            messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=self)
            return
        fecha_texto, nombre, apellidos, documento_texto = textos
        try:
            fecha_ingreso = Hotel.convertir_fecha(fecha_texto)
        except ValueError:
            messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado "
                                            "(aaaa-mm-dd).", parent=self)
            return
        if not documento_texto.isdigit():
            messagebox.showerror("Error", "El documento de identidad debe ser numérico.",
                                 parent=self)
            return
        huesped = Huesped(nombre, apellidos, int(documento_texto))
        try:
            self.__hotel.registrar_ingreso(self.__numero_habitacion_reservada,
                                           huesped, fecha_ingreso)
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self)
            return
        messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
        self.destroy()


class VentanaSalida(tk.Toplevel):

    def __init__(self, padre: tk.Misc, hotel: Hotel, numero: int):
        super().__init__(padre)
        self.__hotel = hotel
        self.__numero_habitacion = numero
        self.__habitacion_ocupada = hotel.buscar_habitacion(numero)
        self.__campo_fecha_salida = None
        self.__etiqueta_cantidad_dias = None
        self.__etiqueta_total_pago = None
        self.__boton_registrar_salida = None
        self.__inicio()
        self.title("Salida huéspedes")
        self.resizable(False, False)
        ubicar_respecto_a(self, padre)
        self.__campo_fecha_salida.focus_set()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()
        huesped = self.__habitacion_ocupada.get_huesped()
        ttk.Label(contenedor, text=f"Habitación: {self.__numero_habitacion}",
                  font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(contenedor, text=f"Huésped: {huesped.get_nombres()} "
                                   f"{huesped.get_apellidos()}").grid(
            row=1, column=0, sticky="w", pady=(4, 0))
        fecha_ingreso = self.__hotel.buscar_fecha_ingreso_habitacion(self.__numero_habitacion)
        ttk.Label(contenedor, text=f"Fecha de ingreso: {fecha_ingreso}").grid(
            row=2, column=0, sticky="w", pady=(4, 0))
        ttk.Label(contenedor, text="Fecha de salida (aaaa-mm-dd):").grid(
            row=3, column=0, sticky="w", pady=(10, 2))
        self.__campo_fecha_salida = ttk.Entry(contenedor, width=28)
        self.__campo_fecha_salida.grid(row=4, column=0, sticky="ew")
        self.__campo_fecha_salida.bind("<KeyRelease>", lambda evento: self.__borrar_calculo())
        ttk.Button(contenedor, text="Calcular", command=self.__al_calcular).grid(
            row=5, column=0, sticky="ew", pady=(8, 8))
        self.__etiqueta_cantidad_dias = ttk.Label(contenedor)
        self.__etiqueta_cantidad_dias.grid(row=6, column=0, sticky="w")
        self.__etiqueta_total_pago = ttk.Label(contenedor)
        self.__etiqueta_total_pago.grid(row=7, column=0, sticky="w", pady=(2, 0))
        self.__boton_registrar_salida = ttk.Button(contenedor, text="Registrar salida",
                                                   command=self.__al_registrar_salida)
        self.__boton_registrar_salida.grid(row=8, column=0, sticky="ew", pady=(10, 0))
        self.__borrar_calculo()

    def __borrar_calculo(self) -> None:
        self.__etiqueta_cantidad_dias.config(text="Cantidad de días:")
        self.__etiqueta_total_pago.config(text="Total: $")
        self.__boton_registrar_salida.state(["disabled"])

    def __al_calcular(self) -> None:
        self.__borrar_calculo()
        try:
            fecha_salida = Hotel.convertir_fecha(self.__campo_fecha_salida.get())
        except ValueError:
            messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado "
                                            "(aaaa-mm-dd).", parent=self)
            return
        huesped = self.__habitacion_ocupada.get_huesped()
        if fecha_salida <= huesped.get_fecha_ingreso():
            messagebox.showerror("Mensaje", "La fecha de salida debe ser mayor que la "
                                            "fecha de ingreso.", parent=self)
            return
        huesped.set_fecha_salida(fecha_salida)
        cantidad = huesped.obtener_dias_alojamiento()
        valor = cantidad * self.__habitacion_ocupada.get_precio_dia()
        self.__etiqueta_cantidad_dias.config(text=f"Cantidad de días: {cantidad}")
        self.__etiqueta_total_pago.config(text=f"Total: $ {valor:,.0f}")
        self.__boton_registrar_salida.state(["!disabled"])

    def __al_registrar_salida(self) -> None:
        self.__hotel.registrar_salida(self.__numero_habitacion)
        messagebox.showinfo("Mensaje", "Se ha registrado la salida del huésped", parent=self)
        self.destroy()


class VentanaPrincipal(tk.Tk):

    def __init__(self, hotel: Hotel):
        super().__init__()
        self.__hotel = hotel
        self.__inicio()
        self.title("Hotel")
        self.resizable(False, False)
        self.__centrar_en_pantalla()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Consultar habitaciones", command=self.__al_consultar)
        menu_opciones.add_command(label="Salida de huéspedes", command=self.__al_salida)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Gestión de huéspedes del hotel",
                  font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(contenedor, text="Use el menú para consultar las habitaciones\n"
                                   "o registrar la salida de un huésped.").pack(
            anchor="w", pady=(6, 0))

    def __centrar_en_pantalla(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 3
        self.geometry(f"+{x}+{y}")

    def __al_consultar(self) -> None:
        VentanaHabitaciones(self, self.__hotel)

    def __al_salida(self) -> None:
        texto = simpledialog.askstring("Salida de huéspedes", "Ingrese número de habitación:",
                                       parent=self)
        if texto is None:
            return
        try:
            numero = int(texto.strip())
        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de número.", parent=self)
            return
        if numero < 1 or numero > Hotel.CANTIDAD_HABITACIONES:
            messagebox.showwarning("Mensaje", "El número de habitación debe estar entre 1 y 10.",
                                   parent=self)
        elif self.__hotel.buscar_habitacion_ocupada(numero):
            VentanaSalida(self, self.__hotel, numero)
        else:
            messagebox.showinfo("Mensaje", "La habitación ingresada no ha sido ocupada.",
                                parent=self)


class Principal:

    @staticmethod
    def main() -> None:
        hotel = Hotel()
        mi_ventana_principal = VentanaPrincipal(hotel)
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()
