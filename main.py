import tkinter as tk
import pandas as pd
from functions import *
from cargando import *
from validations import *
from tkinter import filedialog
from tkinter import messagebox
import os

CLAVES = "claves.sdf"
RESPUESTAS = "respuestas.sdf"
IDENTIFI= "identifi.sdf"
TEMA = "ABCDPQRS"
DF_CLAVES = pd.DataFrame()
DF_IDENTIFI = pd.DataFrame()
DF_RESPUESTAS = pd.DataFrame()
NAV_BG = 'gray'
BTN_BG = 'gray'
BTN_FG = 'white'
PANEL_BG = 'white'
PANEL_WIDTH = 600
PANEL_HEIGHT = 300

carga = Cargar()

class Navbar(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config(bg=NAV_BG, height=50, width=600)

        self.file_button = tk.Button(self, text='Archivos', bg=BTN_BG, fg=BTN_FG, bd=0, command=self.show_file)
        self.validation_button = tk.Button(self, text='Validar', bg=BTN_BG, fg=BTN_FG, bd=0, command=self.show_validation)
        self.qualify_button = tk.Button(self, text='Calificar', bg=BTN_BG, fg=BTN_FG, bd=0, command=self.show_qualify)
        
        self.file_button.pack(side='left', fill='both', expand=True)
        self.validation_button.pack(side='left', fill='both', expand=True)
        self.qualify_button.pack(side='left', fill='both', expand=True)
        
        self.file_panel = tk.Frame(master)
        self.validation_panel = tk.Frame(master)
        self.qualify_panel = tk.Frame(master)
        
        self.file_panel.config(bg=PANEL_BG, height=PANEL_HEIGHT, width=PANEL_WIDTH)
        self.validation_panel.config(bg=PANEL_BG, height=PANEL_HEIGHT, width=PANEL_WIDTH)
        self.qualify_panel.config(bg=PANEL_BG, height=PANEL_HEIGHT, width=PANEL_WIDTH)
        
        self.path_label = tk.Label(self.qualify_panel, text="")
        self.path_label.grid(row=4, column=1)
        # Widgets Archivos
        
        tk.Button(self.file_panel, text='Subir claves', width=20, height=2, command=self.select_folder_claves).grid(row=0, column=0, padx=(100,50), pady=50)
        tk.Button(self.file_panel, text='Cargar Identificadores', width=20, height=2, command=self.select_folder_identifi).grid(row=1, column=0, padx=(100,50), pady=50)
        tk.Button(self.file_panel, text='Cargar respuestas', width=20, height=2, command=self.select_folder_respuestas).grid(row=2, column=0, padx=(100,50), pady=50)

        self.file_entry1 = tk.Text(self.file_panel, width=45, height=30)
        self.file_entry1.configure(bg="#E6E6FA")
        self.file_entry1.grid(row=0, column=1, rowspan=4, padx=(100,50), pady=50)

        # Widgets Validacion

        tk.Button(self.validation_panel, text='Validar estructura', width=20, height=2, command=self.validate1).grid(row=0, column=0, padx=(100,50), pady=20)
        tk.Button(self.validation_panel, text='Validar codigos duplicados', width=20, height=2, command=self.validate2).grid(row=1, column=0, padx=(100,50), pady=20)
        tk.Button(self.validation_panel, text='Validar duplicados de litos', width=20, height=2, command=self.validate3).grid(row=2, column=0, padx=(100,50), pady=20)
        tk.Button(self.validation_panel, text='Validar carnet postulante', width=20, height=2, command=self.validate4).grid(row=3, column=0, padx=(100,50), pady=20)
        tk.Button(self.validation_panel, text='Validar lito no localizado', width=20, height=2, command=self.validate5).grid(row=4, column=0, padx=(100,50), pady=20)
        
        self.file_entry2 = tk.Text(self.validation_panel, width=45, height=30)
        self.file_entry2.configure(bg="#E6E6FA")
        self.file_entry2.grid(row=0, column=1, rowspan=5, padx=(100,50), pady=50)
        
        # Widgets Calificador

        tk.Button(self.qualify_panel, text='Calificar normal', width=20, height=2).grid(row=0, column=0, padx=(100,50), pady=50)
        tk.Button(self.qualify_panel, text='Calificar anonima', width=20, height=2).grid(row=1, column=0, padx=(100,50), pady=50)
        tk.Button(self.qualify_panel, text='Calificar ambos', width=20, height=2).grid(row=2, column=0, padx=(100,50), pady=50)
        tk.Button(self.qualify_panel, text='Guardar en..', width=20, height=2).grid(row=3, column=0, padx=(100,50), pady=50)

        self.file_entry3 = tk.Text(self.qualify_panel, width=50, height=30)
        self.file_entry3.configure(bg="#E6E6FA")
        self.file_entry3.grid(row=0, column=1, rowspan=4, padx=(100,50), pady=50)

        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()
    
    def select_folder_claves(self):
        global DF_CLAVES
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, CLAVES)
        if ruta_archivo != "":
            # messagebox.showerror("ESTA ES TU RUTA", f"{ruta_archivo}")
            DF_CLAVES = carga.leer_claves(ruta_archivo)
            # self.file_entry1.delete("1.0", "end")
            self.file_entry1.insert("end", f"\nSe cargaron las claves ..")
            return 

    def select_folder_respuestas(self):
        global DF_RESPUESTAS
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, RESPUESTAS)
        if ruta_archivo != "":
            # messagebox.showerror("ESTA ES TU RUTA", f"{ruta_archivo}")
            DF_RESPUESTAS = carga.leer_respuestas(ruta_archivo)
            # self.file_entry1.delete("2.0", "end")
            self.file_entry1.insert("end", f"\nSe cargaron las respuestas ..")

            return 

    def select_folder_identifi(self):
        global DF_IDENTIFI
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, IDENTIFI)
        if ruta_archivo != "":
            DF_IDENTIFI = carga.leer_indentifi(ruta_archivo)
            self.file_entry1.insert("end", f"\nSe cargaron los identificadores ..")
            return

    def show_file(self):
        self.file_panel.pack(side='top', fill='both', expand=True)
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()
        
    def show_validation(self):
        self.file_panel.pack_forget()
        self.qualify_panel.pack_forget()
        self.validation_panel.pack(side='top', fill='both', expand=True)
        
    def show_qualify(self):
        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack(side='top', fill='both', expand=True)

    def validate1(self):
        res = estructure_solution(DF_CLAVES, DF_RESPUESTAS, DF_IDENTIFI, TEMA)
        self.file_entry2.insert("end", f"\n{res}")
        pass
    def validate2(self):
        res = duplicated_code_solution(DF_IDENTIFI)
        self.file_entry2.insert("end", f"\n{res}")

    def validate3(self):
        res = duplicated_litio_solution(DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")
        pass

    def validate4(self):
        res = applicant_card_solution(DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")
        pass

    def validate5(self):
        res = " validate 5 "
        self.file_entry2.insert("end", f"\n{res}")
        pass
root = tk.Tk()
root.title("AdminUnica")
root.geometry("800x600")
navbar = Navbar(root)
navbar.pack(side='top', fill='x')
root.mainloop()
