import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from modificar import additional_action, SearchReplaceWindow

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtrado de Datos")
        self.root.geometry("500x400")

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

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")])
        if self.files:
            self.to_csv_button.config(state=tk.NORMAL)
            self.to_excel_button.config(state=tk.NORMAL)
            self.additional_action_button.config(state=tk.NORMAL)
            self.search_replace_button.config(state=tk.NORMAL)
            self.files_label.config(text="\n".join(self.files))
            messagebox.showinfo("Archivos Seleccionados", f"{len(self.files)} archivos seleccionados")

    def clear_selection(self):
        self.files = []
        self.to_csv_button.config(state=tk.DISABLED)
        self.to_excel_button.config(state=tk.DISABLED)
        self.additional_action_button.config(state=tk.DISABLED)
        self.search_replace_button.config(state=tk.DISABLED)
        self.files_label.config(text="")
        messagebox.showinfo("Selección Limpiada", "Se ha limpiado la selección de archivos")

    def convert_to_csv(self):
        output_dir = 'csv_files'
        os.makedirs(output_dir, exist_ok=True)
        for file in self.files:
            if file.endswith('.xlsx'):
                df = pd.read_excel(file, engine='openpyxl')
                new_file = os.path.join(output_dir, os.path.basename(file).replace('.xlsx', '.csv'))
                df.to_csv(new_file, index=False)
        messagebox.showinfo("Conversión Completa", "Todos los archivos se han convertido a CSV")

    def convert_to_excel(self):
        output_dir = 'excel_files'
        os.makedirs(output_dir, exist_ok=True)
        for file in self.files:
            if file.endswith('.csv'):
                df = pd.read_csv(file)
                new_file = os.path.join(output_dir, os.path.basename(file).replace('.csv', '.xlsx'))
                df.to_excel(new_file, index=False, engine='openpyxl')
        messagebox.showinfo("Conversión Completa", "Todos los archivos se han convertido a Excel")

    def perform_additional_action(self):
        additional_action(self.files)

    def open_search_replace_window(self):
        SearchReplaceWindow(self.root, self.files)

class SearchReplaceWindow:
    def __init__(self, root, files):
        self.root = tk.Toplevel(root)
        self.root.title("Buscar y Reemplazar")
        self.files = files

        self.search_label = tk.Label(self.root, text="Buscar:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)

        self.replace_label = tk.Label(self.root, text="Reemplazar con:")
        self.replace_label.pack(pady=5)
        self.replace_entry = tk.Entry(self.root)
        self.replace_entry.pack(pady=5)

        self.preview_button = tk.Button(self.root, text="Buscar", command=self.preview_search)
        self.preview_button.pack(pady=10)

        self.replace_button = tk.Button(self.root, text="Reemplazar", command=self.perform_replace)
        self.replace_button.pack(pady=10)

        self.text = tk.Text(self.root, height=10, width=50)
        self.text.pack(pady=10)

    def preview_search(self):
        search_term = self.search_entry.get()
        self.text.delete(1.0, tk.END)
        for file in self.files:
            df = pd.read_excel(file, engine='openpyxl') if file.endswith('.xlsx') else pd.read_csv(file)
            result = df.applymap(lambda x: str(x).replace(search_term, f"[{search_term}]") if isinstance(x, (str, int, float)) else x)
            self.text.insert(tk.END, f"Archivo: {os.path.basename(file)}\n")
            self.text.insert(tk.END, result.head().to_string())
            self.text.insert(tk.END, "\n\n")

    def perform_replace(self):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        for file in self.files:
            df = pd.read_excel(file, engine='openpyxl') if file.endswith('.xlsx') else pd.read_csv(file)
            df = df.applymap(lambda x: str(x).replace(search_term, replace_term) if isinstance(x, (str, int, float)) else x)
            if file.endswith('.xlsx'):
                df.to_excel(file, index=False, engine='openpyxl')
            else:
                df.to_csv(file, index=False)
        messagebox.showinfo("Reemplazo Completo", "Todos los reemplazos se han completado")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
