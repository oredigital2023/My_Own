import pandas as pd
import random

def main():
    excel_file = input("Nombre del archivo Excel: ")
    data_frame = file_upload(excel_file)
    
    if data_frame is not None:
        print(data_frame)
    else:
        print("Error al cargar el archivo")


    combinacion_ganadora = generar_combinacion(data_frame)

    # Mostrar resultados
    print("Combinación Ganadora:", combinacion_ganadora)


# Función para cargar datos desde un archivo Excel
def file_upload(file):
    try: 
        data = pd.read_excel(file, parse_dates=["fecha"])
        return data 
    except FileNotFoundError: 
        print("Archivo no encontrado. Verifica que el nombre o la ruta sean correctos.")
        return None
    
# Función para realizar análisis temporal agrupando por fechas
def analisis_temporal(datos, periodo):
    if periodo == 'semana':
        datos_agrupados = datos.groupby(datos['fecha'].dt.isocalendar().week)
    elif periodo == 'mes':
        datos_agrupados = datos.groupby(datos['fecha'].dt.to_period("M"))
    elif periodo == 'ano':
        datos_agrupados = datos.groupby(datos['fecha'].dt.year)
    else:
        print("Período no reconocido. Se realizará el análisis sin agrupar.")
        datos_agrupados = None

    if datos_agrupados is not None:
        frecuencias_temporales = calcular_frecuencias(datos_agrupados)
        print(f"Frecuencias Temporales ({periodo}):")
        print(frecuencias_temporales)

    return frecuencias_temporales

# Función para generar combinación ganadora
def generar_combinacion(datos):
    # Calcular probabilidades basadas en el análisis histórico
    probabilidades = calcular_probabilidades(datos)

    # Seleccionar números basados en las probabilidades calculadas
    combinacion = seleccionar_numeros(probabilidades)

    # Comprobar si se debe incluir un número de reintegro
    if incluir_reintegro():
        reintegro = seleccionar_reintegro(datos)
        combinacion.append(reintegro)
    
    # Realizar análisis temporal agrupando por mes
    frecuencias_temporales = analisis_temporal(datos, "mes")

    return combinacion

# Función para calcular probabilidades de cada número
def calcular_probabilidades(datos):
    frecuencias = calcular_frecuencias(datos)
    total_sorteos = len(datos)
    probabilidades = frecuencias / total_sorteos
    return probabilidades

# Función para calcular la frecuencia de aparición de cada número
def calcular_frecuencias(datos_agrupados):
    frecuencias = {i: 0 for i in range(1, 50)}
    for nombre_grupo, grupo in datos_agrupados:
        for _, sorteo in grupo.iterrows():
            numeros_sorteo = sorteo[['n1', 'n2', 'n3', 'n4', 'n5', 'n6']].tolist()
            for numero in numeros_sorteo:
                frecuencias[numero] += 1
    return pd.Series(frecuencias)

# Función para seleccionar números basados en probabilidades
def seleccionar_numeros(probabilidades):
    seleccionados = []
    for _ in range(6):
        numero_seleccionado = ruleta(probabilidades)
        seleccionados.append(numero_seleccionado)
        probabilidades[numero_seleccionado] = 0
    return seleccionados

# Método de la ruleta para seleccionar un número basado en probabilidades
def ruleta(probabilidades):
    seleccion = random.uniform(0, 1)
    acumulado = 0
    for numero, probabilidad in probabilidades.items():
        acumulado += probabilidad
        if seleccion <= acumulado:
            return numero

# Función para determinar si se incluirá un número de reintegro
def incluir_reintegro():
    return random.uniform(0, 1) <= 1.0

# Función para seleccionar un número de reintegro basado en frecuencias
def seleccionar_reintegro(datos):
    frecuencias_reintegro = datos['R'].value_counts()
    reintegro_seleccionado = frecuencias_reintegro.idxmax()
    return reintegro_seleccionado

if __name__ == "__main__": 
    main()
