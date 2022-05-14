from Parser import regexParser

#REchain ="(ab*c(dUf*a(bUc)ab(cd*)*))kd"
#REchain ="aU(bcU(fg))Uef(go)*ab"
#REchain ="aUa(((ab*Ub*c*(d)*)*U(ab*)*U(c*Ud*)))"
#REchain = "abcdeUfghij*(aUb)UklmnopUa*"
REchain = "((((a*)*bcUdc)U(cd))k*ue*(bc*(b*e*)*)*U(abcde*(fg)U(ab)))U(be*fg*)"

if __name__ == "__main__":
    RE_parser = regexParser()
    REchain = RE_parser.removeSpaces(REchain)
    #FASE 1: Definir symbolos
    RE_parser.DEFINE_SYMBOLS("U","*")
    #FASE 2: Ver cadenas invalidas
    if(not RE_parser.CHECK_FOR_INVALID_CHAINS(REchain)):
        print("Error en fase 2...")   
        raise NameError("Tu cadena es invalida, corrígela") 
    RE_parser.PARENTHESIZE_ALL_FRAGMENTS(REchain) 
    RE_parser.CHECK_FOR_INVALID_CHAINS(REchain) # Revalido por si las dudas
    pass