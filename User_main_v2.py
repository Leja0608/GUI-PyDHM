import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import  Label
from pyDHM import utilities
from pyDHM import numericalPropagation
from pyDHM import phaseCompensation
from PIL import ImageTk, Image
import numpy as np
import design
import process_numericalprogation
import general_configuration
import process_phaseCompensation
import os 
from tkinter import  filedialog, Label
from pyDHM import phaseShifting
import process_phaseshifting
from tkinter import scrolledtext

from tkinter import Tk, Canvas
from PIL import Image, ImageDraw, ImageTk

import tkinter as tk
from tkinter import IntVar
from PIL import Image, ImageTk

class User_Interface:
    def __init__(self, master):
        self.Posicion_Img = 0
        self.output_compe = 0 
        self.master = master
        master.geometry("1366x680")  
        master.title("User_pyDHM")
        self.auxiliar_unidades = 0
        self.general_aux= IntVar()
        self.label_title =  IntVar()
        self.label_title.set(3)
        self.variable = None 

        self.ancho = 1366
        self.altura = 680

        self.ruta_0 = self.ruta_1 = self.ruta_2 = self.ruta_3 = self.ruta_4 = self.ruta_5 = None
        
        args = ['arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9', 'arg10', 'arg11', 'arg12', 'arg13']
        self.args = [tk.StringVar() for _ in range(len(args))]
        for i, arg in enumerate(args):
            setattr(self, arg, self.args[i])

        extra_args = ['image_main', 'cuadro_ruta', 'argc1', 'argc2', 'argc3', 'argc4', 'argc5', 'argc6', 'argc7', 'argc8', 'argc9']
        self.extra_args = [tk.StringVar() for _ in range(len(extra_args))]
        for i, arg in enumerate(extra_args):
            setattr(self, arg, self.extra_args[i])
        
        extra_args_shift = ['arg1_shift', 'arg2_shift', 'arg3_shift', 'arg4_shift']
        self.extra_args_shift = [tk.StringVar() for _ in range(len(extra_args_shift))]
        for i, arg in enumerate(extra_args_shift):
            setattr(self, arg, self.extra_args_shift[i])

        self.label()
    
        self.title_frame = tk.Frame(master, bg="white")
        self.title_frame.pack(side="top", fill="x")

        botones_config = [{'text': "Numerical propagation", 'command': lambda:  self.Numerical_propagation("white")},
                          {'text': "Phase compensation", 'command': lambda: self.phase_comp("white")},
                          {'text': "Phase-shifting", 'command': lambda: self.Phase_shifting("white")},
                          {'text': "Settings", 'command': lambda: ...}]
        buttons = design.crear_botones_title(self.title_frame, botones_config)
       
        self.button2 = buttons[1]
        self.button3 = buttons[2]
        self.button4 = buttons[3]
        
        self.title_label = tk.Label(self.title_frame, text="PyDHM", font=("Arial", 20), bg="white")
        self.title_label.pack(side="left", padx=10, pady=5)

        self.title_label1 = tk.Label(self.title_frame, text=str(self.txt_label), font=("Arial", 20), bg="white")
        
        self.title_label1.pack(side="left", padx=10, pady=5)

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(side="top", fill="both", expand=True)
        self.main_frame.configure(bg='white')

        texto = """      PyDHM graphical user interface is a friendly tool for working with pyDHM library, based on an intuitive visual platform that enables interactive use through direct graphical menus.
        PyDHM is a Python library that provides a set of numerical processing algorithms for reconstructing amplitude and phase images for a broad range of optical DHM configurations.
        """

        texto_widget = tk.Text(self.main_frame, wrap=tk.WORD, font=("Arial", 20), bg='white', height=10, width=40)
        texto_widget.insert("1.0", texto)
        texto_widget.place(x=60, y=100)

        texto2 = """        Welcome to pyDHM graphical user interface aimed at Digital Holographic Microscopy (DHM) applications.

        Please select the package to work
                Numerical propagation
                Phase Compensation
                Phase-Shifting 
        """

        texto_widget2 = tk.Text(self.main_frame, wrap=tk.WORD, font=("Arial", 20), bg='white', height=10, width=40)
        texto_widget2.insert("1.0", texto2)
        texto_widget2.place(x=700, y=100)
    
        self.imagen1 = Image.open("Logos\eafit-logo.png")
        self.imagen2 = Image.open("Logos\logoITM.png")
        self.imagen3 = Image.open("Logos\standard.png")

        self.imagen1 = self.imagen1.resize((200, 100))  
        self.imagen2 = self.imagen2.resize((200, 100))
        self.imagen3 = self.imagen3.resize((200, 100))

        self.imagen1 = ImageTk.PhotoImage(self.imagen1)
        self.imagen2 = ImageTk.PhotoImage(self.imagen2)
        self.imagen3 = ImageTk.PhotoImage(self.imagen3)

        self.label_imagen1 = tk.Label(self.main_frame, image=self.imagen1)
        self.label_imagen1.place(x=100, y=500)
        self.label_imagen2 = tk.Label(self.main_frame, image=self.imagen2)
        self.label_imagen2.place(x=600, y=500)
        self.label_imagen3 = tk.Label(self.main_frame, image=self.imagen3)
        self.label_imagen3.place(x=1100, y=500)

    def Numerical_propagation(self, color):
        self.bandera_holo = 0
        self.flag_plotHolo = 0
        self.general_aux.set(0)
        self.label_title.set(0)
        general_configuration.clear_widget(self)
        self.main_frame.configure(bg=color)
        self.label()

        canvas = tk.Canvas(self.main_frame, bg=color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        parametros = [
            {'coordenadas': (10, 700 / 40, 1 / 4 * 1366 - 10, 700 / 8), 'fill': 'white', 'outline': 'blue', 'width': 1},
            {'coordenadas': (10, 700 / 6, 1 / 4 * 1366 - 10, 700 / 3), 'fill': 'white', 'outline': 'blue', 'width': 1},
            {'coordenadas': (10, 700 / 3 + 25, 1 / 4 * 1366 - 10, 2 / 3 * 700 - 10), 'fill': 'white', 'outline': 'blue', 'width': 1},
            {'coordenadas': (10, 2 * 700 / 3 + 25, 1 / 4 * 1366 - 10, 700 - 100), 'fill': 'white', 'outline': 'blue', 'width': 1},
        ]

        design.crear_rectangulos(canvas, parametros)

        tamanio_cuadrado = 480

        parametros_nuevos = [
            {'coordenadas': (1 / 4 * 1366 + 10, 10, 1 / 4 * 1366 + 10 + tamanio_cuadrado, 10 + tamanio_cuadrado), 'fill': 'white', 'outline': 'blue', 'width': 1},
            {'coordenadas': (1 / 4 * 1366 + 30 + tamanio_cuadrado, 10, 1 / 4 * 1366 + 30 + 2 * tamanio_cuadrado, 10 + tamanio_cuadrado), 'fill': 'white', 'outline': 'blue', 'width': 1},
        ]

        design.crear_rectangulos(canvas, parametros_nuevos)

        for param in parametros_nuevos:
            design.crear_botones_cuadro(canvas, param['coordenadas'],self)
        
        rectangulo_abajo = {'coordenadas': (1 / 4 * 1366 + 10, 550, 3 / 4 * 1366-90, 610), 'fill': 'white', 'outline': 'blue', 'width': 1}
        design.crear_rectangulos(canvas, [rectangulo_abajo])

        rectangulo_abajo1 = {'coordenadas': (3 / 4 * 1366 - 80, 550, 1340- 10, 610), 'fill': 'white', 'outline': 'blue', 'width': 1}
        design.crear_rectangulos(canvas, [rectangulo_abajo1])

        button_width = 150
        button_height = 30
        button_reset = tk.Button(self.main_frame, text="Reset", command=...)
        button_reset.configure(width=16, height=1)
        button_reset.place(x=380, y=570)

        button_save = tk.Button(self.main_frame, text="Save", command=...)
        button_save.configure(width=16, height=1)
        button_save.place(x=590, y=570)

        button_propagate = tk.Button(self.main_frame, text="Propagate", command=...)
        button_propagate.configure(width=16, height=1)
        button_propagate.place(x=785, y=570)

        text_color = 'blue'
        text_bg = 'white'
        text_font = ("Arial", 16)

        textos = ['New Hologram', 'Propation Method', 'Paramters', 'Spacial Filter']

        for i, param in enumerate(parametros):
            x1, y1, x2, y2 = param['coordenadas']
            texto_x = x1 + 50
            texto_y = y1-15
            texto = textos[i]
            label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
            label.place(x=texto_x, y=texto_y)

        textos_2 = ['Hologram / Fourier Transform', 'Amplitude / Phase']

        for i, param in enumerate(parametros_nuevos):
            x1, y1, x2, y2 = param['coordenadas']
            texto_x = x1 + 50
            texto_y = y1-15
            texto = textos_2[i]
            label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
            label.place(x=texto_x, y=texto_y)

        textos_3 = ['Actions']
        coordenadas = rectangulo_abajo['coordenadas']
        x1, y1, x2, y2 = coordenadas
        texto_x = x1 + 50
        texto_y = y1 - 15
        texto = textos_3[0]
        label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
        label.place(x=texto_x, y=texto_y)

        textos_4 = ['Propagate Function']
        coordenadas = rectangulo_abajo1['coordenadas']
        x1, y1, x2, y2 = coordenadas
        texto_x = x1 + 50
        texto_y = y1 - 15
        texto = textos_4[0]
        label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
        label.place(x=texto_x, y=texto_y)

        label_from = tk.Label(canvas, text="From:")
        label_from.place(x=rectangulo_abajo1['coordenadas'][0] + 10, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_from = tk.Entry(canvas,width=5)
        entry_from.place(x=rectangulo_abajo1['coordenadas'][0] + 70, y=rectangulo_abajo1['coordenadas'][1] + 20)

        label_to = tk.Label(canvas, text="To:")
        label_to.place(x=rectangulo_abajo1['coordenadas'][0] + 150, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_to = tk.Entry(canvas,width=5)
        entry_to.place(x=rectangulo_abajo1['coordenadas'][0] + 190, y=rectangulo_abajo1['coordenadas'][1] + 20)

        label_step = tk.Label(canvas, text="Step:")
        label_step.place(x=rectangulo_abajo1['coordenadas'][0] + 270, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_step = tk.Entry(canvas,width=5)
        entry_step.place(x=rectangulo_abajo1['coordenadas'][0] + 310, y=rectangulo_abajo1['coordenadas'][1] + 20)

        process_numericalprogation.assign_args(self,None,None,None)
        process_numericalprogation.create_radio_buttons(self)
        process_numericalprogation.crear_desplegable_filtro(self)
        process_numericalprogation.agregar_imagen(self)

    def phase_comp(self,color):
        self.general_aux.set(1)

        self.label_title.set(1)
        
        general_configuration.clear_widget(self)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.main_frame.configure(bg=color) 

        canvas = tk.Canvas(self.main_frame, bg=color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.label()

        parametros_rectangulos = [{'coordenadas': (10, altura/40, 1/4 * ancho-10, altura/8), 'fill': 'white', 'outline': 'blue', 'width': 1},
                                  {'coordenadas': (10, altura/6, 1/4 * ancho-10, altura/3+50), 'fill': 'white', 'outline': 'blue', 'width': 1},
                                  {'coordenadas': (10, altura/3+75, 1/4 * ancho-10, 2/3 * altura+80), 'fill': 'white', 'outline': 'blue', 'width': 1},
                                  ]

        rectangulos = design.crear_rectangulos(canvas, parametros_rectangulos)

        tamanio_cuadrado = 480

        parametros_nuevos = [
            {'coordenadas': (1 / 4 * 1366 + 10, 10, 1 / 4 * 1366 + 10 + tamanio_cuadrado, 10 + tamanio_cuadrado), 'fill': 'white', 'outline': 'blue', 'width': 1},
            {'coordenadas': (1 / 4 * 1366 + 30 + tamanio_cuadrado, 10, 1 / 4 * 1366 + 30 + 2 * tamanio_cuadrado, 10 + tamanio_cuadrado), 'fill': 'white', 'outline': 'blue', 'width': 1},
        ]

        design.crear_rectangulos(canvas, parametros_nuevos)

        for param in parametros_nuevos:
            design.crear_botones_cuadro(canvas, param['coordenadas'],self)
        
        rectangulo_abajo = {'coordenadas': (1 / 4 * 1366 + 10, 550, 3 / 4 * 1366-90, 610), 'fill': 'white', 'outline': 'blue', 'width': 1}
        design.crear_rectangulos(canvas, [rectangulo_abajo])

        rectangulo_abajo1 = {'coordenadas': (3 / 4 * 1366 - 80, 550, 1340- 10, 610), 'fill': 'white', 'outline': 'blue', 'width': 1}
        design.crear_rectangulos(canvas, [rectangulo_abajo1])

        
        button_width = 150
        button_height = 30
        button_reset = tk.Button(self.main_frame, text="Reset", command=...)
        button_reset.configure(width=16, height=1)
        button_reset.place(x=380, y=570)

        button_save = tk.Button(self.main_frame, text="Save", command=...)
        button_save.configure(width=16, height=1)
        button_save.place(x=590, y=570)

        button_propagate = tk.Button(self.main_frame, text="Propagate", command=...)
        button_propagate.configure(width=16, height=1)
        button_propagate.place(x=785, y=570)

        text_color = 'blue'
        text_bg = 'white'
        text_font = ("Arial", 16)

        textos = ['New Hologram', 'Compensation Method', 'Paramters']

        for i, param in enumerate(parametros_rectangulos):
            x1, y1, x2, y2 = param['coordenadas']
            texto_x = x1 + 50
            texto_y = y1-15
            texto = textos[i]
            label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
            label.place(x=texto_x, y=texto_y)

        textos_2 = ['Hologram / Fourier Transform', 'Amplitude / Phase']

        for i, param in enumerate(parametros_nuevos):
            x1, y1, x2, y2 = param['coordenadas']
            texto_x = x1 + 50
            texto_y = y1-15
            texto = textos_2[i]
            label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
            label.place(x=texto_x, y=texto_y)

        textos_3 = ['Actions']
        coordenadas = rectangulo_abajo['coordenadas']
        x1, y1, x2, y2 = coordenadas
        texto_x = x1 + 50
        texto_y = y1 - 15
        texto = textos_3[0]
        label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
        label.place(x=texto_x, y=texto_y)

        textos_4 = ['Propagate Function']
        coordenadas = rectangulo_abajo1['coordenadas']
        x1, y1, x2, y2 = coordenadas
        texto_x = x1 + 50
        texto_y = y1 - 15
        texto = textos_4[0]
        label = tk.Label(canvas, text=texto, font=text_font, fg=text_color, bg=text_bg)
        label.place(x=texto_x, y=texto_y)

        label_from = tk.Label(canvas, text="From:")
        label_from.place(x=rectangulo_abajo1['coordenadas'][0] + 10, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_from = tk.Entry(canvas,width=5)
        entry_from.place(x=rectangulo_abajo1['coordenadas'][0] + 70, y=rectangulo_abajo1['coordenadas'][1] + 20)

        label_to = tk.Label(canvas, text="To:")
        label_to.place(x=rectangulo_abajo1['coordenadas'][0] + 150, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_to = tk.Entry(canvas,width=5)
        entry_to.place(x=rectangulo_abajo1['coordenadas'][0] + 190, y=rectangulo_abajo1['coordenadas'][1] + 20)

        label_step = tk.Label(canvas, text="Step:")
        label_step.place(x=rectangulo_abajo1['coordenadas'][0] + 270, y=rectangulo_abajo1['coordenadas'][1] + 20)

        entry_step = tk.Entry(canvas,width=5)
        entry_step.place(x=rectangulo_abajo1['coordenadas'][0] + 310, y=rectangulo_abajo1['coordenadas'][1] + 20)
        self.create_rad_comp()
        self.parametros_comp(list_args = None, list_names = None, unit = self.variable)
        process_phaseCompensation.agregar_imagen(self)

    def create_rad_comp(self):
        self.VCom = IntVar()
        self.VCom.set(6)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()

        text_values = ["Full ROI", "Efficient ROI", "Cost Function", "Compensation no-telecentric"]
        values = [0, 1, 2, 3, 6]

        radio_buttons = design.crear_radio_buttons(self.main_frame, text_values, self.VCom, values, "white", self.parametros_comp, ancho/60, altura/5)
        
    
    def parametros_comp(self, list_args: list = None, list_names: list = None, unit: str = None):
        
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        
        if self.VCom.get() == 0:
            print(self.widget_refs)
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            if list_args is None:
                list_args = [self.argc1, self.argc2, self.argc3, self.argc4,self.argc5,self.argc6]
            if list_names is None:
                list_names = ["Upper", "Wavelength", "Pitch x", "Pitch y","S","Step"]
            if self.variable is not None:
                list_names = [f"{name} ({self.variable})" for name in list_names]

            y = 0
            for arg, name in zip(list_args, list_names):
                arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
                arg_entry.place(x=ancho/12+17, y=altura/3+110+y)
                text_refer = tk.Label(self.main_frame, text=name, bg="white")
                text_refer.place(x=30, y=altura/3+110+y)
                y += 20
                self.widget_refs.append(arg_entry)
                self.widget_refs.append(text_refer)
            
        elif self.VCom.get() == 1:
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            if list_args is None:
                list_args = [self.argc1, self.argc2, self.argc3, self.argc4,self.argc5,self.argc6]
            if list_names is None:
                list_names = ["Upper", "Wavelength", "Pitch x", "Pitch y","S","Step"]
            if self.variable is not None:
                list_names = [f"{name} ({self.variable})" for name in list_names]
            y = 0
            for arg, name in zip(list_args, list_names):
                arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
                arg_entry.place(x=ancho/12+17, y=altura/3+110+y)
                text_refer = tk.Label(self.main_frame, text=name, bg="white")
                text_refer.place(x=30, y=altura/3+110+y)
                y += 20
                self.widget_refs.append(arg_entry)
                self.widget_refs.append(text_refer)

        elif self.VCom.get() == 2:
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            if list_args is None:
                list_args = [self.argc1, self.argc2, self.argc3]
            if list_names is None:
                list_names = ["Wavelength", "Pitch x", "Pitch y"]
            y = 0
            if self.variable is not None:
                list_names = [f"{name} ({self.variable})" for name in list_names]
            for arg, name in zip(list_args, list_names):
                arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
                arg_entry.place(x=ancho/12+17, y=altura/3+110+y)
                text_refer = tk.Label(self.main_frame, text=name, bg="white")
                text_refer.place(x=30, y=altura/3+110+y)
                y += 20
                self.widget_refs.append(arg_entry)
                self.widget_refs.append(text_refer)

        elif self.VCom.get() == 3:
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            if list_args is None:
                list_args = [self.argc1, self.argc2, self.argc3, self.argc4,self.argc5,self.argc6,self.argc7]
            if list_names is None:
                list_names = [ "Wavelength", "Pitch x", "Pitch y","X1","X2","Y1","Y2"]
            if self.variable is not None:
                list_names = [f"{name} ({self.variable})" for name in list_names]
            y = 0
            for arg, name in zip(list_args, list_names):
                arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
                arg_entry.place(x=ancho/12+17, y=altura/3+110+y)
                text_refer = tk.Label(self.main_frame, text=name, bg="white")
                text_refer.place(x=30, y=altura/3+110+y)
                y += 20
                self.widget_refs.append(arg_entry)
                self.widget_refs.append(text_refer)
        elif self.VCom.get() == 6:
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            label_instruction = tk.Label(self.main_frame, text="Select a compensation method \u2191", bg="white",font=("Arial", 16))
            label_instruction.place(x=20, y=2*altura/3-50)
            self.widget_refs.append(label_instruction)

    def Phase_shifting(self, color):
        self.general_aux.set(2)
        self.label_title.set(2)

        self.arg1_shift = tk.StringVar()
        self.arg2_shift = tk.StringVar()
        self.arg3_shift = tk.StringVar()
        self.arg4_shift = tk.StringVar()

        general_configuration.clear_widget(self)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()

        canvas = tk.Canvas(self.main_frame, bg=color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.label()

    def label(self):
        if hasattr(self, "title_label1"):  
            self.title_label1.pack_forget()

        self.txt_label = tk.StringVar()
        lista =[]
        if self.label_title.get()  == 0: 
            self.txt_label = 'Numerical Progation'
            self.title_label1 = tk.Label(self.title_frame, text="Numerical Progation", font=("Arial", 20), bg="white")
            self.title_label1.pack(side="left", padx=10, pady=5)

        elif self.label_title.get() == 1:
            self.txt_label = 'Phase compensation'
            self.title_label1 = tk.Label(self.title_frame, text="Phase compensation", font=("Arial", 20), bg="white")
            self.title_label1.pack(side="left", padx=10, pady=5)
        elif self.label_title.get()  == 2:
            self.txt_label = 'Phase-shifting'
            self.title_label1 = tk.Label(self.title_frame, text="Phase-shifting", font=("Arial", 20), bg="white")
            self.title_label1.pack(side="left", padx=10, pady=5)
        else:
            self.txt_label = ' '

# Crear la ventana principal
root = tk.Tk()
app = User_Interface(root)
root.mainloop()
