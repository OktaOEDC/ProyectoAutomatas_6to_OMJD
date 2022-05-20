from PySimpleAutomata import automata_IO
import copy

class regexAutomataMaker():
    def __init__(self):
        self.UNION = ""
        self.STAR = ""
        self.AFITemplate = {
            # Arreglo de alfabeto (los caracteres en la regex)
            "alphabet": [],
            "states": [],             # Arreglo de estados
            "initial_state": "",      # Estado inicial 
            "accepting_states": [],   # Arreglo de estados de aceptacion
            # Arreglo de arreglos de transiciones [estadoSalida, parteCadena, estadollegada]
            "transitions": {}
        }
        self.stateIndexCounter = 0
        self.automataIndexCounter = 0
        self.epsilonKey = 0

    def AFIToJson(self, AFI: dict):
        #bien rara la libreria, en codigo debes trabajarlo con su formato DOT
        # pero para exportarlo a json debo hacerlo objero json
        # y si lo tiene pero solo lo exporta a archivo
        # Sección obtenida de esa funcion
        AFIJson = {
            'alphabet': list(AFI['alphabet']),
            'states': list(AFI['states']),
            'initial_state': AFI['initial_state'],
            'accepting_states': list(AFI['accepting_states']),
            'transitions': list()
        }

        for transition in AFI['transitions']:
            AFIJson['transitions'].append(
                [transition[0], transition[1], AFI['transitions'][transition]])
        return AFIJson

    def getNextEpsilonID(self):
        # Dado que estamos usando AFDs, debemos usar truquillos 
        # para que usar una transicion tenga > de 1 destino posible
        ID = hex(self.epsilonKey)
        self.epsilonKey += 1
        return ID[2:]

    def getNextAutomataStateID(self):
        ID = hex(self.stateIndexCounter)
        self.stateIndexCounter += 1
        return ID

    def getNextAutomataID(self):
        ID = hex(self.automataIndexCounter)
        self.automataIndexCounter += 1
        return ID[2:]

    def setTreeToSearch(self, treeNode: dict, treeCoordinate: str):
        self.automataTree = treeNode
        self.findAutomataLeafs(self.automataTree, treeCoordinate)

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def mixAutomatas(self, left: dict, right: dict, fusionDict: dict):
        fusionDict["alphabet"] += right["alphabet"]
        fusionDict["states"] += right["states"]
        fusionDict["accepting_states"] += right["accepting_states"]
        # No hay += para diccionarios, por lo tanto hay dos fors para hacerlo a mano
        for key, value in left["transitions"].items():
            fusionDict["transitions"][key] = value
        for key, value in right["transitions"].items():
            fusionDict["transitions"][key] = value
        return fusionDict

    def createAutomataLeaf(self, automataParts: list, fragment: dict):
        automataPartsIndex = 0
        osNameChain = fragment["chain"]
        osNameChain = osNameChain.replace("*","\u204E")
        # Crear una hoja en base a partes solo involucra operaciones de concatenacion
        if(len(automataParts) == 1):
            # Si la hoja es solo 1 parte, poner en el diccionario esta 
            #  parte sin procesarla
            fragment["AFI"] = self.AFIToJson(automataParts[0])
            automata_IO.dfa_to_dot(
                automataParts[0],
                str(f"{self.getNextAutomataID()}"),
                f"./Automatas/Leafs/{osNameChain}")
            return

        # Templete con el primer elemento en mente
        fusionedAutomata = {}
        fusionedAutomata["alphabet"] = automataParts[0]["alphabet"]
        fusionedAutomata["states"] =  automataParts[0]["states"]
        fusionedAutomata["accepting_states"] = []
        fusionedAutomata["transitions"] = automataParts[0]["transitions"]
        fusionedAutomata["initial_state"] = automataParts[0]["initial_state"]

        while(automataPartsIndex < (len(automataParts)-1)):
            # Concatenar:
            #  * El izquierdo pierde estados de aceptacion
            #  * Salen transiciones epsilon de los previos estados de aceptacion
            #    del izquierdo al estado inicial del derecho
            leftAutomata = copy.deepcopy(automataParts[automataPartsIndex])
            rightAutomata = copy.deepcopy(automataParts[automataPartsIndex+1])
            # Hacer copia de los estados de aceptacion de la izquierda
            leftPrevAcceptingStates = leftAutomata["accepting_states"]
            # Vaciar los estados de aceptacion del de la izquierda (es relativo el ser izquierdo lol)
            leftAutomata["accepting_states"] = []
            fusionedAutomata["accepting_states"] = []
            # Conseguir el estado previo del automata de la derecha (ab)
            #  que recibira la transición del de la izuquierda
            rightTargetState = rightAutomata["initial_state"]
            # Fusionar automatas
            fusionedAutomata = self.mixAutomatas(leftAutomata, rightAutomata, fusionedAutomata)
            # Conectar cada uno de los estados de aceptacion del de la izquierda
            #   al inicial del de la derecha con epsilon
            for leftPrevAcceptingState in leftPrevAcceptingStates:
                tupleKey = (leftPrevAcceptingState, f"ε({self.getNextEpsilonID()})")
                fusionedAutomata["transitions"][tupleKey] = rightTargetState
            automataPartsIndex += 1
        fragment["AFI"] = self.AFIToJson(fusionedAutomata)
        automata_IO.dfa_to_dot(
            fusionedAutomata,
            str(f"{self.getNextAutomataID()}"),
            f"./Automatas/Leafs/{osNameChain}")
        return


    def createAutomataLeafParts(self, fragment, treeCoordinate: str):
        fragment["AFI"] = "{}"
        charIndex = 0
        chain = fragment["chain"]
        leafParts = []
        automataParts = []

        # Conseguir las partes para aplicar operaciones
        while(charIndex < (len(chain))):
            char = chain[charIndex]
            if(charIndex != (len(chain)-1)):
                if((chain[charIndex+1] == self.STAR) and (char != "(" and char != ")")):
                    # Si no es el ultimo caracter de la cadena y el caracter que sige es una estrella
                    #  mientras estamos viendo una terminal ... o sea -> a* en vez de a
                    leafParts.append(f"{char}{self.STAR}")
                    charIndex += 1
                elif((chain[charIndex+1] != self.STAR) and (char != "(" and char != ")")):
                    leafParts.append(f"{char}")
            charIndex += 1
        # Crear automatas de cada parte
        for part in leafParts:
            tempAutomata = copy.deepcopy(self.AFITemplate)
            letter = part[0]
            if(len(part) == 1):
                # ej: a
                state1 = self.getNextAutomataStateID()
                state2 = self.getNextAutomataStateID()
                tempAutomata["states"] = [state1, state2]
                tempAutomata["initial_state"] = state1
                tempAutomata["accepting_states"] = [state2]
                tempAutomata["alphabet"] = [letter]
                tempAutomata["transitions"] = {(state1,letter):state2}
                # automata_IO.dfa_to_dot(
                #     tempAutomata,
                #     str(f"{self.getNextAutomataID()}_{treeCoordinate}"),
                #     "./Automatas/")
                automataParts.append(tempAutomata)
            elif(len(part) == 2):
                # ej: b*
                state1 = self.getNextAutomataStateID()
                state2 = self.getNextAutomataStateID()
                state3 = self.getNextAutomataStateID()
                tempAutomata["states"] = [state1, state2, state3]
                tempAutomata["initial_state"] = state1
                tempAutomata["accepting_states"] = [state1, state3]
                tempAutomata["alphabet"] = [letter, "ε"]
                tempAutomata["transitions"] = {
                    (state1,f"ε({self.getNextEpsilonID()})"):state2,
                    (state2,letter):state3,
                    (state3,f"ε({self.getNextEpsilonID()})"):state2
                }
                # automata_IO.dfa_to_dot(
                #     tempAutomata,
                #     str(f"{self.getNextAutomataID()}_{treeCoordinate}"),
                #     "./Automatas/")
                automataParts.append(tempAutomata)
        
        self.createAutomataLeaf(automataParts, fragment)

    def findAutomataLeafs(self, treeNode: dict, treeCordinate: str):
        nodefragments = [value for key,
                         value in treeNode.items() if 'fragment' in key.lower()]
        numberOfFragments = len(nodefragments)
        x = 5
        for fragment in range(numberOfFragments):
            isLeaf = treeNode[f"fragment{fragment}"]["isLeaf"] == True
            isUnionLeaf = treeNode[f"fragment{fragment}"]["chain"] == self.UNION
            coord = treeCordinate + str(fragment)
            if((isLeaf) and (isUnionLeaf)):
                # Hojas de Union por defecto no se convierten en automatas
                #  sino que mas arriba en la recursion unen hojas
                pass
            elif((isLeaf) and (not isUnionLeaf)):
                # Hojas no Union son cadenas sin recursion que se deben
                #  convertir en automatas
                self.createAutomataLeafParts(treeNode[f"fragment{fragment}"], coord)
                #print("Is Leaf")
            elif(not isLeaf):
                # No hojas se deben seguir recurriendo para encontrar sus hojas
                self.findAutomataLeafs(treeNode[f"fragment{fragment}"], coord)
        return treeNode
    pass
