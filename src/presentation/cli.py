from src.domain.exceptions import ErroDeDominio
from src.domain.value_objects import Posicao, StatusPartida


class InterfaceTerminal:
    def __init__(self, iniciar_partida, fazer_jogada):
        self.iniciar_partida = iniciar_partida
        self.fazer_jogada = fazer_jogada

    def jogar(self):
        partida = self.iniciar_partida.executar()
        print("Jogo da Velha")
        print("Digite linha e coluna de 1 a 3.")

        while partida.status == StatusPartida.EM_ANDAMENTO:
            self.mostrar_tabuleiro(partida)
            print(f"Vez do jogador {partida.jogador_atual.value}")
            try:
                linha = int(input("Linha: ")) - 1
                coluna = int(input("Coluna: ")) - 1
                partida = self.fazer_jogada.executar(linha, coluna)
            except ValueError:
                print("Digite apenas números.")
            except ErroDeDominio as erro:
                print(erro)

        self.mostrar_tabuleiro(partida)
        if partida.status == StatusPartida.VENCIDA:
            print(f"O jogador {partida.vencedor.value} venceu!")
        else:
            print("Deu velha, ninguém ganhou.")

    def mostrar_tabuleiro(self, partida):
        print()
        for linha in range(3):
            casas = []
            for coluna in range(3):
                simbolo = partida.tabuleiro.simbolo_em(Posicao(linha, coluna))
                casas.append(simbolo.value if simbolo else " ")
            print(" " + " | ".join(casas))
            if linha < 2:
                print("---+---+---")
        print()
