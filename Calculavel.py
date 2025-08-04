import math

class Calculavel:
    @staticmethod
    def calcular(expressao):
        try:
            expressao = expressao.replace("√", "math.sqrt")
            return eval(expressao, {"__builtins__": None, "math": math})
        except Exception as e:
            raise ValueError(f"Erro ao calcular expressão: {str(e)}")

    @staticmethod
    def exponenciar(base, expoente):
        try:
            return math.pow(base, expoente)
        except Exception as e:
            raise ValueError(f"Erro na exponenciação: {str(e)}")

    @staticmethod
    def porcentagem(valor, percentual):
        return round((valor * percentual) / 100, 6)

    @staticmethod
    def raiz_quadrada(valor):
        if valor < 0:
            raise ValueError("Não é possível calcular raiz de número negativo.")
        return round(math.sqrt(valor), 6)

    @staticmethod
    def reciproco(valor):
        if valor == 0:
            raise ZeroDivisionError("Não é possível dividir por zero.")
        return round(1 / valor, 6)