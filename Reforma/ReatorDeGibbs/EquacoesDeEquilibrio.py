from ..Molecula.Molecula import Molecula
import numpy as np

class EquacoesDeEquilibrio:
    def __init__(self, moleculas: list[Molecula], constantesDeEquilibrio: list[float],
                 coeficientesEstequiometricos: list[int], pressao: float):
        self.moleculas = moleculas
        self.constantesDeEquilibrio = constantesDeEquilibrio
        self.pressao = pressao
        self.coeficientesEstequiometricos = coeficientesEstequiometricos
    
    def EquacoesDoEquilibrio(self, x):
        self._MolsFinal(x)
        self._FracaoMols()
        F = np.zeros(len(self.coeficientesEstequiometricos))
        for i in range(len(self.coeficientesEstequiometricos)):
            F[i] = self._EquacaoEquilibrio(self.coeficientesEstequiometricos[i], self.constantesDeEquilibrio[i], x)
        return F

    def _EquacaoEquilibrio(self, coeficientesEstequiometricos:list, constanteDeEquilibrio:float, x):
        numerador = 1
        denominador = 1
        for molecula, coefEstequiometrico in zip(self.moleculas, coeficientesEstequiometricos):
                if molecula.faseGas:
                    if coefEstequiometrico >= 1:
                        numerador *= (molecula.fracaoMolar*molecula.fugacidade*self.pressao)**(coefEstequiometrico)
                    else:
                        denominador *= (molecula.fracaoMolar*molecula.fugacidade*self.pressao)**abs(coefEstequiometrico)
        return numerador - constanteDeEquilibrio*denominador
    
    def _FracaoMols(self):        
        molsTotal = 0
        
        for i in range(len(self.moleculas)):
            if self.moleculas[i].faseGas:
                molsTotal+= self.moleculas[i].molsFinal
        
        for i in range(len(self.moleculas)):
            if self.moleculas[i].faseGas:
                self.moleculas[i].fracaoMolar = self.moleculas[i].molsFinal/molsTotal
            else:
                self.moleculas[i].fracaoMolar = 1

    def _MolsFinal(self, X):
        for i in range(len(self.moleculas)):
            self.moleculas[i].molsFinal = self.moleculas[i].molInicial
            for r in range(len(self.coeficientesEstequiometricos)):
                self.coefEstqRxn = self.coeficientesEstequiometricos[r]
                self.moleculas[i].molsFinal += float(self.coefEstqRxn[i])*X[r]