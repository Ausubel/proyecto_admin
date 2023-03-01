import tkinter as tk

NAV_BG = 'gray'
BTN_BG = 'gray'
BTN_FG = 'white'
PANEL_BG = 'white'
PANEL_WIDTH = 600
PANEL_HEIGHT = 300

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
        
        tk.Button(self.file_panel, text='Subir claves').grid(row=0, column=0, padx=(100,50), pady=50)
        tk.Button(self.file_panel, text='Cargar Identificadores').grid(row=1, column=0, padx=(100,50), pady=50)
        tk.Button(self.file_panel, text='Cargar respuestas').grid(row=2, column=0, padx=(100,50), pady=50)
        tk.Button(self.file_panel, text='Validar').grid(row=3, column=0, padx=(100,50), pady=50)
        
        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()

    def show_file(self):
        self.file_panel.pack(side='top', fill='both', expand=True)
        self.validation_panel.pack_forget()
        self.qualify_panel.pack_forget()
        
    def show_validation(self):
        self.file_panel.pack_forget()
        self.validation_panel.pack(side='top', fill='both', expand=True)
        self.qualify_panel.pack_forget()
        
    def show_qualify(self):
        self.file_panel.pack_forget()
        self.validation_panel.pack_forget()
        self.qualify_panel.pack(side='top', fill='both', expand=True)


root = tk.Tk()
root.geometry("800x600")
navbar = Navbar(root)
navbar.pack(side='top', fill='x')
root.mainloop()