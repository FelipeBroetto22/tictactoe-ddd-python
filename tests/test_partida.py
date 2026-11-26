import unittest

from src.application.fazer_jogada import FazerJogada
from src.application.iniciar_partida import IniciarPartida
from src.domain.exceptions import PartidaEncerrada, PosicaoInvalida, PosicaoOcupada
from src.domain.value_objects import Posicao, Simbolo, StatusPartida
from src.infrastructure.memoria_repository import MemoriaRepository


class TestPartida(unittest.TestCase):
    def setUp(self):
        repositorio = MemoriaRepository()
        IniciarPartida(repositorio).executar()
        self.fazer_jogada = FazerJogada(repositorio)

    def jogar(self, jogadas):
        for linha, coluna in jogadas:
            partida = self.fazer_jogada.executar(linha, coluna)
        return partida

    def test_vitoria_na_horizontal(self):
        partida = self.jogar([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
        self.assertEqual(partida.status, StatusPartida.VENCIDA)
        self.assertEqual(partida.vencedor, Simbolo.X)

    def test_vitoria_na_vertical(self):
        partida = self.jogar([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)])
        self.assertEqual(partida.vencedor, Simbolo.X)

    def test_vitoria_na_diagonal(self):
        partida = self.jogar([(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)])
        self.assertEqual(partida.vencedor, Simbolo.X)

    def test_vitoria_do_o(self):
        partida = self.jogar([(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)])
        self.assertEqual(partida.vencedor, Simbolo.O)

    def test_empate(self):
        partida = self.jogar(
            [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]
        )
        self.assertEqual(partida.status, StatusPartida.EMPATADA)
        self.assertIsNone(partida.vencedor)

    def test_posicao_ocupada(self):
        self.jogar([(1, 1)])
        with self.assertRaises(PosicaoOcupada):
            self.fazer_jogada.executar(1, 1)

    def test_fora_do_tabuleiro(self):
        with self.assertRaises(PosicaoInvalida):
            self.fazer_jogada.executar(3, 0)
        with self.assertRaises(PosicaoInvalida):
            self.fazer_jogada.executar(0, -1)

    def test_jogada_invalida_nao_troca_o_turno(self):
        self.jogar([(1, 1)])
        with self.assertRaises(PosicaoOcupada):
            self.fazer_jogada.executar(1, 1)
        partida = self.jogar([(0, 0)])
        self.assertEqual(partida.tabuleiro.simbolo_em(Posicao(0, 0)), Simbolo.O)

    def test_partida_encerrada(self):
        self.jogar([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])
        with self.assertRaises(PartidaEncerrada):
            self.fazer_jogada.executar(2, 2)


if __name__ == "__main__":
    unittest.main()
