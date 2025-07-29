import numpy as np
import math
from typing import Tuple

class ResiduaisPengRobinson:
    def __init__(self, R: float, temperatura: float, pressao: float, omega: float, tc: float, pc: float):
        self.t = temperatura
        self.p = pressao
        self.omega = omega
        self.tc = tc
        self.pc = pc
        self.tr = self.t/self.tc
        self.pr = self.p/self.pc
        self.R = R
    
    def _k(self) -> float:
        k = 0.37464+ 1.5422*self.omega-0.2699*self.omega**2
        return k
    
    def _alpha(self) -> float:
        alpha = (1+self._k()*(1-self.tr**(1/2)))**2
        return alpha
    
    def _talphalinha(self)->float:
        k = self._k()
        talphalinha = -k*self.tr**(1/2)*(1+k*(1-self.tr**(1/2)))
        return talphalinha
    
    def _A(self)->float:
        A = 0.45724*self.pr/(self.tr**2)*self._alpha()
        return A
    
    def _B(self)->float:
        B = 0.07780*self.pr/self.tr
        return B

    # def _a(self)->float:
    #     a = 0.45724*self.R**2*self.tc**2/self.pc
    #     return a
    
    # def _b(self)->float:
    #     b = 0.07780*self.R*self.tc/self.pc
    #     return b

    def _fatorDeCompressibilidade(self) -> float:
        B = self._B()
        A = self._A()
        raizes = np.roots([1, B-1, -3*B**2+A-2*B, -A*B+B**2+B**3])
        numerosReais = [numero for numero in raizes if np.isreal(numero)]
        Z = np.real(max(numerosReais))
        return Z

    def _fatorComZ(self)-> float:
        B = self._B()
        Z = self._fatorDeCompressibilidade()
        numerador = Z + (1 + 2**(1/2))*B
        denominador = Z + (1 - 2**(1/2))*B
        fatorcomz = math.log(numerador/denominador)
        return fatorcomz
    
    def _fatorphi(self)-> float:
        fatorphi = 1/(2*2**(1/2))*(5.8771208/self.tr)
        return fatorphi

    def PropriedadesTermodinamicas(self) -> Tuple[float, float, float]:
        fatorphi = self._fatorphi()
        fatorcomz = self._fatorComZ()
        talphalinha = self._talphalinha()
        alpha = self._alpha()
        z = self._fatorDeCompressibilidade()

        cte = fatorphi*(talphalinha - alpha)*fatorcomz 
        Hr = self.R*self.t*(cte+(z-1))
        Ur = self.R*self.t*(cte)
        Sr = self.R*(math.log(z - self._B())+fatorphi*talphalinha*fatorcomz)

        return Hr, Ur, Sr