import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

#fig = plt.figure()  #se crea una figura sin axes
#fig, ax = plt.subplots() #una figura con un sigle axes
#fig, axs =  plt.subplots(2, 2) # una figura con una cuadricula de ejes 2x2 
# una figura con un eje a la izquierda y dos a la derecha:
#fig, axs = plt.subplot_mosaic([['left', 'right_top'],['left', 'right_bottom']])
#plt.show()

def main():
    excel_file = input("Excel file name: ")
    data_frame = file_upload(excel_file)
    
    if data_frame is not None:
        print(data_frame)
    else:
        print("Error uploading file")
        
    total_income, total_cost, final_balance = analyze_finances(data_frame)   

    plot_finances(total_income, total_cost, final_balance)

def file_upload(file):
    try: 
        data = pd.read_excel(file)
        data["Date"] = pd.to_datetime(data["Date"])
        return data 
    except FileNotFoundError: 
        print("File not found. Check that the name or path is correct.")
        return None


    
def analyze_finances(data):
    total_income = data[data["Transaction Type"] == "Income"]["Amount"].sum()
    total_cost = data[data["Transaction Type"] == "Spent"]["Amount"].sum()
    final_balance = total_income - total_cost
    return total_income, total_cost, final_balance
"""
def plot_finances(total_income, total_cost, final_balance):
    #Nombre de las categorias para el grafico de barras
    
    categories = ["Total Income", "Total Cost", "Final Balance"]

    #Valores correspondientes a las categorias
    values = [total_income, total_cost, final_balance]
    print(values)
    #Crear grafico de barras
    plt.bar(categories, values, color=["green", "red", "blue"])

    #Anadir etiquetas y titulo
    plt.xlabel = ("Categorie")
    plt.ylabel = ("Amount")
    plt.title = ("Monthly Financial Analysis")
    #plt.xticks(rotation=45)
    for i, value in enumerate(values):
        plt.text(i, value, f"${format(value, ',.2f')}", ha="center", va="center", rotation=0)
    """
    
def plot_finances(total_income, total_cost, final_balance):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    categories = ["Total Income", "Total Cost", "Final Balance"]
    values = [total_income, total_cost, final_balance]
    
    ax.bar(categories, values, zs=0, zdir='y', width=0.8, color=['green', 'yellow', 'blue'], edgecolor='black', alpha=1, linewidth=2)
    
    ax.set_title("Monthly Financial Analysis", color='red', fontsize=14)
    ax.set_xlabel("Categorie", color='red')
    ax.set_ylabel("Amount", color='red')
    ax.set_zlabel("Value", color='red')

    for i, value in enumerate(values):
        ax.text(i, value, 0, f"${format(value, ',.2f')}", ha="center", va="bottom", fontsize=10)

    plt.show()

# Ejemplo de uso:
#expense_percentage = [30, 40, 15, 10, 5]
#plot_finances(expense_percentage)

    #plt.show()

if __name__ == "__main__":
    main()


