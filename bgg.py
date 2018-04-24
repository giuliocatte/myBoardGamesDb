import threading
import time
import webbrowser

import bottle
import fire

USERNAME = 'giuliokatte'

from source import gui
from source.main import BGG

bgg = BGG(user=USERNAME)
s = gui.Site(bgg)
gui.set_routes(s)


class MyWSGIRefServer(bottle.ServerAdapter):
	server = None

	def run(self, handler):
		from wsgiref.simple_server import make_server, WSGIRequestHandler
		if self.quiet:
			class QuietHandler(WSGIRequestHandler):
				def log_request(*args, **kw): pass
			self.options['handler_class'] = QuietHandler
		self.server = make_server(self.host, self.port, handler, **self.options)
		self.server.serve_forever(poll_interval=0.5)

	def stop(self):
		self.server.shutdown()


class Launcher:
	def serve(self):
		bottle.run(**s.site_data)

	def generate(self):
		server = MyWSGIRefServer(**s.site_data)
		t = threading.Thread(target=bottle.run, kwargs={'server': server})
		t.start()
		webbrowser.open(s.url + 'owned')
		time.sleep(0.5)
		server.stop()

	def download(self):
		bgg.refresh_collection()

fire.Fire(Launcher)
