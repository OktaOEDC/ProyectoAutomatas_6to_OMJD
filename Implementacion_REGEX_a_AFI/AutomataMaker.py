from tty import OSPEED
from xxlimited import new
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
        # bien rara la libreria, en codigo debes trabajarlo con su formato DOT
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

    def AFIToDot(self, AFI: dict):
        # El reverso de la funcion de arriba
        # Version modificada de funcion dfa_json importer para
        #  que agarre de memoria en vez de disco
        AFIJson = copy.deepcopy(AFI)

        transitions = {}  # key [state ∈ states, action ∈ alphabet]
        #                   value [arriving state ∈ states]
        for (origin, action, destination) in AFIJson['transitions']:
            transitions[origin, action] = destination

        AFI = {
            'alphabet': set(AFIJson['alphabet']),
            'states': set(AFIJson['states']),
            'initial_state': AFIJson['initial_state'],
            'accepting_states': set(AFIJson['accepting_states']),
            'transitions': transitions
        }
        return AFI

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
        return ID

    def setTreeToSearch(self, treeNode: dict, treeCoordinate: str):
        self.automataTree = treeNode
        self.findAutomataLeafs(self.automataTree, treeCoordinate)

    def nodesSTAR(self, node: dict):
        starizedNode = copy.deepcopy(self.AFITemplate)
        newState = self.getNextAutomataStateID()
        previousInitial = node["initial_state"]
        starizedNode["alphabet"] = node["alphabet"]
        starizedNode["states"] = node["states"]
        starizedNode["initial_state"] = newState
        starizedNode["accepting_states"] = node["accepting_states"]
        starizedNode["transitions"] = node["transitions"]
        for prevAcceptingState in node["accepting_states"]:
            starizedNode["transitions"].append(
                [prevAcceptingState,
                 f"ε({self.getNextEpsilonID()})",
                  previousInitial]
            )
        starizedNode["states"].append(newState)
        starizedNode["accepting_states"].append(newState)
        starizedNode["transitions"].append(
                [newState,
                 f"ε({self.getNextEpsilonID()})",
                  previousInitial]
        )
        return starizedNode

    def nodesUNION(self, left: dict, right: dict):
        unionizedNode = copy.deepcopy(self.AFITemplate)
        newStart = self.getNextAutomataStateID()
        leftInit = left["initial_state"]
        rightInit = right["initial_state"]
        unionizedNode["alphabet"] = right["alphabet"] + left["alphabet"] 
        unionizedNode["states"] = right["states"] + left["states"] + [newStart]
        unionizedNode["accepting_states"] = right["accepting_states"] + left["accepting_states"]
        unionizedNode["initial_state"] = newStart
        unionizedNode["transitions"] = left["transitions"] + right["transitions"]
        unionizedNode["transitions"].append([newStart,f"ε({self.getNextEpsilonID()})",leftInit])
        unionizedNode["transitions"].append([newStart,f"ε({self.getNextEpsilonID()})",rightInit])
        return unionizedNode

    def nodesCONCAT(self, left: dict, right: dict):
        concatanatedNode = copy.deepcopy(self.AFITemplate)
        concatanatedNode["alphabet"] = right["alphabet"] + left["alphabet"] 
        concatanatedNode["states"] = right["states"] + left["states"]
        concatanatedNode["accepting_states"] = right["accepting_states"] 
        concatanatedNode["initial_state"] = left["initial_state"]
        concatanatedNode["transitions"] = left["transitions"] + right["transitions"]
        for leftPrevAcceptingState in left["accepting_states"]:
            concatanatedNode["transitions"].append(
                [leftPrevAcceptingState,
                 f"ε({self.getNextEpsilonID()})",
                  right["initial_state"]]
            )
        return concatanatedNode

    def createAutomataTreeNode(self, treeNode: dict):
        # Al crear un nodo ya sea en base a nodos previos o hojas
        #  las reglas son un poco más simples que crear la hoja desde 0
        # Solo pueden pasar 3 cosas: Concatenación de hojas/nodos, Union de nodos/hojas
        #  o "estrellizacion?" del nodo entero
        # Primero revisar si al final se debe aplicar asterisco
        mustStarNode = False
        if(treeNode["chain"][-1] == self.STAR):
            mustStarNode = True
        numberOfFragments = len([value for key,
                         value in treeNode.items() if 'fragment' in key.lower()])
        fullNode = treeNode[f"fragment{0}"]["AFI"]
        fragmentIndex = 0
        while(fragmentIndex < numberOfFragments-1):
            if(fragmentIndex < numberOfFragments-2):
                # Solo puede haber simbolo de UNION en esa circnstancia
                if(treeNode[f"fragment{fragmentIndex+1}"]["chain"] == self.UNION):
                    fullNode = self.nodesUNION(fullNode, treeNode[f"fragment{fragmentIndex+2}"]['AFI'])
                    fragmentIndex += 1
                else:
                    fullNode = self.nodesCONCAT(fullNode, treeNode[f"fragment{fragmentIndex+1}"]['AFI'])
            else:
                fullNode = self.nodesCONCAT(fullNode, treeNode[f"fragment{fragmentIndex+1}"]['AFI'])
            fragmentIndex += 1 
        # Al acbar convertirlo en AFI compatible con JSON .. o no porque las hojas ya lo eran?
        #fullNode = self.AFIToJson(fullNode)
        if(mustStarNode):
            fullNode = self.nodesSTAR(fullNode)
        return fullNode

    def recursiveAutomataTreeMaker(self, treeNode: dict, OSpathChain: str):
        nodefragments = [value for key,
                         value in treeNode.items() if 'fragment' in key.lower()]
        numberOfFragments = len(nodefragments)
        chain = treeNode["chain"]
        # Es verdadero hasta que alguno no lo sea
        allFragmentsAreUnionsOrAutomatas = True 
        for fragment in range(numberOfFragments):
            # SI su AFI es vacio no es automata
            isAutomata = False 
            if(treeNode[f"fragment{fragment}"]["AFI"] != []):
                isAutomata = True       
            isUnionLeaf = treeNode[f"fragment{fragment}"]["chain"] == self.UNION
            if(((isAutomata) and (isUnionLeaf))or((isAutomata) and (not isUnionLeaf))or(not isAutomata and isUnionLeaf)):
                pass
            elif(not isAutomata):
                allFragmentsAreUnionsOrAutomatas = False
                self.recursiveAutomataTreeMaker(treeNode[f"fragment{fragment}"], OSpathChain+chain+"/")
        # Solo se debe revisar al final 1 solo vez si todos los fragmentos son automatas
        if(allFragmentsAreUnionsOrAutomatas):
            print(f"All fragments of chain {chain} are automatas")
            # Sí todos los fragmentos son automatas hacemos que este nodo se covierta en automata
            treeNode["AFI"] = self.createAutomataTreeNode(treeNode)
            osNameChain = treeNode["chain"]
            osNameChain = osNameChain.replace("*", "\u204E")
            automata_IO.dfa_to_dot(
                self.AFIToDot(treeNode["AFI"]),
                str(f"{self.getNextAutomataID()}"),
                f"./Automatas/Nodes/{OSpathChain}{osNameChain}")
            x = 5

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def checkForLeafStar(self, AFI: dict, chain: str):
        if(chain[-1] == self.STAR):
            # ej: (ab)*
            prevInitState = AFI["initial_state"]
            prevAcceptingStates = AFI["accepting_states"]
            # Crear nuevo estado inicial y conectarlo al previo con epsilon
            newState = self.getNextAutomataStateID()
            AFI["accepting_states"].append(newState)
            AFI["states"].append(newState)
            AFI["initial_state"] = newState
            tupleKey = (newState,
                            f"ε({self.getNextEpsilonID()})")
            AFI["transitions"][tupleKey] = prevInitState
            # Conectar los previos de aceptacion con epsilon al inicial original
            for acceptingState in prevAcceptingStates:
                tupleKey = (acceptingState, f"ε({self.getNextEpsilonID()})")
                AFI["transitions"][tupleKey] = prevInitState
            return AFI
        else:
            # ej: (ab)
            return AFI
        pass

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
        osNameChain = osNameChain.replace("*", "\u204E")
        # Crear una hoja en base a partes solo involucra operaciones de concatenacion
        if(len(automataParts) == 1):
            # Si la hoja es solo 1 parte, poner en el diccionario esta
            #  parte sin procesarla
            # Pero antes de acabar revisar si hay que aplicarle estrella
            automataParts[0] = self.checkForLeafStar(automataParts[0], fragment["chain"])
            fragment["AFI"] = self.AFIToJson(automataParts[0])
            automata_IO.dfa_to_dot(
                automataParts[0],
                str(f"{self.getNextAutomataID()}"),
                f"./Automatas/Leafs/{osNameChain}")
            return

        # Templete con el primer elemento en mente
        fusionedAutomata = {}
        fusionedAutomata["alphabet"] = automataParts[0]["alphabet"]
        fusionedAutomata["states"] = automataParts[0]["states"]
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
            fusionedAutomata = self.mixAutomatas(
                leftAutomata, rightAutomata, fusionedAutomata)
            # Conectar cada uno de los estados de aceptacion del de la izquierda
            #   al inicial del de la derecha con epsilon
            for leftPrevAcceptingState in leftPrevAcceptingStates:
                tupleKey = (leftPrevAcceptingState,
                            f"ε({self.getNextEpsilonID()})")
                fusionedAutomata["transitions"][tupleKey] = rightTargetState
            automataPartsIndex += 1
        # Revisar si debemos aplicar estrella a toda la hoja antes de finalizar su proceso
        fusionedAutomata = self.checkForLeafStar(fusionedAutomata, fragment["chain"])
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
                tempAutomata["transitions"] = {(state1, letter): state2}
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
                    (state1, f"ε({self.getNextEpsilonID()})"): state2,
                    (state2, letter): state3,
                    (state3, f"ε({self.getNextEpsilonID()})"): state2
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
                self.createAutomataLeafParts(
                    treeNode[f"fragment{fragment}"], coord)
                #print("Is Leaf")
            elif(not isLeaf):
                # No hojas se deben seguir recurriendo para encontrar sus hojas
                self.findAutomataLeafs(treeNode[f"fragment{fragment}"], coord)
        return treeNode
