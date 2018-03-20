# coding=utf-8
'''
Programa que realiza las graficas a partir de un archivo csv
'''
import e as e
import plotly as plotly


'''
Programa que realiza las graficas a partir de un archivo csv
'''
try:
    import e as e
    import csv
    import sys
    import plotly
    import plotly.offline as py
    import plotly.graph_objs as go
    plotly.tools.set_credentials_file(username='nogala@gmail.com', api_key='mrtEjdnx2Y2M6llWUDxv')
    print("Bibliotecas cargadas correctamente")
except ImportError as e:
    print('La biblioteca ${e} no se cargo adecuadamente')
    sys.exit(1)

def leearchivo(data_file):
    '''
    Funcion que abre un archvio csv y lo regresa como una lista de filas, separadas
    :param archivo:
    :return:
    '''

    with open(data_file, 'rt') as file:
        reader = csv.reader(file, delimiter=";")
        datos = list(reader)
        return datos

def transormadatos(datos):
    '''
    Función que lee el archivo y selecciona las categorias, engargados e id de cada proceso
    :param datos: El contenido del archivo
    :param matrices: Matriz de cada encargado aqui
    :param categorias: Categorias de los procesos
    :return: regresa las matrices y las categorias
    '''

    categorias = {}
    matrices = {}

    for fila in datos:
        fila[0] = str(fila[0]).replace(" ", "")
        if fila[0] is "":
            fila[0] = "No Asignado"
        if str(fila[0]) not in matrices:
            matrices[str(fila[0])] = []
            matrices[str(fila[0])].append([fila[0], str(fila[1]), str(fila[2])])
        else:
            matrices[str(fila[0])].append([fila[0], str(fila[1]), str(fila[2])])
        if str(fila[2]) not in categorias:
            categorias[str(fila[2])] = 0
    return matrices, categorias

def calculaestadisticas(matrices):
    '''
    Calcula las estadisticas de cada uno de los encargados
    :param matrices: Matrices de todos los encargados
    :return: estadisticas de cada categoria
    '''
    estadisticas = {}
    for matrix in matrices:
        datosmatrix = matrices[matrix]
        for elementos in datosmatrix:
            if matrix not in estadisticas:
                estadisticas[matrix] = dict(categorias)
            estadisticas[matrix][elementos[2]] += 1
    return estadisticas

def guardararchivo(final):
    '''
    Guarda el archivo de salida
    :param ruta: es el nombre donde se almacena el archivo
    :return:
    '''
    with open(final, 'wt') as file:
        for matrix in estadisticas:
            cadena = "Encargado, " + str(categorias.keys()).replace("[", "").replace("]", "").replace("\'", "") + "\n"
            print(cadena)
            file.write(cadena)
            cadena = matrix + "    " + "     "
            for cat in estadisticas[matrix]:
                cadena += str(estadisticas[matrix][cat]) + "     " + "      "
            print(cadena)
            file.write(cadena)

def grafica(datos, usuario):
    '''
    Crea los valores de la grafica
    :param datos: estadisticas del usuario
    :param usuario: nombre del usuario
    :return:
    '''
    valorx = datos.keys()
    valory = datos.values()
    trace = go.Bar(
        x=valorx,
        y=valory,
        opacity=0.6,
        name=usuario)
    return trace

def generadatosgraficos(estadisticas):
    '''
    Funcion que genera los valores de las graficas
    :param estadisticas: datos estadisticos de cada usuario
    :return: datos para las graficas de cada usuario
    '''
    data = []
    for persona in estadisticas:
        trace = grafica(estadisticas[persona], persona)
        data.append(trace)
    return data



if __name__ == '__main__':
    ('\n'
     '    Funcion principal para hacer el programa ejecutable desde linea de codigo con\n'
     '    $ python merce.py [data_file] [final] [salida]\n'
     '    ')
    if (len(sys.argv)) != 3:
        ('\n'
         '        Toma los valores default asignados mas adelante \n'
         '        data_file: archivo de origen\n'
         '        final: ruta donde se va a guardar el archivo de estadisticas\n'
         '        salida: ruta donde se guarda la grafica\n'
         '        ')
        data_file = "data_file/Id.csv"
        final = "data_file/final.csv"
        salida = "output/grafica.html"
    else:
        ('\n'
         '        Toma los datos de entrada y asigna los datos de salida de desde la linea de comandos\n'
         '        data_file: archivo de origen\n'
         '        final: ruta donde se va a guardar el archivo de estadisticas\n'
         '        salida: ruta donde se guarda la grafica\n'
         '        ')
        data_file = sys.argv[0]
        final = sys.argv[1]
        salida = sys.argv[2]

    datos = leearchivo(data_file)
    datos.pop(0)

    matrices, categorias = transormadatos(datos)

    estadisticas = calculaestadisticas(matrices)

    guardararchivo(final)

    datosgrafica = generadatosgraficos(estadisticas)

    layout = go.Layout(title="Estadisticas")
    fig = go.Figure(data=datosgrafica, layout=layout)
    py.plot(fig, filename=salida)

