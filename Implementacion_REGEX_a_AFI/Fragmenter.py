"""
El fragmentador analizará todos los fragmentos de una cadena
procesada para saber que tan dentro estan en una cadena
para así irlos resolviendo de adentro hacia afuera.
Farmentos chiquitos primero (muy dentro de la recursion)
"""


class regexFragmenter():
    def __init__(self):
        self.fragmentTree = {}
        self.UNION = ""
        self.STAR = ""
        self.fragmentTree = {}

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def isThisFragmentLeaf(self, chain: str):
        # Si es una hojita llegamos al punto maximo de recursion para esta parte de la cadena
        if(chain.count("(") == 1):
            return True
        else:
            return False

    def isChainWhole(self, fragment: str, chain: str):
        if(fragment == chain):
            return True
        else:
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
        charIndex = 0
        fragmentNumber = 0

        while(charIndex < len(chain)):
            # Buscar el nivel de recursion actual
            char = chain[charIndex]
            if(char == "("):
                currentRecursionLevel += 1
            elif(char == ")"):
                currentRecursionLevel -= 1

            if(currentRecursionLevel == level):
                writingList = True

            if(writingList):
                templist.append(char)

            if((writingList) and (currentRecursionLevel+1) == level and (char == ")")):
                templistString = "".join(templist)
                # NOTA -> CHAIN != FRAGMENT; uno es la cadena que llega y otro es el fragmento a recurrir
                # Revisar si el siguiente caracter de este es asterisco, para llevarnoslo tambien
                #  y saltarnoslo en la siguiente iteracion de esta recursion
                isThisFragmentLeaf = self.isThisFragmentLeaf(templistString)
                isChainWhole = self.isChainWhole(templistString, chain)
                try:
                    if(chain[charIndex+1] == self.STAR):
                        templist.append(self.STAR)
                        templistString = "".join(templist)
                        charIndex += 1
                except:
                    # Era el final de la cadena por lo tanto no hay asterisco
                    # si alguien sabe una forma más limpia de evitar esto digame
                    pass
                writingList = False

                treeNode[f"fragment{fragmentNumber}"] = {}
                treeNode[f"fragment{fragmentNumber}"]["AFI"] = []
                treeNode[f"fragment{fragmentNumber}"]["chain"] = templistString
                treeNode[f"fragment{fragmentNumber}"]["isLeaf"] = isThisFragmentLeaf
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
                    pass  # Hora de crackear ventanas B)
                fragmentNumber += 1
                templist = []

            if((not writingList) and (char == self.UNION)):
                treeNode[f"fragment{fragmentNumber}"] = {}
                treeNode[f"fragment{fragmentNumber}"]["AFI"] = []
                treeNode[f"fragment{fragmentNumber}"]["chain"] = self.UNION
                treeNode[f"fragment{fragmentNumber}"]["isLeaf"] = True
                fragmentNumber += 1

            templistString = "".join(templist)
            charIndex += 1
