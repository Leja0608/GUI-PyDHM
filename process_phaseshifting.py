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

def process_phaseshifting(self,path,i,m):
        if m == 0:
            ancho = self.main_frame.winfo_width()
            self.hologram = utilities.imageRead(path)
            self.hologram1 = self.hologram.resize((200,200),Image.LANCZOS)
            self.img_hologram = ImageTk.PhotoImage(self.hologram1)
            self.label_hologram = Label(self.main_frame, image=self.img_hologram)
            self.label_hologram.place(x=ancho/4+50, y=50)
            #self.Img_Show.append(self.hologram1)
        if i == 0:
            ancho = self.main_frame.winfo_width()
            self.hologram = utilities.imageRead(path)
            self.transf_fourier = utilities.FT(self.hologram)
            self.FT_intensity = utilities.intensity(self.transf_fourier,True)
            self.img_FT = Image.fromarray(self.FT_intensity)
            self.img_FT = self.img_FT.resize((200,200),Image.LANCZOS)
            self.img_FT = ImageTk.PhotoImage(self.img_FT)
            self.label_FT = Label(self.main_frame, image=self.img_FT)
            self.label_FT.place(x=ancho/2+150, y=50)
            self.Img_Show.append(self.img_FT)


def display_images(self, output):
    ancho = self.main_frame.winfo_width()
    altura = self.main_frame.winfo_height()
    inten = utilities.amplitude(output, False)
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



        
        

        


