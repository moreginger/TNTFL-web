from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import json
from mimetools import Message
import os
from io import StringIO
import subprocess
import tntfl.test.shared_get as Get


class Deployment(Get.TestRunner):
    def setUp(self):
        if 'QUERY_STRING' in os.environ:
            del(os.environ['QUERY_STRING'])
        super(Deployment, self).setUp()

    def _getJson(self, page, query=None):
        response = self._get(page, query)
        headers = Message(StringIO(response.split('\n')[0]))
        if 'content-type' not in headers:
            print(response)
        self.assertEqual(headers['content-type'], 'application/json')
        body = ''.join(response.split('\n')[2:])
        self.assertTrue(len(body) > 0)
        return json.loads(body)

    def _page(self, page):
        return os.path.join(os.getcwd(), page)

    def _get(self, page, query):
        self._setQuery(query)
        return subprocess.check_output(['python', self._page(page)])

    def _setQuery(self, query):
        if query is not None:
            os.environ['QUERY_STRING'] = query

    def _getStatus(self, page, query):
        response = self._get(page, query)
        headers = response.split('\n')[0]
        return Message(StringIO(headers))['status']


class AddGame(Get.Tester, Deployment):
    def testAddGame(self):
        self._testPageReachable('game.cgi', 'method=add&redPlayer=foo&redScore=5&bluePlayer=bar&blueScore=5')

    def testAddGameApi(self):
        self._getJson('game.cgi', 'method=add&view=json&redPlayer=foo&redScore=5&bluePlayer=bar&blueScore=5')

    def testAddYellowStripeApi(self):
        self._getJson('game.cgi', 'method=add&view=json&redPlayer=foo&redScore=10&bluePlayer=bar&blueScore=0')

    def testNoSinglePlayer(self):
        status = self._getStatus('game.cgi', 'method=add&view=json&redPlayer=cxh&redScore=10&bluePlayer=cxh&blueScore=0')
        self.assertEqual(status, '400 Bad Request')


class Pages(Get.Pages, Deployment):
    pass


class PlayerApi(Get.PlayerApi, Deployment):
    def testNoPlayer(self):
        status = self._getStatus('player.cgi', 'view=json')
        self.assertEqual(status, '400 Bad Request')

    def testMissingPlayer(self):
        status = self._getStatus('player.cgi', 'view=json&player=missing')
        self.assertEqual(status, '404 Not Found')


class HeadToHeadApi(Get.HeadToHeadApi, Deployment):
    def testMissingPlayers(self):
        status = self._getStatus('headtohead.cgi', 'view=json')
        self.assertEqual(status, '400 Bad Request')

    def testInvalidPlayer(self):
        status = self._getStatus('headtohead.cgi', 'view=json&player1=jrem&player2=missing')
        self.assertEqual(status, '404 Not Found')


class RecentApi(Get.RecentApi, Deployment):
    pass


class LadderApi(Get.LadderApi, Deployment):
    pass


class GameApi(Get.GameApi, Deployment):
    def testNoGame(self):
        status = self._getStatus('game.cgi', 'view=json')
        self.assertEqual(status, '400 Bad Request')

    def testInvalidGame(self):
        status = self._getStatus('game.cgi', 'view=json&game=123')
        self.assertEqual(status, '404 Not Found')

    def testInvalidAdd(self):
        status = self._getStatus('game.cgi', 'view=json&method=add')
        self.assertEqual(status, '400 Bad Request')


class GamesApi(Get.GamesApi, Deployment):
    pass


class PunditApi(Get.PunditApi, Deployment):
    pass


class PredictApi(Get.PredictApi, Deployment):
    pass


class ActivePlayersApi(Get.ActivePlayersApi, Deployment):
    pass


class SpeculateApi(Get.SpeculateApi, Deployment):
    pass


class StatsApi(Get.StatsApi, Deployment):
    pass
