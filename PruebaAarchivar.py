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

def agregarNota(nombre, win):    
    #Revisa todos los botones de la ventana y busca la que se llame "Add a note" (botón para agregar)
    ctrl = devolverControl("Add a note", "Button", win)
    ctrl.click_input() #clicamos para abrir la ventana de agregar nuevo
    ctrl = devolverControl("Note title", "Edit", win) #buscamos el control para agregarle titulo en la nota
    ctrl.click_input()
    ctrl.type_keys(nombre, with_spaces=True) # escribimos el nombre que nos dan como parametro
    

def archivar(nombre, win):
    #devuelve el control con el nombre del archivo (se dirige al botón de la nota con ese nombre)
    ctrl = devolverControl(nombre, "Text", win) 
    ctrl.right_click_input() #clic derecho para abrir el menu contextual
    time.sleep(1) #se espera a que abra
    # Conecta con el menú contextual (última ventana activa)
    menu = win.child_window(control_type="Menu")  
    ctrl = devolverControl("Archive", "Button", menu) #devuelve el control del botón de archivar
    ctrl.click_input() #archivamos
    
def revisarArchivado(nombre, win):
    ctrl = devolverControl("Archive", "Button", win) #entramos al apartado de archivados
    ctrl.click_input()
    time.sleep(1)
    ctrl = devolverControl(nombre, "Text", win) #buscamos una nota que tenga el nombre que nos dieron como parametro
    return ctrl is not None # devuelve true si existe, false si no

def pruebaArchivar(win):
    agregarNota("Prueba", win) #agregamos una nota
    time.sleep(1)
    archivar("Prueba", win) #la archivamos
    time.sleep(1)
    return revisarArchivado("Prueba", win) #devolvemos true si se archivó, false si no

win = conectarAplicacion() #obtenemos la ventana

if pruebaArchivar(win): #mostramos una alerta dependiendo del resultado de la prueba
    mostrarAlerta("Prueba completada con éxito")
else:
    mostrarAlerta("Prueba completada con errores: No se agregó la nota al archivo")
    
    