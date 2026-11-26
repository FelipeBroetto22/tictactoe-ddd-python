from src.application.fazer_jogada import FazerJogada
from src.application.iniciar_partida import IniciarPartida
from src.infrastructure.memoria_repository import MemoriaRepository
from src.presentation.cli import InterfaceTerminal


def main():
    repositorio = MemoriaRepository()
    interface = InterfaceTerminal(IniciarPartida(repositorio), FazerJogada(repositorio))
    interface.jogar()


if __name__ == "__main__":
    main()
