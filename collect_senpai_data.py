from riotAPIwrapper import ritoWrap
import os
import json
import sys
import time

rw = ritoWrap(os.environ['RIOT_API_KEY'])
parsed = []


def main():
    # f = open(argv[1],'r')
    league = rw.request_challenger_league_summoners()
    print league

    for summoner in league['entries']:
        print(summoner['playerOrTeamName'], summoner['playerOrTeamId'])
        parsed.append({'summonerId':summoner['playerOrTeamId'],
                       'summonerName':summoner['playerOrTeamName'],
                       'top_champs':rw.request_all_champs(summoner['playerOrTeamId'])})
        time.sleep(1.5)
    out = open(sys.argv[1], 'w')
    out.write(json.dumps(parsed))
    out.close()
    # f.close()

if __name__ == '__main__':
    main()
