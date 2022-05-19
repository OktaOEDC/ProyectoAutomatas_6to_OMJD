from PySimpleAutomata import NFA

class regexAutomataMaker():
    def __init__(self):
        self.UNION = ""
        self.STAR = ""

    def setTreeToSearch(self, treeNode):
        self.automataTree = treeNode
        self.findAutomataLeafs(self.automataTree)

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def createAutomataLeaf(self, fragment):
        fragment["AFI"] = "{}"
        pass

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
