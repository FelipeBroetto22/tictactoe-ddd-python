from src.domain.repositories import PartidaRepository


class MemoriaRepository(PartidaRepository):
    def __init__(self):
        self._partida = None

    def salvar(self, partida):
        self._partida = partida

    def buscar(self):
        return self._partida
