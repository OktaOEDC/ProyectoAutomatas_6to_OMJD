from Preparer import regexPreparer
from Fragmenter import regexFragmenter
from AutomataMaker import regexAutomataMaker
import json

#chain = "(ab*c(dUf*a(bUc)ab(cd*)*))kd"
#chain = "aU(bcU(fg))Uef(go)*ab"
#chain = "aUa(((ab*Ub*c*(d)*)*U(ab*)*U(c*Ud*)))"
#chain = "abcdeUfghij*(aUb)UklmnopUa*"
chain = "((((a*)*bcUdc)U(cd))k*ue*(bc*(b*e*)*)*U(abcde*(fg)U(ab)))*U(be*fg*)"

if __name__ == "__main__":
    RE_parser = regexPreparer()
    RE_fragmenter = regexFragmenter()
    RE_AFIMaker = regexAutomataMaker()
    RE_chain = RE_parser.removeSpaces(chain)
    # PARSER
    # FASE 1: Definir symbolos en cada una de las clases que procesan la cadena
    RE_parser.DEFINE_SYMBOLS("U", "*")
    RE_fragmenter.DEFINE_SYMBOLS("U", "*")
    RE_AFIMaker.DEFINE_SYMBOLS("U", "*")
    # FASE 2: Ver cadenas invalidas
    if(not RE_parser.CHECK_FOR_INVALID_CHAINS(RE_chain)):
        print("Error en fase 2...")
        raise NameError("Tu cadena es invalida, corrígela")
    # Fase 3 y 4: Crear fragmentos con parentesis para cada sección de la cadena
    RE_chain = RE_parser.PARENTHESIZE_ALL_FRAGMENTS(RE_chain)
    RE_parser.CHECK_FOR_INVALID_CHAINS(RE_chain)  # Revalido por si las dudas
    # FRAGMENTER
    # Fase 5: Crear arbol de recursion para representar la cadena por partes
    RE_fragmenter.fragmentTree["Root"] = {}
    RE_fragmenter.fragmentTree["Root"]["chain"] = RE_chain
    RE_fragmenter.fragmentTree["Root"]["isLeaf"] = False
    RE_fragmenter.fragmentByRecursion(
        RE_chain, 0, RE_fragmenter.fragmentTree["Root"])
    # Fase 6: Definir en el arbol de busqueda sus hojas
    RE_AFIMaker.setTreeToSearch(RE_fragmenter.fragmentTree["Root"], "0")
    osPathChain = RE_fragmenter.fragmentTree["Root"]["chain"]
    osPathChain = osPathChain.replace("*", "\u204E")
    osPathChain += "/"
    RE_AFIMaker.recursiveAutomataTreeMaker(RE_fragmenter.fragmentTree["Root"], osPathChain)
    json_object = json.dumps(RE_AFIMaker.automataTree, indent=4)
    with open("jsonTree.json", "wt") as outfile:
        outfile.write(json_object)
    pass
