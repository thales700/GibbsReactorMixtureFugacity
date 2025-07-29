import pandas as pd
import numpy as np
from Reforma.ReatorDeGibbs.GibbsMinimization import *
import matplotlib.pyplot as plt

nomeMoleculas = ["CH4", "H2O", "H2", "CO", "CO2"]#, "C"]
moleculas = [CH4, H2O, H2,  CO, CO2]#, C]
coeficientesEstequiometricos = [
    #CH4   H2O  H2,  CO,  CO2,  C  
    #SRM
    [-1,     -1,  3,   1,   0,  0],
    #Secundária SRM
    [-1,     -2,  4,   0,   1,  0],    
    # #DRM
    [-1,      0,  2,   2,   -1, 0],
    #WGS
    [0,    -1,   1,   -1,  1, 0],
    #Decomposicao do Metano
    [-1,   0,   2,    0,   0,  1],
    #Desproporção do Monóxido de Carbono
    [0,    0,   0,    -2,  1,  1],
    #Redução do Monóxido de Carbono
    [0,     1,   -1,  -1,  0,   1],
    #Redução do Dióxido de Carbono
    [0,     2,  -2,   0,  -1,   1]
]

athomsByMolecule =[
    #C   #H   #O
    [1,   4,   0], #CH4
    [0,   2,   1], #H2O
    [0,   2,   0], #H2
    [1,   0,   1], #CO
    [1,   0,   2], #CO2
    #[1,   0,   0] #C
]

initialStep = [0.2, 0.2, 0.5, 0.2, 0.1]
bounds = [(0, 30), (0, 30), (0, 30), (0, 30), (0, 30)]

Pressao = 1 #bar
Temperatures = [x for x in range(600, 1500, 50)]
ComposicaoCH4 = [x/10 for x in range(60, 85, 5)]
# initialMolsCH4 = 10
# initialMolsCO2 = initialMolsCH4*0.8
# initialMolslH2O = initialMolsCH4*0.4
results = []
for Temperature in Temperatures:
    for composicao in ComposicaoCH4:
        molsIniciais = [
            #"CH4",      "H2O", "H2", "CO", "CO2", "C"
            #composicao,  (10-composicao), 0,   0,  10-composicao, 0
            composicao,   0,      0,   0,    (10-composicao)
        ]
        result = GibbsMinimization(Temperature, Pressao, nomeMoleculas,
                            moleculas, coeficientesEstequiometricos,
                            molsIniciais, athomsByMolecule, initialStep, bounds)
        results.append(result)

finalCalcDf = pd.DataFrame(results)
#finalCalcDf.to_excel('FirstReactorWithoutCoke_LessData.xlsx')
finalCalcDf.to_hdf('FirstReactorWithoutCoke_LessData.h5', key='s')
# print(finalCalcDf['fugacidadeH2'])

# plt.figure(figsize=(10,6))
# plt.subplot(1, 2, 1)
# plt.plot(finalCalcDf['temperatura'] - 273, (finalCalcDf['CH4in'] - finalCalcDf['CH4final'])/finalCalcDf['CH4in'], label ='xCH4', color = 'black', marker = 's')
# plt.plot(finalCalcDf['temperatura'] - 273, (finalCalcDf['CO2in'] - finalCalcDf['CO2final'])/finalCalcDf['CO2in'], label ='xCO2', color = 'lime', marker = '^')
# plt.plot(finalCalcDf['temperatura'] - 273, finalCalcDf['H2final']/(2*finalCalcDf['CH4in']+initialMolslH2O), label = 'Rend. H2', color = 'blue', marker = 'o')
# plt.plot(finalCalcDf['temperatura'] - 273, finalCalcDf['COfinal']/(finalCalcDf['CH4in']+initialMolsCO2), label = 'Rend. CO', color = 'red', marker = 'v')
# plt.plot(finalCalcDf['temperatura'] - 273, finalCalcDf['Cfinal']/(finalCalcDf['CH4in']+initialMolsCO2), label = 'Rend. C', color = 'magenta', marker = '<')
# plt.xlabel('Temperatura ºC')
# plt.ylabel('Parametros %')
# plt.legend()
# plt.show()
