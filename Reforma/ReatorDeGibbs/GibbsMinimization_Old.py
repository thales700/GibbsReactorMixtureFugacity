import numpy as np
from ..Molecula.DataBase_Old import *
from scipy.optimize import minimize, shgo
from .EquilibrioConstrains import EquacoesDeEquilibrio
from ..ConstanteDeEquilibrio.ConstanteDeEquilibrio import ConstanteDeEquilibrio
from ..Fugacidade.FugacidadeMisturaPengRobinson import FugacidadeMisturaPengRobinson
#from ..Fugacidade.PengRobinsonPuro import FugacidadePengRobinson


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
            #CteCalculate.dGFormacaoReal(Temperatura, Pressao, moleculas[i])
        else:
            CteCalculate.dGFormacaoTemperatura(Temperatura, Pressao, moleculas[i])
            #CteCalculate.dGFormacaoReal(Temperatura, Pressao, moleculas[i])
    
    def SystemToMinimize(molsAndLagrangianMultipliers:list):
        molsFinal = molsAndLagrangianMultipliers[0:len(nomeMoleculas)]
        lagrangianMultipliers = molsAndLagrangianMultipliers[len(nomeMoleculas):]
        dGibbsReactions = 0
        molSemCarbono = molsFinal[0:len(molsFinal)-2]
        totalMols = sum(molSemCarbono)
        for molFinal, molecula in zip(molsFinal, moleculas):
            molecula.molsFinal = molFinal
            if molecula.faseGas:
                molecula.fracaoMolar = molFinal/totalMols
                #molecula.fugacidade = FugacidadePengRobinson(Temperatura, Pressao, molecula)
            else:
                molecula.fracaoMolar = 1
                #molecula.fugacidade = 1

        FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
        

        for i in range(len(moleculas)):
            if moleculas[i].faseGas:
                dGibbsReactions += molsFinal[i]*(moleculas[i].dGFormacaoReal + R*Temperatura*np.log(moleculas[i].fracaoMolar*Pressao*moleculas[i].fugacidade))
                for j in range(len(lagrangianMultipliers)):
                    dGibbsReactions+= lagrangianMultipliers[j] * athomsByMolecule[i][j]
            
            else:
                dGibbsReactions += molsFinal[i]*(moleculas[i].dGFormacaoReal)
                for j in range(len(lagrangianMultipliers)):
                    dGibbsReactions+= lagrangianMultipliers[j] * athomsByMolecule[i][j]
        return dGibbsReactions    

    def CarbonConstraint(molsFinal):
        molsFinal = molsFinal[0:len(nomeMoleculas)]
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[0] - totalAthoms[0]

    def HydrogenConstraint(molsFinal):
        molsFinal = molsFinal[0:len(nomeMoleculas)]
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[1] - totalAthoms[1]

    def OxygenConstraint(molsFinal):
        molsFinal = molsFinal[0:len(nomeMoleculas)]
        finalAthomsAmount = np.dot(molsFinal,athomsByMolecule)
        return finalAthomsAmount[2] - totalAthoms[2]

    # def EquilibriaConstrain1(molsFinal):
    #     totalMols = sum(molsFinal)
    #     for molFinal, molecula in zip(molsFinal, moleculas):
    #         molecula.molsFinal = molFinal
    #         if molecula.faseGas:
    #             molecula.fracaoMolar = molFinal/totalMols
    #         else:
    #             molecula.fracaoMolar = 1

    #     FugacidadeMisturaPengRobinson(Temperatura, Pressao, moleculas)
    #     equacoesSimples = EquacoesDeEquilibrio(moleculas, constantesDeEquilibrio, coeficientesEstequiometricos, Pressao).EquacoesDoEquilibrio(molsFinal)
    #     return sum(equacoesSimples)

    constraints = [
    {'type': 'eq', 'fun': CarbonConstraint},
    {'type': 'eq', 'fun': HydrogenConstraint},
    {'type': 'eq', 'fun': OxygenConstraint},
    #{'type': 'eq', 'fun': EquilibriaConstrain1}
    ]
    
    solution = minimize(SystemToMinimize, initialStep, bounds = bounds, constraints=constraints, method='SLSQP', tol=1e-9)
    
    
    for i in range(len(moleculas)):
        moleculas[i].molsFinal = solution.x[i]

    resultado = {"temperatura":Temperatura, "pressao":Pressao}
    for i in range(len(moleculas)):
        molecula = moleculas[i]
        if molecula.molInicial !=0:
            resultado[nomeMoleculas[i]+'in'] = moleculas[i].molInicial
    
    for i in range(len(constantesDeEquilibrio)): 
        resultado["k"+str(i+1)] = constantesDeEquilibrio[i]
        resultado['dGibbs'+str(i+1)] = -np.log(constantesDeEquilibrio[i])*R*Temperatura

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