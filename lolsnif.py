import requests
import json
from time import sleep

class LeagueSniffer:
    """Creates a Sniffer to pull data form Riot's API for League of Legends."""
    def __init__(self, apikey=None):
        if not keypath:
            raise Exception("No API key was parsed")
        self.__apikey = apikey

    
    def doApiRequest(self, url=None, query=None):
        """Sends an direct request for Riot's API."""
        if not url:
            raise Exception("doApiRequest needs an URL")
        
        url += ('&' if '?' in url else '?') + 'api_key={0}'.format(self.__apikey)
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
                if aux['status_code'] == 429:
                    print('Reached the limit of requests, sleeping for one second.')
                    print('Watch out, you can be blacklisted by Riot for exceding the limit all the time.')
                    sleep(1)
                else:
                    raise Exception(aux['message'])
            else:
                break
                
        return data

    def getRegions(self):
        """ Returns a list of current active regions of Riot's servers. """
        url = 'http://status.leagueoflegends.com/shards'
        data = self.doApiRequest(url)
        regions = []
        for region in data:
            regions.append(region['slug'])
        # Idk why korea isn't listed on active shards
        # Also, garena/china ???
        regions.append('kr')
        return regions

    def getChampions(self):
        """
        Returns a dict using the format dict[ChampionID] -> ChampionName.
        """
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all'
        data = self.doApiRequest(url)
        champs = {}
        for row in data['keys']:
            champs[row] = data['keys'][row]
        return champs

    def getItems(self):
        """
        Returns a dict using the format dict[ItemID] -> ItemName.
        """
        url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?itemListData=all'
        data = self.doApiRequest(url)['data']
        items = {}
        for item_key in data:
            item = data[item_key]    
            items[item['id']] = item['name']
        return items

    def getChallengerPlayersID(self, region=None):
        """Returns the summonerID of all players on challenger league of certain region."""
        if not region:
            raise Exception("getChallengerPlayersID needs an region to be specified")
        url = 'https://{0}.api.pvp.net/api/lol/{0}/v2.5/league/challenger?type=RANKED_SOLO_5x5'.format(region)
        data = self.doApiRequest(url)
        pids = []
        for player in data['entries']:
            pids.append(player['playerOrTeamId'])
        return pids

    def getMasterPlayersID(self, region=None):
        """Returns the summonerID of all players on master league of certain region."""
        if not region:
            raise Exception("getMasterPlayersID needs an region to be specified")
        url = 'https://{0}.api.pvp.net/api/lol/{0}/v2.5/league/master?type=RANKED_SOLO_5x5'.format(region)
        data = self.doApiRequest(url)
        pids = []
        for player in data['entries']:
            pids.append(player['playerOrTeamId'])
        return pids

    def getMatchList(self, region=None, pid=None, query=None)
        """Returns an list of MatchIDs for a given player on a region."""
        if not region or pid:
            raise Exception("getMatchList needs a valid Region and SummonerID")
        url = 'https://{0}.api.pvp.net/api/lol/{0}/v2.2/matchlist/by-summoner/{1}'.format(region, pid)
        data = self.doApiRequest(url, query)['matches']
        matches = []
        for match in data:
            matches.append(match['matchId'])
        return matches

    def getMatch(self, region=None, matchid=None, timeline=False)
        """Returns full mathch info, timeline arg optional."""
        if not region or matchid:
            raise Exception("getMatch needs a valid Region and MatchID")
        url = 'https://{0}.api.pvp.net/api/lol/{0}/v2.2/match/{1}'.format(region, matchid)
        if timeline:
            url += '?includeTimeline=True'
        data = self.doApiRequest(url)
        #Not finished
        return data
