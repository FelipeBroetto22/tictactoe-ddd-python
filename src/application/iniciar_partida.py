from src.domain.entities import Partida


class IniciarPartida:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def executar(self):
        partida = Partida()
        self.repositorio.salvar(partida)
        return partida
