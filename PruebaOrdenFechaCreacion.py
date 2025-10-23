from pathlib import Path
from pywinauto import Application
import time
import tkinter as tk
from tkinter import messagebox

#muestra alertas en pantalla
def mostrarAlerta(texto):
    messagebox.showinfo("Alerta", texto)

def mostrarSiNo(texto):
    return messagebox.askyesno("Pregunta", texto)
    
def conectarAplicacion():
    app = Application(backend="uia")
    #La aplicación ya está abierta desde antes de ejecutar, solo se conecta
    app.connect(title_re=".*Notesnook.*")
    # Se concentra en la ventana
    win = app.top_window()
    win.set_focus()
    return win # retorna la ventana para usarla

# devuelve un control de la ventana por su nombre(ya sea total o parcial) y tipo
def devolverControl(nombre_parcial, tipo, win):
    for ctrl in win.descendants(control_type=tipo):
        if ctrl.window_text().startswith(nombre_parcial):
            ctrl.set_focus()
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
    ctrl = devolverControlPorAutomationID("search", "Edit", win) #devuelve el campo de busqueda
    ctrl.click_input()
    ctrl.type_keys("^a{BACKSPACE}")  # Limpia el campo
    ctrl.type_keys(texto, with_spaces=True) #escribe el nombre que queremos buscar
    time.sleep(0.5) #espera corta por los resultados
def agregarNota(nombre, win):    
    #Revisa todos los botones de la ventana y busca la que se llame "Add a note" (botón para agregar)
    ctrl = devolverControl("Add a note", "Button", win)
    ctrl.click_input() #clicamos para abrir la ventana de agregar nuevo
    ctrl = devolverControl("Note title", "Edit", win) #buscamos el control para agregarle titulo en la nota
    ctrl.click_input()
    ctrl.type_keys(nombre, with_spaces=True) # escribimos el nombre que nos dan como parametro
    ctrl = devolverControl("Start writing your note...", "Text", win) #devuelve el campo para agregarle contenido
    ctrl.click_input()
    ctrl.type_keys("Prueba", with_spaces=True) #escribimos el contenido
    
def ordenarFechaAscendente(win):
    buscar(win, "Prueba")
    ctrl = devolverControl("Grouped by", "Button", win) #devuelve el control menu de filtros
    ctrl.click_input()
    ctrl = devolverControl("Sort by", "Button", win) #nos dirigimos al apartado de sort by
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Date edited", "Button", win) #Ordenar por fecha de edición
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Grouped by", "Button", win) 
    ctrl.click_input()
    ctrl = devolverControl("Order by", "Button", win) 
    ctrl.click_input()
    ctrl = ctrl = devolverControl("Oldest - newest", "Button", win) #ordenamos de antiguo a reciente
    ctrl.click_input()
    
def ordenarFechaDescendente(win):
    buscar(win, "Prueba")
    ctrl = devolverControl("Grouped by", "Button", win) #devuelve el control menu de filtros
    ctrl.click_input()
    ctrl = devolverControl("Sort by", "Button", win) #nos dirigimos al apartado de sort by
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Date edited", "Button", win) #Ordenar por fecha de edición
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Grouped by", "Button", win) 
    ctrl.click_input()
    ctrl = devolverControl("Order by", "Button", win) 
    ctrl.click_input()
    ctrl = ctrl = devolverControl("Newest - oldest", "Button", win) #ordenamos de reciente a antiguo
    ctrl.click_input()

    
def pruebaBusquedaOrdenPorFecha(ord, win):
    #preguntamos al usuario si están ordenadas las notas de manera correcta (tiene que verificar manualmente)
    if ord =="A":
        ordenarFechaAscendente(win)
        return mostrarSiNo("¿Está ordenado de antiguo a reciente?") #devuelve true si se responde "Sí", sino false
    else: 
        ordenarFechaDescendente(win)
        return mostrarSiNo("¿Está ordenado de reciente a antiguo?") #devuelve true si se responde "Sí", sino false
    

def agregarNotas(win):
    #agregamos las notas y damos un margen de 5 segundos para que haya un margen de edición
    agregarNota("Primero", win)
    time.sleep(5)
    agregarNota("Segundo", win)
    time.sleep(5)
    agregarNota("Tercero", win)
    time.sleep(5)
    
win = conectarAplicacion()
agregarNotas(win) 
prueba1= pruebaBusquedaOrdenPorFecha("A", win)
prueba2 =pruebaBusquedaOrdenPorFecha("D", win)
if prueba1:
    if prueba2:
        mostrarAlerta("Prueba completada con éxito") #si ambas pruebas devuelven true es un éxito
    else:
        mostrarAlerta("Prueba completada con errores: Ordenamiento descendente incorrecto") # si solo la prueba2 falla, falló el descendente
else:
    if prueba2:
         mostrarAlerta("Prueba completada con errores: Ordenamiento ascendente incorrecto") # si solo la prueba1 falla, falló el ascendente
    else:
         mostrarAlerta("Prueba completada con errores: ambos ordenamientos incorrectos") # si ambas fallan
   
