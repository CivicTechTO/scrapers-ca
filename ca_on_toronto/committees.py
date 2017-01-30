from pupa.scrape import Organization
from utils import CanadianScraper

import yaml


REQUIRED_KEYS = ['classification', 'name']
DEFAULT_SOURCE = 'https://github.com/t0ronto-ca/dataset-toronto-council-committees'

def has_required_keys(org):
    return all([key in org for key in REQUIRED_KEYS])

class TorontoCommitteeScraper(CanadianScraper):


    def allOrganizations(self):
        response = self.get('https://raw.githubusercontent.com/t0ronto-ca/dataset-toronto-council-committees/master/data/committees.yml?4')
        return yaml.load(response.text)

    def validOrganizations(self):
        return [org for org in self.allOrganizations() if has_required_keys(org)]

    def allCommittees(self):
        return [org for org in self.allOrganizations() if org.get('classification') == 'committee']

    def scrape(self):
        for org in self.validOrganizations():
            if org['name'] == 'Toronto City Council':
                continue

            allowed_args = ['name', 'classification', 'founding_date', 'dissolution_date']
            data = {k:v for k,v in org.items() if k in allowed_args}

            o = Organization(**data)

            for name_data in org.get('other_names', []):
                o.add_name(**name_data)

            for identifier_data in org.get('identifiers', []):
                o.add_identifier(**identifier_data)

            o.extras = org.get('extras', {})
            o.add_source(DEFAULT_SOURCE)
            yield o
