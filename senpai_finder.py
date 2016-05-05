import json
from riotAPIwrapper import ritoWrap

class SenpaiFinder:

    def __init__(self, summoner, league, summoner_top_champs=None):
        """

        :param summoner:
        :param league:
        :return:
        """
        self.summoner = summoner
        self.league = league
        self.summoner_top_champs = summoner_top_champs
        self.generateScoreVector(summoner_top_champs)

    def findSenpai(self):
        for player in self.league:
            player['top_champs']
        pass

    def similarity(self, senpai_champs):

        pass

    def generateScoreVector(self, top_champs):
        # TODO: create an array of double where the index is championId and the value at the index is level*scoreSinceLastLevel
        current_champs = json.load(open('static/assets/riot_champion_data/lol-champions_6_8_1.json'))
        print current_champs.keys()
