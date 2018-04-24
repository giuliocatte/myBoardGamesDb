import requests
import json
import sqlite3


DBNAME = 'bgg_{}.db'


class BGG:

	def __init__(self, user):
		self.username = user
		self.__collection = None

	def refresh_collection(self):
		self.save_collection(self.retrieve_collection())

	def retrieve_collection(self):
		resp = requests.get('https://bgg-json.azurewebsites.net/collection/{}?grouped=true'.format(self.username))
		if resp.status_code != 200:
			raise RuntimeError("{} error from bgg: {}".format(resp.status_code, resp.text))
		return resp.json()

	def save_collection(self, collection):
		conn = sqlite3.connect(DBNAME.format(self.username))
		conn.execute('CREATE TABLE IF NOT EXISTS collection (id int not null, data text not null)')
		for game in collection:
			conn.execute('INSERT INTO collection (id, data) VALUES (?, ?)', (game['gameId'], json.dumps(game)))
		conn.commit()

	def load_collection(self):
		# la connessione non puo' essere di istanza, perche' viene usata in un thread diverso da quello in cui
		# viene generata l'istanza
		conn = sqlite3.connect(DBNAME.format(self.username))
		res = conn.execute('SELECT data FROM collection')
		return [json.loads(d[0]) for d in iter(res.fetchone, None)]

	@property
	def collection(self):
		c = self.__collection
		if not c:
			c = self.__collection = self.load_collection()
		return c

	@property
	def owned_games(self):
		for game in self.collection:
			if game['owned']:
				yield game


