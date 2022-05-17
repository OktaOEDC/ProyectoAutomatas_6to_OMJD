"""
El fragmentador analizará todos los fragmentos de una cadena
procesada para saber que tan dentro estan en una cadena
para así irlos resolviendo de adentro hacia afuera.
Farmentos chiquitos primero (muy dentro de la recursion)
"""
class regexFragmenter():
    def __init__(self, union: str, star: str):
        self.fragmentTree = {}
        self.UNION = union
        self.STAR = star
        self.fragmentTree = {}
        pass

    def isThisFragmentLeaf(self, chain: str):
        # Si es una hojita llegamos al punto maximo de recursion para esta parte de la cadena
        if(chain.count("(") == 1):
            return True
        else:
            return False
        pass

    def isChainWhole(self, chain: str):
        currentRecursionLevel = 0
        chainList = list(chain)
        for charIndex in range(len(chain)):
            char = chain[charIndex]
            if(char == "("):
                currentRecursionLevel  +=1
            elif(char==")"):
                currentRecursionLevel -= 1
            if((currentRecursionLevel == 0) and (charIndex == len(chain)-1) or charIndex == len(chain)):
                # Si llegamos al parentesis de cierre antes del fin de la cadena:
                # Tambien consideramos que el parentesis pueda estar antes de un asterisco
                # y no, no es posible que esto pase -> (abc)e dado que todo se parentesiza
                # así que ver una terminal sola al final y confundirla con asterisco no es posible
                return True
            elif((currentRecursionLevel == 0) and ((charIndex != len(chain)-1) or (charIndex != len(chain)))):
                return False

    def fragmentByRecursion(self, chain: str, targetRecursionLevel: int, treeNode: dict):
        # Divide
        #  la cadena varias veces por nivel de fragmentación
        #  creando varias listas

        level = targetRecursionLevel
        currentRecursionLevel = -1
        writingList = False
        templistString = ""
        templist = []
        wroteStartingIndex = False
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
                if(not wroteStartingIndex):
                    startingIndex = charIndex
                    wroteStartingIndex = True


            if(writingList):
                templist.append(char)

            if((writingList) and (currentRecursionLevel+1) == level and (char == ")")):
                ## NOTA -> CHAIN != FRAGMENT; uno es la cadena que llega y otro es el fragmento a recurrir
                # Revisar si el siguiente caracter de este es asterisco, para llevarnoslo tambien
                #  y saltarnoslo en la siguiente iteracion de esta recursion
                endingIndex = charIndex
                isThisFragmentLeaf = self.isThisFragmentLeaf(templistString)
                isChainWhole = self.isChainWhole(chain)
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
                if(chain == "(((a*)*(bc)U(dc))U(cd))"):
                    x = 5
                treeNode[f"fragment{fragmentNumber}"] = {}
                treeNode[f"fragment{fragmentNumber}"]["chain"] = templistString
                treeNode[f"fragment{fragmentNumber}"]["indexes"] = (startingIndex,endingIndex)
                treeNode[f"fragment{fragmentNumber}"]["isLeaf"] = self.isThisFragmentLeaf(templistString)
                if((not isThisFragmentLeaf) and (isChainWhole)):
                    self.fragmentByRecursion(
                        treeNode[f"fragment{fragmentNumber}"]["chain"],
                        targetRecursionLevel, 
                        treeNode[f"fragment{fragmentNumber}"]
                    )
                elif((not isThisFragmentLeaf) and (not isChainWhole)):
                    self.fragmentByRecursion(
                        treeNode[f"fragment{fragmentNumber}"]["chain"],
                        1, 
                        treeNode[f"fragment{fragmentNumber}"]
                    )
                elif(isThisFragmentLeaf):
                    return
                fragmentNumber += 1
                wroteStartingIndex = False
                templist = []

            if((not writingList) and (char == self.UNION)):
                treeNode[f"fragment{fragmentNumber}"] = {}
                treeNode[f"fragment{fragmentNumber}"]["chain"] = self.UNION
                treeNode[f"fragment{fragmentNumber}"]["indexes"] = (charIndex,charIndex)
                fragmentNumber += 1                    
                pass

            templistString = "".join(templist)
            charIndex += 1