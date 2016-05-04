import requests
from collections import deque
import time

# Based off of the Riot-Watcher wrapper found at:
# https://github.com/pseudonym117/Riot-Watcher/blob/master/riotwatcher/riotwatcher.py


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

class LoLException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return self.error

    def __eq__(self, other):
        if isinstance(other, "".__class__):
            return self.error == other
        elif isinstance(other, self.__class__):
            return self.error == other.error and self.headers == other.headers
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(LoLException).__hash__()


error_400 = "Bad request"
error_401 = "Unauthorized"
error_403 = "Blacklisted key"
error_404 = "Game data not found"
error_429 = "Too many requests"
error_500 = "Internal server error"
error_503 = "Service unavailable"
error_504 = 'Gateway timeout'

def raise_status(response):
    if response.status_code == 400:
        raise LoLException(error_400, response)
    elif response.status_code == 401:
        raise LoLException(error_401, response)
    elif response.status_code == 403:
        raise LoLException(error_403, response)
    elif response.status_code == 404:
        raise LoLException(error_404, response)
    elif response.status_code == 429:
        raise LoLException(error_429, response)
    elif response.status_code == 500:
        raise LoLException(error_500, response)
    elif response.status_code == 503:
        raise LoLException(error_503, response)
    elif response.status_code == 504:
        raise LoLException(error_504, response)
    else:
        response.raise_for_status()


class RateLimit:
    def __init__(self, allowed_requests, seconds):
        self.allowed_requests = allowed_requests
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_requests

class ritoWrap:

    def __init__(self, api_key, default_region=NORTH_AMERICA, limits=(RateLimit(10, 10), RateLimit(500, 600))):
        """
        Initializes the ritoWrap object with an API key so that it can make requests on
        riot API
        :param api_key: the API key of the developer or app
        :param default_region: default region for api calls
        :return: n/a
        """
        self.api_key = api_key
        self.default_region = default_region
        self.limits = limits

    def base_request(self, endpoint, region, static=False, **kwargs):
        """
        Does not perform URL construction of sub API's.
        Constructs the URL endpoint using the endpoint parameter and performs
        a call to Riot API.


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

        # if not self.limits.request_available():
            # time.sleep(10)

        r = requests.get(
            'https://{proxy}.api.pvp.net/{url}'.format(
                proxy='global' if static else region,
                static='static-data/' if static else '',
                region=region,
                url=endpoint
            ),
            params=args
        )
        # TODO: handle error codes from Riot API
        if not static:
            for lim in self.limits:
                # lim.reload()
                lim.add_request()
        raise_status(r)
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
        """

        :param summ_id:
        :param region:
        :return:
        """
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/score'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region)

    def request_top_champs(self, summ_id, region=None, count=3):
        """

        :param summ_id:
        :param region:
        :param count:
        :return:
        """
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/topchampions'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region,
            count=count)

    def request_all_champs(self, summ_id, region=None):
        """

        :param summ_id:
        :param region:
        :return:
        """
        if region is None:
            region = self.default_region
        return self.base_request('/championmastery/location/{platformId}/player/{playerId}/champions'.format(
            platformId=platforms[region],
            playerId=summ_id),
            region)

    def request_id_from_name(self, username, region=None):
        """

        :param username:
        :param region:
        :return:
        """
        if region is None:
            region = self.default_region
        r = self.base_request('/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'.format(
            region=region,
            summonerNames=username.lower().strip()),
            region)
        return r[username.lower().strip()]['id']

    def request_master_league_summoners(self, region=None):
        if region is None:
            region = self.default_region
        return self.base_request('/api/lol/{region}/v2.5/league/master'.format(
            region=region),
            region,
            type='RANKED_SOLO_5x5')
