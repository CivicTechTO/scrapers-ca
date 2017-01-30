from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'


class TorontoPersonScraper(CSVScraper):
    csv_url = 'https://raw.githubusercontent.com/t0ronto-ca/dataset-toronto-elected-officials/master/data/contact-info.csv'
    district_name = '{district name} ({district id})'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
        'John Filion': ['John Fillion'],
        'Michelle Berardinetti': ['Michelle Holland'],
    }
