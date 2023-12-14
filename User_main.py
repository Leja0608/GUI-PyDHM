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

class User_Interface():
    
    def __init__(self, master):
        self.Posicion_Img  = 0
        self.output_compe = 0 
        self.master = master
        master.state("zoomed")
        master.title("User_pyDHM")
        self.auxiliar_unidades = 0
        self.general_aux= IntVar()
        self.label_title =  IntVar()
        self.label_title.set(3)
        self.variable = None 

        self.ruta_0 = self.ruta_1 = self.ruta_2 = self.ruta_3 = self.ruta_4 = self.ruta_5 = None
        
        args = ['arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'arg7', 'arg8', 'arg9', 'arg10', 'arg11', 'arg12', 'arg13']
        self.args = [tk.StringVar() for _ in range(len(args))]
        for i, arg in enumerate(args):
            setattr(self, arg, self.args[i])

        extra_args = ['image_main', 'cuadro_ruta', 'argc1', 'argc2', 'argc3', 'argc4', 'argc5', 'argc6', 'argc7', 'argc8', 'argc9']
        self.extra_args = [tk.StringVar() for _ in range(len(extra_args))]
        for i, arg in enumerate(extra_args):
            setattr(self, arg, self.extra_args[i])
        
        extra_args = ['arg1_shift', 'arg2_shift','arg3_shift','arg4_shift']
        self.extra_args = [tk.StringVar() for _ in range(len(extra_args))]
        for i, arg in enumerate(extra_args):
            setattr(self, arg, self.extra_args[i])

        self.label()
    
        self.title_frame = tk.Frame(master, bg="white")
        self.title_frame.pack(side="top", fill="x")

        botones_config = [{'text': "Numerical propagation", 'command': lambda: self.Numerical_propagation("white")},
                          {'text': "Phase compensation", 'command': lambda: self.phase_comp("white")},
                          {'text': "Phase-shifting", 'command': lambda: self.Phase_shifting("white")},
                          {'text': "Settings", 'command': lambda: general_configuration.open_settings(self)}]
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
        
        self.general_aux.set(0)
        self.label_title.set(0)
        

        general_configuration.clear_widget(self)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.main_frame.configure(bg=color)
        self.inten = None
        self.Phase = None
        self.label_inten = None
        self.label_Phase = None
        self.label()
        def reset_func():
            for child in self.main_frame.winfo_children():
                if isinstance(child, ttk.Entry):
                    child.delete(0, tk.END)
            process_numericalprogation.reset_buttom(self)
            
        def propagate_func():
            
            if self.V1.get() == 0:
                self.output = numericalPropagation.angularSpectrum(self.filter,float(self.arg1.get()),float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()))
                process_numericalprogation.display_images(self,self.output)

            elif self.V1.get() == 1:
                self.output = numericalPropagation.fresnel(self.filter,float(self.arg1.get()),float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()))
                process_numericalprogation.display_images(self,self.output)

            elif self.V1.get() == 5:
                self.output = numericalPropagation.bluestein(self.filter,float(self.arg1.get()),float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()),float(self.arg12.get()),float(self.arg13.get()))
                process_numericalprogation.display_images(self,self.output)

        canvas = tk.Canvas(self.main_frame, bg=color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        parametros = [{'coordenadas':(10,altura/40, 1/4 * ancho-10, altura/8 ),'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, 5, ancho/6, altura/18), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (10, altura/6, 1/4 * ancho-10, altura/3), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, altura/7, ancho/6, altura/5-5), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}, 
                      {'coordenadas': (10, altura/40, 1/4 * ancho-10, altura/8), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20,5, ancho/6, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas':(10, altura/3+25, 1/4 * ancho-10, 2/3 * altura -10),'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20,altura/3+10, ancho/6, altura/2-67), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas':(10, 2*altura/3+25, 1/4 * ancho-10, altura-100),'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20,2*altura/3+10, ancho/6, 2*altura/3 +45), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+25,10, 1/4 * ancho+425,altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40,2, ancho/4+300, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas': (1/4*ancho+25,altura/2+30, 1/4 * ancho+425,altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40,altura/2+20, ancho/4+300, altura/2+60 ),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+450,10, 1/4 * ancho+850,altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (12*ancho/20-15,2, 17*ancho/20-90, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas': (1/4*ancho+450,altura/2+30, 1/4 * ancho+850,altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+460,altura/2+20, 17*ancho/20-90, altura/2+60),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (18*ancho/20-22,10, ancho-20,altura/3), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (18*ancho/20-12,2, ancho - 28, altura/18 ),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas':(10, altura-90, 1/4 * ancho-10, altura-10),'fill': 'white', 'outline': 'blue', 'width': 2}]
        rectangulos = design.crear_rectangulos(canvas, parametros)

        txt = design.crear_label(self.main_frame, text="Hologram",bg="#326CF7", font=("Calibri", 14),fg="white",x=6*ancho/18,y=6)
        txt = design.crear_label(self.main_frame, text="Amplitude",bg="#326CF7", font=("Calibri", 14),fg="white",x=6*ancho/18,y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Fourier Transform",bg="#326CF7", font=("Calibri", 14),fg="white",x=12*ancho/20+40,y=6)
        txt = design.crear_label (self.main_frame, text="Phase",bg="#326CF7", font=("Calibri", 14),fg="white",x=12*ancho/20+50,y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Actions",bg="#326CF7", font=("Calibri", 14),fg="white",x=18*ancho/20+14,y=6)


        txt = design.crear_label(self.main_frame, text="From:", bg="white", font=("Arial", 12), fg="black", x=30, y=altura-80)
        txt = design.crear_label(self.main_frame, text="To:", bg="white", font=("Arial", 12), fg="black", x=180, y=altura-80)
        txt = design.crear_label(self.main_frame, text="Step:", bg="white", font=("Arial", 12), fg="black", x=80, y=altura-50)

        process_numericalprogation.assign_args(self,None,None,None)
        process_numericalprogation.create_radio_buttons(self)
        process_numericalprogation.crear_desplegable_filtro(self)
        process_numericalprogation.agregar_imagen(self)
        #general_configuration.Logos(self)
        self.propagation_AS()     

        button2 = tk.Button(self.main_frame, text="Reset", command=reset_func)
        button2.configure(width=16, height=1)
        button2.place(x=18*ancho/20-15, y=altura/5-30)

        button3 = tk.Button(self.main_frame, text="Save", command=...)  
        button3.configure(width=16, height=1)
        button3.place(x=18*ancho/20-15, y=altura/5+20)

        button1 = tk.Button(self.main_frame, text="Propagate", command=propagate_func)
        button1.configure(width=16, height=1)
        button1.place(x=18*ancho/20-15, y=altura/8-30)
    
    def propagation_AS(self):

        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()

        label_from = design.crear_label(self.main_frame, text="From:", bg="white", font=("Arial", 12), fg="black", x=20, y=altura-80)
        label_to = design.crear_label(self.main_frame, text="To:", bg="white", font=("Arial", 12), fg="black", x=180, y=altura-80)
        label_step = design.crear_label(self.main_frame, text="Step:", bg="white", font=("Arial", 12), fg="black", x=20, y=altura-50)  

        entry_from = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_from.place(x=70, y=altura-80)
        entry_to = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_to.place(x=220, y=altura-80)
        entry_step = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_step.place(x=70, y=altura-50)

        button1 = tk.Button(self.main_frame, text="Calculate", command=lambda: self.calculate_button_clicked_AS(entry_from, entry_to, entry_step))
        button1.place(x=250, y=altura-50)  
        self.button1 = button1

    def calculate_button_clicked_AS(self, entry_from, entry_to, entry_step):
        global from_value
        from_value = int(entry_from.get())
        to_value = int(entry_to.get())
        global step_value 
        step_value = int(entry_step.get())
        

        num_iterations = abs((to_value - from_value) // step_value) + 1
     
        confirm_window = Toplevel()
        confirm_window.title("Confirmación")
        confirm_window.geometry("220x120") 
        confirm_window.configure(bg="white") 

        message = f"You are going to generate {num_iterations} results for propagation. Are you sure?"
        
        message_label = Label(confirm_window, text=message, wraplength=200, bg="white")
        message_label.pack(pady=10)
       
        def continue_propagation(self):
            
            confirm_window.destroy()
            results_window = Toplevel()
            results_window.title("Results")
            results_window.geometry("1000x500")
            results_window.configure(bg="white")

            canvas = tk.Canvas(results_window, bg="white", highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            parametros_rectangulos = [
            {'coordenadas': (10, 30, 490, 430), 'fill': 'white', 'outline': 'blue', 'width': 2},
            {'coordenadas': (20, 20, 300, 60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
            {'coordenadas': (510, 30, 990, 430), 'fill': 'white', 'outline': 'blue', 'width': 2},
            {'coordenadas': (520, 20, 820, 60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
            ]

            rectangulos = design.crear_rectangulos(canvas, parametros_rectangulos)
            amplitude =[]
            phase = []
            for i in range (from_value,(to_value+step_value),step_value):
                if self.V1.get()  == '0':
                    propagate = numericalPropagation.angularSpectrum(self.output,float(i),float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()))
                    [x,y] = process_phaseCompensation.display_images_propagate_for(self,propagate, results_window) 
                    amplitude.append(x)
                    phase.append(y)
                elif self.V1.get()  == '1':
                    propagate = numericalPropagation.angularSpectrum(self.output,float(i), float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()))
                    [x,y] =process_phaseCompensation.display_images_propagate_for(self,propagate, results_window)     
                    amplitude.append(x)
                    phase.append(y)
                elif self.V1.get()  == '5':
                    propagate = numericalPropagation.angularSpectrum(self.output,float(i),float(self.arg2.get()),float(self.arg3.get()),float(self.arg4.get()))
                    [x,y] =process_phaseCompensation.display_images_propagate_for(self,propagate, results_window)  
                    amplitude.append(x)
                    phase.append(y)
            print(len(amplitude))  
            self.aux1 = len(amplitude)
            self.Posicion_Img =0
            def aumentar (self):
                x = amplitude[self.Posicion_Img]
                y = phase[self.Posicion_Img]
                process_phaseCompensation.image_propagate(self,x,y,results_window)
                self.Posicion_Img  = self.Posicion_Img  + 1 
                if self.Posicion_Img  >= self.aux1:
                    self.Posicion_Img  = self.aux1- 1
            def disminuir (self):  
                x = amplitude[self.Posicion_Img]
                y = phase[self.Posicion_Img]      
                process_phaseCompensation.image_propagate(self,x,y,results_window)
                self.Posicion_Img  = self.Posicion_Img  - 1 
                if self.Posicion_Img  <= 0:
                    self.Posicion_Img  = 0
                
            button_1 = Button(canvas, text="Next", command=lambda:aumentar(self))
            button_1.place(x=200,y=450)
       
            button_2 = Button(canvas, text="Previous", command= lambda: disminuir(self))
            button_2.place(x=700,y=450)

                    
        def cancel_propagation():
            entry_from.delete(0, 'end') 
            entry_to.delete(0, 'end')    
            entry_step.delete(0, 'end') 
            confirm_window.destroy()

        continue_button = Button(confirm_window, text="Yes,continue", command=lambda: continue_propagation(self))
        continue_button.pack(side="left", padx=10)
       
        cancel_button = Button(confirm_window, text="Cancel", command=cancel_propagation)
        cancel_button.pack(side="right", padx=10)
        confirm_window.mainloop()

    def phase_comp (self,color):
        self.general_aux.set(1)

        self.label_title.set(1)
        
        general_configuration.clear_widget(self)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.main_frame.configure(bg=color) 

        canvas = tk.Canvas(self.main_frame, bg=color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.label()
        parametros_rectangulos = [{'coordenadas': (10, altura/40, 1/4 * ancho-10, altura/8), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, 5, ancho/6, altura/18), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (10, altura/6, 1/4 * ancho-10, altura/3+50), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, altura/7, ancho/6, altura/5-5), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (10, altura/3+75, 1/4 * ancho-10, 2/3 * altura+80), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, altura/3+60, ancho/6, altura/2-17), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (10, 2*altura/3+105, 1/4 * ancho-10, altura-15), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, 2*altura/3+90, ancho/6, 2*altura/3 +123), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (1/4*ancho+25, 10, 1/4 * ancho+425, altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40, 2, ancho/4+300, altura/18), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (1/4*ancho+25, altura/2+30, 1/4 * ancho+425, altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40, altura/2+20, ancho/4+300, altura/2+60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (1/4*ancho+450, 10, 1/4 * ancho+850, altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (12*ancho/20-15, 2, 17*ancho/20-90, altura/18), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (1/4*ancho+450, altura/2+30, 1/4 * ancho+850, altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+460, altura/2+20, 17*ancho/20-90, altura/2+60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (1/4*ancho+450,altura/2+30, 1/4 * ancho+850,altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+460,altura/2+20, 17*ancho/20-90, altura/2+60),'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                                  {'coordenadas': (18*ancho/20-22,10, ancho-20,altura/3), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (18*ancho/20-12,2, ancho - 28, altura/18 ),'fill': '#326CF7', 'outline': 'blue', 'width': 2}]

        rectangulos = design.crear_rectangulos(canvas, parametros_rectangulos)

        txt = design.crear_label(self.main_frame, text="Hologram", bg="#326CF7", font=("Calibri", 14), fg="white", x=6*ancho/18, y=6)
        txt = design.crear_label(self.main_frame, text="Amplitude", bg="#326CF7", font=("Calibri", 14), fg="white", x=6*ancho/18, y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Fourier Transform", bg="#326CF7", font=("Calibri", 14), fg="white", x=12*ancho/20+40, y=6)
        txt = design.crear_label(self.main_frame, text="Phase", bg="#326CF7", font=("Calibri", 14), fg="white", x=12*ancho/20+50, y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Propagation", bg="#326CF7", font=("Calibri", 14), fg="white", x=60, y=altura-127)
        txt = design.crear_label(self.main_frame, text="From:", bg="white", font=("Arial", 12), fg="black", x=30, y=altura-80)
        txt = design.crear_label(self.main_frame, text="To:", bg="white", font=("Arial", 12), fg="black", x=180, y=altura-80)
        txt = design.crear_label(self.main_frame, text="Step:", bg="white", font=("Arial", 12), fg="black", x=80, y=altura-50)


        def reset_func():
            ...
        def propagate_func():
            if self.VCom.get()  == 0:
                self.output_compe = phaseCompensation.FRS(self.hologram,bool(self.argc1.get()), float(self.argc2.get()), float(self.argc3.get()),float(self.argc4.get()), float(self.argc5.get()), int(self.argc6.get()))
                process_phaseCompensation.display_images(self,self.output_compe)    
            elif self.VCom.get()  == 1:
                self.output_compe= phaseCompensation.ERS(self.hologram,bool(self.argc1.get()), float(self.argc2.get()), float(self.argc3.get()),float(self.argc4.get()), float(self.argc5.get()), float(self.argc6.get()))
                process_phaseCompensation.display_images(self,self.output_compe)    
            elif self.VCom.get()  == 2:
                self.output_compe= phaseCompensation.CFS(self.hologram,float(self.argc1.get()), float(self.argc2.get()), float(self.argc3.get()))
                process_phaseCompensation.display_images(self,self.output_compe)  
            elif self.VCom.get()  == 3:
                ...
                #not yet
        

        txt = design.crear_label(self.main_frame, text="Actions",bg="#326CF7", font=("Calibri", 14),fg="white",x=18*ancho/20+14,y=6)

        button2 = tk.Button(self.main_frame, text="Reset", command=reset_func)
        button2.configure(width=16, height=1)
        button2.place(x=18*ancho/20-15, y=altura/5-30)

        button3 = tk.Button(self.main_frame, text="Save", command=...)  
        button3.configure(width=16, height=1)
        button3.place(x=18*ancho/20-15, y=altura/5+20)

        button1 = tk.Button(self.main_frame, text="Propagate", command=propagate_func)
        button1.configure(width=16, height=1)
        button1.place(x=18*ancho/20-15, y=altura/8-30)

        process_phaseCompensation.agregar_imagen(self)
        #general_configuration.Logos(self)
        self.create_rad_comp()
        self.parametros_comp(list_args = None, list_names = None, unit = self.variable)
        self.propagation()
        

    def create_rad_comp(self):
        self.VCom = IntVar()
        self.VCom.set(6)
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()

        text_values = ["Full ROI", "Efficient ROI", "Cost Function", "Compensation no-telecentric"]
        values = [0, 1, 2, 3, 6]

        radio_buttons = design.crear_radio_buttons(self.main_frame, text_values, self.VCom, values, "white", self.parametros_comp, ancho/60, altura/5)

        txt = Label(self.main_frame, text="Compensation Method",bg="#326CF7", font=("Calibri", 14),fg="white")
        txt.place(x=ancho/32-10,y=altura/7+2)

    def parametros_comp(self, list_args: list = None, list_names: list = None, unit: str = None):
        
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        
        txt = Label(self.main_frame, text="Parameters", bg="#326CF7", font=("Calibri", 14), fg="white")
        txt.place(x=60, y=altura/3+63)
        
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

    def propagation(self):

        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()

        label_from = design.crear_label(self.main_frame, text="From:", bg="white", font=("Arial", 12), fg="black", x=20, y=altura-80)
        label_to = design.crear_label(self.main_frame, text="To:", bg="white", font=("Arial", 12), fg="black", x=180, y=altura-80)
        label_step = design.crear_label(self.main_frame, text="Step:", bg="white", font=("Arial", 12), fg="black", x=20, y=altura-50)  

        entry_from = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_from.place(x=70, y=altura-80)
        entry_to = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_to.place(x=220, y=altura-80)
        entry_step = Entry(self.main_frame, width=15, bd=1, relief="solid")
        entry_step.place(x=70, y=altura-50)

        button1 = tk.Button(self.main_frame, text="Calculate", command=lambda: self.calculate_button_clicked_AS(entry_from, entry_to, entry_step))
        button1.place(x=250, y=altura-50)  
        self.button1 = button1

    def calculate_button_clicked(self, entry_from, entry_to, entry_step):
        global from_value
        from_value = int(entry_from.get())
        to_value = int(entry_to.get())
        global step_value 
        step_value = int(entry_step.get())
        

        num_iterations = abs((to_value - from_value) // step_value) + 1
     
        confirm_window = Toplevel()
        confirm_window.title("Confirmación")
        confirm_window.geometry("220x120") 
        confirm_window.configure(bg="white") 

        message = f"You are going to generate {num_iterations} results for propagation. Are you sure?"
        
        message_label = Label(confirm_window, text=message, wraplength=200, bg="white")
        message_label.pack(pady=10)
       
        def continue_propagation(self):
            
            confirm_window.destroy()
            results_window = Toplevel()
            results_window.title("Results")
            results_window.geometry("1000x500")
            results_window.configure(bg="white")

            canvas = tk.Canvas(results_window, bg="white", highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            parametros_rectangulos = [
            {'coordenadas': (10, 30, 490, 430), 'fill': 'white', 'outline': 'blue', 'width': 2},
            {'coordenadas': (20, 20, 300, 60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
            {'coordenadas': (510, 30, 990, 430), 'fill': 'white', 'outline': 'blue', 'width': 2},
            {'coordenadas': (520, 20, 820, 60), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
            ]

            rectangulos = design.crear_rectangulos(canvas, parametros_rectangulos)
            amplitude =[]
            phase = []
            for i in range (from_value,(to_value+step_value),step_value):
                
                if self.VCom.get()  == 0:
                    propagate = numericalPropagation.angularSpectrum(self.output_compe,float(i), float(self.argc2.get()),float(self.argc3.get()),float(self.argc4.get()))
                    [x,y] = process_phaseCompensation.display_images_propagate_for(self,propagate, results_window) 
                    amplitude.append(x)
                    phase.append(y)
                elif self.VCom.get()  == 1:
                    propagate = numericalPropagation.angularSpectrum(self.output_compe,float(i), float(self.argc2.get()),float(self.argc3.get()),float(self.argc4.get()))
                    [x,y] =process_phaseCompensation.display_images_propagate_for(self,propagate, results_window)     
                    amplitude.append(x)
                    phase.append(y)
                elif self.VCom.get()  == 2:
                    propagate = numericalPropagation.angularSpectrum(self.output_compe,float(i), float(self.argc1.get()),float(self.argc2.get()),float(self.argc3.get()))
                    [x,y] =process_phaseCompensation.display_images_propagate_for(self,propagate, results_window)  
                    amplitude.append(x)
                    phase.append(y)
                
            self.aux1 = len(amplitude)
        
            def aumentar ():
                x = amplitude[self.Posicion_Img]
                y = phase[self.Posicion_Img]
                process_phaseCompensation.image_propagate(self,x,y,results_window)
                self.Posicion_Img  = self.Posicion_Img  + 1 
                if self.Posicion_Img  >= self.aux1:
                    self.Posicion_Img  = self.aux1- 1
            def disminuir ():  
                x = amplitude[self.Posicion_Img]
                y = phase[self.Posicion_Img]      
                process_phaseCompensation.image_propagate(self,x,y,results_window)
                self.Posicion_Img  = self.Posicion_Img  - 1 
                if self.Posicion_Img  <= 0:
                    self.Posicion_Img  = 0
                
            button_1 = Button(canvas, text="Next", command=lambda:aumentar())
            button_1.place(x=200,y=450)
       
            button_2 = Button(canvas, text="Previous", command= lambda: disminuir())
            button_2.place(x=700,y=450)

                    
        def cancel_propagation():
            entry_from.delete(0, 'end') 
            entry_to.delete(0, 'end')    
            entry_step.delete(0, 'end') 
            confirm_window.destroy()

        continue_button = Button(confirm_window, text="Yes, Continue", command=continue_propagation(self))
        continue_button.pack(side="left", padx=10)
       
        cancel_button = Button(confirm_window, text="Cancel", command=cancel_propagation)
        cancel_button.pack(side="right", padx=10)
        confirm_window.mainloop()

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
        parametros = [{'coordenadas':(10,altura/40, 1/4 * ancho-10, 2*altura/3-200 ),'fill': 'white', 'outline': 'blue', 'width': 2}, 
                      {'coordenadas': (20,5, ancho/6, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas':(10, altura/3+40, 1/4 * ancho-10, 2/3 * altura-100),'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20,altura/3+30, ancho/6, altura/2-45), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas':(10, altura/2+30, 1/4 * ancho-10, 2*altura/3+75),'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20,altura/2+20, ancho/6, 2*altura/3-50), 'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+25,10, 1/4 * ancho+425,altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40,2, ancho/4+300, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas': (1/4*ancho+25,altura/2+30, 1/4 * ancho+425,altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+40,altura/2+20, ancho/4+300, altura/2+60 ),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+450,10, 1/4 * ancho+850,altura/2 -53.5), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (12*ancho/20-15,2, 17*ancho/20-90, altura/18),'fill': '#326CF7', 'outline': 'blue', 'width': 2},
                      {'coordenadas': (1/4*ancho+450,altura/2+30, 1/4 * ancho+850,altura - 40), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (1/4*ancho+460,altura/2+20, 17*ancho/20-90, altura/2+60),'fill': '#326CF7', 'outline': 'blue', 'width': 2},{'coordenadas': (18*ancho/20-22,10, ancho-20,altura/3), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (18*ancho/20-12,2, ancho - 28, altura/18 ),'fill': '#326CF7', 'outline': 'blue', 'width': 2}]
        rectangulos = design.crear_rectangulos(canvas, parametros)

        txt = design.crear_label(self.main_frame, text="Hologram",bg="#326CF7", font=("Calibri", 14),fg="white",x=6*ancho/18,y=6)
        txt = design.crear_label(self.main_frame, text="Amplitude",bg="#326CF7", font=("Calibri", 14),fg="white",x=6*ancho/18,y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Fourier Transform",bg="#326CF7", font=("Calibri", 14),fg="white",x=12*ancho/20+40,y=6)
        txt = design.crear_label (self.main_frame, text="Phase",bg="#326CF7", font=("Calibri", 14),fg="white",x=12*ancho/20+50,y=altura/2+25)
        txt = design.crear_label(self.main_frame, text="Actions",bg="#326CF7", font=("Calibri", 14),fg="white",x=18*ancho/20+14,y=6)

        self.create_rb_phaseshifting()

        def propagation():
            if self.VShif.get() == 0:
                self.output_shif= phaseShifting.PS5(self.holo1,self.holo2,self.holo3,self.holo4,self.holo5)
                process_phaseshifting.display_images(self,self.output_shif)
            elif self.VShif.get() == 1:
                self.output_shif= phaseShifting.PS4(self.holo1,self.holo2,self.holo3,self.holo4)
                process_phaseshifting.display_images(self,self.output_shif)
            elif self.VShif.get() == 2:
                self.output_shif= phaseShifting.PS3(self.holo1,self.holo2,self.holo3)
                process_phaseshifting.display_images(self,self.output_shif)
            elif self.VShif.get() == 3:
                self.output_shif= phaseShifting.SOSR(self.holo1,self.holo2,self.holo3,self.holo4,float(self.arg1_shift.get()),float(self.arg2_shift.get()),float(self.arg3_shift.get()),float(self.arg4_shift.get()),1,4)
                process_phaseshifting.display_images(self,self.output_shif)
            elif self.VShif.get() == 4:
                w = float(self.arg2_shift.get())
                x = float(self.arg3_shift.get())
                y = float(self.arg4_shift.get())
                self.output_shif= phaseShifting.BPS3(self.holo1,self.holo2,self.holo3,w,x,y)
                process_phaseshifting.display_images(self,self.output_shif)
            elif self.VShif.get() == 5:
                self.output_shif= phaseShifting.BPS2(self.holo1,self.holo2,float(self.arg2_shift.get()),float(self.arg3_shift.get()),float(self.arg4_shift.get()))
                process_phaseshifting.display_images(self,self.output_shif)
                

        button2 = tk.Button(self.main_frame, text="Reset", command=...)
        button2.configure(width=16, height=1)
        button2.place(x=18*ancho/20-15, y=altura/5-30)

        button3 = tk.Button(self.main_frame, text="Save", command=...)  
        button3.configure(width=16, height=1)
        button3.place(x=18*ancho/20-15, y=altura/5+20)

        button1 = tk.Button(self.main_frame, text="Propagate", command=propagation)
        button1.configure(width=16, height=1)
        button1.place(x=18*ancho/20-15, y=altura/8-30)

        self.parametros_shifting()
        self.load_imgs_shif()
       
        datos = [{'coordenadas': (10, 2*altura/3+105, 1/4 * ancho-10, altura-15), 'fill': 'white', 'outline': 'blue', 'width': 2},{'coordenadas': (20, 2*altura/3+90, ancho/6, 2*altura/3 +123), 'fill': '#326CF7', 'outline': 'blue', 'width': 2}]
        rectangulos = design.crear_rectangulos(canvas, datos)
        txt = design.crear_label(self.main_frame, text="Propagation", bg="#326CF7", font=("Calibri", 14), fg="white", x=60, y=altura-127)
        self.propagation()

        self.argshif(list_args = None, list_names = None, unit = self.variable)

    def create_rb_phaseshifting(self):
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.VShif = IntVar()
        self.VShif.set(6)

        txt = Label(self.main_frame, text="Shifting Method",bg="#326CF7", font=("Calibri", 14),fg="white")
        txt.place(x=ancho/32,y=6)

        text_values = ["5 Frames", "4 Frames", "3 Frames", "Quadrature Method","Blind 3 Raw Frames", "Blind 2 Raw Frames"]
        values = [0, 1, 2, 3, 4, 5]

        radio_buttons = design.crear_radio_buttons(self.main_frame, text_values, self.VShif, values, "white", lambda: self.parametros_shifting(), ancho/60, 50)

        param_label = tk.Label(self.main_frame, text="Parameters", bg="#326CF7", font=("Calibri", 14),fg="white")
        param_label.place(x=ancho/32, y=350)
        self.entries = []

    def argshif(self, list_args: list = None, list_names: list = None, unit: str = None):   
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        def enable_disable_entries():
            selected_value = self.VShif.get()
            enable_entries = selected_value > 2

            for entry in self.entries:
                entry.config(state='normal' if enable_entries else 'disabled')

        if list_args is None:
            list_args = [self.arg1_shift, self.arg2_shift, self.arg3_shift, self.arg4_shift]
        if list_names is None:
            list_names = ["Upper", "Wavelength", "Pitch x", "Pitch y"]
        if unit is not None:
            list_names = [f"{name} ({unit})" for name in list_names]
        y = 0
        for arg, name in zip(list_args, list_names):
            arg_entry = ttk.Entry(self.main_frame, textvariable=arg)
            arg_entry.place(x=ancho/12+17, y=altura/2+70+y)
            self.entries.append(arg_entry)
            text_refer = tk.Label(self.main_frame, text=name, bg="white")
            text_refer.place(x=ancho/55, y=altura/2+70+y)
            y += 20

       
        self.VShif.trace_add("write", lambda *args: enable_disable_entries())

       
        enable_disable_entries()

    def parametros_shifting(self):
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.cant_img = 0

        txt = Label(self.main_frame, text="Load images", bg="#326CF7", font=("Calibri", 14), fg="white")
        txt.place(x=ancho/32, y=altura/3+32)
        if self.VShif.get() == 0:
            self.cant_img = 5
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc1 = tk.Label(self.main_frame, text="You must upload 5 images", bg="white",font=("Arial", 12))
            txt_opc1.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc1)
        elif self.VShif.get() == 1:
            self.cant_img = 4
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc2 = tk.Label(self.main_frame, text="You must upload 4 images", bg="white",font=("Arial", 12))
            txt_opc2.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc2)
        elif self.VShif.get() == 2:
            self.cant_img = 3
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc3 = tk.Label(self.main_frame, text="You must upload 3 images", bg="white",font=("Arial", 12))
            txt_opc3.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc3)
        elif self.VShif.get() == 3:
            self.cant_img = 4
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc4 = tk.Label(self.main_frame, text="You must upload 4 images", bg="white",font=("Arial", 12))
            txt_opc4.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc4)
        elif self.VShif.get() == 4:
            self.cant_img = 3
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc5 = tk.Label(self.main_frame, text="You must upload 3 images", bg="white",font=("Arial", 12))
            txt_opc5.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc5)
        elif self.VShif.get() == 5:
            self.cant_img = 2
            self.widget_refs = []
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            txt_opc6 = tk.Label(self.main_frame, text="You must upload 2 images", bg="white",font=("Arial", 12))
            txt_opc6.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(txt_opc6)
        else :
            self.widget_refs = []
            self.cant_img = 0
            for i in self.widget_refs:
                i.place_forget()
                i.destroy()
            self.widget_refs = []
            label_instruction = tk.Label(self.main_frame, text="Select a  method \u2191", bg="white",font=("Arial", 14))
            label_instruction.place(x=20, y=2*altura/3-140)
            self.widget_refs.append(label_instruction)

    def load_imgs_shif(self):
        ancho = self.main_frame.winfo_width()
        altura = self.main_frame.winfo_height()
        self.rutas = []
        self.Img_Show =[]
        self.list_FT = []

        def load_extra():
            ventana_extra = tk.Toplevel()
            ventana_extra.title("Load Images")
            ventana_extra.configure(bg="white")

            cuadros_ruta = []

            self.list = []

            def seleccionar_imagen(cuadro_ruta):
                image_path = filedialog.askopenfilename()
                cuadro_ruta.delete(0, "end")
                cuadro_ruta.insert(0, image_path)

            cantidad_imagenes_requeridas = self.cant_img

            for i in range(5):
                label_text = f"Holo {i + 1}"
                label = tk.Label(ventana_extra, text=label_text, font=("Calibri", 12), bg="white")
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

                cuadro_ruta = Entry(ventana_extra, width=30, bd=1, relief="solid")
                cuadro_ruta.grid(row=i, column=1, padx=10, pady=5)
                cuadros_ruta.append(cuadro_ruta)  # Agregar el cuadro de texto a la lista

                boton_seleccionar = tk.Button(ventana_extra, text='...', command=lambda cuadro=cuadro_ruta: seleccionar_imagen(cuadro))
                boton_seleccionar.grid(row=i, column=2, padx=10, pady=5)

                if i >= cantidad_imagenes_requeridas:
                    cuadro_ruta.configure(state="disabled")

            def load_and_close():
                self.aux = 0 
                self.aux1= 0
                #print("Número de cuadros de ruta:", len(cuadros_ruta))
                for i, cuadro_ruta in enumerate(cuadros_ruta):
                    ruta = cuadro_ruta.get()
                    if ruta:
                        self.rutas.append(ruta)

                for i, ruta in enumerate(self.rutas):
                    setattr(self, f"ruta_{i}", ruta)

                for i in range (len(self.rutas)):
                    if i == 0:
                        self.x1 = os.path.abspath(self.ruta_0)
                        self.list.append(self.x1)
                        self.holo1 = utilities.imageRead(self.x1)
                    elif i == 1:
                        self.x2 = os.path.abspath(self.ruta_1)
                        self.list.append(self.x2)
                        self.holo2 = utilities.imageRead(self.x2)
                    elif i == 2:
                        self.x3 = os.path.abspath(self.ruta_2)
                        self.list.append(self.x3)
                        self.holo3 = utilities.imageRead(self.x3)
                    elif i == 3:
                        self.x4 = os.path.abspath(self.ruta_3)
                        self.list.append(self.x4)
                        self.holo4 = utilities.imageRead(self.x4)
                    elif i == 4:
                        self.x5 = os.path.abspath(self.ruta_4)
                        self.list.append(self.x5)
                        self.holo5 = utilities.imageRead(self.x5)

                ventana_extra.destroy()     

                self.image_main = os.path.abspath(self.ruta_0)
                process_phaseshifting.process_phaseshifting(self,path=self.image_main,i=0,m=0)
                self.cuadro_texto_derecha.insert(0,'1')
                self.cuadro_texto_izquierda.insert(0,'1')
            
            boton_load = tk.Button(ventana_extra, text="Load", command=load_and_close, font=("Calibri", 12))
            boton_load.grid(row=5, column=1, padx=10, pady=5, columnspan=2)

        boton_izquierda = tk.Button(self.main_frame, text="←", command= lambda: self.show_holo_down())
        boton_derecha = tk.Button(self.main_frame, text="→", command= lambda: self.show_holo_up())

        boton_izquierda.place(x=ancho/4+22, y=altura/2-50)
        boton_derecha.place(x=ancho/2+62, y=altura/2-50)

        boton_izquierda1 = tk.Button(self.main_frame, text="←", command=lambda: self.show_FT_down())
        boton_derecha1 = tk.Button(self.main_frame, text="→", command=lambda: self.show_FT_up())

        boton_izquierda1.place(x=ancho/2+110, y=altura/2-50)
        boton_derecha1.place(x=3*ancho/4+145, y=altura/2-50)

        self.cuadro_texto_izquierda = tk.Entry(self.main_frame,bd=2)
        self.cuadro_texto_derecha = tk.Entry(self.main_frame,bd=2)

        self.cuadro_texto_izquierda.place(x=ancho/4+182, y=altura/2-50, width=40)
        self.cuadro_texto_derecha.place(x=ancho/2+280, y=altura/2-50, width=40)

        load_images_button = tk.Button(self.main_frame, text="Load Images", command=load_extra, font=("Calibri", 12))
        load_images_button.place(x=ancho/32+180, y=2*altura/3-145)


    def show_holo_up(self):
        self.aux+=1

        if self.aux >= len(self.rutas):
            self.aux = len(self.rutas)-1

        process_phaseshifting.process_phaseshifting(self,path=self.list[self.aux],i=1,m=0)

        self.cuadro_texto_izquierda.delete(0,"end")
        self.cuadro_texto_izquierda.insert(0,self.aux+1)
        

    def show_holo_down(self):
        self.aux-=1

        if self.aux <= 0:
            self.aux = 0

        process_phaseshifting.process_phaseshifting(self,path=self.list[self.aux],i=1,m=0)

        self.cuadro_texto_izquierda.delete(0,"end")
        self.cuadro_texto_izquierda.insert(0,self.aux+1)
    

    def show_FT_up(self):
        self.aux1+=1

        if self.aux1 >= len(self.rutas):
            self.aux1 = len(self.rutas)-1

        process_phaseshifting.process_phaseshifting(self,path=self.list[self.aux1],i=0,m=1)

        self.cuadro_texto_derecha.delete(0,"end")
        self.cuadro_texto_derecha.insert(0,self.aux1+1)
      
        

    def show_FT_down(self):
        self.aux1-=1

        if self.aux1 <= 0:
            self.aux1 = 0

        process_phaseshifting.process_phaseshifting(self,path=self.list[self.aux1],i=0,m=1)

        self.cuadro_texto_derecha.delete(0,"end")
        self.cuadro_texto_derecha.insert(0,self.aux1+1)

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
        
ventana = tk.Tk()
app = User_Interface(master=ventana)
ventana.mainloop()