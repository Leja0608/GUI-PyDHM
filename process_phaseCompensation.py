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

def agregar_imagen(self):
        ancho =  self.ancho
        altura = self.altura
        txt = design.crear_label(self.main_frame, "File", "white", ("Calibri", 12), "black", ancho/60, 35)
        self.cuadro_ruta = Entry(self.main_frame, width=40, bd=1,relief="solid")
        self.cuadro_ruta.place(x=ancho/24,y=40)
        boton_config = {'text': '...', 'command': lambda: seleccionar_imagen(self, cuadro_ruta=self.cuadro_ruta), 'x': ancho/5+33, 'y': 35}

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
        process_phasecompensation(self)
        return img

def process_phasecompensation(self):
        ancho =  self.ancho
        altura = self.altura
        self.hologram = utilities.imageRead(self.image_main)
        self.hologram1 = self.hologram.resize((200,200),Image.LANCZOS)
        self.img_hologram = ImageTk.PhotoImage(self.hologram1)
        self.label_hologram = Label(self.main_frame, image=self.img_hologram)
        self.label_hologram.place(x=ancho/4+50, y=50)
        self.transf_fourier = utilities.FT(self.hologram)
        self.FT_intensity = utilities.intensity(self.transf_fourier,True)
        self.FT_intensity = general_configuration.rescale(self,self.FT_intensity )
        self.img_FT = Image.fromarray(self.FT_intensity)
        self.img_FT = self.img_FT.resize((200,200),Image.LANCZOS)
        self.img_FT = ImageTk.PhotoImage(self.img_FT)
        self.label_FT = Label(self.main_frame, image=self.img_FT)
        self.label_FT.place(x=ancho/2+150, y=50)


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

def display_images_propagate_for(self, output, pantalla):
    
    inten = utilities.amplitude(output, True)
    inten = general_configuration.rescale(self,inten)
    self.inten = Image.fromarray(inten)
    self.inten = self.inten.resize((300, 300), Image.LANCZOS)
    self.inten = ImageTk.PhotoImage(self.inten)
    

    phase = utilities.phase(output)
    phase = general_configuration.rescale(self,phase)
    self.Phase = Image.fromarray(phase)
    self.Phase = self.Phase.resize((300, 300), Image.LANCZOS)
    self.Phase = ImageTk.PhotoImage(self.Phase)
    
    return self.inten, self.Phase

def image_propagate(self,img_amplitude,img_phase,pantalla):
        inten = Label(pantalla, image=img_amplitude)
        inten.place(x=80, y=80)

        Phase = Label(pantalla, image=img_phase)
        Phase.place(x=580, y=80) 
      