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
import general_configuration

def crear_desplegable_filtro (self):
        ancho =  self.ancho
        altura = self.altura
        txt= design.crear_label(self.main_frame, "Select Filter", "white", ("Calibri", 12), "black", 20, 2*altura/3+80)
        opciones = ["Circular filter", "Rectangular filter", "Manual rectangular filter"]
    
        self.desplegable = ttk.Combobox(self.main_frame, values=opciones, state="readonly")
        self.desplegable.place(x=ancho/13, y=2*altura/3+80, width=200)

        botones_config = [
            {'text': 'Settings', 'fg': 'black', 'bg': '#B3B5BB', 'command': lambda: funcion_del_boton(self, self.desplegable.get()), 'x': ancho/6 + 20, 'y': 2*altura/3+120},
            {'text': 'Display', 'fg': 'black', 'bg': '#B3B5BB', 'command': lambda: display(self), 'x': 30, 'y': 2*altura/3+120}
        ]

        botones = []
        for config in botones_config:
            button = tk.Button(self.main_frame, text=config['text'], command=config['command'])
            button.place(x=config['x'], y=config['y'])  # Posición
            botones.append(button)

        boton_settings = botones[0]
        boton_display = botones[1]

def display_images(self, output):
    ancho =  self.ancho
    altura = self.altura
    inten = utilities.amplitude(output, True)
    inten = general_configuration.rescale(self,inten)
    self.inten = Image.fromarray(inten)
    self.inten = self.inten.resize((200, 200), Image.LANCZOS)
    self.inten = ImageTk.PhotoImage(self.inten)
    self.label_inten = Label(self.main_frame, image=self.inten)
    self.label_inten.place(x=ancho/4+50, y=400)

    phase = utilities.phase(output)
    phase = general_configuration.rescale(self,phase)
    self.Phase = Image.fromarray(phase)
    self.Phase = self.Phase.resize((200, 200), Image.LANCZOS)
    self.Phase = ImageTk.PhotoImage(self.Phase)
    self.label_Phase = Label(self.main_frame, image=self.Phase)
    self.label_Phase.place(x=ancho/2+150, y=400)


def log_scalling (self,flag,variable):
    ancho =  self.ancho
    altura = self.altura
    if flag ==0:
        self.transf_fourier = utilities.FT(self.hologram)
        self.FT_intensity = utilities.intensity(self.transf_fourier,variable)
        self.img_FT = Image.fromarray(self.FT_intensity)
        self.img_FT = self.img_FT.resize((200,200),Image.LANCZOS)
        self.img_FT = ImageTk.PhotoImage(self.img_FT)
        self.label_FT = Label(self.main_frame, image=self.img_FT)
        self.label_FT.place(x=ancho/2+150, y=50)

    else:
        output = self.output
        inten = utilities.amplitude(output,variable)
        inten = general_configuration.rescale(self,inten)
        self.inten = inten
        self.inten = Image.fromarray(self.inten)
        self.inten = self.inten.resize((200,200),Image.LANCZOS)
        self.inten = ImageTk.PhotoImage(self.inten)
        self.label_inten = Label(self.main_frame, image=self.inten)
        self.label_inten.place(x=ancho/4+50, y=400)

def assign_args(self, list_args: list = None, list_names: list = None, unit: str = None):
        ancho =  self.ancho
        altura = self.altura

        if list_args is None:
            list_args = [self.arg1, self.arg2, self.arg3, self.arg4]
        if list_names is None:
            list_names = ["Distance", "Wavelength", "Pitch x", "Pitch y"]
        if unit is not None:
            list_names = [f"{name} ({unit})" for name in list_names]

        y = 0
        for arg, name in zip(list_args, list_names):
            arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
            arg_entry.place(x=ancho/12+17, y=altura/3+60+y)
            text_refer = tk.Label(self.main_frame, text=name, bg="white")
            text_refer.place(x=ancho/55, y=altura/3+60+y)
            y += 20

def agregar_imagen(self):
        ancho =  self.ancho
        altura = self.altura
        txt = design.crear_label(self.main_frame, "File", "white", ("Calibri", 12), "black", ancho/60, 46)
        self.cuadro_ruta = Entry(self.main_frame, width=40, bd=1,relief="solid")
        self.cuadro_ruta.place(x=ancho/24,y=50)
        boton_config = {'text': '...', 'command': lambda: seleccionar_imagen(self, cuadro_ruta=self.cuadro_ruta), 'x': ancho/5+33, 'y': 45}

        boton = tk.Button(self.main_frame, text=boton_config['text'], command=boton_config['command'])
        boton.place(x=boton_config['x'], y=boton_config['y'])  # Posición

        boton = boton 

def seleccionar_imagen(self,cuadro_ruta):
        global img
        self.image_main = filedialog.askopenfilename()
        cuadro_ruta.delete(0, "end")
        cuadro_ruta.insert(0, self.image_main)
        self.image_main = os.path.abspath(self.image_main)
        img = Image.open(self.image_main)
        print(type(self.image_main))
        process_numericalPropagation(self)
        return img

def process_numericalPropagation(self):
        ancho =  self.ancho
        altura = self.altura
        if self.bandera_holo== 0:
            self.hologram = utilities.imageRead(self.image_main)
            self.hologram1 = self.hologram.resize((400,400),Image.LANCZOS)
            self.img_hologram = ImageTk.PhotoImage(self.hologram1)
            self.label_hologram = Label(self.main_frame, image=self.img_hologram)
            self.label_hologram.place(x=ancho/4+50, y=50)
        elif self.bandera_holo == 1:
            self.transf_fourier = utilities.FT(self.hologram)
            self.FT_intensity = utilities.intensity(self.transf_fourier,True)
            self.img_FT = Image.fromarray(self.FT_intensity)
            self.img_FT = self.img_FT.resize((400,400),Image.LANCZOS)
            self.img_FT = ImageTk.PhotoImage(self.img_FT)
            self.label_FT = Label(self.main_frame, image=self.img_FT)
            self.label_FT.place(x=ancho/4+50, y=50)

def funcion_del_boton(self, opcion):
    self.rad = None
    self.Cx = None
    self.Cy = None
    self.X1 = None
    self.X2 = None
    self.Y1 = None
    self.Y2 = None

    ventana = tk.Toplevel(self.main_frame)
    ventana.geometry("600x250")
    ventana.configure(bg="white")

    canvas = tk.Canvas(ventana, bg="white", width=600, height=500)
    canvas.place(x=0, y=0)

    def accept():
        if opcion == "Circular filter":
            funcion_filtro(self, filter="Circular filter")
            self.Filtro = "Circular filter"
            self.rad = self.arg5.get()
            self.Cx = self.arg6.get()
            self.Cy = self.arg7.get()
        elif opcion == "Rectangular filter":
            funcion_filtro(self, filter="Rectangular filter")
            self.Filtro = "Rectangular filter"
            self.X1 = self.arg8.get()
            self.X2 = self.arg9.get()
            self.Y1 = self.arg10.get()
            self.Y2 = self.arg11.get()
        elif opcion == "Manual rectangular filter":
            ventana.destroy()
            self.x1, self.x2, self.y1, self.y2 = general_configuration.sfmr(img)
            funcion_filtro(self, filter="Manual rectangular filter")
            self.Filtro = "Manual rectangular filter"
    
        ventana.destroy()

    def reset():
        for entry in list_entries:
            entry.delete(0, tk.END)

    canvas.create_rectangle(10, 25, 280, 190, fill='white', outline='blue', width=2)
    #rectangulos = design.crear_rectangulos(canvas, [{'coordenadas': (40, 10, 250, 45), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}])
    
    #rectangulos_rectangular = design.crear_rectangulos(canvas, [{'coordenadas': (310, 10, 560, 45), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}])
    txt = design.crear_label(canvas, text="Circular Filter", bg="white", font=("Calibri", 14), fg="blue", x=80, y=13)
    list_names = ["Radius:", "Cent X:", "Cent Y:"]
    list_entries = []

    for i in range(len(list_names)):
        lbl = tk.Label(canvas, text=list_names[i], bg="white")
        lbl.place(x=60, y=60+i*30)
        ent = tk.Entry(canvas, relief="solid")
        ent.place(x=130, y=60+i*30)
        list_entries.append(ent)

    self.arg5 = list_entries[0]
    self.arg6 = list_entries[1]
    self.arg7 = list_entries[2]

    canvas.create_rectangle(290, 25, 590, 190, fill='white', outline='blue', width=2)
    #rectangulos_rect = design.crear_rectangulos(canvas, [{'coordenadas': (310, 10, 560, 45), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}])
    txt_rect = design.crear_label(canvas, "Rectangular Filter", "white", ("Calibri", 14), "blue", 370, 13)
    list_names_rect = ["X1:", "X2:", "Y1:", "Y2:"]
    list_entries_rect = []

    for i in range(len(list_names_rect)):
        lbl = tk.Label(canvas, text=list_names_rect[i], bg="white")
        lbl.place(x=350, y=60+i*30)
        ent = tk.Entry(canvas, relief="solid")
        ent.place(x=400, y=60+i*30)
        list_entries_rect.append(ent)

    self.arg8 = list_entries_rect[0] 
    self.arg9 = list_entries_rect[1]
    self.arg10 = list_entries_rect[2]
    self.arg11 = list_entries_rect[3]

    if opcion == "Circular filter":
        for entry in list_entries_rect:
            entry.config(state="disabled")
        for entry in list_entries:
            entry.config(state="normal")
    elif opcion == "Rectangular filter":
        for entry in list_entries:
            entry.config(state="disabled")
        for entry in list_entries_rect:
            entry.config(state="normal")

    botones_config = [
        {'text': 'Accept', 'command': accept, 'x': 110, 'y': 200},
        {'text': 'Reset', 'command': reset, 'x': 430, 'y': 200}
    ]

    botones = []

    for config in botones_config:
        button = tk.Button(canvas, text=config['text'], command=config['command'])
        button.place(x=config['x'], y=config['y'])
        botones.append(button)

    boton_accept = botones[0]
    boton_reset = botones[1]



def funcion_filtro(self,filter): 
        
        if type(self.image_main) == str:
            hologram = utilities.imageRead(self.image_main)
            if filter == "Circular filter" :
                self.filter = utilities.sfc(self.hologram,int(self.arg5.get()),int(self.arg6.get()),int(self.arg7.get()),False)
            elif filter == "Rectangular filter" :
                self.filter = utilities.sfr(self.hologram, int(self.arg8.get()), int(self.arg9.get()), int(self.arg10.get()), int(self.arg11.get()), False)
            else :
                self.filter = utilities.sfr(self.hologram, self.x1,self.x2, self.y1, self.y2, False)

def reset_buttom(self):
    self.cuadro_ruta.delete(0, tk.END)
    self.desplegable.set("")
    self.label_hologram.destroy()
    self.label_hologram = None
    self.label_FT.destroy()
    self.label_FT = None
    self.label_Phase.destroy()
    self.label_Phase = None
    self.label_inten.destroy() 
    self.label_inten = None

def Param_Blus(self, list_args: list = None, list_names: list = None, unit: str = None):  
        if self.V1.get() == 5:
            
            if self.y == 0:
                self.y = 1 
                ancho =  self.ancho
                altura = self.altura
                if list_args is None:
                    list_args= [self.arg12, self.arg13]
                if list_names is None:
                    list_names = ["Pitch x out", "Pitch y out"]
                if unit is not None:
                    list_names = [f"{name} ({unit})" for name in list_names]

                y = 0
                if self.x == 0 :
                    self.widget_refs = []
                    self.x = 1

                for arg, name in zip (list_args,list_names):
                    arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
                    arg_entry.place(x=ancho/12+17, y=altura/3+150+y)
                    text_refer = tk.Label(self.main_frame, text=name, bg="white")
                    text_refer.place(x=ancho/55, y=altura/3+150+y)
                    y += 20
                    self.widget_refs.append(arg_entry)
                    self.widget_refs.append(text_refer)
            else:
                ...
            if self.auxiliar_unidades == 1: 
                ...
        else:
            self.y = 0
            for widget in self.widget_refs:
                widget.place_forget()
                widget.destroy()
            self.widget_refs = []


def display(self):
        filter = self.Filtro
        print(filter)
        if type(self.image_main) == str:
                self.hologram = utilities.imageRead(self.image_main)
        if filter == "Circular filter" :
                self.filter = utilities.sfc(self.hologram,int(self.rad),int(self.Cx),int(self.Cy),True)
        elif filter == "Rectangular filter" :
                self.filter = utilities.sfr(self.hologram, int(self.X1), int(self.X2), int(self.Y1), int(self.Y2), True)
        elif filter == "Manual rectangular filter":
            self.filter = utilities.sfr(self.hologram, self.x1,self.x2, self.y1, self.y2, True)

def create_radio_buttons(self):
        self.V1= IntVar()
        self.V1.set(2)

        self.label_FT = None
        self.label_inten = None
        print(self.V1)
        self.y = 0
        self.z = 0
        self.x = 0
        ancho =  self.ancho
        altura = self.altura
        
        text_values = ["Angular spectrum", "Fresnel transform", "Fresnel-Bluestein"]
        values = [0, 1, 5]

        radio_buttons = design.crear_radio_buttons(self.main_frame, text_values, self.V1, values, "white", lambda: Param_Blus(self, list_names=None, list_args=None,unit= self.variable), ancho/60, altura/5)

        # configuracion = [
        #     {'text': 'Logarithmic Scaling', 'command': lambda: log_Ft(), 'x': 12 * ancho / 20, 'y': altura / 2 - 50}
        # ]

        # botones = []
        # for config in configuracion:
        #     button = tk.Button(self.main_frame, text=config['text'], command=config['command'])
        #     button.place(x=config['x'], y=config['y'])  # Posición
        #     botones.append(button)

        # boton_logarithmic = botones[0]

        def log_Ft():
            boton_volver = tk.Button(self.main_frame, text= "←",fg="black", bg="#B3B5BB", padx=2, pady=2, bd=1, relief='solid',command= lambda: volver_FT())
            boton_volver.place(x= 12*ancho/18+28,y = altura/2-50)

            def volver_FT():
                log_scalling(self,0,True)
                self.main_frame.after(100, hide_button)
   
            def hide_button():
                boton_volver.place_forget()
            log_scalling(self,0,False)
             
        # botones_config = [
        #     {'text': 'Zoom', 'command': lambda: general_configuration.zoom(self), 'x': 12 * ancho/20 + 200, 'y': altura/2 - 50},
        #     {'text': 'Unwrapping', 'command': None, 'x': 12 * ancho/20 + 100, 'y': altura - 35},
        #     {'text': 'Intensity', 'command': lambda: log_Ampl(), 'x': 1/4 * ancho + 150, 'y': altura - 35}
        # ]

        # botones = []
        # for config in botones_config:
        #     button = tk.Button(self.main_frame, text=config['text'], command=config['command'])
        #     button.place(x=config['x'], y=config['y'])  # Posición
        #     botones.append(button)

        # boton1 = botones[0]
        # boton2 = botones[1]
        # boton3 = botones[2]

        def log_Ampl():

            boton_volver_amp = tk.Button(self.main_frame, text= "←",fg="black", bg="#B3B5BB", padx=2, pady=2, bd=1, relief='solid',command= lambda: volver_amp())
            boton_volver_amp.place(x=1/2 * ancho-70, y=altura - 35)

            def volver_amp():
                log_scalling(self,1,True)
                self.main_frame.after(100, hide_button)
   
            def hide_button():
                boton_volver_amp.place_forget()
            
            log_scalling(self,1,False)



