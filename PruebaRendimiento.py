import time
from statistics import mean
from tkinter import messagebox
from pywinauto import Application


def conectarAplicacion():
    app = Application(backend="uia")
    #La aplicación ya está abierta desde antes de ejecutar, solo se conecta
    app.connect(title_re=".*Notesnook.*")
    # Se concentra en la ventana
    win = app.top_window()
    win.set_focus()
    return win

def mostrarAlerta(texto):
    messagebox.showinfo("Alerta", texto)

def devolverControl(nombre_parcial, tipo, win):
    for ctrl in win.descendants(control_type=tipo):
        if ctrl.window_text().startswith(nombre_parcial):
            return ctrl
    return None

#devuelve el control guiandose de su propiedad automation_id (necesario para un control que su nombre era "")
def devolverControlPorAutomationID(helptext, tipo, win):
    for ctrl in win.descendants(control_type=tipo):
        props = ctrl.get_properties()
        if props.get("automation_id") == helptext:
            return ctrl
    return None

def buscar(win, texto):
    ctrl = devolverControlPorAutomationID("search", "Edit", win)
    ctrl.click_input()
    ctrl.type_keys("^a{BACKSPACE}")  # Limpia el campo
    ctrl.type_keys(texto, with_spaces=True)
    time.sleep(0.5) #espera corta por los resultados

def agregarNota(nombre, win):    
    #Revisa todos los botones de la ventana y busca la que se llame "Add a note" (botón para agregar)
    ctrl = devolverControl("Add a note", "Button", win)
    ctrl.click_input()
    time.sleep(0.5)
    ctrl = devolverControl("Note title", "Edit", win)
    ctrl.click_input()
    ctrl.type_keys(nombre, with_spaces=True)

def agregarNotas(notas, win):
    for i in notas:
        agregarNota(i, win)

def pruebaRendimientoBusqueda(win, busquedas):
    tiempos = []

    for texto in busquedas:
        inicio = time.perf_counter()
        buscar(win, texto)
        fin = time.perf_counter()
        duracion = fin - inicio
        tiempos.append(duracion)
    promedio = mean(tiempos)
    return promedio



win = conectarAplicacion()


busquedas = [f"Prueba{i}" for i in range(1, 51)]
notas = [f"Prueba{i}" for i in range(1, 201)]

agregarNotas(notas, win)
mostrarAlerta(str(pruebaRendimientoBusqueda(win, busquedas)))
