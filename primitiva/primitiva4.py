import pandas as pd
import random

def main():
    excel_file = input("Nombre del archivo Excel: ")
    if validar_archivo(excel_file):
        data_frame = pd.read_excel(excel_file, parse_dates=["fecha"])
        combinacion_ganadora = generar_combinacion(data_frame)
    
        print("Combinación Ganadora:", combinacion_ganadora)
    else:
        print("Error al cargar el archivo")


def validar_archivo(archivo):
    try:
        data = pd.read_excel(archivo, parse_dates=["fecha"])
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(e)
        return False


def generar_combinacion(datos):
    # Calcular probabilidades de cada número
    probabilidades = calcular_probabilidades_historicas(datos)

    # Seleccionar números basados en las probabilidades calculadas
    combinacion = seleccionar_numeros(probabilidades)

    # Agregar número de reintegro
    reintegro = seleccionar_reintegro_probabilidades(datos)
    combinacion.append(reintegro)

    # Mover el número de reintegro a la séptima posición
    combinacion.insert(6, combinacion.pop())
    
    """# Comprobar si se debe incluir un número de reintegro
    if incluir_reintegro():
        reintegro = seleccionar_reintegro_probabilidades(datos)
        combinacion.append(reintegro) """

    return combinacion




def calcular_probabilidades_historicas(datos):
    frecuencias_historicas = calcular_frecuencias(datos)
    total_sorteos_historicos = len(datos)
    probabilidades_historicas = frecuencias_historicas / total_sorteos_historicos
    return probabilidades_historicas


def calcular_frecuencias(datos):
    frecuencias = {i: 0 for i in range(1, 50)}
    for _, sorteo in datos.iterrows():
        numeros_sorteo = sorteo[['n1', 'n2', 'n3', 'n4', 'n5', 'n6']].tolist()
        for numero in numeros_sorteo:
            frecuencias[numero] += 1
    return pd.Series(frecuencias)

def seleccionar_numeros(probabilidades):
    # Ordenar la DataFrame por probabilidad de aparicion
    probabilidades = probabilidades.sort_values(ascending=False)

    # Selecciona los 12 numeros con mayor probabilidad de aparicion
    combinados = probabilidades.head(12).index.to_list()

    # Selecciona seis numeros aleatorios entre los 12
    combinados_aleatorios = random.sample(combinados, 6)
    combinados_aleatorios.sort()
    return combinados_aleatorios

"""def seleccionar_numeros(probabilidades):
    seleccionados = []
    for _ in range(6):
        numero_seleccionado = ruleta(probabilidades)
        seleccionados.append(numero_seleccionado)
        probabilidades[numero_seleccionado] = 0
    return seleccionados
"""

"""
def ruleta(probabilidades):
    seleccion = random.uniform(0.3, 1)
    acumulado = 0
    for numero, probabilidad in probabilidades.items():
        acumulado += probabilidad
        if seleccion <= acumulado:
            return numero

"""
def incluir_reintegro():
    return True #random.uniform(0, 1) <= 0.5


def seleccionar_reintegro_probabilidades(datos):
    # Contar el número de veces que aparece cada número de reintegro
    frecuencias = {}
    for _, sorteo in datos.iterrows():
        reintegro = sorteo['R']
        if reintegro not in frecuencias:
            frecuencias[reintegro] = 0
            frecuencias[reintegro] += 1

    # Seleccionar el número con mayor frecuencia
    reintegro_seleccionado = max(frecuencias, key=frecuencias.get)

    return reintegro_seleccionado 


if __name__ == "__main__": 
    main()