def DeltaParametro(parametros: list[float], coeficientes: list[int]):
    delta = 0
    for parametro, coeficiente in zip(parametros, coeficientes):
        delta += parametro*coeficiente
    return delta
    