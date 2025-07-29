class Molecula:
    def __init__(self, dHformacao: float, dGformacao: float, temperaturaReferencia: float, faseGas: bool):        
        self.dHformacao = dHformacao
        self.dGformacao = dGformacao
        self.temperaturaReferencia = temperaturaReferencia
        self.fugacidade: float = 1
        self.molInicial: float = None
        self.fracaoMolar: float = None
        self.molsFinal: float = None
        self.faseGas: bool = faseGas
        self.dGFormacaoReal:float = None
    
    def SetPropriedadesEstado(self, w: float, Tc: float, Pc: float, Zc: float, Vc: float):
        self.Tc = Tc
        self.Pc = Pc
        self.w = w
        self.Zc = Zc
        self.Vc = Vc

    def SetPropriedadesCp(self, A: float, B: float, C: float, D: float, E: float):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E