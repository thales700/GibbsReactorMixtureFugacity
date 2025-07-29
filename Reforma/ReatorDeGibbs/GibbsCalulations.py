from scipy.optimize import fsolve
from scipy.optimize import least_squares, fsolve
from .EquacoesDeEquilibrio import EquacoesDeEquilibrio
from ..ConstanteDeEquilibrio.ConstanteDeEquilibrio import ConstanteDeEquilibrio
from ..Fugacidade.FugacidadeMisturaPengRobinson import FugacidadeMisturaPengRobinson
from ..Molecula.DataBase import *

def GibbsCalculations(Temperatura: float, Pressao: float, nomeMoleculas:list[str], moleculas:list[Molecula], coeficientesEstequiometricos: list, molsIniciais: list, estimativasIniciais: list, regioesDeBusca: list):

    #Configuracao dos molsIniciais e fugacidade 
    for i in range(len(moleculas)):
        moleculas[i].molInicial = molsIniciais[i]
        moleculas[i].fugacidade = 1

    #R em kJ/mol.K
    constantesDeEquilibrio = ConstanteDeEquilibrio(
                                                        moleculas,
                                                        coeficientesEstequiometricos,
                                                        8.314462e-3, 
                                                        Temperatura, 
                                                        Pressao).CalcularKNaTemperatura()

    equacoesSimples = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao)
    #solucaoSimples = least_squares(equacoesSimples.EquacoesDoEquilibrio,  x0 = estimativasIniciais, bounds=regioesDeBusca)
    solucaoSimples = fsolve(equacoesSimples.EquacoesDoEquilibrio,  estimativasIniciais)

    FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
    equacoesFmix = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao)
    #initial_guess = [estimativa for estimativa in solucaoSimples.x]
    initial_guess = [estimativa for estimativa in solucaoSimples]
    #solucao = least_squares(equacoesFmix.EquacoesDoEquilibrio, x0 = initial_guess, bounds=regioesDeBusca) 
    solucao = fsolve(equacoesFmix.EquacoesDoEquilibrio, initial_guess) 
    #solucao = brute(equacoesFmix.EquacoesDoEquilibrio, ranges=regioesDeBusca) 

    resultado = {"temperatura":Temperatura, "pressao":Pressao}
    resultado[nomeMoleculas[0]+'in'] = moleculas[0].molInicial
    resultado[nomeMoleculas[1]+'in'] = moleculas[1].molInicial
    for i in range(len(constantesDeEquilibrio)): 
        resultado["k"+str(i+1)] = constantesDeEquilibrio[i]
        
    for i in range(len(constantesDeEquilibrio)):
        #resultado["cs"+str(i+1)] = solucao.x[i]
        resultado['cs'+str(i+1)] = solucao[i]

    resultado['xCH4'] = (moleculas[0].molInicial-moleculas[0].molsFinal)/moleculas[0].molInicial

    molsFinal = 0
    for nome, molecula in zip(nomeMoleculas, moleculas):
        resultado[nome+"final"] = molecula.molsFinal
        if nome != "C":
            molsFinal+= molecula.molsFinal
        resultado["fugacidade"+nome] = molecula.fugacidade
    
    for nome, molecula in zip(nomeMoleculas, moleculas):
        if nome != "C":
            resultado['y'+nome] = molecula.molsFinal/molsFinal
        else:
            resultado['w'+nome] = 1

    return resultado