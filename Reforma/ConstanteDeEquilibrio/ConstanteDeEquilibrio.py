# import math
# import numpy as np
# from scipy.integrate import romberg, quad       
# from ..Molecula.Molecula import Molecula
# from ..ConstanteDeEquilibrio.DeltaParametro import DeltaParametro
# from ..PropriedadesDaReacao.PropriedadesDaReacao import PropriedadesDaReacao
# from ..PropriedadesTermodinamicas.ResiduaisPengRobinson import ResiduaisPengRobinson

# class ConstanteDeEquilibrio:
#     def __init__(self, moleculas: list[Molecula], coeficientesEstequiometricos: list[list], R: float, temperatura: float, pressao: float):
#         self.moleculas = moleculas
#         self.coeficientesEstequiometricos = coeficientesEstequiometricos
#         self.tFinal = temperatura
#         self.dHRxnIdeal = []
#         self.dGrxnIdeal = []
#         self.dSrxnIdeal = []
#         self.R = 8.314e-3
#         self.Pressao = pressao

#     def SetPropriedadesGasIdeal(self):
#         for i in range(len(self.coeficientesEstequiometricos)):
#             self.dHRxnIdeal.append(PropriedadesDaReacao.CalcularDeltaHReacao(self.moleculas, self.coeficientesEstequiometricos[i]))
#             self.dGrxnIdeal.append(PropriedadesDaReacao.CalcularDeltaGReacao(self.moleculas, self.coeficientesEstequiometricos[i]))
#             self.dSrxnIdeal.append((self.dHRxnIdeal[i] - self.dGrxnIdeal[i])/298)

#     def CalcularKNaTemperatura(self) -> list[float]: # type: ignore
#         self.SetPropriedadesGasIdeal()
#         dHRxns = []
#         dSRxns= []
#         dGRxns = []
#         Krxns = []

#         def _CpEntalpia(T, coefEstequiometricos):
#             deltaCp = 0.0
#             for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
#                 deltaCp += coeficiente*(molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)
#             return deltaCp
        
#         def _CpEntropia(T, coefEstequiometricos):
#             deltaCp = 0.0
#             for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
#                 if molecula.faseGas:
#                     deltaCp += coeficiente*(molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)
#                 # else:
#                 #     deltaCp += coeficiente*(molecula.A+molecula.B+molecula.C/(T**2))
#             return deltaCp/T
        
#         def SegundoTermo(P, coefEstequiometricos):
#             deltaRP = 0
#             for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
#                 if molecula.faseGas:
#                     deltaRP = coeficiente*self.R/P
#                     #deltaRP += self.R/P
#             return deltaRP
        
#         for i in range(len(self.coeficientesEstequiometricos)):
#             coeficientesEstequiometricos = self.coeficientesEstequiometricos[i]
#             integralEntalpia = quad(_CpEntalpia, 298, self.tFinal, args=(coeficientesEstequiometricos))[0]
#             integralEntropiaPrimeiroTermo = quad(_CpEntropia, 298, self.tFinal, args=(coeficientesEstequiometricos))[0] 
#             dHRxns.append(self.dHRxnIdeal[i] + self.R*integralEntalpia)
#             #dSRxns.append(self.dSrxnIdeal[i] + self.R*integralEntropiaPrimeiroTermo - quad(SegundoTermo, 1, self.Pressao, args=(coeficientesEstequiometricos))[0])
#             dSRxns.append(self.dSrxnIdeal[i] + self.R*integralEntropiaPrimeiroTermo)
#             dGRxns.append(dHRxns[i] - self.tFinal*dSRxns[i]) 
#             Krxns.append(math.exp(-dGRxns[i]/(self.R*self.tFinal)))

#         return Krxns

#     def _ConstanteEquilibrio(self, temperatura: float):
#         return math.exp(-self.dGrxnIdeal/(self.R*temperatura))
    
#     def _RPEntropia(self, Pressao, coefEstequiometricos):
#         return -np.sum(coefEstequiometricos)*self.R/self.Pressao    

#     def dGFormacaoTemperatura(self, T, P, molecula: Molecula):
#         def Cp(T):
#             return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)

#         def CpT(T):
#             return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)/T
        
#         def SegundoTermo(P):
#             return self.R/P

#         entalpiaFormacaoTemp = self.R*quad(Cp, 298, T)[0]
#         entroPiaTempPrimeiroTermo = self.R*quad(CpT, 298, T)[0]   
#         entalpiaFormacaoTemp += molecula.dHformacao
#         #entropiaSegundoTermo = -quad(SegundoTermo, 1, P)[0] if molecula.faseGas else 0
#         #entropiaFormacaoTemp = entroPiaTempPrimeiroTermo + entropiaSegundoTermo + (molecula.dHformacao - molecula.dGformacao)/298
#         entropiaFormacaoTemp = entroPiaTempPrimeiroTermo + (molecula.dHformacao - molecula.dGformacao)/298
#         molecula.dGFormacaoReal = (entalpiaFormacaoTemp - T*entropiaFormacaoTemp)
    
#     def dGFormacaoReal(self, T, P, molecula: Molecula):
#         def Cp(T):
#             return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)

#         def CpT(T):
#             return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)/T
        
#         def SegundoTermo(P):
#             return self.R/P

#         entalpiaIdeal = self.R*quad(Cp, 298, T)[0] + molecula.dHformacao
#         entropiaIdeal = self.R*quad(CpT, 298, T)[0] -quad(SegundoTermo, 1, P)[0]  + (molecula.dHformacao - molecula.dGformacao)/298
#        #entropiaIdeal = self.R*quad(CpT, 298, T)[0] + (molecula.dHformacao - molecula.dGformacao)/298
#         propriedadesResiduais =  ResiduaisPengRobinson(self.R, T, P, molecula.w, molecula.Tc, molecula.Pc)
#         entalpiaResidual, internaResidual, entropiaResidual = propriedadesResiduais.PropriedadesTermodinamicas()
#         entalpiaReal = entalpiaResidual + entalpiaIdeal
#         entropiaReal = entropiaResidual + entropiaIdeal
#         molecula.dGFormacaoReal = (entalpiaReal - T*entropiaReal)

import math
import numpy as np
from scipy.integrate import quad       
from ..Molecula.Molecula import Molecula
from ..ConstanteDeEquilibrio.DeltaParametro import DeltaParametro
from ..PropriedadesDaReacao.PropriedadesDaReacao import PropriedadesDaReacao
from ..PropriedadesTermodinamicas.ResiduaisPengRobinson import ResiduaisPengRobinson

class ConstanteDeEquilibrio:
    def __init__(self, moleculas: list[Molecula], coeficientesEstequiometricos: list[list], R: float, temperatura: float, pressao: float):
        self.moleculas = moleculas
        self.coeficientesEstequiometricos = coeficientesEstequiometricos
        self.tFinal = temperatura
        self.dHRxnIdeal = []
        self.dGrxnIdeal = []
        self.dSrxnIdeal = []
        self.R = 8.314e-3
        self.Pressao = pressao

    def SetPropriedadesGasIdeal(self):
        for i in range(len(self.coeficientesEstequiometricos)):
            self.dHRxnIdeal.append(PropriedadesDaReacao.CalcularDeltaHReacao(self.moleculas, self.coeficientesEstequiometricos[i]))
            self.dGrxnIdeal.append(PropriedadesDaReacao.CalcularDeltaGReacao(self.moleculas, self.coeficientesEstequiometricos[i]))
            self.dSrxnIdeal.append((self.dHRxnIdeal[i] - self.dGrxnIdeal[i])/298)

    def CalcularKNaTemperatura(self) -> list[float]: # type: ignore
        self.SetPropriedadesGasIdeal()
        dHRxns = []
        dSRxns= []
        dGRxns = []
        Krxns = []

        def _CpEntalpia(T, coefEstequiometricos):
            deltaCp = 0.0
            for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
                deltaCp += coeficiente*(molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)
            return deltaCp
        
        def _CpEntropia(T, coefEstequiometricos):
            deltaCp = 0.0
            for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
                if molecula.faseGas:
                    deltaCp += coeficiente*(molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)
                # else:
                #     deltaCp += coeficiente*(molecula.A+molecula.B+molecula.C/(T**2))
            return deltaCp/T
        
        def SegundoTermo(P, coefEstequiometricos):
            deltaRP = 0
            for molecula, coeficiente in zip(self.moleculas, coefEstequiometricos):
                if molecula.faseGas:
                    deltaRP = coeficiente*self.R/P
                    #deltaRP += self.R/P
            return deltaRP
        
        for i in range(len(self.coeficientesEstequiometricos)):
            coeficientesEstequiometricos = self.coeficientesEstequiometricos[i]
            integralEntalpia = quad(_CpEntalpia, 298, self.tFinal, args=(coeficientesEstequiometricos))[0]
            integralEntropiaPrimeiroTermo = quad(_CpEntropia, 298, self.tFinal, args=(coeficientesEstequiometricos))[0] 
            dHRxns.append(self.dHRxnIdeal[i] + self.R*integralEntalpia)
            #dSRxns.append(self.dSrxnIdeal[i] + self.R*integralEntropiaPrimeiroTermo - quad(SegundoTermo, 1, self.Pressao, args=(coeficientesEstequiometricos))[0])
            dSRxns.append(self.dSrxnIdeal[i] + self.R*integralEntropiaPrimeiroTermo)
            dGRxns.append(dHRxns[i] - self.tFinal*dSRxns[i]) 
            Krxns.append(math.exp(-dGRxns[i]/(self.R*self.tFinal)))

        return Krxns

    def _ConstanteEquilibrio(self, temperatura: float):
        return math.exp(-self.dGrxnIdeal/(self.R*temperatura))
    
    def _RPEntropia(self, Pressao, coefEstequiometricos):
        return -np.sum(coefEstequiometricos)*self.R/self.Pressao    

    def dGFormacaoTemperatura(self, T, P, molecula: Molecula):
        def Cp(T):
            return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)

        def CpT(T):
            return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)/T
        
        def SegundoTermo(P):
            return self.R/P

        entalpiaFormacaoTemp = self.R*quad(Cp, 298, T)[0]
        entroPiaTempPrimeiroTermo = self.R*quad(CpT, 298, T)[0]   
        entalpiaFormacaoTemp += molecula.dHformacao
        #entropiaSegundoTermo = -quad(SegundoTermo, 1, P)[0] if molecula.faseGas else 0
        #entropiaFormacaoTemp = entroPiaTempPrimeiroTermo + entropiaSegundoTermo + (molecula.dHformacao - molecula.dGformacao)/298
        entropiaFormacaoTemp = entroPiaTempPrimeiroTermo + (molecula.dHformacao - molecula.dGformacao)/298
        molecula.dGFormacaoReal = (entalpiaFormacaoTemp - T*entropiaFormacaoTemp)
    
    def dGFormacaoReal(self, T, P, molecula: Molecula):
        def Cp(T):
            return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)

        def CpT(T):
            return (molecula.A + molecula.B*T+molecula.C*T**2 + molecula.D/(T**2)+molecula.E*T**3)/T
        
        def SegundoTermo(P):
            return self.R/P

        entalpiaIdeal = self.R*quad(Cp, 298, T)[0] + molecula.dHformacao
        entropiaIdeal = self.R*quad(CpT, 298, T)[0] -quad(SegundoTermo, 1, P)[0]  + (molecula.dHformacao - molecula.dGformacao)/298
       #entropiaIdeal = self.R*quad(CpT, 298, T)[0] + (molecula.dHformacao - molecula.dGformacao)/298
        propriedadesResiduais =  ResiduaisPengRobinson(self.R, T, P, molecula.w, molecula.Tc, molecula.Pc)
        entalpiaResidual, internaResidual, entropiaResidual = propriedadesResiduais.PropriedadesTermodinamicas()
        entalpiaReal = entalpiaResidual + entalpiaIdeal
        entropiaReal = entropiaResidual + entropiaIdeal
        molecula.dGFormacaoReal = (entalpiaReal - T*entropiaReal)