from ast import Delete, excepthandler
from pickle import EMPTY_LIST, FALSE

from numpy import empty


def main():
    datainput() #recoleccion de datos



def datainput():
    pass
    #leer y separar las reglas por ','
    #Reglas=input(print('Introduzca todas las reglas separadas por una \',\' \n la regla tiene que ser escrita de la siguiente forma: S->a|bc|D: ')).strip().replace(" ","").split(",")

    #llamar al separador para generar un diccionario con las Variables y lo que producen.
    #separador()



def separador(Reglas):
    diccionario={}
    Variables=[]
    for i in Reglas:
        i = i.split('->')
        #dividir los resultantes de las reglas y crear un diccionario con las mismas
        dic_keys=list(diccionario.keys())
        if i[0] in Variables: #Si la variable ya existe, solo agregar los productos a la variable correspondiente.
            #try:
                print(i, 'entre y estos son mis valores')
                if '|' in i[1]:
                    temp=i[1].split('|')
                    print(temp,'mi temp')
                    for valortagregable in temp: #separar los valores para que entren individuales y no como una lista.
                        diccionario[i[0]].append(str(valortagregable))
                else:
                    if type(diccionario[i[0]])!=type(list): #Si el valor de la llave no es una lista, conviertelo y agrega el producto.
                        diccionario[i[0]]=list(diccionario[i[0]])
                        diccionario[i[0]].append(i[1])
                    else:
                        diccionario[i[0]].append(i[1])
            #except:
             #   print('Sus reglas no se encuentran separadas correctamente.')
              #  quit()
        else:
            diccionario[i[0]]=i[1].split('|')
        #agregar i[0] a mi lista de variables
        Variables.append(i[0])
        #Remover variables duplicadas
        Variables=list(dict.fromkeys(Variables))
    #validar la informacion
    return validarVariables(Variables,diccionario)#Las variables se agregan al array en orden, por lo que siempre Variables[0] es la variable inicial.
    
    

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
            return removeEmpty(Variables,terminales,diccionario)
            n=False



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
def errorReglaVacia():
    print('Se ha detectado una regla declarada sin ningun producto, el lenguaje introducido no es valido, el programa terminara.')
    quit()


def removeEmpty(Variables,terminales,diccionario):
    for i in Variables: #Remover vacios en variables
        i=i.strip()
        if i=="":
            Variables.remove(i)
    
    
    for i in terminales: #Remover vacios en terminales
        i=i.strip()
        if i=="":
            terminales.remove(i)
    

    #Remover repetidos en las reglas
    for i in diccionario:
        diccionario[i]=list(dict.fromkeys(diccionario[i]))
    #Remover vacios en reglas    
    for i in diccionario:
        for u in diccionario[i]:
            if u=='':
                diccionario[i].remove(u)
    for i in diccionario: #si existe una regla sin productos, invalidar el programa y salir.
        if bool(diccionario[i])==False:
            errorReglaVacia()
    return transformer(Variables,terminales,diccionario)


def transformer(Variables,terminales,diccionario):
    Reglasqi=f'~,~->{Variables[0]}$'
    Reglasqc=[]
    Reglasqa=f'~,$->~'
    #borrar terminales en el ciclo
    for i in terminales:
        Reglasqc.append(f'{i},{i}->~')
            
    #borrar Variables en el ciclo
    for i in diccionario:
        for u in diccionario[i]:
            Reglasqc.append(f'~,{i}->{u}')

    return finisher(Reglasqi,Reglasqc,Reglasqa)

def finisher(qi,qc,qa):
    print(f'la iniciacion (qi) seria: {qi}')
    print(f'las transiciones de ciclo (qc) serian: {qc}')
    print(f'la transicion de aceptacion (qa) seria: {qa}')
    return [f'la iniciacion (qi) seria: {qi}',f'las transiciones de ciclo (qc) serian: {qc}',f'la transicion de aceptacion (qa) seria: {qa}']
main()