class regexPreparer:
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
            f"{self.STAR}{self.STAR}",  # **
            f"{self.UNION}{self.STAR}",  # U*
            f"{self.UNION}{self.UNION}",  # UU
            f"({self.STAR}",  # (*
            "()",  # ()
            f"({self.UNION})",  # (U)
            f"({self.STAR})"  # (*)

        ]
        onlyHasOperatorAndParenthesis = True
        lastSequenceOfTwo = "  "    # Siempre dos caracteres
        lastSequenceOfThree = "   "  # Siempre tres caracteres

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
            if(char == "("):
                numberOfOpenings += 1
            elif(char == ")"):
                numberOfClosures += 1
            # Revisar si no hay dos caracteres seguidos de operacion
            if(lastSequenceOfTwo in listOfInvalidSequences):
                print(
                    "Error: Cadena invalida, secuencia invalida de caracteres de operacion detectada")
                return False
            # Revisar si no hay fragmentos con solo un operador
            if(lastSequenceOfThree in listOfInvalidSequences):
                print(
                    "Error: Hay un fragmento con caracter de operacion pero no terminales")
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
        chainIndex = len(chainList)-1
        parenthesizingMode = False
        operationSymbols = ["(", ")", self.UNION]
        lastParenthesisSeen = ""

        # Primero revisar si tan siquiera hay parentesis
        if ("(" not in chainList or ")" not in chainList):
            return

        while(chainIndex > -1):
            char = chain[chainIndex]
            # Escenario 2: Sí instertamos cierre despues de apuertura
            #  y antes de cierre: invalido
            if(char == "(" and lastParenthesisSeen == ")"):
                chainList = chainCopy
                parenthesizingMode = False
                lastParenthesisSeen = ""
                char = chainList[chainIndex]  # Hacer refresh al char

            chain = "".join(chainList)  # para debugeo

            # Caso de referencia para los escenarios de la fase 3
            if(char == "("):
                lastParenthesisSeen = "("
            elif(char == ")"):
                lastParenthesisSeen = ")"

            # Buscar algun caracter que no sea parentesis o Union
            if((char not in operationSymbols) and (not parenthesizingMode)):
                # Revisar si el caracter que sigue por leer(el previo) es un
                #  un parentesis de cierre, sí es así no entrar en modo
                #  parentesis porque si no se hace fragmento vacio
                # Tambien sirve para no rodear con parentesis fragmentos
                #  aferctsados por el operador estrella
                if(chainList[chainIndex-1] != ")" or chainIndex == 0):
                    chainCopy = chainList[:]
                    parenthesizingMode = True
                    # Al encontrar un caracter que no sea parentesis o UNION
                    chainList.insert(chainIndex+1, ")")
                    # Iteramos por los parentesis de cierre para no crear un fragmento vacio
                    #chainIndex = self.iterateThroughClosingParenthesis(chainList, chainIndex)
                    chainIndex -= 1  # Nos saltamos uno para que el programa no se tope con el parentesis que acaba de poner
                    # Se debe cambiar caracter e indice
                    char = chainList[chainIndex]

            chain = "".join(chainList)  # para debugeo

            # Escenario 2: Sí instertamos cierre despues de apuertura
            #  y antes de cierre: invalido
            # Sí, esto debe hacerse dos veces o si no fragmentos de
            #  1 caracter no se revisan bien
            if(char == "(" and lastParenthesisSeen == ")"):
                chainList = chainCopy
                parenthesizingMode = False
                lastParenthesisSeen = ""
                char = chainList[chainIndex]  # Hacer refresh al char

            if(parenthesizingMode):
                # Primero revisar si este asterisco pertenece a una
                #  terminal o a un parentesis de cierre, le seguimos sí es terminal
                #  si es parentesis de cierre entonces hay que poner parentesis ahí
                # Escenario especial #0 ^^
                if(char == "*" and chain[chainIndex-1] == ")"):
                    chainList.insert(chainIndex+1, "(")
                    parenthesizingMode = False
                    lastParenthesisSeen = ""
                # Escenarioa 1,3,4,5 y 6: Ampezamos a prentesizar antes de algun
                # parentesis y signo de UNION y nos topamos con otro
                #  que no sea la combinacion del escenario 2
                elif(char == ")" or char == self.UNION or char == "("):
                    chainList.insert(chainIndex+1, "(")
                    parenthesizingMode = False
                    lastParenthesisSeen = ""
                # Escenario especial 7: Iniciamos parentesis como en los demas, pero
                #  nos topamos con el inicio de la cadena
                elif(chainIndex == 0):
                    chainList.insert(chainIndex, "(")
                    parenthesizingMode = False
                    lastParenthesisSeen = ""

            chainIndex -= 1
            chain = "".join(chainList)  # para debugeo
        print(chain)
        return chain
