import tkinter as tk
import tkinter.ttk as ttk

ventana = tk.Tk()
ventana.geometry('800x600')
ventana.title('Admision')
ventana.iconbitmap('./images/icono.ico')


def evento_click():
    print('Botón presionado')


# Configurar el navbar
ventana.columnconfigure(0, weight=4)
ventana.columnconfigure(1, weight=4)
ventana.columnconfigure(2, weight=4)

ventana.rowconfigure(0, weight=1)

btnCargar = tk.Button(ventana, text='Cargar Archivos', command=evento_click)
btnCargar.grid(row=0, column=0, sticky='NSWE', padx=5, pady=5)
btnCargar.config(bg='#00ff00', fg='black', font=('Arial', 12))


btnValidar = tk.Button(ventana, text='Validar', command=ventana.destroy)
btnValidar.grid(row=0, column=1, sticky='NSWE', padx=5, pady=5)
btnValidar.config(bg='#00ff00', fg='black', font=('Arial', 12))

btnCalificar = tk.Button(ventana, text='Calificar', command=ventana.destroy)
btnCalificar.grid(row=0, column=2, sticky='NSWE', padx=5, pady=5)
btnCalificar.config(bg='#00ff00', fg='black', font=('Arial', 12))


# Configurar Cuerpo
btnprueba = tk.Button(ventana, text='asdf', command=ventana.destroy)
btnprueba.grid(row=2, column=0, sticky='NSWE', padx=5, pady=5)
btnprueba.config(bg='#00ff00', fg='black', font=('Arial', 12))

btnprueba1 = tk.Button(ventana, text='asdf', command=ventana.destroy)
btnprueba1.grid(row=3, column=0, sticky='NSWE', padx=5, pady=5)
btnprueba1.config(bg='#00ff00', fg='black', font=('Arial', 12))

btnprueba2 = tk.Button(ventana, text='adsf', command=ventana.destroy)
btnprueba2.grid(row=4, column=0, sticky='NSWE', padx=5, pady=5)
btnprueba2.config(bg='#00ff00', fg='black', font=('Arial', 12))

btnprueba3 = tk.Button(ventana, text='adsf', command=ventana.destroy)
btnprueba3.grid(row=5, column=0, sticky='NSWE', padx=5, pady=5)
btnprueba3.config(bg='#00ff00', fg='black', font=('Arial', 12))

btnprueba4 = tk.Button(ventana, text='asdf', command=ventana.destroy)
btnprueba4.grid(row=6, column=0, sticky='NSWE', padx=5, pady=5)
btnprueba4.config(bg='#00ff00', fg='black', font=('Arial', 12))

ventana.rowconfigure(1, weight=2)
ventana.rowconfigure(2, weight=2)
ventana.rowconfigure(3, weight=2)
ventana.rowconfigure(4, weight=2)
ventana.rowconfigure(5, weight=2)
ventana.rowconfigure(6, weight=2)
ventana.rowconfigure(7, weight=2)

# Configurar consola
frame = ttk.Frame(ventana, borderwidth=5,
                  relief='groove', width=200, height=200)
frame.grid(row=1, column=1, sticky='NSWE', padx=5,
           pady=5, rowspan=7, columnspan=2)
label = ttk.Label(frame, text='Consola')
label.pack()


def run():
    ventana.mainloop()


if __name__ == '__main__':
    run()
