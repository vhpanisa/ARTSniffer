import requests
import json
from time import sleep

class _Sniffer():
    def __init__(self):
        pass
    
    def build_url(self, base=None, method=None, query=None, sufix=None, key=None):
        if not ((base or method) and sufix and key):
            print(base, method, sufix, key)
            raise Exception("build_url is missing args")
        
        # Dota2 and LoL
        url = base if base else "" + method if method else ""
        url += ('&' if '?' in url else '?') + (sufix+'={0}').format(key)
        if query:
            for key in query:
                url += ''.join(['&', key, '=', str(query[key])])
                
        return url
        
class DotaSniffer(_Sniffer):
    """ Dota Sniffer Class """
    def __init__(self, apikey=None, tries=3):
        """
        Initialize the sniffer to pull data from Valve's API for DOTA2.
        """
        if not apikey:
            raise Exception("No API key was parsed")
        self.__apikey = apikey
        self.__tries = tries

    
    def make_request(self, method=None, query=None):
        """
        Sends an direct request for DOTA2's API.
        """   
        url = super().build_url('https://api.steampowered.com/', method, query, 'key', self.__apikey) 
        tries = 0
        while True:
            tries += 1
            if tries > self.__tries:
                return None
            r = requests.get(url)
            if r.text.startswith('<html>'): # Got a non-json response. Possible timeout or invalid request.
                continue
            data = json.loads(r.text)
            if 'status' in data:
                aux = data['status']
                if aux['status_code'] == 503: # Server busy, sleeping for one second.
                    sleep(1)
                else:
                    raise Exception(aux['message'])
            else:
                break
        return data

    def get_heroes(self):
        """
        Returns a dict using the format dict[HeroID] -> HeroName.
        """
        return self.make_request('IEconDOTA2_570/GetHeroes/v0001/')

    def get_items(self):
        """
        Returns a dict using the format dict[ItemID] -> ItemName.
        """
        return self.make_request('IEconDOTA2_570/GetGameItems/v0001/')


    def get_match_history(self, query=None):
        """
        Returns an list of the last 100 MatchIDs played
        """
        return self.make_request('IDOTA2Match_570/GetMatchHistory/V001/', query)

    def get_match_details(self, matchid=None):
        """
        Returns full mathch info, timeline arg optional.
        """
        if not matchid:
            raise Exception("getMatchDetails needs a valid MatchID")
        return self.make_request('IDOTA2Match_570/GetMatchDetails/v001/?match_id={0}'.format(matchid))


class LeagueSniffer(_Sniffer):
    """ League of Legends Sniffer Class """
    def __init__(self, apikey=None, tries=3):
        """
        Creates a Sniffer to pull data from Riot's API for League of Legends.
        """
        if not apikey:
            raise Exception("No API key was parsed")
        self.__apikey = apikey
        self.__tries = tries

    
    def make_request(self, method=None, query=None):
        """Sends an direct request for Riot's API."""
        url = super().build_url(method = method, query = query, sufix = 'api_key', key = self.__apikey)
        tries = 0
        while True:
            tries += 1
            if tries > self.__tries:
                return None
            r = requests.get(url)
            if r.text.startswith('<html>'):
                #Got a non-json response. Possible timeout or invalid request
                continue
            data = json.loads(r.text)
            if 'status' in data:
                aux = data['status']
                if aux['status_code'] == 429:
                    #Reached the limit of requests, sleeping for one second
                    #Watch out, you can be blacklisted by Riot for exceding the limit all the time.
                    sleep(1)
                else:
                    raise Exception(aux)
            else:
                break
                
        return data

    def get_regions(self):
        """
        Returns a list of current active regions of Riot's servers.
        """
        url = 'http://status.leagueoflegends.com/shards'
        data = self.doApiRequest(url)
        regions = []
        for region in data:
            regions.append(region['slug'])
        regions.append('kr')
        return regions

    def get_champions(self):
        """
        Returns a dict using the format dict[ChampionID] -> ChampionName.
        """
        return self.make_request('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=all')

    def get_items(self):
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

    def get_challenger_league(self, region=None):
        """
        Returns the summonerID of all players on challenger league of certain region.
        """
        if not region:
            raise Exception("An region needs to be specified")
        return self.make_request('https://{0}.api.pvp.net/api/lol/{0}/v2.5/league/challenger?type=RANKED_SOLO_5x5'.format(region))

    def get_master_league(self, region=None):
        """
        Returns the summonerID of all players on master league of certain region.
        """
        if not region:
            raise Exception("getMasterPlayersID needs an region to be specified")
        return self.make_request('https://{0}.api.pvp.net/api/lol/{0}/v2.5/league/master?type=RANKED_SOLO_5x5'.format(region))

    def get_match_list(self, region=None, pid=None, query=None):
        """
        Returns an list of MatchIDs for a given player on a region.
        """
        if not (region and pid):
            raise Exception("getMatchList needs a valid Region and SummonerID")
        return self.make_request('https://{0}.api.pvp.net/api/lol/{0}/v2.2/matchlist/by-summoner/{1}'.format(region, pid), query)

    def get_match(self, region=None, matchid=None, query=None):
        """
        Returns full mathch info, timeline arg optional.
        """
        if not (region and matchid):
            raise Exception("getMatch needs a valid Region and MatchID")
        return self.make_request('https://{0}.api.pvp.net/api/lol/{0}/v2.2/match/{1}'.format(region, matchid))


class SmiteSniffer:
    def __init__(self, devId=None, authKey=None):
        """Creates a Sniffer to pull data from Smite's API."""
        if not devId and authKey:
            raise Exception("DevID/AuthKey is missing")
        self.__devid = devId
        self.__authkey = authKey
        self.__sessions = []

    def build_url(self, method=None, query=None):
        if not method:
            raise Exception("build_url needs an method")
        
        if not respFormat in query:
            respFormat='json'
        else:
            respFormat=query[respFormat]
            
        url = 'http://api.smitegame.com/smiteapi.svc/'
        url += method + respFormat
        
        #{developerId}/{signature}/{session}/{timestamp}/
        if method != 'ping':
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            url += '/' + self.__devid
            url += '/' + self.makeSignature(method, timestamp)
            if method != 'createsession':
                if len(self.__sessions) == 0:
                    while not self.__createsession(): pass
                url += '/' + self.__sessions[0]
            url += '/' + timestamp
        if query:
            for key in query:
                url += ''.join(['/', str(key)])

                
    def make_request(self, method=None, query=None):
        """Sends an direct request for Smite's API."""
        while True:
            print(url)
            r = requests.get(url)
            if r.text.startswith('<html>'):
                print('Got a non-json response. Possible timeout or invalid request.')
                continue
            data = json.loads(r.text)
            if 'status' in data: #not sure. Check this
                aux = data['status']
                if aux['status_code'] == 503:
                    print('Server busy, sleeping for one second.')
                    sleep(1)
                else:
                    raise Exception(aux['message'])
            else:
                break
                
        return data

    def getGods(self):
        """
        Returns a dict using the format dict[GodID] -> GodName.
        """
        method = 'getgods'
        data = self.doApiRequest(method)
        gods = {}
        print(data)
        sys.exit(0)
        for hero in data['result']['heroes']:
            heroes[hero['id']] = hero['name']
        return heroes

    def getItems(self):
        """
        Returns a dict using the format dict[ItemID] -> ItemName.
        """
        url = 'IEconDOTA2_570/GetGameItems/v0001/'
        data = self.doApiRequest(url)['result']['items']
        items = {}
        for item in data:
            items[item['id']] = item['name']
        return items


    def getMatchHistory(self, query=None):
        """Returns an list of the last 100 MatchIDs played"""
        url = 'IDOTA2Match_570/GetMatchHistory/V001/'
        data = self.doApiRequest(url, query)['result']['matches']
        matches = []
        for match in data:
            matches.append(match['match_id'])
        return matches

    def getMatch(self, matchid=None):
        """Returns full mathch info, timeline arg optional."""
        if not matchid:
            raise Exception("getMatch needs a valid MatchID")
        method = 'IDOTA2Match_570/GetMatchDetails/v001/?match_id={0}'.format(matchid)
        data = self.doApiRequest(method)['result']
        return data
    
    def pingServer(self):
        if 'successful' in self.make_request('ping'):
            return True
        else:
            return False
        
    def __createSession(self):
        method = 'createsession'
        data = self.doApiRequest(method)
        if data['ret_msg'] == 'Approved':
            self.__sessions.append()
            return True
        else:
            print('Data dump debug: ', data)
            return False
        
    def __testSession(self, session=None):
        if not session:
            raise Exception("getMatch needs a valid MatchID")
        method = 'testsession'
        data = self.doApiRequest(method)
        if data.statswith('Invalid'):
            return False
        else:
            return True

    def __makeSignature(self, method, timestamp):
        md5 = hashlib.md5()
        md5.update(self.__devid.encode('utf-8'))
        md5.update(method.encode('utf-8'))
        md5.update(self.__authkey.encode('utf-8'))
        md5.update(timestamp.encode('utf-8'))
        return md5.hexdigest()
