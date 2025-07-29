import numpy as np
from ..Molecula.DataBase import *
from scipy.optimize import minimize, shgo
from .EquilibrioConstrains import EquacoesDeEquilibrio
from ..ConstanteDeEquilibrio.ConstanteDeEquilibrio import ConstanteDeEquilibrio
from ..Fugacidade.FugacidadeMisturaPengRobinson import FugacidadeMisturaPengRobinson
from ..Fugacidade.PengRobinsonPuro import FugacidadePengRobinson


def GibbsMinimization(Temperatura: float, Pressao: float, nomeMoleculas:list[str], moleculas:list[Molecula], 
                      coeficientesEstequiometricos: list, molsIniciais: list, athomsByMolecule: list, initialStep: list,
                      bounds: list):
    R =  8.314462e-3     #R em kJ/mol.K
    totalAthoms = np.dot(molsIniciais,athomsByMolecule)
    CteCalculate = ConstanteDeEquilibrio(moleculas,
                                        coeficientesEstequiometricos,
                                        8.314462e-3, 
                                        Temperatura, 
                                        Pressao)
    constantesDeEquilibrio = CteCalculate.CalcularKNaTemperatura()

    for i in range(len(moleculas)):
        moleculas[i].molInicial = molsIniciais[i]
        moleculas[i].fugacidade = 1
        if moleculas[i].faseGas:
            CteCalculate.dGFormacaoTemperatura(Temperatura, Pressao, moleculas[i])
            #print(str(nomeMoleculas[i])+": " + str(moleculas[i].dGFormacaoReal))
            #CteCalculate.dGFormacaoTemperatura(Temperatura, Pressao, moleculas[i])
        else:
            CteCalculate.dGFormacaoTemperatura(Temperatura, Pressao, moleculas[i])
    
    def SystemToMinimize(molsFinal:list):
        dGibbsReactions = 0
        molSemCarbono = molsFinal[0:5]
        totalMols = sum(molSemCarbono)
        for molFinal, molecula in zip(molsFinal, moleculas):
            molecula.molsFinal = molFinal
            if molecula.faseGas:
                molecula.fracaoMolar = molFinal/totalMols
            else:
                molecula.fracaoMolar = 1

        #FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)            
        
        for molFinal, molecula in zip(molsFinal, moleculas):
            if molecula.faseGas:
                molecula.fugacidade = 1# FugacidadePengRobinson(Temperatura, Pressao, molecula)/Pressao    
                dGibbsReactions+= molFinal*(molecula.dGFormacaoReal + R*Temperatura*np.log(molecula.fracaoMolar*Pressao*molecula.fugacidade))
            else:
                dGibbsReactions+= molFinal*(molecula.dGFormacaoReal)
        return dGibbsReactions
    
    def EquilibriaConstrain1(molsFinal):
        molSemCarbono = molsFinal[0:5]
        totalMols = sum(molSemCarbono)
        for molFinal, molecula in zip(molsFinal, moleculas):
            molecula.molsFinal = molFinal
            if molecula.faseGas:
                molecula.fracaoMolar = molFinal/totalMols
            else:
                molecula.fracaoMolar = 1

        #FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
        equacoesSimples = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao).EquacoesDoEquilibrio(molsFinal)
        return sum(equacoesSimples)
    
    # def EquilibriaConstrain2(molsFinal):
    #     totalMols = sum(molsFinal)
    #     for molFinal, molecula in zip(molsFinal, moleculas):
    #         molecula.molsFinal = molFinal
    #         molecula.fracaoMolar = molFinal/totalMols

    #     FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
    #     equacoesSimples = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao).EquacoesDoEquilibrio(molsFinal)
    #     print('Eq2: '+str(equacoesSimples[1]))
    #     return equacoesSimples[1]
    
    # def EquilibriaConstrain3(molsFinal):
    #     totalMols = sum(molsFinal)
    #     for molFinal, molecula in zip(molsFinal, moleculas):
    #         molecula.molsFinal = molFinal
    #         molecula.fracaoMolar = molFinal/totalMols

    #     FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
    #     equacoesSimples = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao).EquacoesDoEquilibrio(molsFinal)
    #     print('Eq3: '+str(equacoesSimples[2]))
    #     return equacoesSimples[2]

    def CarbonConstraint(molsFinal):
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[0] - totalAthoms[0]

    def HydrogenConstraint(molsFinal):
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[1] - totalAthoms[1]

    def OxygenConstraint(molsFinal):
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[2] - totalAthoms[2]

    constraints = [
    # {'type': 'eq', 'fun': EquilibriaConstrain2},
    # {'type': 'eq', 'fun': EquilibriaConstrain3},
    {'type': 'eq', 'fun': CarbonConstraint},
    {'type': 'eq', 'fun': HydrogenConstraint},
    {'type': 'eq', 'fun': OxygenConstraint},
    #{'type': 'eq', 'fun': EquilibriaConstrain1}
    ]
    solution = minimize(SystemToMinimize, initialStep, bounds = bounds, constraints=constraints, method='SLSQP', tol=1e-9)
    #solution = shgo(SystemToMinimize, bounds = bounds, constraints=constraints)
    
    for i in range(len(solution.x)):
        moleculas[i].molsFinal = solution.x[i]

    resultado = {"temperatura":Temperatura, "pressao":Pressao}
    for i in range(len(moleculas)):
        molecula = moleculas[i]
        if molecula.molInicial !=0:
            resultado[nomeMoleculas[i]+'in'] = moleculas[i].molInicial
    
    for i in range(len(constantesDeEquilibrio)): 
        resultado["k"+str(i+1)] = constantesDeEquilibrio[i]
        resultado['dGibbs'+str(i+1)] = -np.log(constantesDeEquilibrio[i])*R*Temperatura

    #resultado['xCH4'] = (moleculas[0].molInicial-moleculas[0].molsFinal)/moleculas[0].molInicial if moleculas[0].molInicial != 0 else 0
    #resultado['xCO2'] = (moleculas[4].molInicial-moleculas[4].molsFinal)/moleculas[4].molInicial if moleculas[4].molInicial != 0 else 0

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