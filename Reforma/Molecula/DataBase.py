from .Molecula import Molecula
#Pc em Bar
#dH e dG em kJ/mol

CH4 = Molecula(dHformacao = -74.81, dGformacao = -50.72, temperaturaReferencia = 298, faseGas=True)
CH4.SetPropriedadesEstado(w = 0.012, Tc = 191.1, Pc =45.2, Zc= 0.286, Vc= 98.7e-5)
CH4.SetPropriedadesCp(A = 1.702, B= 9.081e-3, C = -2.164e-6, D = 0, E = 0)

H2O = Molecula(dHformacao=-241.818, dGformacao=-228.572, temperaturaReferencia=298, faseGas=True)
H2O.SetPropriedadesEstado(w = 0.344, Tc = 647.3, Pc = 221.2, Zc = 0.227, Vc = 55.3e-5)
H2O.SetPropriedadesCp(A=3.470, B = 1.45e-3,C= 0,D= 0.121e5,E= 0)

H2 = Molecula(dHformacao=0, dGformacao=0,temperaturaReferencia = 298, faseGas=True)
H2.SetPropriedadesCp(A=3.249, B = 0.422e-3, C = 0, D = 0.083e5, E = 0)
H2.SetPropriedadesEstado(w = -0.216, Tc = 33.3, Pc = 12.63, Zc = 0.315, Vc= 65e-5)

CO = Molecula(dHformacao=-110.525, dGformacao=-137.169,temperaturaReferencia = 298, faseGas=True)
CO.SetPropriedadesEstado(w = 0.048, Tc = 132.9, Pc = 34.05, Zc=0.295, Vc = 93.1e-5)
CO.SetPropriedadesCp(A = 3.376, B = 0.557e-3, C = 0, D= -0.031e5, E=0)

CO2 = Molecula(dHformacao=-393.51, dGformacao=-394.359, temperaturaReferencia = 298, faseGas=True)
CO2.SetPropriedadesEstado(w = 0.224, Tc = 304.2, Pc = 71.84, Zc= 0.277, Vc= 94.8e-5)
CO2.SetPropriedadesCp(A = 5.457, B = 1.045e-3, C = 0, D= -1.157e5, E=0)

C = Molecula(dHformacao= 0, dGformacao= 0, temperaturaReferencia= 298, faseGas=False)
C.SetPropriedadesCp(A=2.063, B = 0.514e-3, C=0, D=-1.057e5, E=0)
C.SetPropriedadesEstado(w = 0, Tc = 0, Pc = 0, Zc = 0, Vc = 0)

# CH4 = Molecula(dHformacao = -74.81, dGformacao = -50.72, temperaturaReferencia = 298, faseGas=True)
# CH4.SetPropriedadesEstado(w = 0.008, Tc = 190.6, Pc =4.596, Zc= 0.286, Vc= 98.7e-5)
# CH4.SetPropriedadesCp(A = 1.702, B= 9.081e-3, C = -2.164e-6, D = 0, E = 0)

# CO2 = Molecula(dHformacao=-393.51, dGformacao=-394.359, temperaturaReferencia = 298, faseGas=True)
# CO2.SetPropriedadesEstado(w = 0.225, Tc = 304.2, Pc = 7.382, Zc= 0.277, Vc= 94.8e-5)
# CO2.SetPropriedadesCp(A = 5.457, B = 1.045e-3, C = 0, D= -1.157e5, E=0)

# CO = Molecula(dHformacao=-110.525, dGformacao=-137.169,temperaturaReferencia = 298, faseGas=True)
# CO.SetPropriedadesEstado(w = 0.049, Tc = 132.9, Pc = 3.498, Zc=0.295, Vc = 93.1e-5)
# CO.SetPropriedadesCp(A = 3.376, B = 0.557e-3, C = 0, D= -0.031e5, E=0)

# H2 = Molecula(dHformacao=0, dGformacao=0,temperaturaReferencia = 298, faseGas=True)
# H2.SetPropriedadesEstado(w = -0.22, Tc = 33.2, Pc = 1.298, Zc = 0.315, Vc= 65e-5)
# H2.SetPropriedadesCp(A=3.249, B = 0.422e-3, C = 0, D = 0.083e5, E = 0)

# H2O = Molecula(dHformacao=-241.818, dGformacao=-228.572, temperaturaReferencia=298, faseGas=True)
# H2O.SetPropriedadesEstado(w = 0.344, Tc = 647.3, Pc = 22.12, Zc = 0.227, Vc = 55.3e-5)
# H2O.SetPropriedadesCp(A=3.470, B = 1.45e-3,C= 0,D= 0.121e5,E= 0)

# C = Molecula(dHformacao= 0, dGformacao= 0, temperaturaReferencia= 298, faseGas=False)
# C.SetPropriedadesCp(A=2.063, B = 0.514e-3, C=0, D=-1.057e5, E=0)
# C.SetPropriedadesEstado(w = 0, Tc = 0, Pc = 0, Zc = 0, Vc = 0)