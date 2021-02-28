import json
import os
import requests
import sys
import urllib

class iNatApiClient(object):
    def __init__(self):
        self.__url = "https://api.inaturalist.org/v1"
        self.__token = os.environ["INAT_API_TOKEN"]

    def rest_api_get(self, endpoint, additional_params=None):
        base_params = {"api_token" : self.__token}
        if additional_params is not None:
            full_params = {**base_params, **additional_params}
        else:
            full_params = base_params
        encoded_params = urllib.parse.urlencode(full_params)

        try:
            response = requests.get(self.__url + endpoint + "?"
                + encoded_params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)
        return response.json()
