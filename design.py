import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Radiobutton
from tkinter import  filedialog, Label
from PIL import ImageTk, Image
import os 
import numpy as np
import  cv2 
from matplotlib import pyplot as plt
from tkinter import Tk, Canvas
import process_numericalprogation
from pyDHM import utilities

def crear_label(main_frame, text, bg, font, fg, x, y):
    txt = Label(main_frame, text=text, bg=bg, font=font, fg=fg)
    txt.place(x=x, y=y)

# def crear_rectangulos(canvas, parametros):
#     rectangulos = []

#     for param in parametros:
#         coordenadas = param['coordenadas']
#         fill = param['fill']
#         outline = param['outline']
#         width = param['width']

#         rectangulo = canvas.create_rectangle(coordenadas, fill=fill, outline=outline, width=width)
#         rectangulos.append(rectangulo)

#     return rectangulos

# def crear_rectangulos(canvas, coordenadas, radio, **kwargs):
#     x1, y1, x2, y2 = coordenadas
#     return canvas.create_polygon(
#         x1 + radio, y1,
#         x2 - radio, y1,
#         x2, y1,
#         x2, y2,
#         x2 - radio, y2,
#         x1 + radio, y2,
#         x1, y2,
#         x1, y1 + radio,
#         x1, y1,
#         smooth=True,
#         **kwargs
#     )


def crear_rectangulos(canvas, parametros):
    for param in parametros:
        coordenadas = param['coordenadas']
        radio = 30
        x1, y1, x2, y2 = map(int, coordenadas)
        
        # Dibuja las líneas para formar el rectángulo con esquinas redondeadas
        canvas.create_line(x1 + radio, y1, x2 - radio, y1, fill=param['outline'], width=param['width'])
        canvas.create_line(x1, y1 + radio, x1, y2 - radio, fill=param['outline'], width=param['width'])
        canvas.create_line(x2, y1 + radio, x2, y2 - radio, fill=param['outline'], width=param['width'])
        canvas.create_line(x1 + radio, y2, x2 - radio, y2, fill=param['outline'], width=param['width'])
        
        # Dibuja las esquinas redondeadas
        canvas.create_arc(x1, y1, x1 + 2 * radio, y1 + 2 * radio, start=90, extent=90, style=tk.ARC, outline=param['outline'], width=param['width'])
        canvas.create_arc(x2 - 2 * radio, y1, x2, y1 + 2 * radio, start=0, extent=90, style=tk.ARC, outline=param['outline'], width=param['width'])
        canvas.create_arc(x1, y2 - 2 * radio, x1 + 2 * radio, y2, start=180, extent=90, style=tk.ARC, outline=param['outline'], width=param['width'])
        canvas.create_arc(x2 - 2 * radio, y2 - 2 * radio, x2, y2, start=270, extent=90, style=tk.ARC, outline=param['outline'], width=param['width'])

def crear_botones_cuadro(canvas, coordenadas,self):
    boton = []
    def izq ():
        
        self.bandera_holo = 0 
        if self.bandera_holo <= 0:
            self.bandera_holo == 0
            process_numericalprogation.process_numericalPropagation(self)
            borrar  = boton[0]
            borrar.destroy()
            boton.pop(0)


    def der ():
        def zoom():
            utilities.imageShow(self.FT_intensity ,"FT")

        self.bandera_holo = 1 
        if self.bandera_holo >= 1:
            self.bandera_holo == 1
            process_numericalprogation.process_numericalPropagation(self)
            if len(boton) == 0:
                btn_zoom = tk.Button(canvas, text="Zoom", font=("Arial", 8), command=lambda: zoom())
                btn_zoom.place(x = 575, y= 500)
                boton.append(btn_zoom) 
            

        

    desplazamiento_vertical = -5

    btn_izquierdo = tk.Button(canvas, text="\u2190", font=("Arial", 8), command=lambda: izq())
    btn_izquierdo_window = canvas.create_window(coordenadas[0], coordenadas[3] - desplazamiento_vertical, anchor="nw", window=btn_izquierdo)

    btn_derecho = tk.Button(canvas, text="\u2192", font=("Arial", 8), command=lambda: der())
    btn_derecho_window = canvas.create_window(coordenadas[2] - 40, coordenadas[3] - desplazamiento_vertical, anchor="nw", window=btn_derecho)

def crear_botones_title(title_frame, botones_config):
    botones = []

    for config in botones_config:
        btn = Button(title_frame, text=config['text'], command=config['command'])
        btn.pack(side="right", padx=10, pady=5)
        botones.append(btn)

    return botones

def crear_botones(canvas, botones_config):
    botones = []
    for config in botones_config:
        btn = tk.Button(
            canvas,
            text=config['text'],
            bg=config['bg'],
            fg=config['fg'],
            command=config['command'],
            padx=config.get('padx', 2), 
            pady=config.get('pady', 2),  
            bd=config.get('bd', 1),  
            relief=config.get('relief', 'solid')  
        )
        btn.place(x=config['x'], y=config['y'])
        botones.append(btn)
    
    return botones

def crear_radio_buttons(main_frame, text_values, variable, values, bg, command, x, y):
    radio_buttons = []
    
    for i, text in enumerate(text_values):
        rb = Radiobutton(main_frame, text=text, variable=variable, value=values[i], bg=bg, command=command)
        rb.place(x=x, y=y+(30*i))
        radio_buttons.append(rb)
    
    return radio_buttons