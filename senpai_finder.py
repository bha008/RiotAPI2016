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
        self.league = leagueven
        self.summoner_top_champs = summoner_top_champs

    def findSenpai(self):
        for player in self.league:
            player['top_champs']
        pass

    def similarity(self, senpai_champs):

        pass

    def generateScoreVector(self, top_champs):
        # TODO: create an array of double where the index is championId and the value at the index is level*scoreSinceLastLevel
        pass