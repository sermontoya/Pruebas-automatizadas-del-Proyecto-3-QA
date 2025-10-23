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


    
def desarchivar(nombre, win):
    #tenemos que estar en el menu de archivados
    ctrl = devolverControl(nombre, "Text", win) 
    ctrl.right_click_input() #clic derecho para abrir el menu contextual
    time.sleep(1) #se espera a que abra
    # Conecta con el menú contextual (última ventana activa)
    menu = win.child_window(control_type="Menu")  
    ctrl = devolverControl("Archive", "Button", menu) #devuelve el control del botón de archivar
    ctrl.click_input() #desarchivamos
    
def revisarDesarchivado(nombre, win):
    #temenos que estar en el menu de archivados
    ctrl = devolverControl("Notes", "Button", win) #buscamos el boton de notas (pagina principal)
    ctrl.click_input() #nos devolvemos
    time.sleep(1)
    ctrl = devolverControl(nombre, "Text", win) #buscamos una nota que tenga el nombre que nos dieron como parametro
    return ctrl is not None # devuelve true si existe, false si no

def pruebaDesarchivar(win):
    time.sleep(1)
    desarchivar("Prueba", win) #solo desarchivamos la nota que ya tenemos
    time.sleep(1)
    return revisarDesarchivado("Prueba", win) #devolvemos true si se desarchivó, false si no

win = conectarAplicacion()

if pruebaDesarchivar(win): #mostramos una alerta dependiendo del resultado de la prueba
    mostrarAlerta("Prueba completada con éxito")
else:
    mostrarAlerta("Prueba completada con errores: No se agregó la nota al archivo")
    
    