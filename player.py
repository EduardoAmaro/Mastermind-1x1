import urllib.request
import sys
import time

if len(sys.argv) == 1:
    print("Especifique o número do jogador (0 ou 1)\n\nExemplo:    player.py 0")
    quit()

host = "http://localhost:8080"

player = int(sys.argv[1])

done = False
while not done:
    # Verifica jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == -1, o jogo acabou e o cliente perdeu
    if player_turn == -1:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn == player:

        print("1 - vermelho")
        print("2 - azul")
        print("3 - amarelo")
        print("4 - verde")
        print("5 - rosa")
        print("6 - lilás")
        move = input("Digite quatro números de cores diferentes em ordem sem espaços (ex.: 1235): ")
        while len(move) != 4:
            print("Entrada incorreta")
            move = input("Digite quatro números de cores diferentes em ordem sem espaços (ex.: 1235): ")

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&mov=%s" % (host, player, str(move)))
        msg = eval(resp.read())

        if msg[0] == 0:  # "Jogador x ganhou"
            print(msg[1])
            done = True
        elif msg[0] == 1:  # "Movimento bem sucedido Jogadas restantes: x Avaliação: xxxx"
            print(msg[1])
        elif msg[0] == 2:  # "Você perdeu. Jogador 0 ganhou"
            print(msg[1])
            done = True
        elif msg[0] == 3:  # "Jogadas encerradas, nenhum vencedor"
            print(msg[1])
            done = True
        elif msg[0] == -1:  # "Jogo encerrado"
            print(msg[1])
            done = True
        elif msg[0] == -2:  # "Não é seu turno"
            print(msg[1])
            done = True

    # Diminuir número de requisições
    time.sleep(1)
