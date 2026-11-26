from src.domain.exceptions import PartidaEncerrada, PosicaoOcupada
from src.domain.value_objects import Posicao, Simbolo, StatusPartida

LINHAS_VENCEDORAS = [
    [Posicao(0, 0), Posicao(0, 1), Posicao(0, 2)],
    [Posicao(1, 0), Posicao(1, 1), Posicao(1, 2)],
    [Posicao(2, 0), Posicao(2, 1), Posicao(2, 2)],
    [Posicao(0, 0), Posicao(1, 0), Posicao(2, 0)],
    [Posicao(0, 1), Posicao(1, 1), Posicao(2, 1)],
    [Posicao(0, 2), Posicao(1, 2), Posicao(2, 2)],
    [Posicao(0, 0), Posicao(1, 1), Posicao(2, 2)],
    [Posicao(0, 2), Posicao(1, 1), Posicao(2, 0)],
]


class Tabuleiro:
    def __init__(self):
        self._casas = {}

    def simbolo_em(self, posicao):
        return self._casas.get(posicao)

    def posicao_ocupada(self, posicao):
        return posicao in self._casas

    def marcar(self, posicao, simbolo):
        if self.posicao_ocupada(posicao):
            raise PosicaoOcupada()
        self._casas[posicao] = simbolo

    def esta_cheio(self):
        return len(self._casas) == 9

    def verificar_vencedor(self):
        for linha in LINHAS_VENCEDORAS:
            simbolos = [self.simbolo_em(posicao) for posicao in linha]
            if simbolos[0] is not None and simbolos.count(simbolos[0]) == 3:
                return simbolos[0]
        return None


class Partida:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = Simbolo.X
        self.status = StatusPartida.EM_ANDAMENTO
        self.vencedor = None

    def fazer_jogada(self, posicao):
        if self.status != StatusPartida.EM_ANDAMENTO:
            raise PartidaEncerrada()

        self.tabuleiro.marcar(posicao, self.jogador_atual)

        vencedor = self.tabuleiro.verificar_vencedor()
        if vencedor is not None:
            self.vencedor = vencedor
            self.status = StatusPartida.VENCIDA
        elif self.tabuleiro.esta_cheio():
            self.status = StatusPartida.EMPATADA
        else:
            self.jogador_atual = self.jogador_atual.outro()
