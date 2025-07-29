import numpy as np
import math
from sympy import symbols, Eq, solve
from ..Molecula.Molecula import Molecula

def FugacidadePengRobinson(T: float, P: float, molecula: Molecula):
    Z = symbols('Z')

    Tr = T/molecula.Tc
    Pr = P/molecula.Pc
    k = 0.37464+1.5422*molecula.w-.2699*molecula.w**2
    alpha = (1+k*(1-Tr**0.5))**2
    A = 0.45724*Pr*alpha/Tr**2
    B = 0.7780e-1*Pr/Tr
    raizes = np.roots([1, B-1, -3*B**2+A-2*B, -A*B+B**2+B**3])
    numerosReais = [numero for numero in raizes if np.isreal(numero)]
    Z = max(numerosReais)

    fugacidade = P*math.exp(Z-1-math.log(Z-B)-A*math.log((Z+(1+2**0.5)*B)/(Z+(1-2**0.5)*B))/(2*2**0.5*B))
    return fugacidade