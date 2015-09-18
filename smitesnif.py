import requests
import json
from time import sleep
from datetime import datetime
import hashlib

#15 3 2x
#7FB4C011037D4CBCBB9F454306D747 9 2x


class SmiteSniffer:
    """Creates a Sniffer to pull data from Smite's API."""
    def __init__(self, devId=None, authKey=None):
        if not devId and authKey:
            raise Exception("DevID/AuthKey is missing")
        self.__devid = devId
        self.__authkey = authKey
        self.__sessions = []
        
    def doApiRequest(self, method=None, , query=None):
        """Sends an direct request for Smite's API."""
        if not method:
            raise Exception("doApiRequest needs an method")
        
        if not respFormat in query:
            respFormat='json'
        else:
            respFormat=query[respFormat]

        url = 'http://api.smitegame.com/smiteapi.svc/'
        url += method + respFormat
        if method != 'ping':
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            url += '/' + self.__devid
            url += '/' + self.makeSignature(method, timestamp)
            if method != 'createsession':
                if len(self.__sessions) == 0:
                    while not self.__createsession(): pass
                url += '/' + self.__sessions[0]
            url += '/' + timestamp
        {developerId}/{signature}/{session}/{timestamp}/
        if query:
            for key in query:
                url += ''.join(['/', str(key)])
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
    
    def __pingServer(self):
        if 'successful' in self.doApiRequest('ping')):
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
