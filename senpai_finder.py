import json

class SenpaiFinder:

    def __init__(self, league, summoner_top_champs):
        """

        :param summoner:
        :param league: a list of players and their top ppl
        :return:
        """
        self.league = league
        self.all_keys = self.get_all_champ_Ids()
        self.summoner_score_dict = self.generateScoreDict(summoner_top_champs)

    def findSenpai(self):
        '''
        searches for most similar senpai
        :return:
        '''

        max_sim = 0
        senpaiId = 0
        for senpai in self.league:
            temp_sim = self.get_similarity(senpai['top_champs'])
            if temp_sim > max_sim:
                max_sim = temp_sim
                senpaiId = senpai['summonerId']

        return senpaiId

    def get_similarity(self, senpai_champs):
        '''
        calculates a similarity value based off of player's top champs and senpai's
        :param senpai_champs: list of champs from senpai
        :return:
        '''
        similarity = 0
        senpai_score_dict = self.generateScoreDict(senpai_champs)

        for key in self.summoner_score_dict:
            if self.summoner_score_dict[key] > 0:
                similarity += pow(self.summoner_score_dict[key] - senpai_score_dict[key],2)
        print (similarity)
        return 1.0/(similarity + 1)

    def get_all_champ_Ids(self):
        '''
        loads up a json object containing champ information and returns the champId's as a list
        :return:
        '''
        current_champs = json.load(open('static/assets/riot_champion_data/lol-champions_6_8_1.json'))['data']
        return current_champs.keys()

    def generateScoreDict(self, top_champs):
        '''
        converts a list of mastery information into a dictionary with relative score per championId
        :param top_champs:
        :return:
        '''

        d = {}
        total = 1
        for key in self.all_keys:
            d[int(key)] = 0

        for champ in top_champs:
            d[champ['championId']] = champ['championLevel'] * 5000 + champ['championPointsSinceLastLevel']
        total = sum(d.values())

        for champ in top_champs:
            d[champ['championId']] /= float(total)
        return d


