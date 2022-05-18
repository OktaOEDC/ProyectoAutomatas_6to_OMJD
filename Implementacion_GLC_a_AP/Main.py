from ast import Delete
from pickle import FALSE


def main():
    datainput() #recoleccion de datos



def datainput():
    #leer y separar las reglas por ','
    Reglas=input(print('Introduzca todas las reglas separadas por una \',\' \n la regla tiene que ser escritade la siguiente forma: S->a|bc|D: ')).strip().replace(" ","").split(",")

    #llamar al separador para generar un diccionario con las Variables y lo que producen.
    separador(Reglas)



def separador(Reglas):
    diccionario={}
    Variables=[]
    for i in Reglas:
        i= i.split('->')
        #agregar i[0] a mi lista de variables
        Variables.append(i[0])
        #dividir los resultantes de las reglas y crear un diccionario con las mismas
        diccionario[i[0]]=i[1].split('|')
    #validar la informacion
    validarVariables(Variables,diccionario)#Las variables se agregan al array en orden, por lo que siempre Variables[0] es la variable inicial.
    
    

def validarVariables(Variables=[], diccionario={}):
    n=True #Si en algun punto n!= True, las entradas no son correctas.
    alfabetoVariables=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    while n==True:
        #validar las Variables
        for i in Variables:
            if len(i)>1:
                print('Una de las variables no es independiente.')
                n=False
                break
            if i not in alfabetoVariables:
                print('Una de las variables no es una letra mayúscula del alfabeto.')
                n=False
                break
        #Generar terminales
        terminales=generarTerminales(Variables, diccionario)
        #Validar terminales
        terminales=validarTerminales(terminales,alfabetoVariables,Variables)


        if n==True:
            print('No se encontro ningun error, programa ejecutado con exito')
            print('Las variables son: ',Variables)
            print('Las terminales son: ',terminales)
            print('las reglas son: ',diccionario)
            n=False



def validarTerminales(terminales=[],alfabetoVariables=[],Variables=[]):
        #si un valor en 'terminales' se encuentra en 'alfabetoVariables' removerlo.
    for i in terminales:
        if i in alfabetoVariables:
            if i not in Variables:
                errorVariableNoDeterminada() #caso especial.
            terminales.remove(i)
    terminales=list(dict.fromkeys(terminales)) #remover duplicados en las terminales
    return(terminales)



def errorVariableNoDeterminada(): #Caso utilizado en 'validarTerminales' para cuando una variable es utilizada como parte de un producto, pero no produce nada.
    print('Se ha detectado una variable utilizada que no contiene ninguna regla, el lenguaje introducido no es valido, el programa se terminara.')
    quit()



def generarTerminales(Variables=[], diccionario={}):
    terminales=[]

    #agregar a terminales todos los productos de las reglas
    for i in Variables:
        for u in diccionario[i]:
            terminales.append(u)

    #separar los valores de los productos para que queden solos
    for i in terminales:
        if len(i)>1:
            x=" ".join(i).split(" ")
            for z in x:
                terminales.append(z)
            terminales.remove(i)
    return(terminales)

main()