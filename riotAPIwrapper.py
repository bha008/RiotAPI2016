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
        self.api_key = api_key
        self.default_region = default_region

    def base_request(self, endpoint, region, static=False, **kwargs):
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

    def request_mastery_score(self, summ_id, region=None):
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/score'.format(
            platformId =  platforms[region],
            playerId = summ_id),
            region)