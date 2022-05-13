from sympy import false


class regexParser:
    def __init__(self):
        self.UNION = ""
        self.STAR = ""
        pass
    
    def removeSpaces(self, chain: str):
        return chain.replace(" ", "")

    

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol
        pass

    def CHECK_FOR_INVALID_CHAINS(self, chain: str):
        numberOfOpenings = 0
        numberOfClosures = 0
        listOfInvalidSequences = [
            f"{self.STAR}{self.STAR}",   #**
            f"{self.UNION}{self.STAR}",  #U*
            f"{self.UNION}{self.UNION}", #UU
            f"({self.STAR}",             #(*
            "()",                        #()
            f"({self.UNION})",           #(U)
            f"({self.STAR})"             #(*)  

        ]
        onlyHasOperatorAndParenthesis = True
        lastSequenceOfTwo = "  "    # Siempre dos caracteres
        lastSequenceOfThree = "   " # Siempre tres caracteres

        # Revisar si la cadena inicia con Union o asterisco, o si acaba con Union
        if(chain[0] == "*" or chain[0] == "U" or chain[-1] == "U"):
            print("Error: Inicio o fin de cadena con carcater de operador")
            return False

        for char in chain:
            # Modificar la ultima secuencia de dos y tres caracteres
            lastSequenceOfTwo = f"{lastSequenceOfTwo[1]}{char}"
            lastSequenceOfThree = f"{lastSequenceOfThree[1]}{lastSequenceOfThree[2]}{char}"
            # Identificar si el caracter no es Union, parentesis, o estrella
            #  para así validar la cadena
            if(char != self.UNION or char != self.STAR or char != "(" or char != ")"):
                onlyHasOperatorAndParenthesis = False
            # Contar parentesis
            if(char =="("):
                numberOfOpenings += 1
            elif(char == ")"):
                numberOfClosures += 1
            # Revisar si no hay dos caracteres seguidos de operacion
            if(lastSequenceOfTwo in listOfInvalidSequences):
                print("Error: Cadena invalida, secuencia invalida de caracteres de operacion detectada")
                return False
            # Revisar si no hay fragmentos con solo un operador
            if(lastSequenceOfThree in listOfInvalidSequences):
                print("Error: Hay un fragmento con caracter de operacion pero no terminales")
                return False
        
        # Hacer revision del conteo de parentesis
        if(numberOfClosures != numberOfOpenings):
            print("Error: Cadena invalida, hay exceso de parentesis de cierre o apretura")
            return False
        # Hacer revision de si no hay terminales
        if(onlyHasOperatorAndParenthesis):
            print("Error: Solo hay singos de UNION o asteriscos o parentesis")
        return True

    def PARENTHESIZE_ALL_FRAGMENTS(self, chain: str):
        chainList = list(chain)
        chainIndex = len(chainList)
        # Primero revisar si tan siquiera hay parentesis
        if ("(" not in chainList or ")" not in chainList):
            return

        while(chainIndex != -1):
            char = chain[chainIndex]
            if(char != ")" or char != self.UNION or char != "("):
                # Al encontrar un caracter que no sea parentesis o UNION
                list.insert(chainIndex,")")
                pass
            chainIndex -= 1
        pass
