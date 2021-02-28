def sort_taxons_by_occurences(taxons):
    return dict(sorted(taxons.items(), key=lambda kv: kv[1], reverse=True))

def get_unobserved_taxons(project, user_login):
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