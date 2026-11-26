from dataclasses import dataclass
from enum import Enum

from src.domain.exceptions import PosicaoInvalida


class Simbolo(Enum):
    X = "X"
    O = "O"

    def outro(self):
        return Simbolo.O if self == Simbolo.X else Simbolo.X


class StatusPartida(Enum):
    EM_ANDAMENTO = "em andamento"
    VENCIDA = "vencida"
    EMPATADA = "empatada"


@dataclass(frozen=True)
class Posicao:
    linha: int
    coluna: int

    def __post_init__(self):
        if not (0 <= self.linha <= 2 and 0 <= self.coluna <= 2):
            raise PosicaoInvalida()
