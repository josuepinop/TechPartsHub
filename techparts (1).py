import tkinter as tk
from tkinter import ttk, messagebox

# ========================== CLASES ==========================

class ParteHardware:
    def __init__(self, nombre, codigo, descripcion, fabricante, precio, cantidad, categoria):
        self.nombre = nombre
        self.codigo = codigo
        self.descripcion = descripcion
        self.fabricante = fabricante
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.categoria} | {self.fabricante} | ${self.precio:.2f} | Stock: {self.cantidad}"


class NodoPedido:
    def __init__(self, cliente, codigo_parte):
        self.cliente = cliente
        self.codigo_parte = codigo_parte
        self.siguiente = None


class ListaEnlazadaPedidos:
    def __init__(self):
        self.inicio = None
        self.final = None

    def agregar_pedido(self, cliente, codigo_parte):
        nuevo = NodoPedido(cliente, codigo_parte)
        if self.inicio is None:
            self.inicio = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def procesar_pedido(self):
        if self.inicio is None:
            return None
        pedido = self.inicio
        self.inicio = self.inicio.siguiente
        if self.inicio is None:
            self.final = None
        return pedido

    def obtener_pedidos(self):
        pedidos = []
        actual = self.inicio
        while actual:
            pedidos.append(actual)
            actual = actual.siguiente
        return pedidos


# ========================== ESTRUCTURAS GLOBALES ==========================

inventario = []
pedidos = ListaEnlazadaPedidos()

# ========================== ORDENAMIENTO ==========================

def merge_sort(lista, clave):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], clave)
    derecha = merge_sort(lista[medio:], clave)

    return merge(izquierda, derecha, clave)


def merge(izquierda, derecha, clave):
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if getattr(izquierda[i], clave) <= getattr(derecha[j], clave):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


# ========================== FUNCIONES DE INVENTARIO ==========================

def registrar_parte():
    def guardar():
        try:
            nueva = ParteHardware(
                entry_nombre.get(),
                entry_codigo.get(),
                entry_desc.get(),
                entry_fab.get(),
                float(entry_precio.get()),
                int(entry_cantidad.get()),
                entry_categoria.get()
            )
            inventario.append(nueva)
            messagebox.showinfo("Éxito", "Parte registrada exitosamente.")
            reg_win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Precio y cantidad deben ser numéricos.")

    reg_win = tk.Toplevel()
    reg_win.title("Registrar nueva parte")

    campos = [
        ("Nombre", 0),
        ("Código", 1),
        ("Descripción", 2),
        ("Fabricante", 3),
        ("Precio", 4),
        ("Cantidad", 5),
        ("Categoría", 6)
    ]
    
    entradas = []
    for label, row in campos:
        tk.Label(reg_win, text=label + ":").grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(reg_win)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entradas.append(entry)

    entry_nombre, entry_codigo, entry_desc, entry_fab, entry_precio, entry_cantidad, entry_categoria = entradas

    tk.Button(reg_win, text="Guardar", command=guardar).grid(row=7, columnspan=2, pady=10)


def mostrar_inventario():
    mostrar_win = tk.Toplevel()
    mostrar_win.title("Inventario")

    text = tk.Text(mostrar_win, width=90, height=25)
    text.pack(padx=10, pady=10)

    if not inventario:
        text.insert(tk.END, "Inventario vacío.\n")
    else:
        for parte in inventario:
            text.insert(tk.END, str(parte) + "\n")


def ordenar_inventario():
    def aplicar_orden():
        clave = combo.get()
        claves_validas = {
            "Nombre": "nombre",
            "Precio": "precio",
            "Cantidad": "cantidad"
        }
        if clave in claves_validas:
            inventario[:] = merge_sort(inventario, claves_validas[clave])
            messagebox.showinfo("Éxito", f"Inventario ordenado por {clave}.")
            orden_win.destroy()
        else:
            messagebox.showerror("Error", "Seleccione un criterio válido.")

    orden_win = tk.Toplevel()
    orden_win.title("Ordenar inventario")

    tk.Label(orden_win, text="Ordenar por:", font=("Arial", 11)).pack(pady=5)
    combo = ttk.Combobox(orden_win, values=["Nombre", "Precio", "Cantidad"])
    combo.pack(pady=5)
    tk.Button(orden_win, text="Ordenar", command=aplicar_orden).pack(pady=10)


def buscar_partes():
    def realizar_busqueda():
        criterio = combo.get()
        valor = entry_valor.get().strip().lower()
        resultados = []

        if not valor:
            messagebox.showerror("Error", "Ingrese un valor para buscar.")
            return

        for parte in inventario:
            if criterio == "Nombre" and valor in parte.nombre.lower():
                resultados.append(parte)
            elif criterio == "Código" and valor == parte.codigo.lower():
                resultados.append(parte)
            elif criterio == "Categoría" and valor == parte.categoria.lower():
                resultados.append(parte)

        res_win = tk.Toplevel()
        res_win.title("Resultados de búsqueda")
        text = tk.Text(res_win, width=90, height=25)
        text.pack(padx=10, pady=10)

        if resultados:
            text.insert(tk.END, f"Se encontraron {len(resultados)} resultado(s):\n\n")
            for parte in resultados:
                text.insert(tk.END, str(parte) + "\n")
        else:
            text.insert(tk.END, "No se encontraron coincidencias.")

        buscar_win.destroy()

    buscar_win = tk.Toplevel()
    buscar_win.title("Buscar partes")

    tk.Label(buscar_win, text="Buscar por:", font=("Arial", 11)).pack(pady=5)
    combo = ttk.Combobox(buscar_win, values=["Nombre", "Código", "Categoría"])
    combo.pack(pady=5)

    tk.Label(buscar_win, text="Valor a buscar:", font=("Arial", 11)).pack(pady=5)
    entry_valor = tk.Entry(buscar_win)
    entry_valor.pack(pady=5)

    tk.Button(buscar_win, text="Buscar", command=realizar_busqueda).pack(pady=10)


def seleccionar_k_menores():
    def mostrar_k():
        try:
            k = int(entry_k.get())
            if k <= 0:
                raise ValueError

            if not inventario:
                messagebox.showwarning("Inventario vacío", "No hay partes registradas.")
                return

            if k > len(inventario):
                messagebox.showwarning("Valor inválido", f"Solo hay {len(inventario)} partes registradas.")
                return

            copia = inventario[:]
            seleccionados = []

            for _ in range(k):
                menor = min(copia, key=lambda parte: parte.cantidad)
                seleccionados.append(menor)
                copia.remove(menor)

            resultado_win = tk.Toplevel()
            resultado_win.title("Productos en promoción")
            text = tk.Text(resultado_win, width=90, height=25)
            text.pack(padx=10, pady=10)

            text.insert(tk.END, f"Estos {k} productos están en promoción debido a su bajo stock:\n\n")
            for parte in seleccionados:
                text.insert(tk.END, str(parte) + "\n")

            selec_win.destroy()

        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero válido.")

    selec_win = tk.Toplevel()
    selec_win.title("Ver productos en promoción")

    tk.Label(selec_win, text="Ingrese el valor de k:", font=("Arial", 11)).pack(pady=5)
    entry_k = tk.Entry(selec_win)
    entry_k.pack(pady=5)
    tk.Button(selec_win, text="Mostrar", command=mostrar_k).pack(pady=10)


# ========================== FUNCIONES DE PEDIDOS ==========================

def registrar_pedido():
    def guardar_pedido():
        cliente = entry_cliente.get().strip()
        codigo = entry_codigo.get().strip()

        if not cliente or not codigo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not any(parte.codigo.lower() == codigo.lower() for parte in inventario):
            messagebox.showerror("Error", "No existe una parte con ese código.")
            return

        pedidos.agregar_pedido(cliente, codigo)
        messagebox.showinfo("Éxito", "Pedido registrado correctamente.")
        pedido_win.destroy()

    pedido_win = tk.Toplevel()
    pedido_win.title("Registrar pedido")

    tk.Label(pedido_win, text="Nombre del cliente:").pack(pady=5)
    entry_cliente = tk.Entry(pedido_win)
    entry_cliente.pack(pady=5)

    tk.Label(pedido_win, text="Código del producto:").pack(pady=5)
    entry_codigo = tk.Entry(pedido_win)
    entry_codigo.pack(pady=5)

    tk.Button(pedido_win, text="Guardar pedido", command=guardar_pedido).pack(pady=10)


def ver_pedidos():
    ventana = tk.Toplevel()
    ventana.title("Pedidos pendientes")

    text = tk.Text(ventana, width=60, height=20)
    text.pack(padx=10, pady=10)

    lista = pedidos.obtener_pedidos()
    if not lista:
        text.insert(tk.END, "No hay pedidos pendientes.\n")
    else:
        for i, nodo in enumerate(lista, 1):
            text.insert(tk.END, f"{i}. Cliente: {nodo.cliente}, Código de parte: {nodo.codigo_parte}\n")


def procesar_pedido():
    nodo = pedidos.procesar_pedido()
    if nodo:
        messagebox.showinfo("Pedido procesado", f"Se procesó el pedido de {nodo.cliente} para el producto {nodo.codigo_parte}.")
    else:
        messagebox.showinfo("Sin pedidos", "No hay pedidos para procesar.")


# ========================== INTERFAZ PRINCIPAL ==========================

root = tk.Tk()
root.title("TechParts Hub")
root.geometry("400x500")

tk.Label(root, text="Gestión de Inventario", font=("Arial", 16)).pack(pady=15)

tk.Button(root, text="Registrar nueva parte", width=30, command=registrar_parte).pack(pady=5)
tk.Button(root, text="Mostrar inventario", width=30, command=mostrar_inventario).pack(pady=5)
tk.Button(root, text="Ordenar inventario", width=30, command=ordenar_inventario).pack(pady=5)
tk.Button(root, text="Buscar partes", width=30, command=buscar_partes).pack(pady=5)
tk.Button(root, text="Ver productos en promoción", width=30, command=seleccionar_k_menores).pack(pady=5)

tk.Button(root, text="Registrar pedido", width=30, command=registrar_pedido).pack(pady=5)
tk.Button(root, text="Ver pedidos pendientes", width=30, command=ver_pedidos).pack(pady=5)
tk.Button(root, text="Procesar siguiente pedido", width=30, command=procesar_pedido).pack(pady=5)

tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=20)

root.mainloop()
