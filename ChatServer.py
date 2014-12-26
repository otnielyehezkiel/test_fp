__author__ = 'Otniel Yeheskiel'

#import sys
from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

hangmanpics = ['''
                +---+
                |   |
                    |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                |   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               /    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               / \  |
                    |
              =========== ''']
Kosakata = 'bankok bangalore hyderabad newyork shangai berlin calcutta ' \
           'india australia egypt ghana japan china pakistan afghanistan kenya libya chile ' \
           'bankok bangalore hyderabad newyork shangai berlin calcutta shashank ' \
           'gandhi hitler nehru che jackie brucelee vallabaipatel vivekananda'

class ClientConnect(Channel):

	def __init__(self, *args, **kwargs):
		self.pemain = "lala"
		Channel.__init__(self, *args, **kwargs)
	# Saat client disconnect
	def Close(self):
		self._server.DelPlayer(self)

	##################################
	### Network specific callbacks ###
	##################################

	# Menerima data message dari action 'message' Client lalu Mengirim Message kembali dari Client ke Client lainnya dengan action 'message'
	def Network_message(self, data):
		self._server.SendToAll({"action": "message", "message": data['message'], "who": self.pemain})
	# Mengganti nama pemain dari inputan client
	def Network_pemain(self, data):
		self.pemain = data['pemain']
		self._server.SendPlayers()

class ChatServer(Server):
	channelClass = ClientConnect

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		self.i = 0
		print 'Server launched'
	def increment(self):
		self.i += 1
		return self.i
	# Saat client connect
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
		self.KirimGambar(channel)

	def KirimGambar(self, player):
		self.SendPlayers_2()
	def RandomKata(self):
		indeks_kata = random.randint(0,len(list_kata)-1)    # Random indeks yang ada di list Kosakata
		return random.randint(0,len(list_kata)-1)
	def AddPlayer(self, player):
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		print "players", [p for p in self.players]

	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	# Mengirim ke semua Player data nama2 pemain dengan action 'players'
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.pemain for p in self.players]})
	def SendPlayers_2(self):
		self.SendToAll({"action": "gambar", "gambar": [p for p in hangmanpics]})
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]

	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

host, port = ["localhost",31425]
s = ChatServer(localaddr=(host, int(port)))
s.Launch()
