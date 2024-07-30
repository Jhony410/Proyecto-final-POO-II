import tkinter as tk
from tkinter import messagebox
import pandas as pd

def additional_action(files):
    # Ejemplo de acción adicional: Contar filas en cada archivo y mostrar un mensaje
    file_info = []
    for file in files:
        try:
            if file.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file, engine='openpyxl')
            else:
                continue

            row_count = len(df)
            file_info.append(f"{file}: {row_count} filas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar {file}: {e}")
            return

    info_message = "\n".join(file_info)
    messagebox.showinfo("Información de Archivos", info_message)

class SearchReplaceWindow:
    def __init__(self, parent, files):
        self.parent = parent
        self.files = files
        self.window = tk.Toplevel(parent)
        self.window.title("Buscar y Reemplazar")
        self.window.geometry("400x400")

        # Entry fields for search and replace
        self.search_label = tk.Label(self.window, text="Buscar:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.window)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.replace_label = tk.Label(self.window, text="Reemplazar con:")
        self.replace_label.grid(row=1, column=0, padx=10, pady=5)
        self.replace_entry = tk.Entry(self.window)
        self.replace_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons for search and replace actions
        self.search_button = tk.Button(self.window, text="Buscar", command=self.search)
        self.search_button.grid(row=2, column=0, padx=10, pady=10)

        self.replace_button = tk.Button(self.window, text="Reemplazar", command=self.replace)
        self.replace_button.grid(row=2, column=1, padx=10, pady=10)

        self.preview_text = tk.Text(self.window, height=15, width=50)
        self.preview_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.preview_text.config(state=tk.DISABLED)

    def search(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.")
            return

        results = []
        for file in self.files:
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    continue

                matches = df.apply(lambda row: row.astype(str).str.contains(search_term, na=False).any(), axis=1)
                matching_rows = df[matches]

                if not matching_rows.empty:
                    results.append(f"Archivo: {file}\n{matching_rows.to_string(index=False)}\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar en {file}: {e}")
                return

        if results:
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, "\n\n".join(results))
            self.preview_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Resultados", "No se encontraron coincidencias.")

    def replace(self):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        if not search_term:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de búsqueda.")
            return
        if not replace_term:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un término de reemplazo.")
            return

        for file in self.files:
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.endswith('.xlsx'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    continue

                original_df = df.copy()  # Copia original para validación
                df = df.applymap(lambda x: x.replace(search_term, replace_term) if isinstance(x, str) else x)

                if file.endswith('.csv'):
                    df.to_csv(file, index=False)
                elif file.endswith('.xlsx'):
                    df.to_excel(file, index=False, engine='openpyxl')

                # Validación opcional
                if not self.validate_replacement(original_df, df, search_term, replace_term):
                    messagebox.showwarning("Advertencia", f"No se reemplazaron todas las ocurrencias en {file}")

            except Exception as e:
                messagebox.showerror("Error", f"Error al reemplazar en {file}: {e}")
                return

        messagebox.showinfo("Reemplazo Completo", "El reemplazo se ha completado en todos los archivos seleccionados.")

    def validate_replacement(self, original_df, modified_df, search_term, replace_term):
        """
        Valida si todas las ocurrencias de search_term han sido reemplazadas por replace_term.
        """
        original_occurrences = (original_df.applymap(lambda x: search_term in x if isinstance(x, str) else False)).sum().sum()
        modified_occurrences = (modified_df.applymap(lambda x: replace_term in x if isinstance(x, str) else False)).sum().sum()
        return original_occurrences == modified_occurrences
