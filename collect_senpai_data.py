from riotAPIwrapper import ritoWrap
import os
import json
import sys
import time

regions = {
    'BRAZIL': 'br',
    'EUROPE_NORDIC_EAST': 'eune',
    'EUROPE_WEST': 'euw',
    'KOREA': 'kr',
    'LATIN_AMERICA_NORTH': 'lan',
    'LATIN_AMERICA_SOUTH': 'las',
    'NORTH_AMERICA': 'na',
    'OCEANIA': 'oce',
    'RUSSIA': 'ru',
    'TURKEY': 'tr'
}
rw = ritoWrap(os.environ['RIOT_API_KEY'])
parsed = []


def main():
    # f = open(argv[1],'r')
    for region in regions.keys():
        league = rw.request_challenger_league_summoners(region=regions[region])
        print league

        for summoner in league['entries']:
            print(summoner['playerOrTeamName'], summoner['playerOrTeamId'])
            parsed.append({'summonerId':summoner['playerOrTeamId'],
                           'summonerName':summoner['playerOrTeamName'],
                           'top_champs':rw.request_all_champs(summoner['playerOrTeamId'])})
        out = open(region + '_challenger.json', 'w')
        out.write(json.dumps(parsed))
        out.close()
        time.sleep(10)
        # f.close()

if __name__ == '__main__':
    main()
