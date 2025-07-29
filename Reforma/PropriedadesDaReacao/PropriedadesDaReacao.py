from ..Molecula.Molecula import Molecula

class PropriedadesDaReacao:
    
    @classmethod
    def CalcularDeltaGReacao(self, moleculas: list[Molecula], coeficientes: list[int]):
        dGrxn = 0
        for molecula, coeficiente in zip(moleculas, coeficientes):
            dGrxn += coeficiente*molecula.dGformacao
        return dGrxn

    @classmethod
    def CalcularDeltaHReacao(self, moleculas: list[Molecula], coeficientes: list[int]):
        dHrxn = 0
        for molecula, coeficiente in zip(moleculas, coeficientes):
            dHrxn += coeficiente*molecula.dHformacao
        return dHrxn