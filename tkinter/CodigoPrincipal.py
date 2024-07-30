'''
Maneja con base datos
'''

import os
import mysql.connector
import pandas as pd
from mysql.connector import Error
from tkinter import Tk, Frame, Label, Button, Entry, messagebox, PhotoImage
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sqlalchemy import create_engine
# Función para crear conexión a MySQL a través de HeidySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='u230320.piruw.com',  # Este debe ser el host del servidor remoto
            database='u230320_ejemplo',  # Asegúrate de que este sea el nombre correcto de la base de datos
            user='u230320_williecq',  # Usuario
            password='2004'  # Contraseña
        )
        if connection.is_connected():
            print("Conexión a MySQL exitosa")
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error al conectar con MySQL: {e}")
        return None

# Función para cargar archivos CSV desde un directorio a la base de datos
def load_csv_files_to_db(directory):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                ciudad = os.path.splitext(filename)[0]  # Nombre de la ciudad según el nombre del archivo
                file_path = os.path.join(directory, filename)
                print(f"Cargando archivo: {file_path}")

                data = pd.read_csv(file_path)
                for _, row in data.iterrows():
                    try:
                        cursor.execute("""
                            INSERT INTO datos_meteorologicos (ciudad, ano, mes, dia, temperatura, temperatura_maxima, temperatura_minima, humedad_relativa, velocidad_viento, direccion_viento)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (ciudad, row['Año'], row['Mes'], row['Día'], row['Temperatura'], row['Temperatura máxima'], row['Temperatura mínima'], row['Humedad relativa'], row['Velocidad del viento'], row['Direccion del viento']))
                    except Error as e:
                        print(f"Error al insertar datos para la ciudad {ciudad}: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Información", "Archivos CSV cargados exitosamente")

# Función para obtener datos meteorológicos de la base de datos
def get_weather_data(city, date):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM datos_meteorologicos 
                WHERE ciudad = %s AND CONCAT(ano, '-', LPAD(mes, 2, '0'), '-', LPAD(dia, 2, '0')) = %s
            """, (city, date))
            result = cursor.fetchone()
            cursor.fetchall()  # Leer todos los resultados restantes, si los hay
            return result
        except Error as e:
            print(f"Error al obtener datos meteorológicos: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Función para obtener datos mensuales
def get_monthly_data(city, data_type):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(f"""
                SELECT ano, mes, AVG({data_type}) as avg_value FROM datos_meteorologicos 
                WHERE ciudad = %s 
                GROUP BY ano, mes
                ORDER BY ano, mes
            """, (city,))
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al obtener datos mensuales: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Función para graficar datos mensuales
def plot_monthly_data(city, data_type, data_label):
    data = get_monthly_data(city, data_type)
    if data:
        months = [f"{row['ano']}-{row['mes']:02d}" for row in data]
        values = [row['avg_value'] for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(months, values, marker='o')
        plt.title(f'{data_label} Mensual Promedio en {city}')
        plt.xlabel('Mes')
        plt.ylabel(f'{data_label} Promedio')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Información", "No se encontraron datos mensuales para la ciudad seleccionada")

# Función para obtener datos de temperatura mínima y máxima
def get_temperature_data(city):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT ano, mes, AVG(temperatura_minima) as temp_min, AVG(temperatura_maxima) as temp_max 
                FROM datos_meteorologicos 
                WHERE ciudad = %s 
                GROUP BY ano, mes
                ORDER BY ano, mes
            """, (city,))
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error al obtener datos de temperatura: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Función para graficar el mapa de calor
def plot_heatmap(city):
    data = get_temperature_data(city)
    if data:
        df = pd.DataFrame(data)
        df_pivot_min = df.pivot(index="mes", columns="ano", values="temp_min")  # Para el mapa de calor de temperatura mínima

        plt.figure(figsize=(10, 8))
        sns.heatmap(df_pivot_min, annot=True, fmt=".1f", cmap="coolwarm", cbar_kws={'label': 'Temperatura Mínima (°C)'})
        plt.title(f'Mapa de Calor de Temperatura Mínima en {city}')
        plt.xlabel('Año')
        plt.ylabel('Mes')
        plt.show()

        df_pivot_max = df.pivot(index="mes", columns="ano", values="temp_max")  # Para el mapa de calor de temperatura máxima

        plt.figure(figsize=(10, 8))
        sns.heatmap(df_pivot_max, annot=True, fmt=".1f", cmap="coolwarm", cbar_kws={'label': 'Temperatura Máxima (°C)'})
        plt.title(f'Mapa de Calor de Temperatura Máxima en {city}')
        plt.xlabel('Año')
        plt.ylabel('Mes')
        plt.show()
    else:
        messagebox.showinfo("Información", "No se encontraron datos de temperatura para la ciudad seleccionada")

def prepare_data(ciudad, data_type):
    # Crear conexión a la base de datos
    engine = create_engine('mysql+mysqlconnector://root:discjockey@localhost/meteorologia_nueva')
    
    # Definir la consulta SQL
    query = """
    SELECT ano, mes, dia, temperatura, temperatura_maxima, temperatura_minima, 
           humedad_relativa, velocidad_viento, direccion_viento, latitud, longitud 
    FROM datos_meteorologicos 
    WHERE ciudad = %s
    """

    # Ejecutar la consulta SQL
    print("Ejecutando consulta SQL")
    data = pd.read_sql(query, engine, params=[(ciudad,)])
    print("Consulta SQL ejecutada con éxito")

    # Mostrar los nombres de las columnas
    print("Columnas del DataFrame:", data.columns)

    # Verificar y crear columna 'fecha'
    if 'ano' in data.columns and 'mes' in data.columns and 'dia' in data.columns:
        print("Columnas de fecha encontradas, creando columna 'fecha'")
        data = data.rename(columns={'ano': 'year', 'mes': 'month', 'dia': 'day'})
        data['fecha'] = pd.to_datetime(data[['year', 'month', 'day']])
        data.set_index('fecha', inplace=True)  # Opcional: establece la columna 'fecha' como índice
        print("Columna 'fecha' creada con éxito")
    else:
        print("Faltan columnas de fecha en el DataFrame")

    # Asegurarse de que la columna requerida para el modelo está presente
    if data_type not in data.columns:
        print(f"Columna '{data_type}' no encontrada en el DataFrame")
        return None

    return data

def train_polynomial_model(data, feature, degree=2):
    X = np.arange(len(data)).reshape(-1, 1)  # Creación de índice temporal
    y = data[feature].values

    # Generar características polinómicas
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Error cuadrático medio: {mse}")
    
    return model, poly, X, y

def predict_future_polynomial(model, poly, data, feature, months_to_predict):
    days_per_month = 30  # Aproximadamente, puedes ajustar según la necesidad
    total_days = months_to_predict * days_per_month

    last_date = data.index[-1]
    if not isinstance(last_date, pd.Timestamp):
        last_date = pd.to_datetime(last_date)
    
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=total_days)
    future_index = np.arange(len(data), len(data) + total_days).reshape(-1, 1)
    
    # Transformar los índices futuros en características polinómicas
    future_index_poly = poly.transform(future_index)
    
    # Predecir los valores futuros
    future_predictions = model.predict(future_index_poly)
    
    future_data = pd.DataFrame(data={feature: future_predictions}, index=future_dates)
    
    return future_data

# Función para graficar predicciones    
def plot_predictions(data, future_data, feature, city):
    plt.figure(figsize=(12, 6))  # Ajusta el tamaño si es necesario
    plt.plot(data.index, data[feature], label='Datos Históricos')
    plt.plot(future_data.index, future_data[feature], label='Predicciones Futuras', linestyle='--')
    plt.title(f'Predicción de {feature} en {city}')
    plt.xlabel('Fecha')
    plt.ylabel(f'{feature}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Clase para la interfaz gráfica
class Ventana(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)  # Corrección del error tipográfico
        self.master = master
        self.master.state('zoomed')  # Para que la ventana se abra en pantalla completa
        self.master.title('Puno - Clima')
        self.master.resizable(True, True)  # Permite redimensionar la ventana
        self.frames = {}  # Inicializar el diccionario frames
        self.create_widgets()

    def create_widgets(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame_principal = Frame(self.master, bg='white', highlightbackground='deep pink', highlightthickness=2)
        self.frame_principal.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        Label(self.frame_principal, text='Ciudad:', font=('Comic Sans MS', 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_ciudad = Entry(self.frame_principal, font=('Comic Sans MS', 12), highlightbackground='DarkOrchid1', highlightthickness=2)
        self.entry_ciudad.grid(row=0, column=1, padx=5, pady=5)

        Label(self.frame_principal, text='Fecha:', font=('Comic Sans MS', 12)).grid(row=0, column=2, padx=5, pady=5)
        self.calendario = DateEntry(self.frame_principal, width=12, background='DarkOrchid1', foreground='green2', bd=2, date_pattern='yyyy-mm-dd')
        self.calendario.grid(row=0, column=3, padx=5, pady=5)

        self.bt_buscar = Button(self.frame_principal, text='Buscar', bg='lightblue', command=self.buscar_datos)
        self.bt_buscar.grid(row=0, column=4, padx=5, pady=5)

        self.bt_cargar_csv = Button(self.frame_principal, text='Cargar CSV a MySQL', bg='lightblue', command=self.cargar_csv)
        self.bt_cargar_csv.grid(row=0, column=5, padx=10, pady=5)

        self.data_options = ["temperatura", "temperatura_maxima", "temperatura_minima", "humedad_relativa", "velocidad_viento", "direccion_viento"]
        self.data_labels = ["Temperatura (°C)", "Temperatura Máxima (°C)", "Temperatura Mínima (°C)", "Humedad Relativa (%)", "Velocidad del Viento (m/s)", "Dirección del Viento (°)"]
        self.combobox_data = ttk.Combobox(self.frame_principal, values=self.data_labels, state="readonly")
        self.combobox_data.grid(row=0, column=6, padx=10, pady=5)
        self.combobox_data.current(0)

        self.bt_graficar_mensual = Button(self.frame_principal, text='Graficar Datos Mensuales', bg='lightblue', command=self.graficar_mensual)
        self.bt_graficar_mensual.grid(row=0, column=7, padx=10, pady=5)

        self.bt_graficar_mapa_calor = Button(self.frame_principal, text='Mapa de Calor de Temperaturas', bg='lightblue', command=self.graficar_mapa_calor)
        self.bt_graficar_mapa_calor.grid(row=0, column=8, padx=10, pady=5)

        # Añadir el botón para predecir tendencias
        self.bt_predecir = Button(self.frame_principal, text='Predecir Tendencias', bg='lightblue', command=self.predecir_tendencias)
        self.bt_predecir.grid(row=0, column=9, padx=10, pady=5)

        self.create_info_frame('Temperatura (°C)', 1, 0, 'temperatura.png')
        self.create_info_frame('Temperatura Máxima (°C)', 1, 1, 'temp_max.png')
        self.create_info_frame('Temperatura Mínima (°C)', 1, 2, 'temp_min.png')
        self.create_info_frame('Humedad Relativa (%)', 2, 0, 'humedad.png')
        self.create_info_frame('Velocidad del Viento (m/s)', 2, 1, 'viento.png')
        self.create_info_frame('Dirección del Viento (°)', 2, 2, 'direccionviento.png')

    def create_info_frame(self, label_text, row, col, img_file):
        frame = Frame(self.master, bg='white', highlightbackground='deep pink', highlightthickness=2)
        frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        self.master.grid_rowconfigure(row, weight=1)
        self.master.grid_columnconfigure(col, weight=1)

        img = PhotoImage(file=img_file)
        img_label = Label(frame, image=img, bg='white')
        img_label.image = img  # Guardar una referencia para evitar que se borre la imagen
        img_label.grid(row=0, column=0, padx=10, pady=5)

        Label(frame, text=label_text, font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=10, pady=5)
        data_label = Label(frame, text='N/A', font=('Arial', 12))
        data_label.grid(row=2, column=0, padx=10, pady=5)

        self.frames[label_text] = data_label

    def buscar_datos(self):
        ciudad = self.entry_ciudad.get()
        fecha = self.calendario.get_date().strftime('%Y-%m-%d')
        print(f"Buscando datos para la ciudad: {ciudad} en la fecha: {fecha}")

        weather_data = get_weather_data(ciudad, fecha)
        if weather_data:
            self.frames['Temperatura (°C)'].config(text=f"{weather_data['temperatura']} °C")
            self.frames['Temperatura Máxima (°C)'].config(text=f"{weather_data['temperatura_maxima']} °C")
            self.frames['Temperatura Mínima (°C)'].config(text=f"{weather_data['temperatura_minima']} °C")
            self.frames['Humedad Relativa (%)'].config(text=f"{weather_data['humedad_relativa']} %")
            self.frames['Velocidad del Viento (m/s)'].config(text=f"{weather_data['velocidad_viento']} km/h")
            self.frames['Dirección del Viento (°)'].config(text=f"{weather_data['direccion_viento']} °")
        else:
            messagebox.showinfo("Información", "No se encontraron datos para la ciudad y fecha seleccionadas")

    def cargar_csv(self):
        directory = r"D:\tkinter\datoscsv"  # Ajusta esto a tu directorio correcto
        load_csv_files_to_db(directory)

    def graficar_mensual(self):
        ciudad = self.entry_ciudad.get()
        if ciudad:
            selected_index = self.combobox_data.current()
            data_type = self.data_options[selected_index]
            data_label = self.data_labels[selected_index]
            plot_monthly_data(ciudad, data_type, data_label)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese una ciudad para graficar los datos mensuales")

    def graficar_mapa_calor(self):
        ciudad = self.entry_ciudad.get()
        if ciudad:
            plot_heatmap(ciudad)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese una ciudad para generar el mapa de calor")
    
    def predecir_tendencias(self):
        ciudad = self.entry_ciudad.get()
        if not ciudad:
            messagebox.showwarning("Advertencia", "Por favor ingrese una ciudad para predecir las tendencias")
            return
        
        selected_index = self.combobox_data.current()
        if selected_index == -1:
            messagebox.showwarning("Advertencia", "Por favor seleccione un tipo de dato para la predicción")
            return
        
        data_type = self.data_options[selected_index]
        data_label = self.data_labels[selected_index]
        
        # Preparar los datos
        data = prepare_data(ciudad, data_type)
        if data is not None and not data.empty:
            # Entrenar el modelo polinómico
            model, poly, X, y = train_polynomial_model(data, data_type, degree=3)  # Ajusta el grado del polinomio según sea necesario
            
            # Predecir los próximos 3 meses
            future_data = predict_future_polynomial(model, poly, data, data_type, months_to_predict=3)
            
            # Graficar las predicciones
            plot_predictions(data, future_data, data_type, ciudad)
        else:
            messagebox.showwarning("Advertencia", "No se encontraron datos para la ciudad seleccionada o los datos están vacíos")

# Creación de la ventana principal
if __name__ == "__main__":
    ventana = Tk()
    app = Ventana(ventana)
    ventana.mainloop()
