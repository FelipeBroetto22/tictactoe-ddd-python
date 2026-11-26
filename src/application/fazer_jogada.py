from src.domain.exceptions import PartidaNaoEncontrada
from src.domain.value_objects import Posicao


class FazerJogada:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def executar(self, linha, coluna):
        partida = self.repositorio.buscar()
        if partida is None:
            raise PartidaNaoEncontrada()

        partida.fazer_jogada(Posicao(linha, coluna))
        self.repositorio.salvar(partida)
        return partida
