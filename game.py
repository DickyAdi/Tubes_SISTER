# KELAS GAME, BERISI SELURUH INFORMASI PERMAINAN #

class Game:

	# INISIASI VARIABLE #
	def __init__(self, id):
		self.p1Move = False
		self.p2Move = False
		self.ready = False
		self.id = id
		self.moves = [None, None]
		self.wins = [0, 0]
		self.ties = 0

	def get_player_move(self, p):
		return self.moves[p]

	# INISIASI GERAKAN #
	def play(self, player, move):
		self.moves[player] = move
		if player == 0:
			self.p1Move = True
		else:
			self.p2Move = True

	# CONNECT KE SERVER #
	def connected(self):
		return self.ready

	def bothMove(self):
		return self.p1Move and self.p2Move

	# GAME RULES #
	def winner(self):
		p1 = self.moves[0].upper()[0]
		p2 = self.moves[1].upper()[0]

		winner = -1

		if p1 == "B" and p2 == "G":
			winner = 0
		elif p1 == "G" and p2 == "B":
			winner = 1
		elif p1 == "K" and p2 == "B":
			winner = 0
		elif p1 == "B" and p2 == "K":
			winner = 1
		elif p1 == "G" and p2 == "K":
			winner = 0
		elif p1 == "K" and p2 == "G":
			winner = 1

		return winner

	# RESET GERAKAN #
	def resetMove(self):
		self.p1Move = False
		self.p2Move = False