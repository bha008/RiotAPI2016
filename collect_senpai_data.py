from riotAPIwrapper import ritoWrap
import os
import json
import sys
import time

rw = ritoWrap(os.environ['RIOT_API_KEY'])
parsed = []

def main(argv):
    f = open(argv[1],'r')
    league = json.loads(f.read())

    for summoner in league['entries']:
        print(summoner['playerOrTeamName'], summoner['playerOrTeamId'])
        parsed.append({'summonerId':summoner['playerOrTeamId'],
                       'summonerName':summoner['playerOrTeamName'],
                       'top_champs':rw.request_top_champs(summoner['playerOrTeamId'])})
        time.sleep(1)
    out = open('out.json','w')
    out.write(json.dumps(parsed))
    out.close()
    f.close()

if __name__ == '__main__':
    main(sys.argv)
