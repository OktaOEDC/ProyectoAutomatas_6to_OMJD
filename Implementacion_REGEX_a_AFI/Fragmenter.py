"""
El fragmentador analizará todos los fragmentos de una cadena
procesada para saber que tan dentro estan en una cadena
para así irlos resolviendo de adentro hacia afuera.
Farmentos chiquitos primero (muy dentro de la recursion)
"""

from sympy import false


class regexFragmenter():
    def __init__(self, union: str, star: str):
        self.fragmentTree = {}
        self.UNION = union
        self.STAR = star
        pass

    def findMaximunRecursionLevel(self, chain: str):
        # El nivel maximo de recursion es el numero más alto
        #  de parentesis de entrada que puedes encontrar en 
        #  algun caracter menos el numero de cierres
        currentRecursionlevel = 0
        maximunRecursionlevel = 0 
        for char in chain:
            if(char == "("):
                currentRecursionlevel  +=1
                if(currentRecursionlevel > maximunRecursionlevel):
                    maximunRecursionlevel = currentRecursionlevel
            elif(char==")"):
                currentRecursionlevel -= 1
            pass
        return maximunRecursionlevel

    def fragmentByRecursion(self, chain: str, maximunRecursionLevel: int):
        # Divide
        #  la cadena varias veces por nivel de fragmentación
        #  creando varias listas
        for level in range(maximunRecursionLevel):
            currentRecursionLevel = -1
            writingList = False
            templistString = ""
            templist = []
            self.fragmentTree[level] = {}
            charIndex = 0
            startingIndex = 0
            endingIndex = 0
            fragmentNumber = 0

            while(charIndex < len(chain)):
                #Buscar el nivel de recursion actual
                char = chain[charIndex]
                if(char == "("):
                    currentRecursionLevel  += 1
                elif(char == ")"):
                        currentRecursionLevel -= 1

                if(currentRecursionLevel == level):
                    writingList = True
                    startingIndex = 0


                if(writingList):
                    templist.append(char)

                if((writingList) and (currentRecursionLevel+1) == level and (char == ")")):
                    # Revisar si el siguiente caracter de este es asterisco, para llevarnoslo tambien
                    #  y saltarnoslo en la siguiente iteracion de esta recursion
                    endingIndex = charIndex
                    try:
                        if(chain[charIndex+1]==self.STAR):
                            templist.append(self.STAR)
                            charIndex += 1
                            endingIndex += 1
                    except:
                        # Era el final de la cadena por lo tanto no hay asterisco
                        # si alguien sabe una forma más limpia de evitar esto digame
                        pass
                    writingList = False
                    templistString = "".join(templist)
                    self.fragmentTree[level][f"fragment{fragmentNumber}"] = {}
                    self.fragmentTree[level][f"fragment{fragmentNumber}"]["chain"] = templistString
                    self.fragmentTree[level][f"fragment{fragmentNumber}"]["indexes"] = (startingIndex,endingIndex)
                    fragmentNumber += 1
                    templist = []

                if((not writingList) and (char == self.UNION)):
                    self.fragmentTree[level][f"fragment{fragmentNumber}"] = {}
                    self.fragmentTree[level][f"fragment{fragmentNumber}"]["chain"] = self.UNION
                    self.fragmentTree[level][f"fragment{fragmentNumber}"]["indexes"] = (charIndex,charIndex)
                    fragmentNumber += 1                    
                    pass

                templistString = "".join(templist)
                charIndex += 1