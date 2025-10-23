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
    
def ordenarTituloAscendente(win):
    buscar(win, "Prueba")
    ctrl = devolverControl("Grouped by", "Button", win) #devuelve el control menu de filtros
    ctrl.click_input()
    ctrl = devolverControl("Sort by", "Button", win) #nos dirigimos al apartado de sort by
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Title", "Button", win) #Ordenar por titulo
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Grouped by", "Button", win) 
    ctrl.click_input()
    ctrl = devolverControl("Order by", "Button", win) 
    ctrl.click_input()
    ctrl = ctrl = devolverControl("A to Z", "Button", win) #ordenar de la A a la Z (ascendente)
    ctrl.click_input()
    
def ordenarTituloDescendente(win):
    buscar(win, "Prueba")
    ctrl = devolverControl("Grouped by", "Button", win) #devuelve el control menu de filtros
    ctrl.click_input()
    ctrl = devolverControl("Sort by", "Button", win) #nos dirigimos al apartado de sort by
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Title", "Button", win) #Ordenar por titulo
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl("Grouped by", "Button", win) 
    ctrl.click_input()
    ctrl = devolverControl("Order by", "Button", win) 
    ctrl.click_input()
    ctrl = ctrl = devolverControl("Z to A", "Button", win) #ordenar de la Z a la A (descendente)
    ctrl.click_input()

    
def pruebaBusquedaOrdenPorTitulo(ord, win):
    #preguntamos al usuario si están ordenadas las notas de manera correcta (tiene que verificar manualmente)
    if ord =="A":
        ordenarTituloAscendente(win)
        return mostrarSiNo("¿Está ordenado de la A a la Z?")
    else: 
        ordenarTituloDescendente(win)
        return mostrarSiNo("¿Está ordenado de la Z a la A?")
    

def agregarNotas(win):
    #agregamos las notas 
    agregarNota("Primero", win)
    agregarNota("Segundo", win)
    agregarNota("Tercero", win)
    
win = conectarAplicacion()
agregarNotas(win)    
prueba1= pruebaBusquedaOrdenPorTitulo("A", win)
prueba2 =pruebaBusquedaOrdenPorTitulo("D", win)
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
