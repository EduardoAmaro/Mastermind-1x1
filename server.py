import random
from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


class Mov:
	pinos = [0, 0, 0, 0]  # 1 - vermelho 2 - azul 3 - amarelo 4 - verde 5 - rosa 6 - lilás
	avaliacao = [0, 0, 0, 0]  # 1 - branco 2 - preto


class Game:
	player_0_win = False
	player_1_win = False
	player = 0
	NUMPLAYERS = 2
	jogada_server = Mov()
	jogada_server_player_1 = Mov()
	jogadas_player_0 = [Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov()]
	jogadas_player_1 = [Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov(), Mov()]
	turn_mov = 0
	movimentos = 0
	terminou = False

	def __init__(self):
		colors = [1, 2, 3, 4, 5, 6]
		self.jogada_server.pinos = random.sample(colors, 4)
		self.jogada_server_player_1.pinos = random.sample(colors, 4)

	def set_jogada(self, player, mov):
		movstr = str(mov)
		if player == 0:
			self.jogadas_player_0[self.movimentos].pinos[0] = int(movstr[0])
			self.jogadas_player_0[self.movimentos].pinos[1] = int(movstr[1])
			self.jogadas_player_0[self.movimentos].pinos[2] = int(movstr[2])
			self.jogadas_player_0[self.movimentos].pinos[3] = int(movstr[3])
		else:
			self.jogadas_player_1[self.movimentos].pinos[0] = int(movstr[0])
			self.jogadas_player_1[self.movimentos].pinos[1] = int(movstr[1])
			self.jogadas_player_1[self.movimentos].pinos[2] = int(movstr[2])
			self.jogadas_player_1[self.movimentos].pinos[3] = int(movstr[3])

	def take_turn(self):
		self.player = (self.player + 1) % self.NUMPLAYERS
		return self.player

	def avalia_jogada(self, player):
		result = []
		if player == 0:
			for i in range(0, 4):
				if self.jogadas_player_0[self.movimentos].pinos[i] == self.jogada_server.pinos[i]:
					self.jogadas_player_0[self.movimentos].avaliacao[i] = 2
					result.append(2)
				else:
					entrou = 0
					for j in range(0, 4):
						if self.jogadas_player_0[self.movimentos].pinos[i] == self.jogada_server.pinos[j]:
							self.jogadas_player_0[self.movimentos].avaliacao[i] = 1
							result.append(1)
							entrou = 1
					if entrou == 0:
						result.append(0)
			random.shuffle(result)
			return result
		else:
			for i in range(0, 4):
				if self.jogadas_player_1[self.movimentos].pinos[i] == self.jogada_server_player_1.pinos[i]:
					self.jogadas_player_1[self.movimentos].avaliacao[i] = 2
					result.append(2)
				else:
					entrou = 0
					for j in range(0, 4):
						if self.jogadas_player_1[self.movimentos].pinos[i] == self.jogada_server_player_1.pinos[j]:
							self.jogadas_player_1[self.movimentos].avaliacao[i] = 1
							result.append(1)
							entrou = 1
					if entrou == 0:
						result.append(0)
			random.shuffle(result)
			return result

	def is_win(self, player):
		cont = 0
		if player == 0:
			for i in range(0, 4):
				if self.jogadas_player_0[self.movimentos].avaliacao[i] == 2:
					cont += 1
			if cont == 4:
				return True
			else:
				return False
		else:
			for i in range(0, 4):
				if self.jogadas_player_1[self.movimentos].avaliacao[i] == 2:
					cont += 1
			if cont == 4:
				return True
			else:
				return False

	def make_mov(self, player, mov):
		if self.terminou:
			return -1, "Jogo encerrado"

		if player != self.player:
			return -2, "Não é seu turno"

		if self.movimentos == 9 and self.turn_mov == 1:
			self.terminou = True
			return 3, "Jogadas encerradas, nenhum vencedor"

		self.set_jogada(player, mov)

		result = self.avalia_jogada(player)

		self.turn_mov += 1

		if self.is_win(player):
			if self.turn_mov == 2:
				self.terminou = True
				self.player = -1
			self.take_turn()
			self.player_0_win = True
			return 0, "Jogador {0} ganhou".format(player)

		if self.turn_mov == 2:
			self.movimentos += 1
			self.turn_mov = 0
			if self.player_0_win:
				self.take_turn()
				return 2, "Você perdeu. Jogador 0 ganhou".format(player)

		self.take_turn()
		return 1, "Movimento bem sucedido \nJogadas restantes: {0} \nAvaliação: -{1}- -{2}- -{3}- -{4}-" \
			.format((10 - (self.movimentos + self.turn_mov)), result[0], result[1], result[2], result[3])


game = Game()

# Descomentar as linhas abaixo para que o server mostre as senhas geradas para verificação
# print("player 0: " + str(game.jogada_server.pinos))
# print("player 1: " + str(game.jogada_server_player_1.pinos))


@socketio.on('connect', namespace='/socket')
def socketConnected():
	# need visibility of the global thread object
	socketio.emit('update', namespace='/socket')
	print('Client connected')


@app.route("/jogador")
def jogador():
	if request.args.get('format') == "json":
		if game.terminou:
			return jsonify("0")
		else:
			return jsonify(game.player)
	else:
		if game.terminou:
			return "0"
		else:
			return str(game.player)


@app.route("/move")
def move():
	mov = int(request.args.get('mov'))
	player = int(request.args.get('player'))
	r = game.make_mov(player, mov)

	socketio.emit('update', namespace='/socket')

	if request.args.get('format') == "json":
		return jsonify(r)
	else:
		return str(r)


PORT_NUMBER = 8080

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=PORT_NUMBER)
