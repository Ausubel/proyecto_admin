import tkinter as tk
import pandas as pd
import pyodbc
from functions import *
from cargando import *
from validations import *
from qualify import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import Image, ImageTk

CLAVES = "claves.sdf"
RESPUESTAS = "respuestas.sdf"
IDENTIFI= "identifi.sdf"
TEMA = "ABCDPQRS"
PATRON_CLAVES = 'TRQSP '
PATRON_RESPUESTAS = 'TRQSP *'
DF_CLAVES = pd.DataFrame()
DF_IDENTIFI = pd.DataFrame()
DF_RESPUESTAS = pd.DataFrame()
calificacion_final = pd.DataFrame()
NAV_BG = '#FF010B'
BTN_BG = '#dc3545'
BTN_FG = '#FCF3EA'
PANEL_BG = '#E3882E'
PANEL_WIDTH = 650
PANEL_HEIGHT = 20

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
        
        tk.Button(self.file_panel, text='Subir claves', width=20, height=2, command=self.select_folder_claves).grid(row=0, column=0, padx=(30,30), pady=50)
        tk.Button(self.file_panel, text='Cargar Identificadores', width=20, height=2, command=self.select_folder_identifi).grid(row=1, column=0, padx=(30,30), pady=50)
        tk.Button(self.file_panel, text='Cargar respuestas', width=20, height=2, command=self.select_folder_respuestas).grid(row=2, column=0, padx=(30,30), pady=50)
        tk.Button(self.file_panel, text='Limpiar', width=20, height=2, command=self.clean1).grid(row=3, column=0, padx=(30,30), pady=20)
        
        self.file_entry1 = tk.Text(self.file_panel, width=48, height=25)
        self.file_entry1.configure(bg="#FCF3EA")
        self.file_entry1.grid(row=0, column=1, rowspan=5, padx=(30,30), pady=50)

        # Widgets Validacion

        tk.Button(self.validation_panel, text='Validar estructura', width=20, height=2, command=self.validate1).grid(row=0, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar codigos duplicados', width=20, height=2, command=self.validate2).grid(row=1, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar duplicados de litos', width=20, height=2, command=self.validate3).grid(row=2, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar carnet postulante', width=20, height=2, command=self.validate4).grid(row=3, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar lito no localizado', width=20, height=2, command=self.validate5).grid(row=4, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Limpiar', width=20, height=2, command=self.clean2).grid(row=5, column=0, padx=(30,30), pady=20)

        self.file_entry2 = tk.Text(self.validation_panel, width=48, height=25)
        self.file_entry2.configure(bg="#FCF3EA")
        self.file_entry2.grid(row=0, column=1, rowspan=6, padx=(30,30), pady=50)
        
        # Widgets Calificador

        tk.Button(self.qualify_panel, text='Calificar normal', width=20, height=2, command=self.qualify).grid(row=0, column=0, padx=(30,30), pady=20)
        tk.Button(self.qualify_panel, text='Guardar Resultado', width=20, height=2, command=self.save).grid(row=1, column=0, padx=(30,30), pady=20)
        tk.Button(self.qualify_panel, text='Limpiar', width=20, height=2, command=self.clean3).grid(row=2, column=0, padx=(30,30), pady=20)

        # Panel
        self.file_entry3 = tk.Text(self.qualify_panel, width=48, height=25)
        self.file_entry3.configure(bg="#FCF3EA")
        self.file_entry3.grid(row=0, column=1, rowspan=4, padx=(30,30), pady=50)

        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()
        
        
        # self.show_welcome_message()

    def show_welcome_message(self):
    
        messagebox.showinfo("Bienvenido", "¡Bienvenido a AdminUni!")
        self.show_file()


    def clean1(self):
        self.file_entry1.delete('1.0', tk.END)

    def clean2(self):
        self.file_entry2.delete('1.0', tk.END)

    def clean3(self):
        self.file_entry3.delete('1.0', tk.END)
    
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
        res = estructure_solution(DF_CLAVES, DF_IDENTIFI, DF_RESPUESTAS, TEMA, PATRON_CLAVES, PATRON_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")
    def validate2(self):
        res = duplicated_code_solution(DF_IDENTIFI)
        self.file_entry2.insert("end", f"\n{res}")

    def validate3(self):
        res = duplicated_litio_solution(DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")

    def validate4(self):
        res = applicant_card_solution(DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")

    def validate5(self):
        res = sin_pareja(DF_IDENTIFI, DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n{res}")
        pass

    def qualify(self):
        global calificacion_final
        calificacion_final = qualify_normal(DF_CLAVES, DF_IDENTIFI, DF_RESPUESTAS)
        # if res.empty():
        #     self.file_entry3.insert("end", f"\nAlgo salio mal al calificar")
        # else:
        self.file_entry3.insert("end", f"\nCalificación con exito \n{calificacion_final}")

    def save(self):
        # Abrir conexion
        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-8LNIGLG0;"
            "Database=Admission;"
            "Trusted_Connection=yes;")
        cnxn = pyodbc.connect(cnxn_str)

        # consulta SQL para obtener la tabla
        sql = "SELECT Id, Nombre, codigo, escuela FROM Alumnos"

        # leer la tabla en un dataframe de Pandas
        df_sql = pd.read_sql(sql, cnxn)

        # cerrar la conexión con la base de datos
        cnxn.close()

        # unir los dataframes utilizando la columna "codigo" como clave de unión
        df_merged = pd.merge(calificacion_final, df_sql[['Nombre','codigo', 'escuela']], on='codigo', how='left')

        # Selecciona alugnos campos
        df = df_merged.loc[:, ['codigo', 'Nombre', 'escuela','puntaje']]


        groups = df.groupby(df.escuela)

        # Prueba
        # f_sistemas = groups.get_group("sistemas")

        # f_sistemas.insert(0, 'orden', range(1, len(f_sistemas)+1))

        # valido
        escuelas = df['escuela'].unique()
        
        for i in escuelas:
            especialidad = groups.get_group(i)
            especialidad.insert(0, 'orden', range(1, len(especialidad)+1))
            especialidad.to_csv(f'{i}.csv', index=False, sep=",")

        self.file_entry3.insert("end", f"\nGuardado dastisfactoriamente\n")

root = tk.Tk()
root.title("AdminUnica")
root.geometry("660x520")
navbar = Navbar(root)
navbar.pack(side='top', fill='x')
navbar.show_welcome_message()
root.mainloop()
