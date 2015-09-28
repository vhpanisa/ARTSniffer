#!/usr/bin/python
# -*- coding: utf-8 -*-
from artsnif import LeagueSniffer
from pprint import pprint
from time import time
from sys import exit
import csv

apikey = 'e428f726-3fbd-4831-9dcc-5bc5b278bf73'
cDict = {}

keyd = {'mid': [410503], 'adc': [7842148, 6673314, 11007663]}

pain = {
    'jg': [3345070],
    'mid': [479257],
    'adc': [487082],
    'top': [406381],
    'sup': [14280149],
    }

intz = {
    'sup': [403080],
    'jg': [410074],
    'adc': [7622662],
    'mid': [530555],
    'top': [9861202, 2895521, 770595],
    }

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
        #pprint(match)
        return ''


def get_player_dict(raw_data):
    aux = raw_data['entries']
    ret_data = {}
    for entry in aux:
        ret_data[entry['playerOrTeamId']] = entry['playerOrTeamName']
    return ret_data

def get_champ_dict(raw_data):
    global cDict
    for entry in [raw_data['data'][c] for c in raw_data['data']]:
        cDict[entry['id']] = entry['name']

def make_csv_row(match, champ, role):
    players = match['participants']
    row = {}
    for player in players:
        if player['championId'] == champ:
            stats = player['stats']
            row['champ'] = cDict[champ]
            row['role'] = role
            row['win'] = "Vitória" if stats['winner'] == True else "Derrota"
            d = 1 if stats['deaths'] == 0 else stats['deaths']
            k = stats['kills']
            a = stats['assists']
            row['kda'] = '{:.2f}'.format((k+a)/d)
            break
    return row


def main():
    team = intz
    x = LeagueSniffer(apikey, 3)
    get_champ_dict(x.get_champions())
    enddate = int(time() * 1000) - 2629743 * 1000
    query = {'beginTime': enddate, 'rankedQueues': 'RANKED_SOLO_5x5'}
    valid_matches = []
    for position in team:
        for acc in team[position]:
            for match in x.get_match_list('br', acc, query)['matches']:
                if get_player_role(match) == position:
                    valid_matches.append((match['matchId'], match['champion'], position, match['platformId']))

    csvdata = []
    end = len(valid_matches)
    current = 0
    for match in valid_matches:
        current += 1
        print('Doing {} out of {}'.format(current, end))
        row = x.get_match(match[-1][:2].lower(), match[0])
        if row:
            csvdata.append(make_csv_row(row, match[1], match[2]))
        else:
            pprint(match)
            sys.exit(0)

    keys = csvdata[0].keys()
    with open('g3x_raw_data.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(csvdata)


if __name__ == '__main__':
    main()
