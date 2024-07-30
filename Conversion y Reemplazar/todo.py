'''
Código principal que estará junto a ‘modificar.py’ para que pueda realizar cambios de archivos CSV a EXCEL e incluso poder buscar y reemplazar palabras (algo pequeño que hace Excel de Microsoft), ya mas adelante se explicara el video.
'''

import tkinter as tk # Importamos para la interfaz
from tkinter import filedialog, messagebox # Importamos para la selección de archivos
import pandas as pd # Importamos para el manejo de datos
import os # Importamos para operaciones del sistema
from modificar import additional_action, SearchReplaceWindow # Importamos el archivo modificar.py

class FileConverterApp: # Creamos una clase para la interfaz
    def __init__(self, root): # Creamos el constructor de la clase
        self.root = root # Guardamos la referencia a la ventana principal
        self.root.title("Filtrado de Datos") # Cambiamos el título de la ventana
        self.root.geometry("500x400") # Cambiamos el tamaño de la ventana

        # Botón para seleccionar archivos
        self.select_button = tk.Button(root, text="Seleccionar Archivos", command=self.select_files)
        self.select_button.pack(pady=20)

        # Botón para convertir a CSV
        self.to_csv_button = tk.Button(root, text="Convertir a CSV", command=self.convert_to_csv, state=tk.DISABLED)
        self.to_csv_button.pack(pady=10)

        # Botón para convertir a Excel
        self.to_excel_button = tk.Button(root, text="Convertir a Excel", command=self.convert_to_excel, state=tk.DISABLED)
        self.to_excel_button.pack(pady=10)

        # Botón para realizar acción adicional
        self.additional_action_button = tk.Button(root, text="Acción Adicional", command=self.perform_additional_action, state=tk.DISABLED)
        self.additional_action_button.pack(pady=10)

        # Botón para búsqueda y reemplazo
        self.search_replace_button = tk.Button(root, text="Buscar y Reemplazar", command=self.open_search_replace_window, state=tk.DISABLED)
        self.search_replace_button.pack(pady=10)

        # Botón para limpiar la selección
        self.clear_button = tk.Button(root, text="Limpiar Selección", command=self.clear_selection)
        self.clear_button.pack(pady=10)

        self.files = []
        self.files_label = tk.Label(root, text="")
        self.files_label.pack()

    def select_files(self): # Función para seleccionar archivos
        self.files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]) # Abrimos el cuadro de diálogo para seleccionar archivos
        if self.files:  # Si se seleccionaron archivos
            self.to_csv_button.config(state=tk.NORMAL)  # Habilitamos los botones correspondientes
            self.to_excel_button.config(state=tk.NORMAL)  # Habilitamos los botones correspondientes
            self.additional_action_button.config(state=tk.NORMAL)  # Habilitamos los botones correspondientes
            self.search_replace_button.config(state=tk.NORMAL)  # Habilitamos los botones correspondientes
            self.files_label.config(text="\n".join(self.files))  # Mostramos los archivos seleccionados
            messagebox.showinfo("Archivos Seleccionados", f"{len(self.files)} archivos seleccionados")  # Mostramos un mensaje con la cantidad de archivos seleccionados
        else:  # Si no se seleccionaron archivos
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos")  # Mostramos un mensaje de advertencia

    def clear_selection(self): # Función para limpiar la selección
        self.files = []  # Limpiamos la lista de archivos
        self.to_csv_button.config(state=tk.DISABLED)  # Deshabilitamos los botones correspondientes
        self.to_excel_button.config(state=tk.DISABLED)  # Deshabilitamos los botones correspondientes
        self.additional_action_button.config(state=tk.DISABLED)  # Deshabilitamos los botones correspondientes
        self.search_replace_button.config(state=tk.DISABLED)  # Deshabilitamos los botones correspondientes
        self.files_label.config(text="")  # Limpiamos la etiqueta de archivos
        messagebox.showinfo("Selección Limpiada", "Se ha limpiado la selección de archivos")  # Mostramos un mensaje de confirmación

    def convert_to_csv(self): # Función para convertir a CSV
        output_dir = 'csv_files' # Creamos una carpeta para los archivos CSV
        os.makedirs(output_dir, exist_ok=True) # Creamos la carpeta si no existe
        for file in self.files: # Recorremos la lista de archivos
            if file.endswith('.xlsx'): # Si el archivo es un Excel
                df = pd.read_excel(file, engine='openpyxl') # Leemos el archivo Excel
                new_file = os.path.join(output_dir, os.path.basename(file).replace('.xlsx', '.csv')) # Creamos el nombre del archivo CSV
                df.to_csv(new_file, index=False) # Escribimos el archivo CSV
        messagebox.showinfo("Conversión Completa", "Todos los archivos se han convertido a CSV") # Mostramos un mensaje de confirmación

    def convert_to_excel(self): # Función para convertir a Excel
        output_dir = 'excel_files' # Creamos una carpeta para los archivos Excel
        os.makedirs(output_dir, exist_ok=True) # Creamos la carpeta si no existe
        for file in self.files: # Recorremos la lista de archivos
            if file.endswith('.csv'): # Si el archivo es un CSV
                df = pd.read_csv(file) # Leemos el archivo CSV
                new_file = os.path.join(output_dir, os.path.basename(file).replace('.csv', '.xlsx')) # Creamos el nombre del archivo Excel
                df.to_excel(new_file, index=False, engine='openpyxl') # Escribimos el archivo Excel
        messagebox.showinfo("Conversión Completa", "Todos los archivos se han convertido a Excel") # Mostramos un mensaje de confirmación

    def perform_additional_action(self): # Función para realizar acción adicional
        additional_action(self.files) # Llamamos a la función additional_action del archivo modificar.py

    def open_search_replace_window(self): # Función para abrir la ventana de búsqueda y reemplazo
        SearchReplaceWindow(self.root, self.files) # Llamamos a la clase SearchReplaceWindow del archivo modificar.py

class SearchReplaceWindow: # Creamos una clase para la ventana de búsqueda y reemplazo
    def __init__(self, root, files): # Creamos el constructor de la clase
        self.root = tk.Toplevel(root) # Creamos una ventana nueva
        self.root.title("Buscar y Reemplazar") # Cambiamos el título de la ventana
        self.files = files # Guardamos la lista de archivos

        # Creamos los widgets de la ventana
        self.search_label = tk.Label(self.root, text="Buscar:") # Crea etiquetas para que el usuario ingrese el texto a buscar
        self.search_label.pack(pady=5) 
        self.search_entry = tk.Entry(self.root) # Crea un cuadro de texto para que el usuario ingrese el texto a buscar
        self.search_entry.pack(pady=5) 

        self.replace_label = tk.Label(self.root, text="Reemplazar con:") # Crea etiquetas para que el usuario ingrese el texto a reemplazar
        self.replace_label.pack(pady=5) 
        self.replace_entry = tk.Entry(self.root) # Crea un cuadro de texto para que el usuario ingrese el texto a reemplazar
        self.replace_entry.pack(pady=5)

        self.preview_button = tk.Button(self.root, text="Buscar", command=self.preview_search) # Crea un botón para que el usuario presione para buscar
        self.preview_button.pack(pady=10) 

        self.replace_button = tk.Button(self.root, text="Reemplazar", command=self.perform_replace) # Crea un botón para que el usuario presione para reemplazar
        self.replace_button.pack(pady=10)

        self.text = tk.Text(self.root, height=10, width=50) # Crea un cuadro de texto para que el usuario vea el resultado de la búsqueda y reemplazo
        self.text.pack(pady=10)

    def preview_search(self): # Función para que el usuario vea el resultado de la búsqueda y reemplazo
        search_term = self.search_entry.get() # Obtiene el texto a buscar
        self.text.delete(1.0, tk.END) # Borra el cuadro de texto
        for file in self.files: # Recorre la lista de archivos
            df = pd.read_excel(file, engine='openpyxl') if file.endswith('.xlsx') else pd.read_csv(file) # Lee el archivo
            result = df.applymap(lambda x: str(x).replace(search_term, f"[{search_term}]") if isinstance(x, (str, int, float)) else x) # Reemplaza el texto
            self.text.insert(tk.END, f"Archivo: {os.path.basename(file)}\n") # Muestra el nombre del archivo
            self.text.insert(tk.END, result.head().to_string()) # Muestra el resultado de la búsqueda y reemplazo
            self.text.insert(tk.END, "\n\n") # Agrega un espacio entre archivos

    def perform_replace(self): # Función para que el usuario realice el reemplazo
        search_term = self.search_entry.get() # Obtiene el texto a buscar
        replace_term = self.replace_entry.get() # Obtiene el texto a reemplazar
        for file in self.files: # Recorre la lista de archivos
            df = pd.read_excel(file, engine='openpyxl') if file.endswith('.xlsx') else pd.read_csv(file) # Lee el archivo
            df = df.applymap(lambda x: str(x).replace(search_term, replace_term) if isinstance(x, (str, int, float)) else x) # Reemplaza el texto
            if file.endswith('.xlsx'): # Si el archivo es un Excel
                df.to_excel(file, index=False, engine='openpyxl') # Escribe el archivo
            else: # Si el archivo es un CSV
                df.to_csv(file, index=False) # Escribe el archivo
        messagebox.showinfo("Reemplazo Completo", "Todos los reemplazos se han completado") # Muestra un mensaje de confirmación

if __name__ == "__main__": # Si el archivo se ejecuta como un programa principal
    root = tk.Tk() # Crea una ventana
    app = FileConverterApp(root) # Crea una instancia de la clase FileConverterApp
    root.mainloop() # Inicia el bucle principal de la ventana
