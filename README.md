Servidor e cliente para jogar Mastermind 1x1 feito em Python 3.

## Requisitos
* Python 3
* Flask
* Flask-SocketIO

## Instalando Requisitos
pip install -r requirements.txt

## Executando o server

```
python3 server.py
```

## Executando os clientes

```
python3 player.py 0
```
```
python3 player.py 1
```

O jogo foi desenvolvido para dois jogadores simultâneos. Deste modo, devem ser rodadadas duas instâncias do (`player.py`). Rode o servidor, e após isso rode os dois players, passando como parâmetro o número do jogador (valores: 0 ou 1). Basicamente, o jogo necessita de três terminais simultâneos: um terminal rodando o server, um terminal rodando o player 0 e um terminal rodando o player 1.

## O Jogo
(perdi)

### Pinos de Jogada

* `1` = `Vermelho`
* `2` = `Azul`
* `3` = `Amarelo`
* `4` = `Verde`
* `5` = `Rosa`
* `6` = `Lilás`

### Pinos de Avaliação

* `0` = `Sem pino de avaliação`
* `1` = `Branco`
* `2` = `Preto`

### Regras

Um jogo de Mastermind tem pinos de seis cores diferentes, aleatórias, exceto preto e branco. Os pinos pretos e brancos são menores. Há quatro buracos grandes em cada fileira, em 10 fileiras, uma abaixo da outra. E ao lado delas, um quadrado menor, com quatro buracos menores, dois em cima de dois. Uma fileira, que seria a décima primeira, tem um defletor que esconde seus buracos. O desafiador faz uma combinação com quatro pinos coloridos, sem repetir as cores de cada pino, e as põe na décima primeira fileira e levanta o defletor, escondendo a senha. Então, o desafiado tenta adivinhar a senha, pondo quatro pinos que ele acha que são a senha na primeira fileira, e o desafiador põe os pinos pretos e brancos no quadrado menor ao lado. A regra dos pinos pretos e brancos são essas: o branco significa que há uma cor certa mas lugar errado, o preto significa que há uma cor certa no lugar certo, e nenhum pino significa que uma das cores não é contida na senha. O desafiado vai tentando adivinhar, guiando-se pelos pinos pretos e brancos. Se o desafiado não acertar até a 10ª fileira, o desafiador fecha o defletor e revela a senha, mas se adivinhar, o desafiador põe quatro pinos pretos e revela a senha (Wikipedia).

Deste modo, o Mastermind 1x1 é uma adaptação do jogo aqui apresentado. Dois jogadores tentam adivinhar uma senha gerada aleatoriamente pela máquina. Cada jogador possui uma senha específica. As jogadas são realizadas intercaladamente, por cada jogador, e a máquina avalia a tentativa de acerto a cada jogada, retornando os pinos pretos e brancos referentes à jogada. Os jogadores têm até 10 rodadas para enviar uma senha que seja igual a sua respectiva senha gerada pela máquina. Ganha o jogador que acertar antes a combinação, podendo terminar em empate caso nenhum jogador acerte sua senha, ou ambos acertem com o mesmo número de jogadas.
