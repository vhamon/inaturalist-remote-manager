#!/usr/bin/python3

import sys
import urllib.parse

from inat_manager.core import iNatProject
from inat_manager.utils import get_unobserved_taxons

DEBUG = False

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
