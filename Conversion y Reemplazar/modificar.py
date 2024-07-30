import tkinter as tk # Importamos para la interfaz
from tkinter import messagebox # Importamos para la ventana de mensajes
import pandas as pd # Importamos para el manejo de datos

def additional_action(files): # Función para realizar acción adicional

    file_info = [] # Creamos una lista para almacenar la información de los archivos
    for file in files: # Recorremos la lista de archivos
        try: # Intentamos realizar la acción
            if file.endswith('.csv'): # Si el archivo es un CSV
                df = pd.read_csv(file) # Leemos el archivo CSV
            elif file.endswith('.xlsx'): # Si el archivo es un Excel
                df = pd.read_excel(file, engine='openpyxl') # Leemos el archivo Excel
            else: # Si el archivo no es un CSV ni un Excel
                continue # Continua con el siguiente archivo

            row_count = len(df) # Contamos el número de filas del archivo
            file_info.append(f"{file}: {row_count} filas")  # Agregamos la información del archivo a la lista
        except Exception as e: # Si ocurre un error
            messagebox.showerror("Error", f"Error al procesar {file}: {e}") # Mostramos un mensaje de error
            return # Salimos de la función

    info_message = "\n".join(file_info) # Unimos la información de los archivos en un solo mensaje
    messagebox.showinfo("Información de Archivos", info_message) # Mostramos un mensaje con la información de los archivos

class SearchReplaceWindow: # Creamos una clase para la ventana de búsqueda y reemplazo
    def __init__(self, parent, files): # Creamos el constructor de la clase
        self.parent = parent # Guardamos la referencia a la ventana padre
        self.files = files # Guardamos la lista de archivos
        self.window = tk.Toplevel(parent) # Creamos una ventana nueva
        self.window.title("Buscar y Reemplazar") # Cambiamos el título de la ventana
        self.window.geometry("400x400") # Cambiamos el tamaño de la ventana

        self.search_label = tk.Label(self.window, text="Buscar:") # Etiquetas para los campos de entrada que indican al usuario qué información debe ingresar.
        self.search_label.grid(row=0, column=0, padx=10, pady=5) 
        self.search_entry = tk.Entry(self.window) # Campos de entrada par a que el usuario ingrese la información.
        self.search_entry.grid(row=0, column=1, padx=10, pady=5) 

        self.replace_label = tk.Label(self.window, text="Reemplazar con:") # Etiquetas para los campos de entrada que indican al usuario qué información debe ingresar.
        self.replace_label.grid(row=1, column=0, padx=10, pady=5)
        self.replace_entry = tk.Entry(self.window) # Campos de entrada par a que el usuario ingrese la información.
        self.replace_entry.grid(row=1, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.window, text="Buscar", command=self.search) # Botones para que el usuario presione para buscar y reemplazar.
        self.search_button.grid(row=2, column=0, padx=10, pady=10) 

        self.replace_button = tk.Button(self.window, text="Reemplazar", command=self.replace) # Botones para que el usuario presione para buscar y reemplazar.
        self.replace_button.grid(row=2, column=1, padx=10, pady=10)

        self.preview_text = tk.Text(self.window, height=15, width=50) # Caja de texto para que el usuario vea el resultado de la búsqueda y reemplazo.
        self.preview_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10) 
        self.preview_text.config(state=tk.DISABLED) # Deshabilitamos la caja de texto.

    def search(self): # Función para que el usuario vea el resultado de la búsqueda y reemplazar.
        search_term = self.search_entry.get() # Obtiene el texto a buscar
        if not search_term: # Si no se ingresó ningún texto
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.") # Mostramos un mensaje de advertencia
            return # Salimos de la función

        results = [] # Creamos una lista para almacenar los resultados de la búsqueda
        for file in self.files: # Recorremos la lista de archivos
            try: # Intentamos realizar la acción
                if file.endswith('.csv'): # Si el archivo es un CSV
                    df = pd.read_csv(file)  
                elif file.endswith('.xlsx'): # Si el archivo es un Excel
                    df = pd.read_excel(file, engine='openpyxl') 
                else: # Si el archivo no es un CSV ni un Excel
                    continue # Continua con el siguiente archivo

                matches = df.apply(lambda row: row.astype(str).str.contains(search_term, na=False).any(), axis=1) # Busca el texto en el archivo
                matching_rows = df[matches] # Filtra las filas que coinciden con el texto

                if not matching_rows.empty: # Si se encontraron coincidencias
                    results.append(f"Archivo: {file}\n{matching_rows.to_string(index=False)}\n") # Agrega la información de los resultados a la lista

            except Exception as e: # Si ocurre un error
                messagebox.showerror("Error", f"Error al buscar en {file}: {e}") # Mostramos un mensaje de error
                return # Salimos de la función

        if results: # Si se encontraron coincidencias
            self.preview_text.config(state=tk.NORMAL) # Habilitamos la caja de texto
            self.preview_text.delete("1.0", tk.END) # Borramos el contenido de la caja de texto
            self.preview_text.insert(tk.END, "\n\n".join(results)) # Insertamos los resultados en la caja de texto
            self.preview_text.config(state=tk.DISABLED) # Deshabilitamos la caja de texto
        else: # Si no se encontraron coincidencias
            messagebox.showinfo("Resultados", "No se encontraron coincidencias.") # Mostramos un mensaje de información

    def replace(self): # Función para que el usuario realice el reemplazo.
        search_term = self.search_entry.get() # Obtiene el texto a buscar
        replace_term = self.replace_entry.get() # Obtiene el texto a reemplazar
        if not search_term: # Si no se ingresó ningún texto
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.") # Mostramos un mensaje de advertencia
            return # Salimos de la función
        if not replace_term: # Si no se ingresó ningún texto
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de reemplazo.") # Mostramos un mensaje de advertencia
            return # Salimos de la función

        for file in self.files: # Recorremos la lista de archivos
            try: # Intentamos realizar la acción
                if file.endswith('.csv'): # Si el archivo es un CSV
                    df = pd.read_csv(file) 
                elif file.endswith('.xlsx'): # Si el archivo es un Excel
                    df = pd.read_excel(file, engine='openpyxl') 
                else: # Si el archivo no es un CSV ni un Excel
                    continue # Continua con el siguiente archivo

                original_df = df.copy() # Creamos una copia del DataFrame original
                df = df.applymap(lambda x: x.replace(search_term, replace_term) if isinstance(x, str) else x) # Reemplazamos el texto
 
                if file.endswith('.csv'): # Si el archivo es un CSV
                    df.to_csv(file, index=False) 
                elif file.endswith('.xlsx'): # Si el archivo es un Excel
                    df.to_excel(file, index=False, engine='openpyxl') 

                if not self.validate_replacement(original_df, df, search_term, replace_term): # Validamos si se realizaron los cambios correctamente
                    messagebox.showwarning("Advertencia", f"No se reemplazaron todas las ocurrencias en {file}") # Mostramos un mensaje de advertencia
                    return # Salimos de la función

            except Exception as e: # Si ocurre un error
                messagebox.showerror("Error", f"Error al reemplazar en {file}: {e}") # Mostramos un mensaje de error
                return # Salimos de la función

        messagebox.showinfo("Reemplazo Completo", "El reemplazo se ha completado en todos los archivos seleccionados.") # Mostramos un mensaje de confirmación

    def validate_replacement(self, original_df, modified_df, search_term, replace_term): # Función para validar si se realizaron los cambios correctamente.

        # Contamos el número de ocurrencias de los términos en los DataFrames
        original_occurrences = (original_df.applymap(lambda x: search_term in x if isinstance(x, str) else False)).sum().sum()  
        modified_occurrences = (modified_df.applymap(lambda x: replace_term in x if isinstance(x, str) else False)).sum().sum()  

        # Comparamos el número de ocurrencias antes y después del reemplazo
        return original_occurrences == modified_occurrences # Retornamos True si se realizaron los cambios correctamente