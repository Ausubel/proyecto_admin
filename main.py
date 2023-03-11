import tkinter as tk
import pandas as pd
from cargando import *
from modificar import *
from validations import *
from qualify import *
from tkinter import filedialog
from tkinter import messagebox
import os

CLAVES = "cla_lino.sdf"
RESPUESTAS = "res_lino.sdf"
IDENTIFI= "ide_lino.sdf"
POSTULANTES = "postulantes.csv"
TEMA = 'FGHIJKLMNOPRSTUVWXYZ'
PATRON_CLAVES = 'ABCDE '
PATRON_RESPUESTAS = 'ABCDE *'
DF_CLAVES = pd.DataFrame()
DF_IDENTIFI = pd.DataFrame()
DF_RESPUESTAS = pd.DataFrame()
DF_POSTULANTES = pd.DataFrame()
DF_ANULADOS = pd.DataFrame()
DF_AUSENTE = pd.DataFrame()
calificacion_final = pd.DataFrame()
NAV_BG = '#FF010B'
BTN_BG = '#dc3545'
BTN_FG = '#FCF3EA'
PANEL_BG = '#D88756'
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
        
        self.file_entry1 = tk.Text(self.file_panel, width=97, height=25)
        self.file_entry1.configure(bg="#FCF3EA")
        self.file_entry1.grid(row=0, column=1, rowspan=5, padx=(30,30), pady=50)

        # Widgets Validacion

        tk.Button(self.validation_panel, text='Validar estructura', width=20, height=2, command=self.validate1).grid(row=0, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar codigos duplicados', width=20, height=2, command=self.validate2).grid(row=1, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar duplicados de litos', width=20, height=2, command=self.validate3).grid(row=2, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar carnet postulante', width=20, height=2, command=self.validate4).grid(row=3, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Validar lito no localizado', width=20, height=2, command=self.validate5).grid(row=4, column=0, padx=(30,30), pady=20)
        tk.Button(self.validation_panel, text='Limpiar', width=20, height=2, command=self.clean2).grid(row=5, column=0, padx=(30,30), pady=20)

        self.file_entry2 = tk.Text(self.validation_panel, width=97, height=25)
        self.file_entry2.configure(bg="#FCF3EA")
        self.file_entry2.grid(row=0, column=1, rowspan=6, padx=(30,30), pady=50)
        
        # Widgets Calificador
        self.container = tk.Frame(self.qualify_panel, borderwidth=1, relief=tk.RIDGE, background="#F0F0F0", highlightbackground="#D9D9D9")
        self.container.grid(row=0, column=0, padx=(30,30), pady=50)

        self.listbox = tk.Listbox(self.container)
        self.listbox = tk.Listbox(self.container, width=10, height=5, selectmode="multiple")
        self.listbox.pack(side="left", padx=10, pady=10)
        
        [self.listbox.insert("end", c) for c in TEMA]

        self.entry = tk.Entry(self.container)
        self.entry.pack(side="left", padx=10)

        self.add_button = tk.Button(self.container, text="Modificar", command=lambda: self.modificar(self.listbox, self.entry))
        self.add_button.pack(side="left", padx=10)
        tk.Button(self.qualify_panel, text='Calificar', width=20, height=2, command=self.qualify).grid(row=1, column=0, pady=(50, 30))

        # Panel
        self.file_entry3 = tk.Text(self.qualify_panel, width=70, height=25)
        self.file_entry3.configure(bg="#FCF3EA")
        self.file_entry3.grid(row=0, column=1, rowspan=4, padx=(30,30), pady=50)

        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()
        
    def modificar(self,listbox, entry):
        preguntas = entry.get()
        selection = listbox.curselection()
        for index in selection:
            DF_CLAVES.loc[DF_CLAVES['tema_clave'] == listbox.get(index), 'solucion'] = ''.join(mod_tema(listbox.get(index),preguntas,DF_CLAVES))
            self.file_entry3.insert("end", f"Claves modificadas {listbox.get(index)}:{preguntas}...\n")
        return

    # def show_welcome_message(self):
    #     messagebox.showinfo("Bienvenido", "¡Bienvenido a AdminUni!")
    #     self.show_file()


    def clean1(self):
        self.file_entry1.delete('1.0', tk.END)

    def clean2(self):
        self.file_entry2.delete('1.0', tk.END)

    def clean3(self):
        self.file_entry3.delete('1.0', tk.END)
    
    def select_folder_claves(self):
        global DF_CLAVES
        global DF_RESPUESTAS
        global DF_IDENTIFI
        
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, CLAVES)
        if ruta_archivo != "":
            DF_CLAVES = carga.leer_claves(ruta_archivo)
            self.file_entry1.insert("end", f"\nSe cargaron las claves ..")
        
        ################
        
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, RESPUESTAS)
        if ruta_archivo != "":
            DF_RESPUESTAS = carga.leer_respuestas(ruta_archivo)
            self.file_entry1.insert("end", f"\nSe cargaron las respuestas ..")
        ################
        
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, IDENTIFI)
        if ruta_archivo != "":
            DF_IDENTIFI = carga.leer_indentifi(ruta_archivo)
            self.file_entry1.insert("end", f"\nSe cargaron los identificadores ..")
            return 

    def select_folder_respuestas(self):
        global DF_RESPUESTAS
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, RESPUESTAS)
        if ruta_archivo != "":
            DF_RESPUESTAS = carga.leer_respuestas(ruta_archivo)
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

    def select_folder_postulantes(self):
        global DF_POSTULANTES
        folder_path = filedialog.askdirectory()
        file_name = 'BASE.xlsx'
        ruta_archivo = os.path.join(folder_path, file_name)
        if ruta_archivo != "":
            # DF_POSTULANTES = pd.read_csv(ruta_archivo)
            DF_POSTULANTES = pd.read_excel(ruta_archivo)
            self.file_entry2.insert("end", f"\nArchivo postulantes cargado ..\n")
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
        self.file_entry2.insert("end", f"\n************** VALIDACION 1 **************\n{res}")
    def validate2(self):
        res = duplicated_code_solution(DF_IDENTIFI)
        self.file_entry2.insert("end", f"\n************** VALIDACION 2 **************\n{res}")

    def validate3(self):
        res = duplicated_litio_solution(DF_IDENTIFI,DF_RESPUESTAS)
        self.file_entry2.insert("end", f"\n************** VALIDACION 3 **************\n{res}")

    def validate4(self):
        self.select_folder_postulantes()
        res = applicant_card_solution(DF_IDENTIFI, DF_POSTULANTES)
        self.file_entry2.insert("end", f"\n************** VALIDACION 4 **************\n{res}")

    def validate5(self):
        global DF_ANULADOS
        global DF_AUSENTE
        res, DF_ANULADOS = lito_not_located(DF_IDENTIFI, DF_RESPUESTAS,DF_POSTULANTES)
                
        df = pd.read_excel('BASE.xlsx')

        # Convertir la columna 'codigo' a tipo object
        df['codigo'] = df['codigo'].astype(int)
        DF_IDENTIFI['codigo'] = DF_IDENTIFI['codigo'].astype(int)

        # Hacer el left anti join
        merged = pd.merge(df,DF_IDENTIFI[['codigo']], how='left', left_on='codigo', right_on='codigo', indicator=True)

        # Filtrar los registros que no están en df_identifi
        DF_AUSENTE = merged[merged['_merge'] == 'left_only'][df.columns] ############ AUSENTE

        self.file_entry2.insert("end", f"\n************** VALIDACION 5 **************\n{res}")

        print(f"Estos son ausentes \n\n{DF_AUSENTE}")
        print(f"Estos son anulados \n\n{DF_ANULADOS}")
        
        return


    def qualify(self):
        global calificacion_final
        global DF_AUSENTE
        global DF_ANULADOS
        calificacion_final = qualify_normal(DF_CLAVES, DF_IDENTIFI, DF_RESPUESTAS)

        DF_ANULADOS["CONDICION"] = "NO INGRESO"
        DF_AUSENTE["CONDICION"] = "NO INGRESO"
        DF_ANULADOS["PUNTAJE"] = "Anulado"
        DF_AUSENTE["PUNTAJE"] = "Ausente"
        # DF_ANULADOS['APELLIDOS Y NOMBRES'] = DF_ANULADOS.apply(lambda x: f"{x['APELLIDO PATERNO']} {x['APELLIDO MATERNO']} {x['NOMBRES']}", axis=1)
        # DF_ANULADOS = DF_ANULADOS.drop(['APELLIDO PATERNO', 'APELLIDO MATERNO', 'NOMBRES'], axis=1)

        
        print(f"ANULADOOO\n\n{DF_ANULADOS}")
        print(f"AUSENTEEE\n\n{DF_AUSENTE}")
        DF_AUSENTE['APELLIDOS Y NOMBRES'] = DF_AUSENTE.apply(lambda x: f"{x['AP_PATERNO']} {x['AP_MATERNO']} {x['NOMBRE']}", axis=1)
        DF_ANULADOS['APELLIDOS Y NOMBRES'] = DF_ANULADOS.apply(lambda x: f"{x['AP_PATERNO']} {x['AP_MATERNO']} {x['NOMBRE']}", axis=1)
        DF_ANULADOS = DF_ANULADOS.drop(['AP_PATERNO', 'AP_MATERNO', 'NOMBRE'], axis=1)
        DF_AUSENTE = DF_AUSENTE.drop(['AP_PATERNO', 'AP_MATERNO', 'NOMBRE'], axis=1)
        
        DF_ANULADOS = DF_ANULADOS.reindex(columns=['codigo', 'APELLIDOS Y NOMBRES', 'PUNTAJE', 'CONDICION', 'CARRERA'])
        DF_AUSENTE = DF_AUSENTE.reindex(columns=['codigo', 'APELLIDOS Y NOMBRES', 'PUNTAJE', 'CONDICION', 'CARRERA'])
        
        
        print(f"CALIFICACION FINAL{calificacion_final}")
        self.file_entry3.insert("end", f"\nCalificación con exito \n{calificacion_final}")

        DF_BASE = pd.read_excel("BASE.xlsx")
        # unir los dataframes utilizando la columna "codigo" como clave de unión
        print(f"DF_BASEEE\n{DF_BASE}")

        ### YA CONECTADOS CON EL CODIGO
        merged_df = pd.merge(calificacion_final, DF_BASE[['codigo', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRE', 'CARRERA']], on='codigo')
        merged_df = merged_df[['codigo', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRE', 'puntaje', 'CARRERA']]
        
        print(f"DF UNIDO POR EL CODIGO\n\n{merged_df}")

        ## FINAL TODO UNIDO
        print(f"ESTE EL DF FINAL CON LOS ANULADOS Y AUSENTES :\n\n{merged_df}")

        # print(f"HALLAR COLUMNAS\n\n{merged_df.columns}")

        ## AHORA UNO LAS COLUMAS Y CAMBIO EL NOMBRE DE LAS CABECERAS
        # renombrar las columnas
        merged_df = merged_df.rename(columns={'codigo': 'CODIGO', 'AP_PATERNO': 'APELLIDO PATERNO', 'AP_MATERNO': 'APELLIDO MATERNO', 'NOMBRE': 'NOMBRES', 'puntaje': 'PUNTAJE', 'CARRERA': 'CARRERA'})

        # combinar las columnas de APELLIDO PATERNO, APELLIDO MATERNO y NOMBRES en una sola columna
        merged_df['APELLIDOS Y NOMBRES'] = merged_df.apply(lambda x: f"{x['APELLIDO PATERNO']} {x['APELLIDO MATERNO']} {x['NOMBRES']}", axis=1)

        # eliminar las columnas de APELLIDO PATERNO, APELLIDO MATERNO y NOMBRES
        merged_df = merged_df.drop(['APELLIDO PATERNO', 'APELLIDO MATERNO', 'NOMBRES'], axis=1)

        # ordenar el dataframe por la columna CODIGO
        # merged_df = merged_df.sort_values('CODIGO')
        print(f"ESTO ES RENOMBRADOO\n\n{merged_df}")

        # EN ESTE PASO CAMBIO LA POSICION DE LA COLUMNA APELLIDOS Y NOMBRES
        merged_df = merged_df.reindex(columns=['CODIGO', 'APELLIDOS Y NOMBRES', 'PUNTAJE', 'CARRERA'])


        #### ESTA LINEA ES PARA AGREGAR LA CONDICION COMO NaN
        merged_df['CONDICION'] = pd.Series([float('NaN') for _ in range(len(merged_df))])
        
        print(f"ACA SE MUESTRA EL GENERAL YA ORDENADO RENOMBRADO Y TODO ...\n\n{merged_df}")

        print("##############\n")

        groups = merged_df.groupby('CARRERA')

        with pd.ExcelWriter('resultados1.xlsx') as writer:
            for carrera in merged_df['CARRERA'].unique():
                especialidad = groups.get_group(carrera)
                especialidad.insert(0, 'orden', range(1, len(especialidad)+1))
                especialidad.to_excel(writer, sheet_name=carrera, index=False)
        
        
        # # Unir las columnas de apellidos y nombres
        
        # ########################
        # DF_AUSENTE['APELLIDOS Y NOMBRES'] = DF_AUSENTE['AP_PATERNO'] + ' ' + DF_AUSENTE['AP_MATERNO'] + ' ' + DF_AUSENTE['NOMBRE']

        # # Agregar la columna de puntaje
        # DF_AUSENTE['PUNTAJE'] = 'Ausente'

        # # Reordenar las columnas
        # DF_AUSENTE = DF_AUSENTE[['codigo', 'APELLIDOS Y NOMBRES', 'PUNTAJE', 'CONDICION', 'CARRERA']]

        # # Mostrar el resultado final
        # print(f"AUSENTEEE\n\n{DF_AUSENTE}")
        
        
        
        
        ############################### INTENTO DE AGREGAR LOS AUSENTES Y ANULADOS AL EXCEL
        # leer el archivo excel y almacenar cada hoja en un diccionario
        # excel_file = pd.ExcelFile('resultados1.xlsx')
        # sheets = {}
        # for sheet_name in excel_file.sheet_names:
        #     sheets[sheet_name] = excel_file.parse(sheet_name)

        # agregar filas para estudiantes ausentes
        # for carrera in sheets:
        #     ausentes = DF_AUSENTE.loc[DF_AUSENTE['CARRERA'] == carrera]
        #     for i, row in ausentes.iterrows():
        #         new_row = {'orden': len(sheets[carrera]) + 1,
        #                 'CODIGO': row['codigo'],
        #                 'APELLIDOS Y NOMBRES': f"{row['AP_PATERNO']} {row['AP_MATERNO']} {row['NOMBRE']}",
        #                 'PUNTAJE': 0.0,
        #                 'CARRERA': carrera,
        #                 'CONDICION': 'AUSENTE'}
        #         sheets[carrera] = sheets[carrera].append(new_row, ignore_index=True)


        ################### GENERAR UN EXCEL APARTE
        
        # EXPORTO COMO EN EXCEL LOS ANULADOS Y AUSENTES
        # Crear un objeto ExcelWriter para guardar los DataFrames en un archivo de Excel
        writer = pd.ExcelWriter('mi_archivo.xlsx', engine='xlsxwriter')

        # Guardar el DataFrame DF_ANULADO en la hoja 'DF_ANULADO'
        DF_ANULADOS.to_excel(writer, sheet_name='DF_ANULADO', index=False)

        # Guardar el DataFrame DF_AUSENTE en la hoja 'DF_AUSENTE'
        DF_AUSENTE.to_excel(writer, sheet_name='DF_AUSENTE', index=False)
        writer.save()
        print(f"ANULADOOO\n\n{DF_ANULADOS}")
        print(f"AUSENTEEE\n\n{DF_AUSENTE}")
    def save(self):
        pass

root = tk.Tk()
root.title("AdminUnica")
root.geometry("1100x600")
navbar = Navbar(root)
navbar.pack(side='top', fill='x')
root.resizable(0,0)
root.mainloop()
