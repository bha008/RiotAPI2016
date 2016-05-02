import requests

# constants
BRAZIL = 'br'
EUROPE_NORDIC_EAST = 'eune'
EUROPE_WEST = 'euw'
KOREA = 'kr'
LATIN_AMERICA_NORTH = 'lan'
LATIN_AMERICA_SOUTH = 'las'
NORTH_AMERICA = 'na'
OCEANIA = 'oce'
RUSSIA = 'ru'
TURKEY = 'tr'

platforms = {
    BRAZIL: 'BR1',
    EUROPE_NORDIC_EAST: 'EUN1',
    EUROPE_WEST: 'EUW1',
    KOREA: 'KR',
    LATIN_AMERICA_NORTH: 'LA1',
    LATIN_AMERICA_SOUTH: 'LA2',
    NORTH_AMERICA: 'NA1',
    OCEANIA: 'OC1',
    RUSSIA: 'RU',
    TURKEY: 'TR1'
}

class ritoWrap:

    def __init__(self, api_key, default_region=NORTH_AMERICA):
        """
        Initializes the ritoWrap object with an API key so that it can make requests on
        riot API
        :param api_key: the API key of the developer or app
        :param default_region: default region for api calls
        :return: n/a
        """
        self.api_key = api_key
        self.default_region = default_region

    def base_request(self, endpoint, region, static=False, **kwargs):
        """
        Does not perform URL construction of sub API's.
        Constructs the URL endpoint using the endpoint parameter and performs
        a call to Riot API.

        TODO: handle error codes from Riot API

        :param endpoint: URL endpoint for Riot's RESTful API
        :param region: the region used in building URL's
        :param static: checks for static data (not used)
        :param kwargs: keeping this here for future use (currently not used)
        :return: returns a JSON string from the server
        """
        if region is None:
            region = self.default_region
        args = {'api_key': self.api_key}
        for k in kwargs:
            if kwargs[k] is not None:
                args[k] = kwargs[k]

        r = requests.get(
            'https://{proxy}.api.pvp.net/{url}'.format(
                proxy='global' if static else region,
                static='static-data/' if static else '',
                region=region,
                url=endpoint
            ),
            params=args
        )
        # if not static:
        #     for lim in self.limits:
        #         lim.add_request()
        return r.json()

    def request_mastery_for_champ(self, summ_id, champ_id, region=None):
        """

        :param summ_id: summoner ID or player ID to get data on
        :param champ_id: champion ID to get data on
        :param region: region of the summoner ID
        :return: JSON string containing mastery information on summoner and
        specified champion
        """
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/champion/{championId}'.format(
            platformId=platforms[region],
            playerId=summ_id,
            championId=champ_id),
            region
        )

    def request_mastery_score(self, summ_id, region=None):
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/score'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region)

    def request_top_champs(self, summ_id, region=None):
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/topchampions'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region)

    def request_all_champs(self, summ_id, region=None):
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/champions'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region)

    def request_id_from_name(self, username, region=None):
        if region is None:
            region = self.default_region
        r = self.base_request('/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'.format(
            region=region,
            summonerNames=username),
            region)
        return r[username]['id']