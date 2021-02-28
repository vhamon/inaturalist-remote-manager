import json
import os
import sys

from inat_manager.client import iNatApiClient

DEBUG = False

class iNatObservation(object):
    def __init__(self, json_obj):
        self.__id = json_obj["id"]
        self.__observer = json_obj["user"]["login"]
        self.__taxon = json_obj["taxon"]["name"]

    @property
    def id(self):
        return self.__id

    @property
    def observer(self):
        return self.__observer

    @property
    def taxon(self):
        return self.__taxon

class iNatProject(iNatApiClient):
    def __init__(self, name):
        super().__init__()
        self.__name = name
        json_response = super().rest_api_get("/projects", {"q": self.__name})
        if DEBUG:
            print(json.dumps(json_response, indent=4))

        self.__id = json_response["results"][0]["id"]
        self.per_page = 200
        self.total_observations = sys.maxsize

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    def get_observations_per_page(self, page_number):
        print("Get observations (page {})".format(page_number))
        json_response = super().rest_api_get("/observations",
            {"project_id": self.__id, "page": page_number,
             "per_page": self.per_page})
        if DEBUG:
            print(json.dumps(json_response, indent=4))

        self.total_observations = json_response["total_results"]

        return [iNatObservation(json_result) for json_result in
            json_response["results"]]

    def get_observations(self):
        observations = []
        page_number = 1
        while page_number < self.total_observations/self.per_page:
            observations.extend(self.get_observations_per_page(page_number))
            page_number += 1
        return observations