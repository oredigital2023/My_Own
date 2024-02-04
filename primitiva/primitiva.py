import pandas as pd
import random
import sys
import datetime as dt



#sys.stdout = open('salida_programa.txt', 'w')


def main():
# Imprimir la fecha actual
    print(f"Fecha actual: {dt.date.today()}")

    excel_file = input("Nombre del archivo Excel: ")
    if validar_archivo(excel_file):
        data_frame = pd.read_excel(excel_file, parse_dates=["fecha"])
        print(f"DataFrame: {data_frame}")
        combinacion_ganadora = generar_combinacion(data_frame)
        print(f"Tipos de datos del DataFrame: {data_frame.dtypes}")

        print("Combinación Ganadora:", combinacion_ganadora)
    else:
        print("Error al cargar el archivo")
    #sys.stdout.close()

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
    # Calcular la frecuencia de cada número en los últimos 30 días
    fecha_fin = dt.date.today()
    fecha_inicio = fecha_fin - dt.timedelta(days=365)
    frecuencias = calcular_frecuencias(datos)
    numeros = frecuencias["numero"]
    numeros = numeros.astype(int)
    frecuencias_rango = {numero: calcular_frecuencia_por_fecha_rango(numero, fecha_inicio, fecha_fin, frecuencias) for numero in numeros} #range(1, 50)
    #print(f"Fecha fin: {fecha_fin}")
    print(f"Numeros en frecuencia: {numeros}")
    print(f"Esto es fecuencias: {frecuencias}")
    print(f"Esto es fecuencias_rango: {frecuencias_rango}")
    

    # Seleccionar los 6 números con mayor frecuencia en los últimos 30 días
    probabilidades = pd.Series(frecuencias_rango).sort_values(ascending=False)
    combinacion = seleccionar_numeros(probabilidades)
    #print(f"Esto es probabilidades: {probabilidades}")
    # Agregar número de reintegro
    reintegro = seleccionar_reintegro_probabilidades(datos)
    combinacion.append(reintegro)

    # Mover el número de reintegro a la séptima posición
    combinacion.insert(6, combinacion.pop())

    return combinacion

"""
def calcular_frecuencias(datos):
    frecuencias = {i: {
    "numero" : i,  #agrege esta columna. si no funciona borrar
    "frecuencia": 0,
    "fechas": []
    } for i in range(1, 50)}

    for _, sorteo in datos.iterrows():
        numeros_sorteo = sorteo[['n1', 'n2', 'n3', 'n4', 'n5', 'n6']].tolist()
        fecha_sorteo = sorteo['fecha'].date()

        for numero in numeros_sorteo:
            frecuencias[numero]['frecuencia'] += 1
            frecuencias[numero]['fechas'].append(fecha_sorteo)
    devolver = pd.DataFrame(list(frecuencias.values()))
    print(f"Nombres de las columnas: {devolver.columns}")

    print(f"Frecuencia en Calcular Frecuencias: {devolver}")
    return devolver
    #return pd.DataFrame(frecuencias).T
    """
def calcular_frecuencias(datos):
    frecuencias = []

    for _, sorteo in datos.iterrows():
        numeros_sorteo = sorteo[['n1', 'n2', 'n3', 'n4', 'n5', 'n6']].tolist()
        fecha_sorteo = sorteo['fecha'].date()

        for numero in numeros_sorteo:
            # Buscar si el número ya está en la lista de frecuencias
            index = next((i for i, item in enumerate(frecuencias) if item['numero'] == numero), None)

            if index is not None:
                # Si el número ya está en la lista, actualizar frecuencia y fechas
                frecuencias[index]['frecuencia'] += 1
                frecuencias[index]['fechas'].append(fecha_sorteo)
            else:
                # Si el número no está en la lista, agregar nuevo elemento
                frecuencias.append({'numero': numero, 'frecuencia': 1, 'fechas': [fecha_sorteo]})

    devolver = pd.DataFrame(frecuencias)
    #print(f"Nombres de las columnas: {devolver.columns}")
    #print(f"Frecuencia en Calcular Frecuencias: {devolver}")
    return devolver
"""
def calcular_frecuencias(datos):
    frecuencias = []

    for _, sorteo in datos.iterrows():
        numeros_sorteo = sorteo[['n1', 'n2', 'n3', 'n4', 'n5', 'n6']].tolist()
        fecha_sorteo = sorteo['fecha'].date()

        for numero in range(1, 50):
            # Buscar si el número ya está en la lista de frecuencias
            index = next((i for i, item in enumerate(frecuencias) if item['numero'] == numero), None)

            if index is not None:
                # Si el número ya está en la lista, actualizar frecuencia y fechas
                frecuencias[index]['frecuencia'] += numeros_sorteo.count(numero)
                frecuencias[index]['fechas'].append(fecha_sorteo)
            else:
                # Si el número no está en la lista, agregar nuevo elemento
                frecuencias.append({'numero': numero, 'frecuencia': numeros_sorteo.count(numero), 'fechas': [fecha_sorteo]})

    devolver = pd.DataFrame(frecuencias)
    print(f"Nombres de las columnas: {devolver.columns}")
    print(f"Frecuencia en Calcular Frecuencias: {devolver}")
    return devolver
"""


def calcular_frecuencia_por_fecha_rango(numero, fecha_inicio, fecha_fin, frecuencias):
    #fechas_numero = frecuencias[numero]['fechas']
    #fechas_rango = [fecha for fecha in fechas_numero if fecha_inicio <= fecha <= fecha_fin]
    #return len(fechas_rango)
    #print(f"Frecuencias antes de if: {frecuencias}")
    print(f"Número buscado: {numero}")
    if numero in frecuencias:
        fechas_numero = frecuencias [numero]['fechas']
        fechas_rango = [fecha for fecha in fechas_numero if fecha_inicio <= fecha <= fecha_fin]
        print(f"fecha numero: {fechas_numero}")
        print(f"fecha rango: {fechas_rango}")
        len_fechas_rango = len(fechas_rango)
        print(f"len_fecha_rango: {len_fechas_rango}")
        return len(len_fechas_rango)
    else:
        print("Numero en frecuencias = 0")
        return 0


def seleccionar_numeros(probabilidades):
    # Ordenar la DataFrame por probabilidad de aparicion
    probabilidades = probabilidades.sort_values(ascending=False)

    # Selecciona los 12 numeros con mayor probabilidad de aparicion
    combinados = probabilidades.head(12).index.to_list()

    # Selecciona seis numeros aleatorios entre los 12
    combinados_aleatorios = random.sample(combinados, 6)
    combinados_aleatorios.sort()

    return combinados_aleatorios


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