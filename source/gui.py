import bottle
import os


def routing(route):
    def decorator(f):
        f.route = route
        return f

    return decorator


def set_routes(app):
    for kw in dir(app):
        attr = getattr(app, kw)
        if hasattr(attr, 'route'):
            bottle.route(attr.route)(attr)


BGG_KEYS = ['gameId', 'name', 'image', 'thumbnail', 'minPlayers', 'maxPlayers', 'playingTime', 'isExpansion',
            'yearPublished', 'bggRating', 'averageRating', 'rank', 'numPlays', 'rating', 'owned', 'preOrdered',
            'forTrade', 'previousOwned', 'want', 'wantToPlay', 'wantToBuy', 'wishList', 'userComment']

this_dir = os.path.split(os.path.dirname(__file__))[0]
ASSET_DIR = os.path.join(this_dir, 'assets')
JQUERY_VERSION = '-3.2.1.min'

SITE_DATA = {'host': 'localhost', 'port': 8080}


class Site:

    def __init__(self, bgg):
        self.site_data = SITE_DATA
        self.url = 'http://{0[host]}:{0[port]}/'.format(self.site_data)
        self.bgg = bgg

    def format_td(self, name, content):
        if name == 'gameId':
            content = '<a href="https://boardgamegeek.com/boardgame/{0}" target="_">{0}</a>'.format(content)
        elif name == 'thumbnail' and content:
            content = '<img class="thumbnail" src="{}"/>'.format(content)
        elif name == 'rank':
            try:
                val = int(content)
            except ValueError:
                pass
            else:
                if val < 0:
                    content = 'n/d'
        return '<td>{}</td>'.format(content)

    def bodyrows(self, header, filter=None):
        for game in self.bgg.owned_games:
            if not filter or filter(game):
                yield (self.format_td(h, game.get(h, '')) for h, _ in header)

    @bottle.route('/static/<filename:path>')  # bottle.route routes to the unbound method
    def server_static(filename):
        return bottle.static_file(filename, root=ASSET_DIR)

    @routing('/owned')
    def index(self):
        theme = bottle.request.params.get('theme', 'green')
        header = (
            ('gameId', 'bgg id'),
            ('name', 'Titolo'),
            ('minPlayers', 'giocatori min'),
            ('maxPlayers', 'giocatori max'),
            ('playingTime', 'durata'),
            ('yearPublished', 'anno'),
            ('averageRating', 'voto medio'),
            ('rank', 'posizione in classifica'),
            ('thumbnail', '')
        )
        return '''
		<!DOCTYPE html>
		<html>
			<head>
				<title>My Collection</title>
				<link rel="stylesheet" href="static/tablesorter-master/css/theme.{theme}.css"/>
				<script type="text/javascript" src="static/jquery{jquery}.js"></script>
				<script type="text/javascript" src="static/tablesorter-master/js/jquery.tablesorter.js"></script>
				<script type="text/javascript" src="static/tablesorter-master/js/jquery.tablesorter.widgets.js"></script>
				<script type="text/javascript" src="static/main.js"></script>
				<link rel="stylesheet" href="static/main.css"/>
				<script type="text/javascript">
					var STARTING_SORT = {sort},
                        DONTSORT = {dontsort},
						THEME = "{theme}";
				</script>
			</head>
			<body>
			    <div id="headerwrapper"></div>
				<table id="bggdata">
					<thead>
						<tr>
							{header}
						</tr>
					</thead>
					<tbody>
						{new}
					</tbody>
					<tbody class="tablesorter-no-sort">
						<tr class="body-separator"><th colspan="{cols}">Classici</th></tr>
					</tbody>
					<tbody>
						{classics}
					</tbody>
				</table>

			</body>
		</html>
		'''.format(
            header=''.join('<th>{}</th>'.format(h) for _, h in header),
            new=''.join('<tr>{}</tr>'.format(''.join(r)) for r in
                        self.bodyrows(header, filter=(lambda x: x['yearPublished'] >= 1975))),
            classics=''.join('<tr>{}</tr>'.format(''.join(r)) for r in
                             self.bodyrows(header, filter=(lambda x: x['yearPublished'] < 1975))),
            theme=theme,
            sort=header.index(('rank', 'posizione in classifica'), ),
            jquery=JQUERY_VERSION,
            dontsort=header.index(('thumbnail', '')),
            cols=len(header)
        )
