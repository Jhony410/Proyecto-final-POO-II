USE meteorologia_nueva;

CREATE TABLE datos_meteorologicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad VARCHAR(255),
    ano INT,
    mes INT,
    dia INT,
    temperatura FLOAT,
    temperatura_maxima FLOAT,
    temperatura_minima FLOAT,
    humedad_relativa FLOAT,
    velocidad_viento FLOAT,
    direccion_viento VARCHAR(255),
    latitud FLOAT,
    longitud FLOAT
);
