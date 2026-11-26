class ErroDeDominio(Exception):
    pass


class PosicaoInvalida(ErroDeDominio):
    def __init__(self):
        super().__init__("Essa posição está fora do tabuleiro.")


class PosicaoOcupada(ErroDeDominio):
    def __init__(self):
        super().__init__("Essa posição já está ocupada.")


class PartidaEncerrada(ErroDeDominio):
    def __init__(self):
        super().__init__("A partida já terminou.")


class PartidaNaoEncontrada(ErroDeDominio):
    def __init__(self):
        super().__init__("Não existe partida em andamento.")
