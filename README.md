<h1 style="text-align: center;">UNIVERSIDAD NACIONAL DEL ALTIPLANO PUNO</h1>

<h2 style="text-align: center;">FACULTAD DE INGENIERÍA ELÉCTRICA, ELECTRÓNICA Y SISTEMAS</h2>

<h3 style="text-align: center;">ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</h3>

# Proyecto Final de Programación Orientada a Objetos II

Presentamos el trabajo encargado sobre el análisis de datos meteorológicos en el Perú con Python, utilizando Python, Tkinter, MySQL y Google Colab (para realizar algunas pruebas). El sistema facilita el registro, búsqueda y visualización de datos, así como la generación de gráficos mensuales y una posible predicción para el mes siguiente gracias a la IA, basándose en los datos previos. [SENAMHI](https://www.senamhi.gob.pe/?&p=estaciones).


## Autores

- Jhon Elias Aguilar Anccori (230433)
- Ever Pacha Sayhua (229665)
- William Yeferson Condori Quispe (230320)

## Docente

Ing. Aldo Hernan Zanabria Galvez

## Confguración del entorno ###

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

## Conclusión

Este proyecto demuestra un enfoque robusto y multifacético para el análisis de datos meteorológicos, combinando técnicas de programación, bases de datos y análisis predictivo. La integración de estas herramientas permite una comprensión más profunda del comportamiento climático en el Perú y ofrece un sistema flexible y extensible para la gestión y análisis de grandes volúmenes de datos meteorológicos. El uso de IA para predicciones futuras agrega un valor significativo al permitir una planificación más eficaz basada en datos históricos. Es factible poder modificar la base de datos y tambi´en poder actualizarlos al presente en el que estamos.

## Video
La explicación de los pasos realizados por parte de cada integrante se subirá en el video  [Video explicando](https://www.youtube.com/watch?v=ED3IKcMK6aY&ab_channel=JhonyAguilar). y los códigos usados.

## Archivos filtrados
En la primera parte del video hay archivos CSV para la base de datos y las visualizacione. [Archivos filtrados](https://drive.google.com/drive/folders/1azGwbzTU9VifuwGV1ItdOm3IuBtCpIOX?usp=sharing).
