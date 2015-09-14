import requests
import json
from time import sleep
#C0D257B448BD6FC0D5B4E2D46E02C94
#7"ISteamUser/GetPlayerSummaries/v0002/"

'''
DOTA_MATCH_TYPES = {
    -1: 'Invalid',
    0: 'Public matchmaking',
    1: 'Practice',
    2: 'Tournament',
    3: 'Tutorial',
    4: 'Co-op with bots',
    5: 'Team match',
    6: 'Solo Queue',
    7: 'Ranked',
    8: 'Solo Mid 1vs1'
}
'''

class DotaSniffer:
    """Creates a Sniffer to pull data from Valve's API for DOTA2."""
    def __init__(self, apikey=None):
        if not keypath:
            raise Exception("No API key was parsed")
        self.__apikey = apikey

    
    def doApiRequest(self, method=None, query=None):
        """Sends an direct request for DOTA2's API."""
        if not method:
            raise Exception("doApiRequest needs an method")
        
        url = 'https://api.steampowered.com/'
        url += ('&' if '?' in url else '?') + 'key={0}'.format(self.__apikey)
        if query:
            for key in query:
                url += ''.join(['&', key, '=', query[key]])
        while True:
            r = requests.get(url)
            if r.text.startswith('<html>'):
                print('Got a non-json response. Possible timeout or invalid request.')
                continue
            data = json.loads(r.text)
            if 'status' in data:
                aux = data['status']
                if aux['status_code'] == 503:
                    print('Server busy, sleeping for one second.')
                    sleep(1)
                else:
                    raise Exception(aux['message'])
            else:
                break
                
        return data

    def getHeroes(self):
        """
        Returns a dict using the format dict[HeroID] -> HeroName.
        """
        method = 'IEconDOTA2_570/GetHeroes/v0001/'
        data = self.doApiRequest(method)
        heroes = {}
        for row in data['keys']:
            heroes[row] = data['keys'][row]
        return heroes

    def getItems(self):
        """
        Returns a dict using the format dict[ItemID] -> ItemName.
        """
        url = 'IEconDOTA2_570/GetGameItems/v0001/'
        data = self.doApiRequest(url)['data']
        items = {}
        for item_key in data:
            item = data[item_key]    
            items[item['id']] = item['name']
        return items


    def getMatchHistory(self, query=None)
        """Returns an list of the last 100 MatchIDs played"""
        if not region or pid:
            raise Exception("getMatchList needs a valid Region and SummonerID")
        url = 'IDOTA2Match_570/GetMatchHistory/V001/'
        data = self.doApiRequest(url, query)['matches']
        matches = []
        for match in data:
            matches.append(match['matchId'])
        return matches

    def getMatch(self, matchid=None)
        """Returns full mathch info, timeline arg optional."""
        if not matchid:
            raise Exception("getMatch needs a valid MatchID")
        method = 'IDOTA2Match_570/GetMatchDetails/v001/?match_id={0}'.format(matchid)
        data = self.doApiRequest(method)
        return data
