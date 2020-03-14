#!/usr/bin/python3

import json
import os
import requests
import sys
import urllib.parse

DEBUG = False

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

def sort_taxons_by_occurences(taxons):
    return dict(sorted(taxons.items(), key=lambda kv: kv[1], reverse=True))

def get_unobserved_taxons(project, user_login):
        taxons_unobserved_by_user = {}
        taxons_observed_by_user = {}
        taxons_observed_by_others = {}

        observations = project.get_observations()
        for observation in observations:
            taxon = observation.taxon
            if observation.observer == user_login:
                current_count = 0
                if taxon in taxons_observed_by_user:
                    current_count = taxons_observed_by_user[taxon]
                taxons_observed_by_user.update({taxon: current_count + 1})
            else:
                current_count = 0
                if taxon in taxons_observed_by_others:
                    current_count = taxons_observed_by_others[taxon]
                taxons_observed_by_others.update({taxon: current_count + 1})

        sorted_taxons_observed_by_others = sort_taxons_by_occurences(
            taxons_observed_by_others)

        return {k: v for k, v in sorted_taxons_observed_by_others.items()
            if k not in taxons_observed_by_user}

def main():
    user_login = "vhamon"
    project_name = "Biodiversité d'Ille-et-Vilaine"
    project = iNatProject(project_name)
    unobserved_taxons = get_unobserved_taxons(project, user_login)
    print("Unobserved taxons by {} in {} :".format(user_login, project_name))
    for taxon, occurences in unobserved_taxons.items():
        print("{} ({})".format(taxon, occurences))

if __name__ == "__main__":
    main()
