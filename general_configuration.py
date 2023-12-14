import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import  filedialog, Label
from pyDHM import utilities
from pyDHM import numericalPropagation
from PIL import ImageTk, Image
import os 
import numpy as np
import  cv2 
import design
import process_numericalprogation



def Logos(self):
    ancho = self.main_frame.winfo_width()
    altura = self.main_frame.winfo_height()

    LogoITM = Image.open("LogoITM.png")
    LogoITM = LogoITM.resize((150,100),Image.LANCZOS)
    self.img_LogoITM = ImageTk.PhotoImage(LogoITM)
    label_LogoITM = Label(self.main_frame, image=self.img_LogoITM)
    label_LogoITM.place(x=ancho-160, y=3*altura/4)

    LogoEAFIT = Image.open("LogoEAFIT.png")
    LogoEAFIT = LogoEAFIT.resize((150,100),Image.LANCZOS)
    self.img_LogoEAFIT = ImageTk.PhotoImage(LogoEAFIT)
    label_LogoEAFIT = Label(self.main_frame, image=self.img_LogoEAFIT)
    label_LogoEAFIT.place(x=ancho-160, y=3*altura/4-120)

def sfmr(field):
    global x1_ROI, x2_ROI, y1_ROI, y2_ROI
        
    print('select with the cursor mouse the region where you want to perform the spatial filtering and press the enter key')
    field = np.array(field)
    
    print(field)
    ROI_arrray = np.zeros(4)
    holoFT = np.float64(field)
    fft_holo = cv2.dft(holoFT, flags=cv2.DFT_COMPLEX_OUTPUT)
    fft_holo = np.fft.fftshift(fft_holo)
    fft_holo_image = 20 * np.log(cv2.magnitude(fft_holo[:, :, 0], fft_holo[:, :, 1]))
    minVal = np.amin(np.abs(fft_holo_image))
    maxVal = np.amax(np.abs(fft_holo_image))
    fft_holo_image = cv2.convertScaleAbs(fft_holo_image, alpha=255.0 / (maxVal - minVal),
                                        beta=-minVal * 255.0 / (maxVal - minVal))

    ROI = cv2.selectROI(fft_holo_image, fromCenter=True)
    x1_ROI = int(ROI[1])
    y1_ROI = int(ROI[0])
    x2_ROI = int(ROI[1] + ROI[3])
    y2_ROI = int(ROI[0] + ROI[2])
    ROI_arrray[0] = x1_ROI
    ROI_arrray[1] = y1_ROI
    ROI_arrray[2] = x2_ROI
    ROI_arrray[3] = y2_ROI
    return x1_ROI, x2_ROI, y1_ROI, y2_ROI

def clear_widget(self):
        if self.main_frame.children:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

def zoom(self):
        utilities.imageShow(self.FT_intensity,'Ft-hologram')

def open_settings(self):
        def accept():
            selected_option = desplegable.get()
            ventana.destroy()
            if selected_option == "Units":
                crear_desplegable_unidades(self)
            elif selected_option == "Maximum number of iteration":
                print("Entro")
                # ventana = tk.Toplevel(self.main_frame)
                # ventana.geometry("250x200")
                # ventana.configure(bg="white")
                # canvas = tk.Canvas(ventana, bg="white", width=250, height=200)
                # canvas.place(x=0, y=0)
                # parametros_rectangulo = [{'coordenadas': (20, 20, 240, 190), 'fill': 'white', 'outline': 'blue', 'width': 2}]
                # rectangulos = design.crear_rectangulos(canvas, parametros_rectangulo)
                # txt = design.crear_label(ventana, "Select number of iterations:", "white", None, None, 22, 22)
                # opciones = [10  ,20 , 30 , 40, 50, 60]
                # desplegable_num = ttk.Combobox(ventana, values=opciones, state="readonly")
                # desplegable_num.place(x=50, y=50, width=150)
                ...
            

        def cancel():
            ventana.destroy()

        ventana = tk.Toplevel(self.main_frame)
        ventana.geometry("250x200")
        ventana.configure(bg="white")
        canvas = tk.Canvas(ventana, bg="white", width=250, height=200)
        canvas.place(x=0, y=0)
        design.crear_rectangulos(canvas, [{'coordenadas': (20, 20, 240, 190), 'fill': 'white', 'outline': 'blue', 'width': 2},
            {'coordenadas': (40, 15, 220, 40), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}])

        txt = design.crear_label(ventana, "Settings", "#326CF7", ("Calibri", 11, "bold"), "white", 95, 16)
        txt = design.crear_label(ventana, "Select:", "white", ("Calibri", 11), "black", 100, 50)
        opciones = ["Units","Maximum number of iterations"]
        desplegable = ttk.Combobox(ventana, values=opciones, state="readonly")
        desplegable.place(x=50, y=80, width=150)

        botones_config = [{'text': 'Accept', 'bg': 'blue', 'fg': 'white', 'command': accept, 'x': 80, 'y': 160},
                          {'text': 'Reset', 'bg': 'blue', 'fg': 'white', 'command': cancel, 'x': 150, 'y': 160}]
        botones = design.crear_botones(canvas, botones_config)
        boton_accept = botones[0]
        boton_cancel = botones[1]

def crear_desplegable_unidades(self):
    self.auxiliar_unidades = 1 
    def inicializacion(units):
        args = [self.arg1, self.arg2, self.arg3, self.arg4, self.arg12, self.arg13]
        for arg in args:
            arg.initialize(units)
    def accept():
        unidades = {"Meter": ("m", '1e-0 '),"centimeter": ("cm", '1e-2 '),"milimeter": ("mm", '1e-3 '),"micrometer": ("µm", '1e-6 '),"nanometer": ("nm", '1e-9'),"picometer": ("pm", '1e-12')}
        self.unit = desplegable.get()
        self.variable, unidades_value = unidades.get(self.unit, ("pm", '1e-12'))
        inicializacion(unidades_value)
        ventana.destroy()
        if self.general_aux.get() == 0:
            process_numericalprogation.assign_args(self,list_args=[self.arg1, self.arg2, self.arg3, self.arg4],list_names=["Wavelength", "Distance", "Pitch x", "Pitch y"],unit=self.variable)
            self.y = 0
            process_numericalprogation.Param_Blus(self,list_args=[self.arg12, self.arg13],list_names=["Pitch x out", "Pitch y out"],unit=self.variable)
            self.z = 1
        elif self.general_aux.get() == 2:
            self.argshif( list_args = [self.arg1_shift, self.arg2_shift, self.arg3_shift, self.arg4_shift], list_names =  ["Upper", "Wavelength", "Pitch x", "Pitch y"], unit = self.variable)
        elif self.general_aux.get() == 1:
            self.parametros_comp(list_args = None, list_names = None, unit = self.variable)
            
    def cancel():
        ventana.destroy()
    ventana = tk.Toplevel(self.main_frame)
    ventana.geometry("250x200")
    ventana.configure(bg="white")
    canvas = tk.Canvas(ventana, bg="white", width=250, height=200)
    canvas.place(x=0, y=0)
    parametros_rectangulo = [{'coordenadas': (20, 20, 240, 190), 'fill': 'white', 'outline': 'blue', 'width': 2}]
    rectangulos = design.crear_rectangulos(canvas, parametros_rectangulo)
    txt = design.crear_label(ventana, "Select unites:", "white", None, None, 22, 22)
    opciones = ["Meter","centimeter", "milimeter", "micrometer","nanometer","picometer"]
    desplegable = ttk.Combobox(ventana, values=opciones, state="readonly")
    desplegable.place(x=50, y=50, width=150)
    self.unit = None
    self.variable = None
    botones_config = [{'text': 'Accept', 'bg': 'blue', 'fg': 'white', 'command': accept, 'x':50, 'y': 160},
                        {'text': 'Reset', 'bg': 'blue', 'fg': 'white', 'command': cancel, 'x': 150, 'y': 160}]
    botones = design.crear_botones(canvas, botones_config)
    boton_accept = botones[0]
    boton_cancel = botones[1]


def rescale(self,matrix):
        self.matrix = (((matrix - np.min(matrix))/(np.max(matrix) - np.min(matrix)))*255)
        return self.matrix     

