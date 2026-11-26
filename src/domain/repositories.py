from abc import ABC, abstractmethod


class PartidaRepository(ABC):
    @abstractmethod
    def salvar(self, partida):
        pass

    @abstractmethod
    def buscar(self):
        pass
