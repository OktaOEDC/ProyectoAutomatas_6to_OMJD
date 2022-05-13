from Parser import regexParser

#REchain="(ab*c(dUf*a(bUc)ab(cd*)*))kd"
REchain="(aUbc*d*e*UabUfg)"

if __name__ == "__main__":
    RE_parser = regexParser()
    REchain = RE_parser.removeSpaces(REchain)
    #FASE 1: Definir symbolos
    RE_parser.DEFINE_SYMBOLS("U","*")
    #FASE 2: Ver cadenas invalidas
    if(not RE_parser.CHECK_FOR_INVALID_CHAINS(REchain)):
        print("Error en fase 2...")   
        raise NameError("Tu cadena es invalida, corrígela") 
    RE_parser.PARENTHESIZE_ALL_FRAGMENTS_WITH_UNIONS(REchain) 
    pass