# 🔢 Diccionario que contiene los números del 0 al 9
# Cada número es una matriz de 5 filas x 3 columnas
# 1 = píxel encendido (█)
# 0 = píxel apagado (espacio)
numeros = {
    "0": [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    "1": [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
    "2": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    "3": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    "4": [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
    "5": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    "6": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    "7": [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
    "8": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    "9": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
}


def mostrar_display(lista_numeros):
    #Convertimos todos los números a string y aseguramos 3 dígitos
    lista_numeros = [str(n).zfill(3) for n in lista_numeros]

    #Recorremos cada número de la lista
    for numero in lista_numeros:
        print(f"\nNúmero: {numero}")  # título

        #Cada número tiene 5 filas (alto del display)
        for fila in range(5):
            linea = ""  # aquí armamos la línea completa

            #Recorremos cada dígito del número (ej: "115" → '1','1','5')
            for digito in numero:
                matriz = numeros[digito]  # obtenemos su matriz

                #Recorremos cada columna (3 columnas por dígito)
                for col in range(3):
                    # Si es 1 → dibuja bloque █
                    # Si es 0 → dibuja espacio
                    linea += "█" if matriz[fila][col] == 1 else " "

                linea += "  "  # espacio entre dígitos

            print(linea)  # imprimimos la fila completa


#Lista de números que quieres mostrar
lista = [5, 23, 115, 7]

#Llamamos a la función
mostrar_display(lista)