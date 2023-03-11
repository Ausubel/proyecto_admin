import tkinter as tk
import pandas as pd
from cargando import *
from modificar import *
from validations import *
from qualify import *
from tkinter import filedialog
from tkinter import messagebox
import os

CLAVES = "claves.sdf"
RESPUESTAS = "respuestas.sdf"
IDENTIFI= "identifi.sdf"
POSTULANTES = "postulantes.csv"
TEMA = 'ABCDPQRS'
PATRON_CLAVES = 'TRQSP '
PATRON_RESPUESTAS = 'TRQSP *'
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
        folder_path = filedialog.askdirectory()
        ruta_archivo = os.path.join(folder_path, CLAVES)
        if ruta_archivo != "":
            DF_CLAVES = carga.leer_claves(ruta_archivo)
            self.file_entry1.insert("end", f"\nSe cargaron las claves ..")
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
        calificacion_final = qualify_normal(DF_CLAVES, DF_IDENTIFI, DF_RESPUESTAS)

        print(f"ANULADOOO\n{DF_ANULADOS}")
        print(f"AUSENTEEE{DF_AUSENTE}")
        print(f"CALIFICACION FINAL{calificacion_final}")
        self.file_entry3.insert("end", f"\nCalificación con exito \n{calificacion_final}")

        DF_BASE = pd.read_excel("BASE.xlsx")
        # unir los dataframes utilizando la columna "codigo" como clave de unión
        print(f"DF_BASEEE\n{DF_BASE}")

        ### YA CONECTADOS CON EL CODIGO
        merged_df = pd.merge(calificacion_final, DF_BASE[['codigo', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRE', 'CARRERA']], on='codigo')
        merged_df = merged_df[['codigo', 'AP_PATERNO', 'AP_MATERNO', 'NOMBRE', 'puntaje', 'CARRERA']]
        
        print(f"DF UNIDO POR EL CODIGO\n\n{merged_df}")
        
        ### UNIENDO CON LOS DATAFRAMES AUSENTES Y ANULADOS
        ###### NOTA ACA NO SE AGREGAN LOS DF AUSENTES Y ANULADOS PORQUE LUEGO SE DIFICULTA IDENTIFICARLOS AL REPARTIRLOS DESDE EL DATAFRAME GENERAL
        
        # ## PARA AUSENTE
        # # Concatenamos los DataFrames
        # merged_df = pd.concat([merged_df, DF_AUSENTE])

        # # Reemplazamos los valores faltantes por 0
        # merged_df['puntaje'] = merged_df['puntaje'].fillna(0)

        # ## PARA ANULADOS
        # # Concatenamos los DataFrames
        # merged_df = pd.concat([merged_df, DF_ANULADOS])

        # # Reemplazamos los valores faltantes por 0
        # merged_df['puntaje'] = merged_df['puntaje'].fillna(0)


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
        
        
        
        
        #### EN ESTA LINEA AGREGO LA CONDICION A LOS DATAFRAMES DE DF_AUSENTE Y DF_ANULADO
        DF_ANULADOS["CONDICION"] = "ANULADO"
        DF_AUSENTE["CONDICION"] = "AUSENTE"
        
        
        
        
        ## AHORA PASAMOS A LA PARTE DE REPARTIR POR FACULTAD - EL DF QUE SE USA ES merged_df
        
        
        ########### FUNCIONA PERO PARA CSV #######################
        # groups = merged_df.groupby(merged_df.CARRERA)
        
        # # valido
        # escuelas = merged_df['CARRERA'].unique()
        
        # for i in escuelas:
        #     especialidad = groups.get_group(i)
        #     especialidad.insert(0, 'orden', range(1, len(especialidad)+1))
        #     especialidad.to_csv(f'resultados/{i}.csv', index=False, sep=",")
        ############################################################

        # merged_df = pd.read_csv('merged_data.csv')

        groups = merged_df.groupby('CARRERA')

        with pd.ExcelWriter('resultados1.xlsx') as writer:
            for carrera in merged_df['CARRERA'].unique():
                especialidad = groups.get_group(carrera)
                especialidad.insert(0, 'orden', range(1, len(especialidad)+1))
                especialidad.to_excel(writer, sheet_name=carrera, index=False)

        ## HASTA EL MOMENTO SE GENERA UN EXCEL SIN LOS 

    def save(self):
        pass
        # # Abrir conexion
        # cnxn_str = ("Driver={SQL Server Native Client 11.0};"
        #     "Server=LAPTOP-8LNIGLG0;"
        #     "Database=Admission;"
        #     "Trusted_Connection=yes;")
        # cnxn = pyodbc.connect(cnxn_str)

        # # consulta SQL para obtener la tabla
        # sql = "SELECT Id, Nombre, codigo, escuela FROM Alumnos"

        # # leer la tabla en un dataframe de Pandas
        # df_sql = pd.read_sql(sql, cnxn)

        # # cerrar la conexión con la base de datos
        # cnxn.close()

        # # unir los dataframes utilizando la columna "codigo" como clave de unión
        # df_merged = pd.merge(calificacion_final, df_sql[['Nombre','codigo', 'escuela']], on='codigo', how='left')

        # # Selecciona alugnos campos
        # df = df_merged.loc[:, ['codigo', 'Nombre', 'escuela','puntaje']]


        # groups = df.groupby(df.escuela)

        # # Prueba
        # # f_sistemas = groups.get_group("sistemas")

        # # f_sistemas.insert(0, 'orden', range(1, len(f_sistemas)+1))

        # # valido
        # escuelas = df['escuela'].unique()
        
        # for i in escuelas:
        #     especialidad = groups.get_group(i)
        #     especialidad.insert(0, 'orden', range(1, len(especialidad)+1))
        #     especialidad.to_csv(f'{i}.csv', index=False, sep=",")

        # self.file_entry3.insert("end", f"\nGuardado dastisfactoriamente\n")



root = tk.Tk()
root.title("AdminUnica")
root.geometry("1100x600")
navbar = Navbar(root)
navbar.pack(side='top', fill='x')
root.resizable(0,0)
root.mainloop()
