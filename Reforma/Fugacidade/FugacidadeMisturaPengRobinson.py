import numpy as np
import math
from sympy import symbols, Eq, solve
from ..Molecula.Molecula import Molecula

def FugacidadeMisturaPengRobinson(T: float, P: float, moleculas: list[Molecula]):
    Apure = np.zeros(len(moleculas))
    Bpure = np.zeros(len(moleculas))
    a = 0
    b = 0
    aij = np.zeros((len(moleculas), len(moleculas)))

    for i in range(len(moleculas)):
        if moleculas[i].faseGas:
            Tr = T/moleculas[i].Tc
            Pr = P/moleculas[i].Pc
            k = 0.37464+1.5422*moleculas[i].w-.2699*moleculas[i].w**2
            alpha = (1+k*(1-Tr**0.5))**2
            Apure[i] = 0.45724*Pr*alpha/Tr**2
            Bpure[i] = 0.7780e-1*Pr/Tr
            b += moleculas[i].fracaoMolar*Bpure[i]

    for i in range(len(moleculas)):
        if moleculas[i].faseGas:
            for j in range(len(moleculas)):
                aij[i,j] = (Apure[i]*Apure[j])**(0.5)
                a += moleculas[i].fracaoMolar*moleculas[j].fracaoMolar*aij[i,j]        
    
    raizes = np.roots([1, b-1, -3*b**2+a-2*b, -a*b+b**2+b**3])
    numerosReais = [numero for numero in raizes if np.isreal(numero)]
    Z = max(numerosReais)

    for i in range(len(moleculas)):
        if moleculas[i].faseGas:
            asum = 0
            for j in range(len(moleculas)):
                asum += moleculas[i].fracaoMolar*aij[i,j]
            leftSideTerm = Bpure[i]/b*(Z -1) - math.log(Z - b)
            rightSideTerm = -a/(2*(2**0.5)*b)*(2*asum/a - Bpure[i]/b)*math.log((Z+(1+2**0.5)*b)/(Z+(1-2**0.5)*b))
            moleculas[i].fugacidade = math.exp((leftSideTerm + rightSideTerm))
        
    