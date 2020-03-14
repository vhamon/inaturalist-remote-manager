#!/usr/bin/python3

import json
import os
import requests
import urllib.parse

DEBUG = False

class iNatApiClient(object):
    def __init__(self):
        self.__url = "https://api.inaturalist.org/v1"
        self.__token = os.environ["INAT_API_TOKEN"]

    def rest_api_get(self, endpoint, additional_params):
        base_params = {"api_token" : self.__token}
        full_params = {**base_params, **additional_params}
        encoded_params = urllib.parse.urlencode(full_params)
        response = requests.get(self.__url + endpoint + "?" + encoded_params)
        if response.status_code != 200:
            print("Error in GET request, response with status_code={}".format(
                response.status_code))
            return
        return response.json()

class iNatUser(iNatApiClient):
    def __init__(self, name):
        super(iNatApiClient, self).__init__()
        self.__name = name

    @property
    def name(self):
        return self.__name

    def get(self):
        print("Get user")
        self.__client.get()

class iNatProject(iNatApiClient):
    def __init__(self, name):
        super().__init__()
        self.__name = name
        self.__id = 0

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    def get(self):
        json_response = super().rest_api_get("/projects", {"q": self.__name})
        if DEBUG:
            print(json.dumps(json_response, indent=4))

        self.__id = json_response["results"][0]["id"]

def main():
    myInat = iNatUser("vhamon")
    project = iNatProject("Amphibiens d'Ille-et-Vilaine")
    project.get()

    print("{} ({})".format(project.name, project.id))

if __name__ == "__main__":
    main()
