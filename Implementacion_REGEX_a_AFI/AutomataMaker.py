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

    def getNextAutomataStateID(self):
        ID = hex(self.stateIndexCounter)
        self.stateIndexCounter += 1
        return ID

    def getNextAutomataID(self):
        ID = hex(self.automataIndexCounter)
        self.automataIndexCounter += 1
        return ID

    def setTreeToSearch(self, treeNode):
        self.automataTree = treeNode
        self.findAutomataLeafs(self.automataTree)

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def createAutomataLeaf(self, fragment):
        fragment["AFI"] = "{}"
        charIndex = 0
        chain = fragment["chain"]
        parts = []
        automataParts = []

        # Conseguir las partes para aplicar operaciones
        while(charIndex < (len(chain))):
            char = chain[charIndex]
            if(charIndex != (len(chain)-1)):
                if((chain[charIndex+1] == self.STAR) and (char != "(" and char != ")")):
                    # Si no es el ultimo caracter de la cadena y el caracter que sige es una estrella
                    #  mientras estamos viendo una terminal ... o sea -> a* en vez de a
                    parts.append(f"{char}{self.STAR}")
                    charIndex += 1
                elif((chain[charIndex+1] != self.STAR) and (char != "(" and char != ")")):
                    parts.append(f"{char}")
            charIndex += 1
        # Crear automatas de cada parte
        for part in parts:
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
                automata_IO.dfa_to_dot(
                    tempAutomata,
                    str(self.getNextAutomataID()),
                    "./Automatas/")
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
                    (state1,"ε"):state2,
                    (state2,letter):state3,
                    (state3,"ε"):state2
                }
                automata_IO.dfa_to_dot(
                    tempAutomata,
                    str(self.getNextAutomataID()),
                    "./Automatas/")
            x = 5

    def findAutomataLeafs(self, treeNode):
        nodefragments = [value for key,
                         value in treeNode.items() if 'fragment' in key.lower()]
        numberOfFragments = len(nodefragments)
        x = 5
        for fragment in range(numberOfFragments):
            isLeaf = treeNode[f"fragment{fragment}"]["isLeaf"] == True
            isUnionLeaf = treeNode[f"fragment{fragment}"]["chain"] == self.UNION
            chain = treeNode[f"fragment{fragment}"]["chain"]
            if((isLeaf) and (isUnionLeaf)):
                # Hojas de Union por defecto no se convierten en automatas
                #  sino que mas arriba en la recursion unen hojas
                pass
            elif((isLeaf) and (not isUnionLeaf)):
                # Hojas no Union son cadenas sin recursion que se deben
                #  convertir en automatas
                self.createAutomataLeaf(treeNode[f"fragment{fragment}"])
                pass
            elif(not isLeaf):
                # No hojas se deben seguir recurriendo para encontrar sus hojas
                self.findAutomataLeafs(treeNode[f"fragment{fragment}"])
            pass
        return treeNode
    pass
