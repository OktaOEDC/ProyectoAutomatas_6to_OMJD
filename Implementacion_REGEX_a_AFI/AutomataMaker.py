class regexAutomataMaker():
    def __init__(self):
        self.UNION = ""
        self.STAR = ""

    def DEFINE_SYMBOLS(self, UNIONsymbol: str, STARsymbol: str):
        self.UNION = UNIONsymbol
        self.STAR = STARsymbol

    def createAutomataLeafs(self, treeNode):
        nodefragments = [value for key,
                         value in treeNode.items() if 'fragment' in key.lower()]
        numberOfFragments = len(nodefragments)
        x = 5
        for fragment in range(numberOfFragments):
            isLeaf = treeNode[f"fragment{fragment}"]["isLeaf"] == True
            isUnionLeaf = treeNode[f"fragment{fragment}"]["chain"] == self.UNION
            if((isLeaf) and (isUnionLeaf)):
                # Hojas de Union por defecto no se convierten en automatas
                #  sino que mas arriba en la recursion unen hojas
                print("Is Union leaf")
            elif((isLeaf) and (not isUnionLeaf)):
                # Hojas no Union son cadenas sin recursion que se deben 
                #  convertir en automatas
                print("Is Leaf")
            else:
                # No hojas se deben seguir recurriendo para encontrar sus hojas
                print("Is not a Leaf")
            pass
        pass
    pass
