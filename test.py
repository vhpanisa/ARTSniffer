from artsnif import LeagueSniffer
from pprint import pprint
from time import time

apikey = 'e428f726-3fbd-4831-9dcc-5bc5b278bf73'
keyd = {'mid':[410503], 'adc':[7842148, 6673314, 11007663]}

pain = {'jg':[3345070],
        'mid':[479257],
        'adc':[487082],
        'top':[406381],
        'sup':[14280149]
        }

intz = {'sup':[403080],
        'jg':[410074],
        'adc':[7622662],
        'mid':[530555],
        'top':[9861202, 2895521, 770595]}
cnb = {}


def get_player_role(match):
	if match['lane'] == 'JUNGLE':
		return 'jg'
	elif match['role'] == 'DUO_SUPPORT' or match['role'] == 'DUO':
		return 'sup'
	elif match['role'] == 'DUO_CARRY':
		return 'adc'
	elif match['lane'] == 'MID' and match['role'] == 'SOLO':
		return 'mid'
	elif match['lane'] == 'TOP' and match['role'] == 'SOLO':
		return 'top'
	else:
		pprint(match)
		return ''

def get_player_dict(raw_data):
    aux = raw_data['entries']
    ret_data = {}
    for entry in aux:
        ret_data[entry['playerOrTeamId']] = entry['playerOrTeamName']
    return ret_data

def main():
    x = LeagueSniffer(apikey)
    enddate = int(time()*1000) - 2629743*1000
    query = {'beginTime': enddate, 'rankedQueues': 'RANKED_SOLO_5x5'}
    valid_matches = []
    for position in pain:
        for acc in pain[position]:
            for match in x.get_match_list('br', acc, query)['matches']:
            	if get_player_role(match) == position:
            		valid_matches.append((match['matchId'], match['champion'], position))

    pprint(valid_matches)
    auishuas
    for match in valid_matches:
    	pprint(x.get_match('br', match[0]))

    
if __name__ == '__main__':
	main()
