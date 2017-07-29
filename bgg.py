import requests
import json


class BGG:

	def __init__(self, user):
		self.username = user
		self.__collection = None

	def set_collection(self):
		resp = requests.get('https://bgg-json.azurewebsites.net/collection/{}?grouped=true'.format(self.username))
		if resp.status_code != 200:
			raise RuntimeError("error from bgg", resp.status_code)

		coll = json.loads(resp.text)
		self.__collection = coll

	@property
	def collection(self):
		if not self.__collection:
			self.set_collection()
		return self.__collection

	@property
	def owned_games(self):
		for game in self.collection:
			if game['owned']:
				yield game


