import pandas as pd #Se utiliza para cargar uno de esos archivos CSV en un DataFrame y mostrar sus primeras filas.
import os #Se utiliza para listar los archivos en el directorio actual y filtrar los archivos CSV

def process_file(filename): # Define una función
    # Verificacion
    if filename.endswith('.csv'): # Si el archivo termina en csv
        df = pd.read_csv(filename) # Lee el archivo csv
    elif filename.endswith('.xlsx'): # Si el archivo termina en xlsx
        df = pd.read_excel(filename) # Lee el archivo xlsx
    else: # Si el archivo no termina en csv ni xlsx
        raise ValueError("El archivo debe ser un .csv o .xlsx")

    df['datetime'] = pd.to_datetime(df['AÑO / MES / DÍA'] + ' ' + df['HORA'], format='%Y/%m/%d %H:%M')  # Crear columna

    df.set_index('datetime', inplace=True)  # Establecer datetime como el índice

    df.drop(columns=['AÑO / MES / DÍA', 'HORA'], inplace=True)  # Eliminar columnas innecesarias

    for col in df.columns: # Intentar convertir columnas numéricas a float
        try:  # Intentar convertir columnas numéricas a float
            df[col] = df[col].astype(float) # Si se puede convertir, lo convierte
        except ValueError: # Si no se puede convertir, imprime un mensaje de error
            print(f"La columna '{col}' no se pudo convertir a tipo numérico. Se ignorará para el cálculo del promedio.")

    df_daily = df.resample('D').mean() # Calcular promedios diarios

    df_daily = df_daily.round(1) # Redondear valores a un decimal

    day_wise_averages = [] # Generar promedios diarios
    for day in df_daily.index: # Itera sobre cada indice
        day_data = df_daily.loc[day]  # Obtiene los datos de cada indice
        day_avg = day_data.to_dict()  # Convierte los datos a un diccionario
        day_avg['Fecha'] = day.strftime('%Y-%m-%d')  # Agrega la fecha
        day_wise_averages.append(day_avg)  # Agrega el diccionario a la lista

    df_day_wise = pd.DataFrame(day_wise_averages) # Crear un DataFrame con los promedios diarios
    return df_day_wise # Retorna el DataFrame

# Obtener el directorio que contiene los archivos CSV, o solo el nombre del archivo si es uno solo
data_input = input("Ingrese la ruta del directorio que contiene los archivos CSV, o el nombre del archivo si es uno solo: ")

if os.path.isdir(data_input): # Verificar si es un directorio
    for filename in os.listdir(data_input): # Itera sobre cada archivo en el directorio
        if filename.endswith('.csv') or filename.endswith('.xlsx'): # Verificar si el archivo es un csv o un xlsx
            file_path = os.path.join(data_input, filename) # Ruta del archivo
            df_day_wise = process_file(file_path) # Procesar el archivo

            output_folder = './promedios_diarios' # Ruta de la carpeta de salida
            if not os.path.exists(output_folder): # Verificar si la carpeta de salida existe
                os.makedirs(output_folder) # Crear la carpeta de salida si no existe

            output_file = os.path.join(output_folder, f'promedios_diarios_{filename[:-4]}.csv') # Ruta del archivo de salida
            df_day_wise.to_csv(output_file, index=False) # Guardar el DataFrame en un archivo CSV
 
            print(f"Promedios diarios guardados en: {output_file}") # Imprimir mensaje de éxito

else: # Es un solo archivo
    df_day_wise = process_file(data_input) # Procesar el archivo

    output_folder = './promedios_diarios' # Ruta de la carpeta de salida
    if not os.path.exists(output_folder): # Verificar si la carpeta de salida existe
        os.makedirs(output_folder) # Crear la carpeta de salida si no existe

    output_file = os.path.join(output_folder, f'promedios_diarios_{os.path.basename(data_input)[:-4]}.csv') # Ruta del archivo de salida
    df_day_wise.to_csv(output_file, index=False) # Guardar el DataFrame en un archivo CSV

    print(f"Promedios diarios guardados en: {output_file}") # Imprimir mensaje de éxito