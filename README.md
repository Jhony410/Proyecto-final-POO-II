# Proyecto Final

Presentamos el trabajo encargado sobre el análisis de datos meteorológicos en el Perú con Python, utilizando Python, Tkinter, MySQL y Google Colab (para realizar algunas pruebas). El sistema facilita el registro, búsqueda y visualización de datos, así como la generación de gráficos mensuales y una posible predicción para el mes siguiente gracias a la IA, basándose en los datos previos.


## Autores

- Jhon Elias Aguilar Anccori (Email: jhonykey1415@gmail.com)
- Ever Pacha Sayhua (Email: everpachasayhua@gmail.com)
- William Yeferson Condori Quispe (Email: williamyeferson71@gmail.com)


### Confguración del entorno ###

Para la utilización del código y las diferentes acciones que se realizan en el código principal, necesitamos lo siguiente. 

Serán necesarias algunas librerías adicionales:
* import os
* import mysql.connector
* import pandas as pd
* from mysql.connector import Error
* from tkinter import Tk, Frame, Label, Button, Entry, messagebox, PhotoImage
* from tkinter import ttk
* from tkcalendar import DateEntry
* import matplotlib.pyplot as plt
* import seaborn as sns
* import numpy as np
* from sklearn.model_selection import train_test_split
* from sklearn.linear_model import LinearRegression
* from sklearn.metrics import mean_squared_error
* from sklearn.preprocessing import PolynomialFeatures
* from sqlalchemy import create_engine


#### Ejecución web - Colaboratory

Las librerías con las que trabajaremos ya están instaladas en colaboratory, pero en caso de que no puedan importarlas o que no sea la versión correcta, pueden seguir [las instrucciones oficiales](https://colab.research.google.com/notebooks/snippets/importing_libraries.ipynb) para agregarlas.

#### Entorno local

Con el entorno de conda activado, ejecutar:

```bash
$ conda install -c conda-forge cufflinks-py
$ conda install -c conda-forge missingno
```

Para instalar plotly, pueden seguir las [instrucciones oficiales](https://plotly.com/python/getting-started/#installation). Sin embargo, configurar el entorno `jupyter-lab` o `jupyter-notebook` para que efectivamente muestre los gráficos requiere pasos adicionales, también incluidos en la [documentación](https://plotly.com/python/getting-started/#jupyter-notebook-support). Sin embargo, no pudimos hacerlo funcionar en jupyter-lab :( 

### Profesores ###

Teórico con:
* Georgina Flesia
* Ariel Wolfmann

Práctico con:
* Aldana González Montoro
* Rocio Fonseca
* Nehuen González Montoro
* Mario Agustín Sgró
* Alejandro Garcia
* Facundo Godoy
* Josefina Meirovich
* Laura Montes
