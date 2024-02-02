import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def main():
    excel_file = input("Excel file name: ")
    data_frame = file_upload(excel_file)
    
    if data_frame is not None:
        print(data_frame)
    else:
        print("Error uploading file")

    #type = data_frame.dtypes
    #print(type)

    total_income, total_cost, final_balance =  analyze_finances(data_frame)   
    print(f"Total Income: ${format(total_income,',.2f')}")
    print(f"Total Cost: ${format(total_cost,',.2f')}")
    if final_balance > 0:
        print(f"Final Balance: ${format(final_balance,',.2f')}")
    else:
        print(f"Saldo Negativo: ${format(final_balance,',.2f')}")

    plot_finances(total_income, total_cost, final_balance)
    expense_distribution(data_frame)
    income_extra_analysis(data_frame)

#funcion para cargar datos de un archivo excel
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

def plot_finances(total_income, total_cost, final_balance):
    #Nombre de las categorias para el grafico de barras
    categories = ["Total Income", "Total Cost", "Final Balance"]

    #Valores correspondientes a las categorias
    values = [total_income, total_cost, final_balance]
    #Crear grafico de barras
    final_balance_color = "blue" if final_balance >= 0 else "red"
    colors = ["green", "yellow", final_balance_color]
    plt.bar(categories, values, color=colors, edgecolor='black', zorder=3, alpha=1, linewidth=2)

    #Anadir etiquetas y titulo
    plt.title("Monthly Financial Analysis", color='red', fontsize=14)
    plt.xlabel("Categorie", color='red')
    plt.ylabel("Amount", color='red')
    for i, value in enumerate(values):
        plt.text(i, value, f"${format(value, ',.2f')}", ha="center", va="bottom")
    plt.gcf().set_facecolor('#f0f0f0')  #ajustar el código de color según tus preferencias

    plt.show()

#Analiza la proporción de gastos en cada categoría
def expense_distribution(data):
    #Agrupar por categorias y sumar los gastos para cada categoria
    expense_by_category = data[data["Transaction Type"] == "Spent"].groupby("Category")["Amount"].sum()

    #Calcular la proporcion de gastos en cada categoria
    expense_percentage = expense_by_category / expense_by_category.sum() * 100
    formatted_expense_percentage = expense_percentage.map("{:.2f}%".format)
    #print(f"Expense Percentaje {expense_percentage}")
    #print(f"Formatted expense percentaje {formatted_expense_percentage}")
    print(f"Expense distribution: {formatted_expense_percentage}")
    plt.figure(figsize=(10, 6)) #Tamano del grafico

    #Crear grafico de barras
    expense_percentage.plot(kind="bar", color="blue", edgecolor='black', zorder=3, alpha=1, linewidth=2)

    #Persolanizar el grafico
    plt.title("Distribution of Expenses by Category", color='red', fontsize=14)
    plt.xlabel("Category", color='red')
    plt.ylabel("Expense Percentage", color='red')
    plt.xticks(rotation=45)  #Rotar las etiquetas del eje X para mayor legibilidad

    
    #Mostrar porcentaje encima de las barras
    for i, value in enumerate(expense_percentage):
        plt.text(i, value + 4, formatted_expense_percentage.iloc[i], ha="center", va="center", rotation=45)
    plt.subplots_adjust(bottom=0.23) #ajusta el espacio en la parte inferior
    plt.gcf().set_facecolor('#f0f0f0')  # Puedes ajustar el código de color según tus preferencias

    plt.show()

        
def income_extra_analysis(data):
    # Filtrar ingresos extras
    extra_income = data.loc[(data["Transaction Type"] == "Income") & (data["Description"] == "Extra Income"), "Amount"]

    print("\nIncome Extra Analysis:")
    print(f"Frequency of Extra Income: {len(extra_income)}")
    print(f"Total amount of extra income: ${format(extra_income.sum(), ',.2f')}")
    print(f"Average extra income: ${format(extra_income.mean(), ',.2f')}")


if __name__ == "__main__":
    main()
