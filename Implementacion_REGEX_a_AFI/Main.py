from Preparer import regexPreparer
from Fragmenter import regexFragmenter

#RE_chain = "(ab*c(dUf*a(bUc)ab(cd*)*))kd"
#RE_chain = "aU(bcU(fg))Uef(go)*ab"
#RE_chain = "aUa(((ab*Ub*c*(d)*)*U(ab*)*U(c*Ud*)))"
#RE_chain = "abcdeUfghij*(aUb)UklmnopUa*"
RE_chain = "((((a*)*bcUdc)U(cd))k*ue*(bc*(b*e*)*)*U(abcde*(fg)U(ab)))*U(be*fg*)"

if __name__ == "__main__":
    RE_parser = regexPreparer()
    RE_fragmenter = regexFragmenter("U","*")
    RE_chain = RE_parser.removeSpaces(RE_chain)
    # PARSER
    #FASE 1: Definir symbolos
    RE_parser.DEFINE_SYMBOLS("U","*")
    #FASE 2: Ver cadenas invalidas
    if(not RE_parser.CHECK_FOR_INVALID_CHAINS(RE_chain)):
        print("Error en fase 2...")   
        raise NameError("Tu cadena es invalida, corrígela") 
    # Fase 3 y 4: Crear fragmentos con parentesis para cada sección de la cadena
    RE_chain = RE_parser.PARENTHESIZE_ALL_FRAGMENTS(RE_chain) 
    RE_parser.CHECK_FOR_INVALID_CHAINS(RE_chain) # Revalido por si las dudas
    # FRAGMENTER
    # Fase 1: Encontrar el nivel máximo de recursión
    maximinRecursionLevel = RE_fragmenter.findMaximunRecursionLevel(RE_chain)
    RE_fragmenter.fragmentByRecursion(RE_chain, maximinRecursionLevel, 0, RE_fragmenter.fragmentTree)
    pass