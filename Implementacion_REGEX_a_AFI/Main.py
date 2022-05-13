from Parser import regexParser

#REchain="(ab*c(dUf*a(bUc)ab(cd*)*))kd"
REchain="aU(U)ab"

if __name__ == "__main__":
    RE_parser = regexParser()
    #FASE 1: Definir symbolos
    RE_parser.DEFINE_SYMBOLS("U","*")
    #FASE 2: Ver cadenas invalidas
    if(not RE_parser.CHECK_FOR_INVALID_CHAINS(REchain)):
        print("Error en fase 2...")
    else:
        print("Fase 2 completa")       
    pass