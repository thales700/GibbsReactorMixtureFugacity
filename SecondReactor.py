import pandas as pd
import numpy as np
from Reforma.ReatorDeGibbs.GibbsMinimization import *
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed

nomeMoleculas = ["CH4", "H2O", "H2", "CO", "CO2", "C"]
moleculas = [CH4, H2O, H2,  CO, CO2, C]
coeficientesEstequiometricos = [
    #CH4   H2O  H2,  CO,  CO2,  C  
    #SRM
    [-1,     -1,  3,   1,   0,  0],
    #Secundária SRM
    [-1,     -2,  4,   0,   1,  0],    
    #DRM
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
    [1,   0,   0] #C
]

initialStep = [0.2, 0.2, 0.5, 0.2, 0.1, 1]
bounds = [(0, 30), (0, 30), (0, 30), (0, 30), (0, 30), (0, 30)]


resultFirstReactor = pd.read_hdf('FirstReactorWithoutCoke_LessData.h5', key='s')
#resultFirstReactor = resultFirstReactor.loc[resultFirstReactor['CH4final'] >= 0.05]
initialTemperature = 600 #K
finalTemperatura = 1500 #K
temperatures = [x for x in range(initialTemperature, finalTemperatura+25, 50)]
Pressao = 20 #bar
#Pressao = 1 #bar
#minimalWater = resultFirstReactor['CH4final'].min()*2
print(resultFirstReactor['CH4final'].min()*5, resultFirstReactor['CH4final'].max())
minimalWater = resultFirstReactor['CH4final'].min()*2
maximalWater = resultFirstReactor['CH4final'].max()*2
WaterIN = [x/1000 for x in range(int(minimalWater*1000+500), int(maximalWater*1000),250)]

initialTime = time.time()
results = []

def process_combination(water, temperature, row):
    ch4in = resultFirstReactor['CH4final'].iloc[row]
    co2in = resultFirstReactor['CO2final'].iloc[row]
    h2in = resultFirstReactor['H2final'].iloc[row]
    coin = resultFirstReactor['COfinal'].iloc[row]
    h2oin = resultFirstReactor['H2Ofinal'].iloc[row]
    temperatureR1 = resultFirstReactor['temperatura'].iloc[row]
    ch4inR1 = resultFirstReactor['CH4in'].iloc[row]
    co2inR1 = resultFirstReactor['CO2in'].iloc[row]
    #cFormedR1 = resultFirstReactor['Cfinal'].iloc[row]
    totalWater = water if water > h2oin else h2oin
    molsIniciais = [
        #CH4   "H2O", "H2", "CO", "CO2", "C"
        ch4in, totalWater, h2in, coin, co2in, 0
    ]
    
    gibbs_result = GibbsMinimization(temperature, Pressao, nomeMoleculas,
                                     moleculas, coeficientesEstequiometricos,
                                     molsIniciais, athomsByMolecule, initialStep, bounds)
    
    result = {
        'temperaturaR1': temperatureR1,
        'ch4inR1': ch4inR1,
        'co2inR1': co2inR1,
        'h2inR2': h2in,
        'coinR2': coin,
        'WaterInR2': totalWater,
        'temperaturaR2': temperature,
        'pressaoR2': Pressao,
        'CH4inR2': ch4in,
        'CO2inR2': co2in,
        'H2inR2': h2in,
        'COinR2': coin,
        'H2OinR2': totalWater,
        **gibbs_result
    }
    
    return result

# Processamento paralelo
results = Parallel(n_jobs=-1)(delayed(process_combination)(water, temperature, row) 
                              for water in WaterIN 
                              for temperature in temperatures 
                              for row in range(resultFirstReactor.shape[0]))

# Converte os resultados em um DataFrame
df_results = pd.DataFrame(results)
df_results.to_hdf('SecondReactorWithBothCokeP20_2_LessData.h5', key='s')