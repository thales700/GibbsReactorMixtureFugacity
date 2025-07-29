from ..Molecula.Molecula import Molecula

class CoeficientesToList:
    @classmethod
    def CoeficientesReformaToList(self, moleculas: list[Molecula]):
        return [molecula.coeficienteReforma for molecula in moleculas]

    @classmethod
    def CoeficientesWGSToList(self, moleculas: list[Molecula]):
        return [molecula.coeficienteWGS for molecula in moleculas]