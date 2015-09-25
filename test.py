from artsnif import LeagueSniffer
from pprint import pprint

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

def get_player_dict(raw_data):
    aux = raw_data['entries']
    ret_data = {}
    for entry in aux:
        ret_data[entry['playerOrTeamId']] = entry['playerOrTeamName']
    return ret_data

def main():
    x = LeagueSniffer(apikey)
    #pprint(get_player_dict(x.get_master_league('br')))
    for position in pain:
        for acc in pain[position]:
            pprint(x.get_match_list('br', acc))
            iueajheaeaiueha
    
if __name__ == '__main__':
    main()
